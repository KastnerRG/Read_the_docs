.. DFT documentation master file, created by
   sphinx-quickstart on Fri Mar 22 22:58:41 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project 3: Discrete Fourier Transform (DFT)
===========================================

1) Introduction
---------------

The goal of this project is to design architectures that implement the Discrete Fourier Transform (DFT). DFT is a common operation in signal processing which generates a frequency domain representation of the discrete input signal. We start with the direct implementation of the DFT which is a matrix-vector multiplication. The input signal is a vector of samples and the matrix is composed of a set of basis functions corresponding to discrete cosine and sine waveforms of different frequencies. The multiplication of the input signal with these basis functions describes how well the input signal correlates with those waveforms, which is the value of the Fourier series at that frequency.

2) Materials
------------

The files necessary for this project can be found `here <https://github.com/KastnerRG/pp4fpgas/blob/master/labs/DFT.zip?raw=true>`_.

You can find the following files in the zip file: they are divided into five folders, dft_8_precomputed, dft_32_precomputed, dft_256_precomputed, dft_1024_precomputed, and Demo. Each of the first four folders has its own testbench, out.gold.dat file, and coefficients.h file.

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

You should modify the code to create a number of different architectures that perform tradeoffs between performance and area. For dft_256_precomputed and dft_1024_precomputed designs, you need to use precomputed values from coefficients256.h and coefficients1024.h

For 256-point and 1024-point DFTs, you will create a report describing how you generated these different architectures (code restructuring, pragmas utilized, etc.). For each architecture you should provide its results including the resource utilization (BRAMs, DSP48, LUT, FF), and performance in terms of throughput (number of DFT operations/second), latency, clock cycles, clock frequency (which is fixed to 10 ns). You can do most of the design space exploration on the 256 point DFT. You should pick your “best” 256 architecture and synthesize that as a 1024 DFT.

The 8 and 32 point folders are provided for your convenience. If you would like, you can do some of your initial design space optimization on these smaller architectures. But it is not necessary to use these at all.

The key in this project is to understand the tradeoffs between loop optimizations (unrolling and pipelining) and data partitioning. Therefore you should focus on these optimizations.

4) Optimization Guidelines
--------------------------

* You should use a clock period of 10 ns.

* The output of your architecture must closely match the golden output. Be sure to generate a working function before performing any optimizations. If the result does not match exactly, but is close, please explain why in the report. You should use float for all data types. You do not need to perform bitwidth optimization in this project.

* You may want to start implementing DFT by using HLS math functions for cos() and sin(). Then you can optimize your code based on this baseline code.

* There are many different ways to generate the DFT coefficients including using HLS math functions. These can be implemented as constants when the DFT size is fixed. We have given you the coefficients for both 256 (in coefficients256.h) and 1024 (in coefficients1024.h). They each have two constant arrays, sin_table and cos_table. You can use these coefficient arrays directly as memories in your architectures. You are also free to create your own arrays using a different structure (e.g., 2D array, reordering of elements in the given 1D arrays, etc.). Or you could dynamically generate the coefficients.

* There is significant amount of parallelism that can be exploited by (partially) unrolling the for-loops. Pipelining these (partially) unrolled for-loops should lead to higher throughputs. However, you may find that pipelining doesn't make a difference once you have loop unrolling and array partitioning handled well. When you try to incorporate pipelining, the major issue you will face is data dependencies. You can read more about them `here <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_2/ug902-vivado-high-level-synthesis.pdf#page=133>`_. Since you have some data dependencies, accessing memory will be the major overhead. This is why your estimated clock period may go beyond 10ns; to perform some task within N clock cycles each clock cycle needs to be high for the task to be completed. For example, at clock cycle 1 you might write a[1] and at clock cycle 2 you will need to read a[1] which would not be ready as the operation might take 4 clock cycles. This is a data dependency issue which is very common in pipelining. This is why pipelining does not seem to work well even though your loop unrolling and partitioning is the best you can find. Another reason is that the overhead might not be because of the task (it might take only 1 clock cycle), but the memory it is stored in might have only 2 ports or 1 port and this would mean that the memory cannot be accessed in parallel. You can see the critical path in the Synthesis log itself. Otherwise you can open the Analysis view and view which operation(s) or data path is critical and causing this delay, which in turn limits the performance of pipelining. There is a slightly different conversation `here <https://forums.xilinx.com/t5/High-Level-Synthesis-HLS/Pipeline-and-unroll-in-the-for-loop-which-is-better/td-p/909247>`_ that may be helpful to read through. This paragraph might make more sense after you complete the project, so be sure to read through it again when you're finalizing your report. 

* There are more efficient methods for performing the DFT that exploit the symmetries of the Fourier constants, e.g., the Fast Fourier Transform (FFT). **Do not use these symmetries.** In other words, treat this like a matrix-vector multiply with unknown matrix values. Don’t worry, we will implement FFT architectures soon enough that will fully take advantage of these symmetries in :doc:`Project 4: Fast Fourier Transform (FFT)<project4>`.

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

* **Question 1:** What changes would this code require if you were to use a custom CORDIC similar to what you designed for Project 2? Compared to a baseline code with HLS math functions for cos() and sin(), would changing the accuracy of your CORDIC core make the DFT hardware resource usage change? How would it affect the performance? Note that you do not need to implement the CORDIC in your code, we are just asking you to discuss potential tradeoffs that would be possible if you used a CORDIC that you designed instead of the one from Xilinx.

* **Question 2:** Rewrite the code to eliminate these math function calls (i.e. cos() and sin()) by utilizing a table lookup. How does this change the throughput and area? What happens to the table lookup when you change the size of your DFT?

* **Question 3:** Modify the DFT function interface so that the input and outputs are stored in separate arrays. How does this affect the optimizations that you can perform? How does it change the performance? What about the area results? Modify your testbench to accommodate this change to DFT interface.**You should use this modified interface for the remaining questions.**

* **Question 4:** Study the effects of loop unrolling and array partitioning on the performance and area. What is the relationship between array partitioning and loop unrolling? Does it help to perform one without the other? Plot the performance in terms of number of matrix vector multiply operations per second (throughput) versus the unroll and array partitioning factor. Plot the same trend for area (showing LUTs, FFs, DSP blocks, BRAMs). What is the general trend in both cases? Which design would you select? Why?

* **Question 5:** Please read the dataflow section in the `HLS User Guide pages 145-154 <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis.pdf#page=145>`_, or this `page <https://www.xilinx.com/html_docs/xilinx2017_4/sdaccel_doc/sxx1504034358866.html>`_, and apply dataflow pragma to your design to improve throughput. You may need to change your code and make submodules; an example of dataflow code is available `here <https://github.com/Xilinx/HLS-Tiny-Tutorials/blob/master/coding_dataflow_rewind/diamond.cpp>`_. How much improvement can you make with it? How much does your design use resources? What about BRAM usage? Please describe your architecture with figures on your report. (Make sure to add the dataflow pragma on your top function.) 

* **Question 6:** (Best architecture) Briefly describe your "best" architecture. In what way is it the best? What optimizations did you use to obtain this result? What is tradeoff you consider for the best architecture?

* **Question 7:** (Bonus; streaming architecture) If you create a design using hls::stream, you will get bonus points for Project 3. We do not provide a testbench for this case since this is optional. You must write your own testbench because we expect you to change the function prototype from DTYPE to hls::stream. Please briefly describe what benefit you can achieve with hls::stream and why? NOTE: To get the full bonus point, your design must pass Co-Simulation (Not C-Simulation). You can learn about hls::stream from the `HLS user guide <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis.pdf#page=216>`_. An example of code with both hls::stream and dataflow is available (along with its testbench) `here <https://github.com/Xilinx/SDAccel_Examples/blob/master/getting_started/dataflow/dataflow_stream_array_c/src/N_stage_adders.cpp>`_.

6) PYNQ Demo
------------

For this demo, your will create an IP for the DFT 1024, and run it from the Jupyter notebook using two DMAs. You need to follow the :doc:`Lab 2b: Axistream Multiple DMAs<axidma2>`' example, with the only difference being that you will have 2 inputs and 2 outputs instead of 2 inputs and 1 output. Therefore you will have to enable read and write for both the DMAs, which is different from the lab instructions.

You will additionally need to change the depth of your interface ports to 1024 (you can read more about that `here <https://www.xilinx.com/html_docs/xilinx2017_4/sdaccel_doc/jit1504034365862.html>`_).

Note that the DTYPE struct in this project is exactly like the axis_t typedef we used in Lab 2b, containing a float (data) and an int (last).

Unlike the lab here you cannot start computation immediately after you stream an input struct. You must stream in all struct inputs, then compute the DFT using their float components, and finally stream all outputs as structs. When streaming the output structs, the last bit should be set to 1 for the last struct to be streamed, indicating end of stream. You may need to explicitly set the other last bits to 0, otherwise your stream may terminate early and without warning. You do not need to do this for inputs, as the tool takes care of it for you. Sometimes, the output streaming's last bit is also handled by the tool, but sometimes it may not which will cause the DMA to hang (corresponding to a forever running Jupyter cell) and it is better to hard code it.

Another point worth discussing here is why we use pointers for inputs and outputs, and why we have to increment the pointer manually (like we did in Lab 2b) when we stream inputs and outputs, but why it is a bad idea to use pointers in your code. You cannot use pointers in HLS; pointers are dynamic memory and Vivado HLS will not be able to synthesize it since it is not a deterministic thing (datapath could change depending on inputs). Arrays, on the other hand, are fixed memory locations and therefore they can be synthesized to vectors in RTL. You can use pointers only as ports and you have to specify axistream, otherwise that will lead to synthesis issues as well.

In Vivado, the HP ports are High Performance ports which can be accessed by several interfaces. It is something like dynamic channel (also known as memory) which can access the entire channel at one go. Therefore it is not necessary to enable more than one HP port. This `link <https://forums.xilinx.com/t5/Processor-System-Design-and-AXI/MCDMA-or-Multiple-DMAs-Single-HP-port-or-Multiple-HP-ports/td-p/991992>`_ says to use two HP ports if you value performance. If you use multiple HP ports, in the memory map you can see this will give you more space to access (like 512M instead of 256M). So it is always safer to use separate ports although not required. You should have both DMAs be write-enabled (the lab had only one output, but here you have two outputs, so we'll need both). If you choose to use more than one HP port, HP0 and HP1 should have different masters. So HP0 will have the first DMA as its master, and HP1 will have the second DMA. Two DMAs can point to a single HP port, but two HP ports cannot have the same DMA as master. 


7) Submission Procedure
-----------------------

You must submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (*.cpp, *.h files, and *.tcl) and directly synthesize it. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment (dft_test.cpp, dft.h, etc.).

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "dft" at the top-level. This folder must be organized as follows (similar to project1 or project2):

**Contents:**

* **Report.pdf**

* Folder **dft256_baseline**

* Folder **dft256_optimized1**

* Folder **dft256_optimized2**

* ...

* Folder **dft256_dataflow**

* Folder **dft256_best**

* Folder **dft1024_best**

* Folder **Demo**: DFT.ipynb | dft.bit | dft.hwh

* **Note**: Provide every architecture that you used to answer the questions: make sure each folder contains the source code (*.cpp, *.h, *.tcl only) and the reports (.rpt and .xml).

* **Note** Do **not** submit DFT 8 and 32.

 

8) Grading Rubric
-----------------

**50 points:** Response to the questions in your report. Points will be deducted based upon poor presentation, grammar, formatting, spelling, etc. Results should be discussed succinctly but with a enough detail to understand your architectures and tradeoffs. Tables and figures should be properly labeled, well thought out, and described in the text with comments on both the design that produced each entry, and the observable trends between entries. Spelling errors are unacceptable.

**50 points:** Correct working project on PYNQ.
   


