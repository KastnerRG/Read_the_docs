# nn.py — two-tile matmul chain (int8, r,s,t = 2,8,8), simplified names and prints
import sys, os
import numpy as np
import aie.iron as iron
from aie.iron import ExternalFunction, Program, Runtime, Worker
from aie.iron.placers import SequentialPlacer
from aie.iron.controlflow import range_
from aie.helpers.taplib import TensorAccessPattern, TensorTiler2D
from aie.utils.config import cxx_header_path


@iron.jit(is_placed=False)
def chain_two_tiles(X, W1, W2, Y2_out):
    # sizes must match your dense.cc
    m = k = n = 64
    r, s, t = 2, 8, 8
    dt = Y2_out.dtype

    # tensor types
    A_ty  = np.ndarray[(m, k), np.dtype[dt]]   # X
    W1_ty = np.ndarray[(k, n), np.dtype[dt]]   # W1
    Y1_ty = np.ndarray[(m, n), np.dtype[dt]]   # Y1 (A->B bridge)
    W2_ty = np.ndarray[(n, n), np.dtype[dt]]   # W2
    Y2_ty = np.ndarray[(m, n), np.dtype[dt]]   # Y2

    # -------- DDR → A (Tile A inputs) --------
    of_X_DDR = iron.ObjectFifo(A_ty, name="X_DDR")
    tap_X_to_A = 
    of_X_to_A = of_X_DDR.cons().forward(dims_to_stream=tap_X_to_A.transformation_dims, name="X_to_A")

    of_W1_DDR = iron.ObjectFifo(W1_ty, name="W1_DDR")
    tap_W1_to_A = 
    of_W1_to_A = of_W1_DDR.cons().forward(dims_to_stream=tap_W1_to_A.transformation_dims, name="W1_to_A")

    # -------- A → B --------
    of_Y1_A_to_B = iron.ObjectFifo(Y1_ty, name="Y1_A_to_B")

    # -------- DDR → B (Tile B W2 input) --------
    of_W2_DDR = iron.ObjectFifo(W2_ty, name="W2_DDR")
    tap_W2_to_B = 
    of_W2_to_B = of_W2_DDR.cons().forward(dims_to_stream=tap_W2_to_B.transformation_dims, name="W2_to_B")

    # -------- B → DDR --------
    of_Y2_B = iron.ObjectFifo(Y2_ty, name="Y2_B")
    tap_Y2_to_DDR = 
    of_Y2_to_DDR = of_Y2_B.cons().forward(dims_to_stream=tap_Y2_to_DDR.transformation_dims, name="Y2_to_DDR")

    # kernel used by both tiles
    dense = ExternalFunction(
        "dense",
        source_file=os.path.join(os.path.dirname(__file__), "dense.cc"),
        arg_types=[A_ty, W1_ty, Y1_ty],
        include_dirs=[cxx_header_path()],
    )

    def mm(of_a, of_b, of_c, fn):  # one m×n tile
        c = of_c.acquire(1)
        for i in range_(m):
            for j in range_(n):
                c[i, j] = 0
        a = of_a.acquire(1)
        b = of_b.acquire(1)
        fn(a, b, c)
        of_a.release(1); of_b.release(1); of_c.release(1)

    # tiles
    tile_A = Worker(mm, )  # Y1 = X*W1
    tile_B = Worker(mm, )   # Y2 = Y1*W2

    # runtime: DDR→A, DDR→B, B→DDR
    tap_A_DDR  = TensorTiler2D.group_tiler((m, k), (m, k), (1, 1))[0]
    tap_W1_DDR = TensorTiler2D.group_tiler((k, n), (k, n), (1, 1))[0]
    tap_W2_DDR = TensorTiler2D.group_tiler((n, n), (n, n), (1, 1))[0]
    tap_Y2_DDR = TensorTiler2D.group_tiler((m, n), (m, n), (1, 1))[0]

    rt = Runtime()
    with rt.sequence(A_ty, W1_ty, W2_ty, Y2_ty) as (A_buf, W1_buf, W2_buf, Y2_buf):
        rt.start(tile_A, tile_B)
        tg = rt.task_group()
        rt.fill(of_X_DDR.prod(),  A_buf,  tap=tap_A_DDR,  task_group=tg)   # DDR→A
        rt.fill(of_W1_DDR.prod(), W1_buf, tap=tap_W1_DDR, task_group=tg)   # DDR→A
        rt.fill(of_W2_DDR.prod(), W2_buf, tap=tap_W2_DDR, task_group=tg)   # DDR→B
        rt.drain(of_Y2_to_DDR.cons(),    Y2_buf, tap=tap_Y2_DDR, task_group=tg, wait=True)  # B→DDR
        rt.finish_task_group(tg)

    return Program(iron.get_current_device(), rt).resolve_program(SequentialPlacer())


def main():
    m = k = n = 64
    dtype = np.int8

    X  = iron.randint(0, 128, (m, k), dtype=dtype, device="npu")
    W1 = iron.randint(0, 128, (k, n), dtype=dtype, device="npu")
    W2 = iron.randint(0, 128, (n, n), dtype=dtype, device="npu")
    Y2 = iron.zeros(m * n, dtype=dtype, device="npu")

    # reference
    ref = (X.numpy() @ W1.numpy()) @ W2.numpy()

    # run
    chain_two_tiles(X, W1, W2, Y2)
    got = Y2.numpy().reshape(m, n)

    # only print on failure
    bad = (ref != got)
    errors = int(bad.sum())
    if errors:
        idx = np.argwhere(bad)[:32]
        print(f"FAILED — mismatches: {errors}/{m*n}")
        for r, c in idx:
            print(f"  (r={r}, c={c}) ref={int(ref[r,c])} got={int(got[r,c])}")
        sys.exit(1)

    # success: stay quiet
    print("\nPASSED\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
