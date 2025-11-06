import numpy as np
import sys
import os

import aie.iron as iron
from aie.iron import ExternalFunction, jit
from aie.iron import Kernel, ObjectFifo, Program, Runtime, Worker
from aie.iron.placers import SequentialPlacer
from aie.iron.controlflow import range_
from aie.helpers.taplib import TensorAccessPattern, TensorTiler2D
from aie.utils.config import cxx_header_path

@iron.jit(is_placed=False)
def matrix_multiplication_single_core(input0, input1, output):
    # Use only tile sizes
    m, k, n = 64, 64, 64  # tile moved to/from cores
    r, s, t = 2, 8, 8     # AIE kernel intrinsic size

    element_type = output.dtype

    A_ty = np.ndarray[(m, k), np.dtype[element_type]]
    B_ty = np.ndarray[(k, n), np.dtype[element_type]]
    C_ty = np.ndarray[(m, n), np.dtype[element_type]]

    a_ty = A_ty
    b_ty = B_ty
    c_ty = C_ty

    fifo_A_L3L2 = ObjectFifo(a_ty, name="A_L3L2")
    tap_A_L2L1 = TensorTiler2D.group_tiler((m, k), (r, s), (m // r, k // s))[0]
    fifo_A_L2L1 = fifo_A_L3L2.cons().forward(dims_to_stream=tap_A_L2L1.transformation_dims, name="A_L2L1")

    fifo_B_L3L2 = ObjectFifo(b_ty, name="B_L3L2")
    tap_B_L2L1 = TensorTiler2D.group_tiler((k, n), (s, t), (k // s, n // t))[0]
    fifo_B_L2L1 = fifo_B_L3L2.cons().forward(dims_to_stream=tap_B_L2L1.transformation_dims, name="B_L2L1")

    fifo_C_L1L2 = ObjectFifo(c_ty, name="C_L1L2")
    tap_C_L1L2 = TensorAccessPattern(
        tensor_dims=(m, n),
        offset=0,
        sizes=[m // r, r, n // t, t],
        strides=[r * n, t, r * t, 1],
    )
    fifo_C_L2L3 = fifo_C_L1L2.cons().forward(dims_to_stream=tap_C_L1L2.transformation_dims, name="C_L2L3")

    matmul_kernel = ExternalFunction(
        "dense",
        source_file=os.path.join(os.path.dirname(__file__), "dense.cc"),
        arg_types=[a_ty, b_ty, c_ty],
        include_dirs=[cxx_header_path()],
    )

    def core_fn(of_a, of_b, of_c, matmul):
        # Exactly one output tile now
        for _ in range_(1):
            elem_out = of_c.acquire(1)
            for i in range_(m):
                for j in range_(n):
                    elem_out[i, j] = 0
            # Exactly one A/B tile pair
            for _ in range_(1):
                elem_in_a = of_a.acquire(1)
                elem_in_b = of_b.acquire(1)
                matmul(elem_in_a, elem_in_b, elem_out)
                of_a.release(1)
                of_b.release(1)
            of_c.release(1)

    worker = Worker(core_fn, [fifo_A_L2L1.cons(), fifo_B_L2L1.cons(), fifo_C_L1L2.prod(), matmul_kernel])

    a_tap = TensorTiler2D.group_tiler((m, k), (m, k), (1, 1))[0]
    b_tap = TensorTiler2D.group_tiler((k, n), (k, n), (1, 1))[0]
    c_tap = TensorTiler2D.group_tiler((m, n), (m, n), (1, 1))[0]

    rt = Runtime()
    with rt.sequence(A_ty, B_ty, C_ty) as (A, B, C):
        rt.start(worker)
        tg = rt.task_group()
        rt.fill(fifo_A_L3L2.prod(), A, tap=a_tap, task_group=tg)
        rt.fill(fifo_B_L3L2.prod(), B, tap=b_tap, task_group=tg)
        rt.drain(fifo_C_L2L3.cons(), C, tap=c_tap, task_group=tg, wait=True)
        rt.finish_task_group(tg)

    my_program = Program(iron.get_current_device(), rt)
    return my_program.resolve_program(SequentialPlacer())


def main():
    # Use only tile sizes
    m, k, n = 64, 64, 64
    element_type = np.int8

    # Inputs/outputs are a single tile
    input0 = iron.randint(0, 128, (m, k), dtype=element_type, device="npu")
    input1 = iron.randint(0, 128, (k, n), dtype=element_type, device="npu")
    output = iron.zeros(m * n, dtype=element_type, device="npu")
    ref_vec = np.matmul(input0.numpy(), input1.numpy())

    matrix_multiplication_single_core(input0, input1, output)

    e = np.equal(ref_vec.flatten(), output.numpy())
    errors = np.size(e) - np.count_nonzero(e)
    if not errors:
        print("\nPASS!\n")
        sys.exit(0)
    else:
        print("\nError count: ", errors)
        print("\nfailed.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
