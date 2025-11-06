Project: AMD AI-Engine (AIE) Accelerator
=========================================

AIE is a new kind of accelerator architecture developed by AMD that is distinct from CPUs, GPUs and FPGAs. It is designed to be a highly efficient and flexible architecture for accelerating a wide range of workloads. The AIE architecture is based on a dataflow model of computation, where data flows through a network of processing elements (PEs) that are connected by a network-on-chip (NoC). 

An AI Engine has 24 tiles arranged as 6 rows and 4 columns as shown. Each column has a shim tile, a memory tile and four compute tiles. Each of the 16 compute tiles has a local (L1) memory, a DMA and a VLIW processor optimized for large vector operations. 

.. image:: image/aie.png

There are three main components to programming an AI Engine:

1. **Host code:** This runs on the host CPU outside the AI Engine and is responsible for setting up the AI Engine, creating example data, transferring data & instructions to and from the AI Engine, and verifying the results.
2. **Graph code:** This Python script describes the dataflow within the AI engine. This is acheived by configuring high level primitives such as object fifos, to move data between tiles of the AI Engine. This script also points to the kernel function that will be executed in the VLIW processors of each tile.
3. **Kernel functions:** These are functions that are compiled to run in the VLIW processors that make the compute tiles of the AI Engine.

`Quick Reference to architecture manual, programming guide, API & intrinsic documentation. <https://docs.amd.com/r/en-US/ug1079-ai-engine-kernel-coding>`_

There are multiple ways to specify the host, graph and kernel codes. 

1. C++ for host, graph and kernel code - legacy flow found in some `AIE documentation <https://docs.amd.com/r/en-US/ug1079-ai-engine-kernel-coding>`_
2. C++ for host and kernel code, Python for graph code - older MLIR-AIE/IRON flow. You may see this in some of the examples in this repository.
3. Python for host and graph code, C++/Python for kernel code - new IRON flow. 

The new IRON flow aims to increase developer productivity by providing high level abstractions in Python to control the data movement between tiles of the AI engines. A single-source IRON program has the following parts:


0) Setup
---------------

1. Make sure you are connected to the campus network in one of the following ways:

  * On-campus ethernet
  * On-campus WiFi: **UCSD_PROTECTED** (not UCSD_GUEST)
  * UCSD VPN using Cisco Secure Client `[More Info] <https://support.eng.ucsd.edu/how-to-guides/new-cisco-secure-client>`_

2. Check the `UCSD_2025_Tokens.xlsx` spreadsheets shared as a Canvas Announcement and on Discord #announcement channel, and get the unique token & URL assigned to you.
2. Open a browser and visit your assigned URL (`https://aupcloud.io/aipc-##` and sign in with the unique token `ucsd-iron25-user-##` given to you.
4. Enter the duration (in minutes) you want the instance to run for (e.g., 180) and launch instance
5. Copy the files from `AIE Project Directory <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/aie-project>`_ to `notebooks/mlir-aie/myproject` directory in your AIE instance.


1) Mini Tutorial
------------------------------------

Complete the `mini tutorial <https://github.com/Xilinx/mlir-aie/tree/main/programming_guide/mini_tutorial>`_ to get familiar with the IRON programming flow. The tutorial can be summarized as follows:

1. Routing data through shim tiles & mem tiles: 

  1. Worker -> DDR
  2. DDR -> Worker -> DDR
  3. DDR -> Mem tile -> DDR (of.forward())
  4. DDR -> Mem tile -> Worker -> DDR
  5. DDR -> Mem tile -> Worker -> Mem tile -> DDR

2. Splitting and joining object fifos. 

  1. DDR -> Worker -> DDR
  2. DDR -> OF -> 3x(OFs -> Workers -> OFs) -> OF -> DDR

3. Processing multiple inputs and outputs

  1. DDR (A) -> Worker (C=A) -> DDR (A)
  2. DDR (A,B) -> Worker (C=A+B) -> DDR (C)

4. Runtime Parameters & synchronization

5. TensorAccessPatterns (TAPs)

  0. DDR -> Worker -> DDR
  1. Write a TensorAccessPattern (TAP) on ``.fill()`` such that the output matches the ref
  2. replace tap with ``simple_tiler()``
  3. Observe a new pattern


2) Single Core Tiled Matrix Multiplication
------------------------------------------

To run the basic matrix multiplication:
   ``cd /notebooks/mlir-aie/myproject``

   ``python basic_mm.py``


The following image shows the dataflow for the single core matrix multiplication:

.. image:: image/single_core.png


How it works:

* `r=2, s=8, t=8` are the intrinsic dimensions for the `MMUL` API used in the kernel (C++) code.
* `m, k, n` are the dimensions of the matrices we want to multiply. We mulitply matrix `A` of size `m x k` with matrix `B` of size `k x n` to get output matrix `C` of size `m x n`.
* `main()` function generates random input matrices, and a reference output matrix. It then calls the `matrix_multiplication_single_core` function. This compiles just-in-time (JIT) during the first call and executes.
* The `matrix_multiplication_single_core` function sets up the dataflow through the AI engines via `ObjectFIFOs`, defines the kernel function and compute tile, then performs the runtime operations to transfer data to/from the AI engines and execute the kernel.

**Vector intrinsic size: (r,s,t)**

Each compute core of the AI Engine is a VLIW vector processor. That is, it can perform 512 int8, or 64 int16 multiply-accumulate operations in parallel, within one clock cycle. It also can perform two loads and one store of vectors in one clock cycle. Therefore, to maximize the performance, the kernel code uses `aie::load_v()` and `aie::store_v()` primitive functions to load entire vectors: a row from matrix A of size `r` and a column from matrix B of size `s`. We also use the `MMUL::mac()` primitive to perform the multiply-accumulate on a pair of vectors. We perform four such vector MACs at once to maximize performance. The APIs and primitives are listed `here <https://www.xilinx.com/htmldocs/xilinx2022_2/aiengine_api/aie_api/doc/modules.html>`_.


**Tiling on the fly using ObjectFifos**

The `fifo_A` and `fifo_B` receive sub-matrices of size `m` x `k` and `k` x `n`, respectively. The FIFOs translate those matrices from a row-major format into the `r` x `s`-sized and `s` x `t`-sized blocks required by the hardware's vector instrinsics before sending them into the compute cores memory.

For matrix A (`fifo_A`), this transformation is expressed using the following wraps and strides as a list of tuples `(wrap, stride)`, given as arguments to the `object_fifo()` operation:
(Note that `//` denotes integer floor-division in Python.)

    
* (m // r, r * k),   # Pair 1
* (k // s, s),       # Pair 2
* (r, k),            # Pair 3
* (s, 1),            # Pair 4


Let us break down each component of this pattern. We do so back-to-front for ease of understanding:

* Pair 4: `(s, 1)`
    * This dimension represents the transfer of a single row of a `r` x `s`-sized tile (our target tile size after the transformation).
    * Wrap: `s` is the length of a row of a `r` x `s`-sized block in units of 4 bytes (i32 elements).
    * Stride: A stride of `1` retrieves contiguous elements.
* Pair 3: `(r, k)`
    * Together with the previous dimension, this dimenison represents the transfer of a single `r` x `s`-sized tile.
    * Wrap: `r` is the number of rows of a `r` x `s`-sized tile.
    * Stride: `k` is the stride between first element of each consecutive row along the `m` dimension, i.e. adding this stride to a memory address points to the element in the matrix directly below the original address. 
* Pair 2: `(k // s, s)`
    * Together with the previous dimensions, this dimension represents the transfer of one row of `r` x `s`-sized tiles, i.e. the first `k` x `s` elements of the input array.
    * Wrap: `k // s` is the number of `r` x `s`-sized tiles along the `k` (columns) dimension.
    * Stride: `s` is the stride between starting elements of consecutive blocks along the `k` dimension, i.e. adding this stridde to a memory address points to the same element in the `r` x `s`-sized block directly to the right of the block of the original address.
* Pair 1: `(m // r, r * k)`
    * Together with the previous dimensions, this dimension transfers the entire `m` x `k`-sized matrix as blocks of `r` x `s`-sized tiles.
    * Wrap: `m // r` is the number of `r` x `s`-sized blocks along the `m` (rows) dimension.
    * Stride: `r * k` is the stride between starting elements of consecutive blocks along the `m` dimension, i.e. adding this stride to a memory address points to the same element in the `r` x `s`-sized block directly below the block of the original address.

The following image describes the pattern of the object fifos for matrix A:

.. image:: image/object_fifo.png


3) Whole Array Matrix Multiplication
------------------------------------

In this example, the above single core matrix multiplication is extended to use all compute tiles of the 4x4 AI Engine array. To run the whole array matrix multiplication:
   ``/notebooks/mlir-aie/programming_examples/basic/matrix_multiplication/whole_array``

   ``make run use_iron=1``


The dataflow in the Matrix Multiplication design is as follows. Two submatrices of size `r` x `s` from matrix A are broacasted across the each row of the AIE tiles. Similarly, two submatrices of size `s` x `t` from matrix B are broadcasted across each column of the AIE tiles. The compute tiles perform the vector multiply-accumulate operations on the submatrices and store the results in the output matrix C.


+---------------+---------------+---------------------+---------------------------+
| Matrix        | Size          | Submatrix Size (1.) | Vector Intrinsic Size (2.)|
+===============+===============+=====================+===========================+
| `A` (Input)   | `M` x `K`     | `m` x `k`           | `r` x `s`                 |
+---------------+---------------+---------------------+---------------------------+
| `B` (Input)   | `K` x `N`     | `k` x `n`           | `s` x `t`                 |
+---------------+---------------+---------------------+---------------------------+
| `C` (Output)  | `M` x `N`     | `m` x `n`           | `r` x `t`                 |
+---------------+---------------+---------------------+---------------------------+


**Multiple levels of tiling (M,K,N) -> (m,k,n) -> (r,s,t)**

We first specify the dimensions `M`, `K`, `N` for the input matrices `A` (`MxK`), and `B` (`KxN`), and the output matrix `C` (`MxN`), as well as their data type. To enable efficient computation, our design will split large input matrices into smaller sub-matrix blocks on two levels; we thus also define the sizes of those sub-matrices. 

At the first level, the constants `m`, `k`, and `n` define the size of the submatrices processed by each AIE core. This is done in the dataflow code.At the second level, we further subdivide using smaller sizes `r`, `s` and `t` -- these are the sizes of required by the vector computation intrinsics of the AIEs. We leverage the multidimensional DMAs available in AIEs, through a higher level abstraction (object fifo), to automatically tile and load at this level. 

The two levels of tiling of the output matrix `C` (`MxN`) is shown below:

.. image:: image/tiling.png




4) Questions
-------------

1. In Exercise 5.3 of the mini tutorial, generate 3 different tensor access patterns (TAPs) for a 2D array. Write the equivalent nested loops for data access in each of them.

2. What role do ObjectFIFOs play in the design of the data movement within the AIE array? Describe how ObjectFIFOs facilitate synchronization between compute cores and memory tiles.

3. Discuss the purpose of "ping" and "pong" phases in data transfer. How does this design choice improve performance in handling large matrices?

4. Change the parameters: (m, k, n, r, s, t) in the code for `Whole Array Matrix Multiplication`, generate performance metrics and compile it into a chart, for int8, int16, int32 and float datatypes. Discuss your observations.

5. Extend the basic passthrough example provided, such that the data passes through two compute tiles instead of one. Measure the performance and compare it with the single compute tile design.

6. Given the basic single tile matrix multiplication example, we can combine it with two tile passthrough to create a cascading matrix multiplication design that uses two compute tiles. Fill the blanks in `chained_matmul.py` and get it working. Measure the performance and compare it with the single tile matrix multiplication design. Change the intrinsic sizes from `2,8,8` to `4,8,4` and describe your observations.


5) Optional Project: Optimizing Whole Array Matrix Multiplication for Small N
------------------------------------------------------------------------------

0. `Tutorial <https://github.com/Xilinx/mlir-aie/tree/main/programming_examples/basic/matrix_multiplication/whole_array>`_
1. `Host code <https://github.com/Xilinx/mlir-aie/blob/main/programming_examples/basic/matrix_multiplication/test.cpp>`_
2. `Dataflow code <https://github.com/Xilinx/mlir-aie/blob/main/programming_examples/basic/matrix_multiplication/whole_array/aie2.py>`_
3. `Kernel code <https://github.com/Xilinx/mlir-aie/blob/dfad2074779ce69db95f24cf7cf7a2a1fabf299d/aie_kernels/aie2/mm.cc#L42>`_

.. image:: image/whole_array_design.png

The above image describes the whole array matrix multiplication design for the Ryzen AI device. 

The whole array design is efficient for matrices that are much bigger than the 4x4 AI Engine array. However, if the N dimension is small, it would be wasteful to pad the matrix with zeros. The following is a design that would be more efficient for small N dimensions:

.. image:: image/project.png

Note that dimenison `N` of input matrix B and the output matrix C is smaller than the number of columns in the AI Engine array. Therefore, we can split the input matrix A into two matrices of size `M/2` x `K` We can then broadcast the two submatrices of A across the rows and the two submatrices of B across the different groups of columns of the AI Engine array as shown. 

Start with the whole array design as reference and implement this project. Present a comparison of performance metrics between this design and the whole array design with padded B matrix for different matrix sizes and datatypes. Analyze your observations.
