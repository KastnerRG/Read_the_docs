.. DFT documentation master file, created by
   sphinx-quickstart on Fri Mar 22 22:58:41 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: Discrete Fourier Transform (DFT)
============================================



1) Introduction
---------------

The goal of this project is to design architectures that implement the Discrete Fourier Transform (DFT). DFT is a common operation in signal processing which generates a discrete frequency domain representation of the discrete input signal. The input signal is a vector of samples and the matrix is a set of basis functions corresponding to discrete cosine and sine waveforms of different frequencies. The multiplication of the input signal with these basis functions describes how well the input signal correlates with those waveforms, which is the value of the Fourier series at that frequency.

We start with the direct implementation of the DFT which is a form of a matrix-vector multiplication. Future projects describe how to refactor the code to perform a fast Fourier transform.

2) Materials
------------

You can download the project files here:

* `DFT Project Repo <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/project3>`_

The repository is organized into five folders, dft_8_precomputed, dft_32_precomputed, dft_256_precomputed, dft_1024_precomputed, and Demo. Each of the first four folders has its own testbench, out.gold.dat file, and coefficients.h file.

Each dft_xx_precomputed folder contains following files:

* dft.cpp - the baseline implementation for the dft function.

* dft.h - header file

* dft_test.cpp - test bench

* coefficientsX.h - a file containing the values of corresponding to one sine/cosine period sampled based upon the DFT points. For example, an 8 point DFT has 8 samples across both the sine and cosine function evenly spaced across one period. This is equivalent to dividing one rotation in the complex plane equally by the number of points in the DFT.

* out.gold.dat - "Golden” output. The testbench (dft_test.cpp) generates a sample input and calls the function dft in dft.cpp with that sample input. This output of the function is compared to the expected output. This will indicate PASS or FAIL. If it fails, then the code in the folder Demo: dft.bit | dft.tcl | project3_host.ipynbn dft is incorrect. There are four different versions of depending on the DFT size and way in which the DFT coefficients were generated.

* script.tcl and directives.tcl file to create the project

Demo folder contains one file:

* DFT.ipynb - notebook for demo

3) Project Goal
---------------

You should modify the code to create a number of different architectures that perform tradeoffs between performance and resource utilization. For dft_32_precomputed and dft_1024_precomputed designs, you need to use precomputed values from coefficients32_2D.h and coefficients1024.h

For 32-point and 1024-point DFTs, you will create a report describing how you generated these different architectures (code restructuring, pragmas utilized, etc.). For each architecture you should provide its results including the resource utilization (BRAMs, DSP48, LUT, FF), and performance in terms of throughput (number of DFT operations/second), latency, clock cycles, clock frequency (which is fixed to 10 ns).

The 8 and 256 point folders are provided for your convenience. If you would like, you can do some of your initial design space optimization on these smaller architectures. But it is not necessary to use these at all.

The key in this project is to understand the tradeoffs between loop optimizations (unrolling and pipelining) and data partitioning. Therefore you should focus on these optimizations.

4) Optimization Guidelines
--------------------------

* You should use a clock period of 10 ns.

* The output of your architecture must closely match the golden output. Be sure to generate a working function before performing any optimizations. If the result does not match exactly, but is close, please explain why in the report. You should use float for all data types. You do not need to perform bitwidth optimization in this project.

* You may want to start implementing DFT by using HLS math functions for cos() and sin(). Then you can optimize your code based on this baseline code.

* There are many different ways to generate the DFT coefficients including using HLS math functions. These can be implemented as constants when the DFT size is fixed. We have given you the coefficients for both 32 (in coefficients32_2D.h) and 1024 (in coefficients1024.h). They each have two constant arrays, sin_table and cos_table. You can use these coefficient arrays directly as memories in your architectures. You are also free to create your own arrays using a different structure (e.g., 2D array, reordering of elements in the given 1D arrays, etc.). Or you could dynamically generate the coefficients.

* There is significant amount of parallelism that can be exploited by (partially) unrolling the for-loops. Pipelining these (partially) unrolled for-loops should lead to higher throughputs. However, you may find that pipelining does not make a difference once you have loop unrolling and array partitioning handled well. When you try to incorporate pipelining, the major issue you will face is data dependencies. You can read more about them `here <https://docs.xilinx.com/r/2022.2-English/ug1399-vitis-hls/Managing-Pipeline-Dependencies>`_. Since you have some data dependencies, accessing memory will be the major overhead. This is why your estimated clock period may go beyond 10ns; to perform some task within N clock cycles each clock cycle needs to be high for the task to be completed. For example, at clock cycle 1 you might write a[1] and at clock cycle 2 you will need to read a[1] which would not be ready as the operation might take 4 clock cycles. This is a data dependency issue which is very common in pipelining. This is why pipelining does not seem to work well even though your loop unrolling and partitioning is the best you can find. Another reason is that the overhead might not be because of the task (it might take only 1 clock cycle), but the memory it is stored in might have only 2 ports or 1 port and this would mean that the memory cannot be accessed in parallel. You can see the critical path in the Synthesis log itself. Otherwise you can open the Analysis view and view which operation(s) or data path is critical and causing this delay, which in turn limits the performance of pipelining. There is a slightly different conversation `here <https://support.xilinx.com/s/question/0D52E00006hpjyTSAQ/pipeline-and-unroll-in-the-for-loop-which-is-better?language=en_US>`_ that may be helpful to read through. This paragraph might make more sense after you complete the project, so be sure to read through it again when you're finalizing your report.

* Unsafe Math Optimizations: Arithmetic associative laws do not necessarily hold using floating point types; the order that you perform a series of arithmetic functions can change their result. E.g., from `What Every Computer Scientist Should Know About Floating-Point Arithmetic <https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html>`_, "Due to roundoff errors, the associative laws of algebra do not necessarily hold for floating-point numbers. For example, the expression (x+y)+z has a totally different answer than x+(y+z) when x = 1030, y = -1030 and z = 1 (it is 1 in the former case, 0 in the latter)." By default, the HLS tool only performs safe optimizations. This may result in unexpected behaviors when using floating point types, e.g., the HLS tool may not do parallelizing arithmetic operations even though they could be performed in parallel. This can be turned off using the unsafe_math_optimizations compiler flag or explicitly stating for a code block to use `expression balancing <https://docs.xilinx.com/r/en-US/ug1399-vitis-hls/pragma-HLS-expression_balance>`_.

* One of the questions will ask you to read about dataflow and apply it to your design. You can think of dataflow as task-level or function-level pipelining. It uses functions (with their limited variable scopes, and clearly defined inputs and outputs) to parallelize some tasks with others. Therefore, roughly speaking, the more function calls you make the better. Or said another way, break your code up so that the functionality does not change but your code is more modular: there will be more function calls happening and therefore more opportunities for function-level pipelining will exist. Now, there are some other things you need to ensure. Dataflow implements FIFO buffers for variables (you can read this in the documentation linked in the question below) and because of this you should limit your reuse of old variables. Each memory address should only be written to once and read from once, but sometimes it is preferable to write back to the memory address repeatedly. It's up to you to determine which is best (or even necessary) for each variable in your design. This means in most variable scopes you will have some extra variables whose entire purpose is to be intermediate variables between functions. There's also an example code linked below that may be helpful to see how intermediate variables and passing variables by reference between functions is done.

* There are more efficient methods for performing the DFT that exploit the symmetries of the Fourier constants, e.g., the Fast Fourier Transform (FFT). **Do not use these symmetries.** In other words, treat this like a matrix-vector multiply with unknown matrix values. The :doc:`Fast Fourier Transform (FFT) Project <project4>` uses an FFT architecture that provides substantial improvement to this DFT architecture.

* You do not need to report your optimizations for your 8 point and 256 point DFT; these folders are provided for your convenience. Since these will very likely synthesize much faster than larger point DFT functions, it may be useful to use these to debug your code or in your initial design space exploration.

* Your report must explicitly state how you calculated the throughput results.

* Here are samples for throughput results achieved by previous students for the DFT project:

		+-----------------------------+---------+
		| Examples of max throughput: | DFT1024 |
		+-----------------------------+---------+
		| Hz                          | 89      |
		+-----------------------------+---------+

5) Questions
------------

Questions 1-5 refers to DFT 32.

* **Question 1: DFT32 Baseline** Implement a baseline HLS implementation for `dft_32`. You may use the `cos()` and `sin()` functions from the math library.
	* **(a)** Now think about if you were to use a custom CORDIC algorithm to calculate `cos()` and `sin()` (you don't have to implement this). Would changing the accuracy of your CORDIC core make the DFT hardware resource usage change? How would it affect the performance?
* **Question 2: DFT32 Table Lookup** Rewrite the code to eliminate these math function calls (i.e. `cos()` and `sin()`) by utilizing a table lookup. Use the provided `*_2D.h` file.
	* **(a)** Make a table that shows the change in resource utilization and performance with between Question 1 and 2.
* **Question 3: DFT32 Interface Change** Modify the DFT function interface so that the input and outputs are stored in separate arrays. Modify the testbench to accommodate this change to DFT interface.
	* **(a)** Why did we do this? Does it affect what optimizations you can perform?
	* **(b)** Make a table that shows the resource utilization and performance from before and after this change.
	* **(c)** Describe the results you see.
* **Question 4: DFT32 Array Partitioning** Experiment with array partitioning. Partition all arrays in your implementation. For now, make sure that your loops are being pipelined with a target II of 1.
	* **(a)** Use block partitioning. Try factors of 1 (i.e. without partitioning), 2, 4, 8, 16, and 32. Make a table showing the achieved II, resource utilization, and performance of each of these implementations.
	* **(b)** Plot resource utilization vs the partition factor on one plot.
	* **(c)** Plot throughput & latency vs the partition factor on separate plots.
* **Question 5: DFT32 Loop Unrolling** Experiment with loop unrolling. Unroll the inner loop only. Use the best array partitioning from Question 4. In order to prevent automatic unrolling by Vitis HLS, you will need to remove the ``#pragma HLS PIPELINE`` pragmas from both loops. Double check that your explicit unrolling is being applied by looking at the synthesis report.
	* **(a)** Try factors of 1 (i.e. without unrolling), 2, 4, 8, 16, and 32. Make a table showing the achieved II, resource utilization, and performance of each of these implementations.
	* **(b)** Plot resource utilization vs the partition factor on one plot.
	* **(c)** Plot throughput & latency vs the partition factor on separate plots.

Questions 6-9 refers to DFT 1024.

* **Question 6: DFT1024 Baseline** You should refer to the baseline DFT code at Figure 4.15 of the textbook.

 - **(a)** Write a basline DFT1024 using the ``sin()`` and ``cos()`` math functions. Do not apply any HLS pragmas. Report latency, throughput, and resource utilization.
 - **(b)** A full 2D lookup table no longer fits on a PYNQ-Z2 board. We can only store a 1D array of precomputed ``sin()`` and ``cos()`` values. Re-write the baseline DFT1024 to use the pre-computed values. Report the latency, throughput and resource utilization.

* **Question 7: DFT1024 Loop optimization**  The baseline DFT1024 from Figure 4.15 of the textbook has data dependencies in the inside loop, which could limit parallelism. One way to tackle this issue is to interchange the two loops. Implement this change and report the latency, throughput, and resource.

* **Question 8: DFT1024 Best Design:** Now that you have explored different optimizations for DFT32, we can go ahead and try their ideas on DFT1024.

 - **(a)** Try any optimization techniques and describe your methodology.
 - **(b)** Report the latency, throughput, and resource utilization of your best design. Your design **must** fit on the PYNQ-Z2 board, which mean all resource utilizations must be less than 100%.
 - **Warning:** Avoid agressively unrolling loops, partionging arrays, or pipelining. This could lead to long design synthesis time, and your design may not fit on board.

* **Question 9: Streaming Interface Synthesis:** Modify your design to allow for streaming inputs and outputs using ``hls::stream``.  You must write your own testbench to account for the function interface change from DTYPE to proper ``hls::stream``.  You can learn about ``hls::stream`` from the `HLS Stream Library <https://docs.amd.com/r/en-US/ug1399-vitis-hls/HLS-Stream-Library>`_. You should also follow the :doc:`Lab: Axistream Multiple DMAs <axidma2>` example. Report the latency, throughput, and resource utilization of your design. Resource utilization must be under 100%. Using your optmized DFT1024 is optional, you can also just convert the baseline DFT1024 to streaming interface.

6) PYNQ Demo
------------

For this demo, your will create an IP for the DFT 1024, and run it from the Jupyter notebook using two DMAs. You should follow the :doc:`Lab: Axistream Multiple DMAs <axidma2>` example.

Another point worth discussing here is why we use pointers for inputs and outputs, and why we have to post-increment the pointer manually (like we did in the multiple DMA lab) when we stream inputs and outputs, but why it is a bad idea to use pointers in your code. You cannot use pointers in HLS; pointers are dynamic memory and Vivado HLS will not be able to synthesize it since it is not a deterministic thing (datapath could change depending on inputs). Arrays, on the other hand, are fixed memory locations and therefore they can be synthesized to vectors in RTL. You can use pointers only as ports and even then you have to specify axistream, otherwise that will lead to synthesis issues as well.

High Performance (HP) AXI ports can be accessed by multiple manager/subordinates. Arbritation is handled by the AXI interconnect. Therefore it is not necessary to enable more than one HP port. This `Xilinx recommends <https://support.xilinx.com/s/question/0D52E00006hpn9gSAA/mcdma-or-multiple-dmas-single-hp-port-or-multiple-hp-ports?language=en_US>`_ using two HP ports if you value performance. If you use multiple HP ports, in the memory map you can see this will give you more space to access (like 512M instead of 256M). So it is always safer to use separate ports although not required. You should have both DMAs be write-enabled (the lab had only one output, but here you have two outputs, so we'll need both). If you choose to use more than one HP port, HP0 and HP1 should have different managers. So HP0 will have the first DMA as its manager, and HP1 will have the second DMA. Two DMAs can point to a single HP port, but two HP ports cannot have the same DMA as manager. Pay attention to which DMAs have been assigned to which interface variables, so you know what values are coming out of the fabric.


7) Submission Procedure
-----------------------

For this project, you must submit a report (PDF) and your code via gradescope. You can find the link to the gradescope assignment in Canvas. Be sure to mark the appropriate page for each question. Be sure to include a link to your github repo and a video for the demo **in the PDF** and mark it accordingly on gradescope. Follow the same instructions for the demo video as in Project: CORDIC.

You must submit your code and .rpt files for each question. Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (``*.cpp``, ``*.h`` files, and ``*.ini`` and ``Makefile``) and directly synthesize it. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well.

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "dft" at the top-level. This folder must be organized as follows (similar to the structure in other projects):

**Contents:**

* **Report.pdf**

* Folder **Q1**
  - coefficients32_2D.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat
  - Reports subfolder
    - .rpt files with intelligible naming (i.e. ``baseline.rpt``)

* Folder **Q2**
  - coefficients32_2D.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat
  - Reports subfolder
    - .rpt files with intelligible naming (i.e. ``table_lookup.rpt``)

* Folder **Q3**
  - coefficients32_2D.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat
  - Reports subfolder
    - .rpt files with intelligible naming (i.e. ``interface_change.rpt``)

* Folder **Q4**
  - coefficients32_2D.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat
  - Reports subfolder
    - .rpt files with intelligible naming (i.e. ``array_partition_1.rpt``)

* Folder **Q5**
  - coefficients32_2D.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat
  - Reports subfolder
    - .rpt files with intelligible naming (i.e. ``loop_unrolling_2.rpt``)

* Folder **Q6b** Your answer to question **6.(b)**: coefficients1024.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat | dft_csynth.rpt

* Folder **Q7** Your answer to question **7**: coefficients1024.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat | dft_csynth.rpt

* Folder **Q8** Your best DFT1024 design: coefficients1024.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat | dft_csynth.rpt

* Folder **Q9** Your DFT1024 with streaming interfaces and streaming testbench: coefficients1024.h | dft.h | dft.cpp | dft_test.cpp | Makefile | __hls_config.ini | output.gold.dat | dft_csynth.rpt

* Folder **Demo**: ``DFT.ipynb`` | ``dft.bit`` | ``dft.hwh``





8) Grading Rubric
-----------------

**70 points:** Response to the questions in your report. 

**30 points:** Full points for correct working DFT1024 on PYNQ. If you have difficulty getting it to work, you can get partial credit (25) for a correctly working DFT32 design on PYNQ.
