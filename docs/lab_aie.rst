Lab: AMD AI-Engine (AIE) Accelerator
=====================================

0) Setup
---------------

1. Login to ``waiter.ucsd.edu`` via RDP (Remote Desktop). Make sure you are in "UCSD Protected" network or connected to UCSD VPN.
2. Open the browser and go to ``http://149.199.80.97:8002``
3. Type your username, select ``mlir-aie`` from the dropdown, and click ``Start``.
4. Open a terminal, navigate to ``mlir-aie/programming_examples/basic/matrix_multiplication/whole_array/`` and run ``make run`` to run the example.


1) Introduction to AI Engine (AIE)
----------------------------------

AIE is a new kind of accelerator architecture developed by AMD that is distinct from CPUs, GPUs and FPGAs. It is designed to be a highly efficient and flexible architecture for accelerating a wide range of workloads. The AIE architecture is based on a dataflow model of computation, where data flows through a network of processing elements (PEs) that are connected by a network-on-chip (NoC). 

An AI Engine has 24 tiles arranged as 6 rows and 4 columns as shown. Each column has a shim tile, a memory tile and four compute tiles. Each of the 16 compute tiles has a local (L1) memory, a DMA and a VLIW processor optimized for large vector operations. 

.. image:: image/aie.png

There are three main components to programming an AI Engine:

1. **Host code (test.cpp):** This runs on the host CPU outside the AI Engine and is responsible for setting up the AI Engine, creating example data, transferring data & instructions to and from the AI Engine, and verifying the results.
2. **Dataflow description (aie.py):** This Python script describes the dataflow within the AI engine. This is acheived by configuring high level primitives such as object fifos, to move data between tiles of the AI Engine. This script also points to the kernel function that will be executed in the VLIW processors of each tile.
3. **Kernel functions (aie_kernels/aie2/mm.cc):** These are C++ functions that are compiled to run in the VLIW processors that make the compute tiles of the AI Engine.


2) Matrix Multiplication with AI Engine
-------------------------

At a high level, each example does the following (in order):

1. **Defining Matrix Dimensions and Data Types:** We first specify the dimensions `M`, `K`, `N` for the input matrices `A` (`MxK`), and `B` (`KxN`), and the output matrix `C` (`MxN`), as well as their data type. To enable efficient computation, our design will split large input matrices into smaller sub-matrix blocks on two levels; we thus also define the sizes of those sub-matrices. At the first level, the constants `m`, `k`, and `n` define the size of the submatrices processed by each AIE core. At the second level, we further subdivide using smaller sizes `r`, `s` and `t` -- these are the sizes of required by the vector computation intrinsics of the AIEs. Tiling of the output matrix is shown below:

.. image:: image/tiling.png

2. **Constructing an AIE Array Configuration:** The NPU hardware is comprised of components laid out in a two-dimensional grid of rows and columns. Based on the matrix sizes and tiling factors, we choose the number of rows, columns, and total number of compute cores of the AIE device that the design should utilize. We then configure the AI Engine array, memory tiles, and shim tiles.

3. **Defining Data Movement Inside the NPU:** ObjectFIFOs are a data movement abstraction for buffering data and synchronizing between AIE components. We configure ObjectFIFOs for `A`, `B` and `C` to transfer and buffer data between AIE components in chunks of the previously defined sizes (`mxk`, `kxn` and `mxn`, respecively).

4. **Defining Core Computations:** The `core_body()` function contains the code that will be loaded onto each AIE core. This code describes the matrix multiplication using the input submatrices `a` and `b` acquired through the ObjectFIFOs. The results are accumulated in the output submatrix `c`.

5. **Defining External Data Transfer Sequences:** The `aie.runtime_sequence()` op sets up matrix data movement from the host into the AIE compute cores, and back to the host after computation. It initializes Data Movement Accelerator (DMA) transfers, sets memory access patterns, and performs synchronization.

6. **Generating the Design:** The `my_matmul()` function triggers the code generation process and represents the main entry point of the design. The final print statement outputs the MLIR representation of the AIE array configuration.


Detailed Design Explanation
+++++++++++++++++++++++++++

The configuration of the AI Engine array is described in the `aie2.py` file.
It is linked against a compute microkernel which is implemented in C++.
The following sections elaborate on each of the steps outlined in the high-level summary above.

| Note: The term "tile" has two distinct meanings in the following discussion that should be distinguishable from context:
|  * AIE tiles are components of the hardware, specifically Shim, Memory and Compute tiles.
|  * Matrix tiles are smaller sub-matrices of the larger input and output matrices.

1. Defining Matrix Dimensions and Data Types
+++++++++++++++++++++++++++++++++++++++++++++++++

In the first section of the code in `aie2.py`, we define the following constants:

+---------------+---------------+---------------------+---------------------------+
| Matrix        | Size          | Submatrix Size (1.) | Vector Intrinsic Size (2.)|
+===============+===============+=====================+===========================+
| ``A`` (Input) | ``M`` x ``K`` | ``m`` x ``k``       | ``r`` x ``s``             |
+---------------+---------------+---------------------+---------------------------+
| ``B`` (Input) | ``K`` x ``N`` | ``k`` x ``n``       | ``s`` x ``t``             |
+---------------+---------------+---------------------+---------------------------+
| ``C`` (Output)| ``M`` x ``N`` | ``m`` x ``n``       | ``r`` x ``t``             |
+---------------+---------------+---------------------+---------------------------+



The input and output matrix sizes are given by the user. We subdivide the input matrices `A`, `B` and the output matrix `C` into smaller, manageable "tiles" (or submatrices) at two levels:

1. **Tiling to Compute Core Submatrix Chunks:** The input and output matrices stream to/from the AIE compute cores in chunks of size of `m`x`k`, `k`x`n` and `n`x`m`. Tiling into these chunks allows each of the computation cores to concurrently work on distinct sub-sections of the input matrices in parallel, which improves performance. This also reduces on-chip memory requirements. The final result is re-assembled using the sub-matrix results of all cores.

| This tiling occurs in the `aie.runtime_sequence()` operation describing the host-to-memory-tile transfer.

We describe it further below, in section *"5. Defining External Data Transfer Sequences"*.

2. **Tiling to Vector Intrinsic Size:** The AIE compute cores calculate the matrix multiplication using efficient "multiply-accumulate" vector intrinsic instructions (`MAC` instructions). These hardware instructions process very small blocks of the matrix: size `r`x`s` blocks of `A` and size `s`x`t` blocks of  `B`, producing an output of size `r`x`t` (`C`). 

| This tiling occurs in the inner-AIE data movements. We describe it in the section *"3. Defining Data Movement Inside the NPU"*.
| The vector intrinsic size is dictated by the hardware and the compute microkernel.

2. Constructing an AIE Array Configuration
+++++++++++++++++++++++++++++++++++++++++++

In the next section of the code, we obtain handles to the components of the hardware. 

The Neural Processing Unit (NPU) is physically structured as an array of 6 rows and 4 columns. The lower two rows contain so-called "shim" and "memory" tiles, and the upper four rows are made up of AIE compute cores (AIEs):

1. **Shim tiles:** A single row of shim tiles on the bottom of the core array is responsible for interfacing with the external host for data movement. In our code, they are represented by a list: `[_0_ShimTile, _1_ShimTile, _2_ShimTile, _3_ShimTile]`

2. **Memory tiles:** A row of memory tiles with scratchpad memory is located above the shim tiles. These memory cores are responsible for staging and distributing the data during processing. In our code, they are represented by a list: `[_0_MemTile, _1_MemTile, _2_MemTile, _3_MemTile]`

3. **Compute tiles:** In each of the four columns, there are 4 rows of computation tiles above the memory tiles. This makes for a total of 16 computation cores, which in this design are configured to perform the matrix multiplication. In our code, they are represented by a list of lists, `cores`, showing their two-dimensional arrangement.

3. Defining Data Movement Inside the NPU:
+++++++++++++++++++++++++++++++++++++++++

We use "ObjectFIFOs" to abstractly describe the data movement and synchronization between AIE Compute, Memory and Shim tiles. ObjectFIFOs present an interface that behaves like a First-In-First-Out queue. To achieve this, they take care of DMA configuration, acquiring and releasing locks, and managing buffers. 

There are several ObjectFIFOs used in this design, which are created using the `object_fifo()` Python binding:

1. Host &rightarrow; Memory Tiles: `inA_fifos`, `inB_fifos` move the input matrices from the external host (via the shim tiles) in row 0 to the memory tiles in row 1.

2. Memory Tiles &rightarrow; Compute Tiles: `memA_fifos`, `memB_fifos` move input data from the memory tiles in row 1 to the compute tiles in rows 2-5.

3. Compute Tiles &rightarrow; Memory Tiles &rightarrow; Host: Analogously, `memC_fifos` and `OutC_fifos` move the output data out from the compute cores to the memory tiles (`memC_fifos`) and from there out to the external host via the shim tiles (`OutC_fifos`).

Each of `inA_fifos`, `inB_fifos`, `OutC_fifos`, `memA_fifos`, `memB_fifos` and `memC_fifos` are Python dictionaries, containing a separate ObjectFIFO instance for each column of AIE compute cores in the array. The respective `*_names` lists contain the names of these ObjectFIFOs.

Of note is the `object_fifo_link()` operation. This operation establishes a connection between the `mem*` FIFOs and the `in*` and `outC` FIFOs. By linking ObjectFIFOs, the output received at one end of the source FIFO is fed as input into the ObjectFIFO listed as the destination.

.. image:: image/whole_array.png


3) Single Core Matrix Multiplication
-------------------------------------

.. image:: image/single_core.png


