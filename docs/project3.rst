.. DFT documentation master file, created by
   sphinx-quickstart on Fri Mar 22 22:58:41 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: Discrete Fourier Transform (DFT)
===========================================

1) Introduction
--------------

The goal of this project is to design architectures that implement the Discrete Fourier Transform (DFT). DFT is a common operation in signal processing which generates a frequency domain representation of the discrete input signal. We start with the direct implementation of the DFT which is a matrix-vector multiplication. The input signal is a vector of samples and the matrix is composed of a set of basis functions corresponding to discrete cosine and sine waveforms of different frequencies. The multiplication of the input signal with these basis functions describes how well the input signal correlates with those waveforms, which is the value of the Fourier series at that frequency.

2) Materials
-----------

The files neccessary for this project can be got from `here <https://github.com/KastnerRG/pp4fpgas/blob/master/labs/DFT.zip?raw=true>`_ 

You can find the following files in the zip file. These are divided into five folders, dft_8_precomputed, dft_32_precomputed, dft_256_precomputed, dft_1024_precomputed, and Demo. Each of the first four folders has its own testbench, out.gold.dat file, and coefficients.h file.

Each dft_xx_precomputed folder contains following files:

* dft.cpp -the baseline implementation for the dft function.

* dft.h -header file

* dft_test.cpp -test bench

* coefficientsX.h -a file containing the values of corresponding to one sine/cosine period sampled based upon the DFT points. For example, an 8 point DFT has 8 samples across both the sine and cosine function evenly spaced across one period. This is equivalent to dividing one rotation in the complex plane equally by the number of points in the DFT.

* out.gold.dat -"Golden” output. The testbench (dft_test.cpp) generates a sample input and calls the function dft in dft.cpp with that sample input. This output of the function is compared to the expected output. This will indicate PASS or FAIL. If it fails, then the code iFolder Demo: dft.bit | dft.tcl | project3_host.ipynbn dft is incorrect. There are four different versions of depending on the DFT size and way in which the DFT coefficients were generated.

* script.tcl and directives.tcl file to create the project

Demo folder contains one file:

* DFT.ipynb - notebook for demo

3) Project Goal
--------------

You should modify the code to create a number of different architectures that perform tradeoffs between performance and area. For dft_256_precomputed and dft_1024_precomputed designs, you need to use precomputed values from coefficients256.h and coefficients1024.h

For 256-point and 1024-point DFTs, you will create a report describing how you generated these different architectures (code restructuring, pragmas utilized, etc.). For each architecture you should provide its results including the resource utilization (BRAMs, DSP48, LUT, FF), and performance in terms of throughput (number of DFT operations/second), latency, clock cycles, clock frequency (which is fixed to 10 ns). You can do most of the design space exploration on the 256 point DFT. You should pick your “best” 256 architecture and synthesize that as a 1024 DFT.

The 8 and 32 point folders are provided for your convenience. If you would like, you can do some of your initial design space optimization on these smaller architectures. But it is not necessary to use these at all.

The key in this project is to understand the tradeoffs between loop optimizations (unrolling and pipelining) and data partitioning. Therefore you should focus on these optimizations.

4) Optimization guidelines
-------------------------

* You should use a clock period of 10 ns.

* The output of your architecture must closely match the golden output. Be sure to generate a working function before performing any optimizations. If the result does not match exactly, but is close, please explain why in the report. You should use float for all data types. You do not need to perform bitwidth optimization of this project.

* You may want to start implementing DFT by using HLS math functions for cos() and sin(). Then you can optimize your code based on this baseline code.

* There are many different ways to generate the DFT coefficients including using HLS math functions. These can be implemented as constants when the DFT size is fixed. We have given you the coefficients for both 256 (in coefficients256.h) and 1024 (in coefficients1024.h). They each have two constant arrays, sin_table and cos_table. You can use these coefficient arrays directly as memories in your architectures. You are also free to create your own arrays using a different structure (e.g., 2D array, reordering of elements in the given 1D arrays, etc.). Or you could dynamically generate the coefficients.

* There is significant amount of parallelism that can be exploited by (partially) unrolling the for loops. Pipelining these (partially) unrolled for loops should lead to higher throughputs.

* There are more efficient methods for performing the DFT that exploit the symmetries of the Fourier constants, e.g., the fast Fourier transform (FFT). **Do not use these symmetries.** In other words, treat this like a matrix-vector multiply with unknown matrix values. Don’t worry, we will implement FFT architectures soon enough that will fully take advantage of these symmetries.

* You do not need to report your optimizations for your 8 point and 32 point DFT; these folders are provided for your convenience. Since these will very likely synthesize much faster than larger point DFT functions, it may be useful to use these to debug your code or in your initial design space exploration.

* Your report must explicitly state how you calculated the throughput results. Note that this is often not simply a function of the latency and the clock period, and involves using the initiation interval.

5) Questions
-----------

* **Question 1:** What changes would this code require if you were to use a custom CORDIC similar to what you designed for Project 2? Compared to a baseline code with HLS math functions for cos() and sin(), would changing the accuracy of your CORDIC core make the DFT hardware resource usage change? How would it affect the performance? Note that you do not need to implement the CORDIC in your code, we are just asking you to discuss potential tradeoffs that would be possible if you used a CORDIC that you designed instead of the one from Xilinx.

* **Question 2:** Rewrite the code to eliminate these math function calls (i.e. cos() and sin()) by utilizing a table lookup. How does this change the throughput and area? What happens to the table lookup when you change the size of your DFT?

* **Question 3:** Modify the DFT function interface so that the input and outputs are stored in separate arrays. How does this affect the optimizations that you can perform? How does it change the performance? What about the area results? Modify your testbench to accommodate this change to DFT interface.**You should use this modified interface for the remaining questions.**

* **Question 4:** Study the effects of loop unrolling and array partitioning on the performance and area. What is the relationship between array partitioning and loop unrolling? Does it help to perform one without the other? Plot the performance in terms of number of matrix vector multiply operations per second (throughput) versus the unroll and array partitioning factor. Plot the same trend for area (showing LUTs, FFs, DSP blocks, BRAMs). What is the general trend in both cases? Which design would you select? Why?

* **Question 5:** Please read dataflow section in the `HLS user guide <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis.pdf#page=145>`_,and apply dataflow pragma to your design to improve throughput. You may need to change your code and make submodules. How much improvement can you make with it? How much does your design use resources? What about BRAM usage? Please describe your architecture with figures on your report. (Make sure to add dataflow pragma on your top function.)

* **Question 6:** (Best architecture) Briefly describe your "best" architecture. In what way is it the best? What optimizations did you use to obtain this result? What is tradeoff you consider for the best architecture?

* **Question 7:** (Bonus; streaming architecture) If you create a design using hls::stream, you will get bonus points of Project 3. We do not provide any testbench for this case since this is optional. You must write your own testbench because we expect you to change the function prototype from DTYPE to hls::stream. Please briefly describe what benefit you can achieve with hls::stream and why? NOTE: To get the full bonus point, your design must pass Co-Simulation (Not C-Simulation). You can learn about hls::stream from the `HLS user guide <ttps://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis.pdf#page=216>`_.

6) PYNQ Demo
------

For this demo, your will create an IP for the DFT 1024, and run it from the Jupyter notebook using DMAs. You need to follow the :doc:`Lab: Axistream Multiple DMAs<axidma2>`'s example, with the only difference being that you will have 2 inputs and 2 outputs instead of 2 inputs and 1 output. Unlike the lab here you cannot start computation immediately after you stream an input. You must stream all inputs, compute DFT and stream all outputs.

7) Submission Procedure
----------------------

You must submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (*.cpp, *.h files, and scripts) and directly synthesize it. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment (dft_test.cpp, dft.h, etc.).

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

* **Note**: Provide the architectures that you used to answer the questions: make sure each folder contains the source code (*.cpp, *.h, *.tcl only) and the reports (.rpt and .xml).

* **Note** Do **not** submit DFT 8 and 32.

 

8) Grading Rubric
----------

**50 points:** Response to the questions in your report. Points will be deducted based upon poor presentation, grammar, formatting, spelling, etc. Results should be discussed succinctly but with a enough detail to understand your architectures and tradeoffs. Tables and figures should be properly labeled, well thought out, and described in the text with comments on both the design that produced each entry, and the observable trends between entries. Spelling errors are unacceptable.

**50 points:** Correct working project on PYNQ.
   


