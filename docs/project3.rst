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

You should modify the code to create a number of different architectures that perform tradeoffs between performance and resource utilization. For dft_256_precomputed and dft_1024_precomputed designs, you need to use precomputed values from coefficients256.h and coefficients1024.h

For 256-point and 1024-point DFTs, you will create a report describing how you generated these different architectures (code restructuring, pragmas utilized, etc.). For each architecture you should provide its results including the resource utilization (BRAMs, DSP48, LUT, FF), and performance in terms of throughput (number of DFT operations/second), latency, clock cycles, clock frequency (which is fixed to 10 ns). You can do most of the design space exploration on the 256 point DFT. You should pick your “best” 256 architecture and synthesize that as a 1024 DFT.

The 8 and 32 point folders are provided for your convenience. If you would like, you can do some of your initial design space optimization on these smaller architectures. But it is not necessary to use these at all.

The key in this project is to understand the tradeoffs between loop optimizations (unrolling and pipelining) and data partitioning. Therefore you should focus on these optimizations.

4) Optimization Guidelines
--------------------------

* You should use a clock period of 10 ns.

* The output of your architecture must closely match the golden output. Be sure to generate a working function before performing any optimizations. If the result does not match exactly, but is close, please explain why in the report. You should use float for all data types. You do not need to perform bitwidth optimization in this project.

* You may want to start implementing DFT by using HLS math functions for cos() and sin(). Then you can optimize your code based on this baseline code.

* There are many different ways to generate the DFT coefficients including using HLS math functions. These can be implemented as constants when the DFT size is fixed. We have given you the coefficients for both 256 (in coefficients256.h) and 1024 (in coefficients1024.h). They each have two constant arrays, sin_table and cos_table. You can use these coefficient arrays directly as memories in your architectures. You are also free to create your own arrays using a different structure (e.g., 2D array, reordering of elements in the given 1D arrays, etc.). Or you could dynamically generate the coefficients.

* There is significant amount of parallelism that can be exploited by (partially) unrolling the for-loops. Pipelining these (partially) unrolled for-loops should lead to higher throughputs. However, you may find that pipelining does not make a difference once you have loop unrolling and array partitioning handled well. When you try to incorporate pipelining, the major issue you will face is data dependencies. You can read more about them `here <https://www.xilinx.com/html_docs/xilinx2021_1/vitis_doc/vitis_hls_optimization_techniques.html#wen1539734225565>`_. Since you have some data dependencies, accessing memory will be the major overhead. This is why your estimated clock period may go beyond 10ns; to perform some task within N clock cycles each clock cycle needs to be high for the task to be completed. For example, at clock cycle 1 you might write a[1] and at clock cycle 2 you will need to read a[1] which would not be ready as the operation might take 4 clock cycles. This is a data dependency issue which is very common in pipelining. This is why pipelining does not seem to work well even though your loop unrolling and partitioning is the best you can find. Another reason is that the overhead might not be because of the task (it might take only 1 clock cycle), but the memory it is stored in might have only 2 ports or 1 port and this would mean that the memory cannot be accessed in parallel. You can see the critical path in the Synthesis log itself. Otherwise you can open the Analysis view and view which operation(s) or data path is critical and causing this delay, which in turn limits the performance of pipelining. There is a slightly different conversation `here <https://support.xilinx.com/s/question/0D52E00006hpjyTSAQ/pipeline-and-unroll-in-the-for-loop-which-is-better?language=en_US>`_ that may be helpful to read through. This paragraph might make more sense after you complete the project, so be sure to read through it again when you're finalizing your report.

* Unsafe Math Optimizations: Arithmetic associative laws do not necessarily hold using floating point types; the order that you perform a series of arithmetic functions can change their result. E.g., from `What Every Computer Scientist Should Know About Floating-Point Arithmetic <https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html>`_, "Due to roundoff errors, the associative laws of algebra do not necessarily hold for floating-point numbers. For example, the expression (x+y)+z has a totally different answer than x+(y+z) when x = 1030, y = -1030 and z = 1 (it is 1 in the former case, 0 in the latter)." By default, the HLS tool only performs safe optimizations. This may result in unexpected behaviors when using floating point types, e.g., the HLS tool may not not parallelizing arithmetic operations even though they could be performed in parallel. This can be turned off using the unsafe_math_optimizations compiler flag or explicitly stating for a code block to use `expression balancing <https://www.xilinx.com/html_docs/xilinx2021_1/vitis_doc/hls_pragmas.html#ariaid-title12>`_.

* One of the questions will ask you to read about dataflow and apply it to your design. You can think of dataflow as task-level or function-level pipelining. It uses functions (with their limited variable scopes, and clearly defined inputs and outputs) to parallelize some tasks with others. Therefore, roughly speaking, the more function calls you make the better. Or said another way, break your code up so that the functionality does not change but your code is more modular: there will be more function calls happening and therefore more opportunities for function-level pipelining will exist. Now, there are some other things you need to ensure. Dataflow implements FIFO buffers for variables (you can read this in the documentation linked in the question below) and because of this you should limit your reuse of old variables. Each memory address should only be written to once and read from once, but sometimes it is preferable to write back to the memory address repeatedly. It's up to you to determine which is best (or even necessary) for each variable in your design. This means in most variable scopes you will have some extra variables whose entire purpose is to be intermediate variables between functions. There's also an example code linked below that may be helpful to see how intermediate variables and passing variables by reference between functions is done.

* There are more efficient methods for performing the DFT that exploit the symmetries of the Fourier constants, e.g., the Fast Fourier Transform (FFT). **Do not use these symmetries.** In other words, treat this like a matrix-vector multiply with unknown matrix values. The :doc:`Fast Fourier Transform (FFT) Project <project4>` uses an FFT architecture that provides substantial improvement to this DFT architecture.

* You do not need to report your optimizations for your 8 point and 32 point DFT; these folders are provided for your convenience. Since these will very likely synthesize much faster than larger point DFT functions, it may be useful to use these to debug your code or in your initial design space exploration.

* Your report must explicitly state how you calculated the throughput results. Note that this is often not simply a function of the latency and the clock period, and involves using the initiation interval (II). Hint: Think about how many outputs you obtain from one run of your DFT operation.

* Here are samples for throughput results achieved by previous students for the DFT project:

		+-----------------------------+--------+---------+
		| Examples of max throughput: | DFT256 | DFT1024 |
		+-----------------------------+--------+---------+
		| DFT/second                  | 1247   | 79      |
		+-----------------------------+--------+---------+
		| Hz                          | 1370   | 89      |
		+-----------------------------+--------+---------+

5) Questions
------------

* **Question 1:** What changes would this code require if you were to use a custom CORDIC similar to what you designed for Project: CORDIC? Compared to a baseline code with HLS math functions for cos() and sin(), would changing the accuracy of your CORDIC core make the DFT hardware resource usage change? How would it affect the performance? Note that you do not need to implement the CORDIC in your code, we are just asking you to discuss potential tradeoffs that would be possible if you used a CORDIC that you designed instead of the one from Xilinx.

* **Question 2:** Rewrite the code to eliminate these math function calls (i.e. `cos()` and `sin()`) by utilizing a table lookup. How does this change the throughput and resource utilization? What happens to the table lookup when you change the size of your DFT?

* **Question 3:** Modify the DFT function interface so that the input and outputs are stored in separate arrays. Modify the testbench to accommodate this change to DFT interface. How does this affect the optimizations that you can perform? How does it change the performance? And how does the resource usage change? **You should use this modified interface for the remaining questions.**

* **Question 4: Loop Optimizations:** Examine the effects of loop unrolling and array partitioning on the performance and resource utilization. What is the relationship between array partitioning and loop unrolling? Does it help to perform one without the other? Plot the performance in terms of number of DFT operations per second (throughput) versus the unroll and array partitioning factor. Plot the same trend for resources (showing LUTs, FFs, DSP blocks, BRAMs). What is the general trend in both cases?  Which design would you select? Why?

* **Question 5: Dataflow:** Apply dataflow pragma to your design to improve throughput. You may need to change your code and make submodules so that it aligns with the task-level or function-level modularity that dataflow can exploit; Xilinx provides `some examples of dataflow code <https://github.com/Xilinx/Vitis-HLS-Introductory-Examples/tree/master/Dataflow>`_. The `HLS User Guide pages 145-154 <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis.pdf#page=145>`_ and `this summary <https://www.xilinx.com/html_docs/xilinx2017_4/sdaccel_doc/sxx1504034358866.html>`_ provide more information.  How much improvement does dataflow provide? How does  dataflow affect resource usage? What about BRAM usage specifically? Did you modify the code to make it more amenable to dataflow? If so, how? Please describe your architecture(s) with figures on your report.

* **Question 6: Best architecture:** Briefly describe your "best" architecture. In what way is it the best? What optimizations did you use to obtain this result? What are the tradeoffs that you considered in order to obtain this architecture?

* **Question 7: Streaming Interface Synthesis:** Modify your design to allow for streaming inputs and outputs using hls::stream.  You must write your own testbench to account for the function interface change from DTYPE to hls::stream.  NOTE: your design must pass Co-Simulation (not just C-Simulation). You can learn about hls::stream from the `HLS Stream Library <https://www.xilinx.com/html_docs/xilinx2021_1/vitis_doc/hls_stream_library.html#mes1539734221433>`_. An example of code with both hls::stream and dataflow is available (along with its testbench) `here <https://github.com/Xilinx/SDAccel_Examples/blob/master/getting_started/dataflow/dataflow_stream_array_c/src/N_stage_adders.cpp>`_, and another `example showing hls::stream between functions <https://github.com/Xilinx/Vitis_Accel_Examples/blob/master/cpp_kernels/dataflow_stream/src/adder.cpp>`_. Describe the major changes that you made to your code to implement the streaming interface. What benefits does the streaming interface provide? What are the drawbacks?

6) PYNQ Demo
------------

For this demo, your will create an IP for the DFT 1024, and run it from the Jupyter notebook using two DMAs. You need to follow the :doc:`Lab: Axistream Multiple DMAs <axidma2>` example, with the major difference being that you will have 2 inputs and 2 outputs instead of 2 inputs and 1 output. Therefore you will have to enable read and write for both the DMAs, which is different from the lab instructions.

You will additionally need to change the depth of your variable interface ports (you can read more about that `here <https://www.xilinx.com/html_docs/xilinx2017_4/sdaccel_doc/jit1504034365862.html>`_). For the single `s_axilite` port, you can either choose to do `port=length` like we did for the lab (in which case you will need to add a constant to your block diagram like we do in the lab, and you will need to write the length from Jupyter to the appropriate address), or you can choose to do `port=return` (in which case `ap_start` will not appear in your HLS IP, and you will need to write 1 to the appropriate address from Jupyter to start the process like in previous projects and labs).

Note that you will need to change the axis data type from the one in the lab. The lab uses an int; the project uses float.

Unlike the lab here you cannot start computation immediately after you stream an input struct. You must stream in all struct inputs, then compute the DFT using their float components, and finally stream all outputs as structs. When streaming the output structs, the `last` bit should be set to 1 for the last struct to be streamed, indicating end of stream. You may need to explicitly set the other `last` bits to 0, otherwise your stream may terminate early and without warning since there may be garbage data at the memory addresses of the struct you create that are streamed out. You do not need to do this for inputs, as the tool takes care of it for you. Sometimes, the output streaming's `last` bit is also handled by the tool, but sometimes it may not be, which will cause the DMA to hang (corresponding to a forever-running Jupyter cell) and it is better to hard code it.

Another point worth discussing here is why we use pointers for inputs and outputs, and why we have to post-increment the pointer manually (like we did in the multiple DMA lab) when we stream inputs and outputs, but why it is a bad idea to use pointers in your code. You cannot use pointers in HLS; pointers are dynamic memory and Vivado HLS will not be able to synthesize it since it is not a deterministic thing (datapath could change depending on inputs). Arrays, on the other hand, are fixed memory locations and therefore they can be synthesized to vectors in RTL. You can use pointers only as ports and even then you have to specify axistream, otherwise that will lead to synthesis issues as well.

High Performance (HP) AXI ports can be accessed by multiple manager/subordinates. Arbritation is handled by the AXI interconnect. Therefore it is not necessary to enable more than one HP port. This `Xilinx recommends <https://support.xilinx.com/s/question/0D52E00006hpn9gSAA/mcdma-or-multiple-dmas-single-hp-port-or-multiple-hp-ports?language=en_US>`_ using two HP ports if you value performance. If you use multiple HP ports, in the memory map you can see this will give you more space to access (like 512M instead of 256M). So it is always safer to use separate ports although not required. You should have both DMAs be write-enabled (the lab had only one output, but here you have two outputs, so we'll need both). If you choose to use more than one HP port, HP0 and HP1 should have different managers. So HP0 will have the first DMA as its manager, and HP1 will have the second DMA. Two DMAs can point to a single HP port, but two HP ports cannot have the same DMA as manager. Pay attention to which DMAs have been assigned to which interface variables, so you know what values are coming out of the fabric.


7) Submission Procedure
-----------------------

You must submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (*.cpp, *.h files, and *.tcl) and directly synthesize it. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well.

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "dft" at the top-level. This folder must be organized as follows (similar to the structure in other projects):

**Contents:**

* **Report.pdf**

* Folder **dft256_baseline**

* Folder **dft256_optimized1**

* Folder **dft256_optimized2**

* ...

* Folder **dft256_dataflow**

* Folder **dft256_best**

* Folder **dft1024_best**

* Folder **Demo**: ``DFT.ipynb`` | ``dft.bit`` | ``dft.hwh``

* **Note**: Provide every architecture that you used to answer the questions: make sure each folder contains the source code (*.cpp, *.h, *.tcl only) and the reports (.rpt and .xml).

* **Note**: Do **not** submit DFT 8 and 32.



8) Grading Rubric
-----------------

**50 points:** Response to the questions in your report. Your answers should be well written and clearly delineated (for example: by copying the questions into the report before answering them, or placing each question under a separate subheading). Additional points (up to 20) will be subtracted for poor formatting and/or answers that are hard to understand. Examples of issues include any spelling errors, multiple/egregious grammar errors, poor presentation of results, lack of written comparison of the results, etc. Report the throughput and resource usage for each design you discuss in your report, and include the files for these designs in your submission. We encourage the use of tables for stating results and the changes that produced them, and figures to draw comparisons between different designs. Use these figures and tables in your discussion. A well-written report is informative but not overly verbose. You will be deducted points if you do not follow the instructions on directory naming and file structure.

**50 points:** Correct working project on PYNQ.
