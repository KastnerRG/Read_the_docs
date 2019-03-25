.. OFDM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project 4: FFT - OFDM Receiver
==============================

1. Introduction
---------------

In this project, you will learn the basic idea behind an orthogonal frequency-division multiplexing (OFDM) system by implementing a simple OFDM receiver in programmable logic. A major part of OFDM is a Fast Fourier Transform (FFT), and thus that is a major focus of this project. The project guides you through the process of building an efficient FFT module one submodule at a time. You are given a set of test benches for the different submodules. You should design and test each individual submodule individually and integrate them into the FFT module. In the final part of the project, you will complete the OFDM receiver by combining the FFT module with a QPSK symbol decoder.

2.Goal
------

The OFDM receiver is divided into two parts -- the FFT and the QPSK decoder. The FFT implementation is divided into multiple stages. The first stage of the FFT reorders the input data using a bit reversal scheme. This gets added into a “software” version of the code which we have provided for you (minus the bit reversal portion). After that, you will create a more hardware friendly FFT architecture. We have provided a set of testbenches for individual functions in addition to the testbenches for the overall FFT. Finally, you must design and implement a QPSK decoder, and integrate it with the FFT to complete the receiver. While the major goal of this project is create a functional core, you will also perform optimizations on the code. **In particular, you have to achieve a target throughput in a final 1024-size FFT design that is less than 2000 clock cycles; therefore with a 10 ns clock period that is 50K FFT operations per second**. This can be achieved by optimizing the submodules properly and using dataflow pragma across the submodules.

3.Materials
-----------

`download link <https://github.com/KastnerRG/pp4fpgas/blob/master/labs/project4.zip?raw=true>`_

You are given a zip file with four folders 0_Initial, 1_Subcomponents, 2_Skeleton_Restructured, and 3_OFDM. Folder 0_Initial contains the files corresponding to the “software” version of the FFT. Folder 2_Skeleton_Restructured provides a framework for a more optimized FFT implementation. Folder 3_OFDM gives a basic structure for the OFDM receiver with QPSK decoder. And folder 1_Subcomponents has a number of subfolders that allow you to create projects for individual functions that you will develop over the project. This is largely for your convenience for testing and development. All of the code developed here will eventually be placed into 0_Initial and 2_Skeleton_Restructured.

The structure of each of these folders is largely the same.

* ~.cpp - The place where you write your synthesizable code.

* ~.h - header file with various definitions that may be useful for developing your code.

* ~test.cpp - test bench out.gold.dat - “Golden” output. The testbench (~test.cpp) generates a sample input and calls the function in ~.cpp with that sample input. This output of the function is compared to the expected output. This will indicate PASS or FAIL. If it fails, then the code in ~.cpp is incorrect.

* script.tcl and directive.tcl - These allow you to easily create a project.

4. Design Instructions
----------------------

The major portion of the OFDM receiver is a 1024-point FFT. The FFT is a more efficient version of the Discrete Fourier Transform (DFT). The FFT utilizes symmetry in the DFT coefficients to provide a recursive implementation that reduces the runtime from O(N^2) to O(N log N) where N is the number of samples in the input signal.

Your tasks for this part of the lab are:

1. Implement a working FFT module that passes the testbench in HLS.

2. Optimize the FFT module to achieve a target throughput

3. Implement the QPSK decoder.

4. Integrate the FFT and decoder into a complete OFDM receiver.

FFT input data reordering via bit reversal

The first step in most optimized FFT implementation is to reorder the input data by performing “bit reversed” swapping. This allows for in-place computation of the FFT, i.e., the resulting “frequency domain” data (as well as the intermediate results) can be stored into the same locations as the input “time domain” data. In addition, the output frequency domain data will be in the “correct order” at the end of the computation.

An example of the bit reversed data for an 8 point FFT is as follows:

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/project4_1.png

n other words, the input data that was initially stored in the array at location 1 is stored in location 4 after the bit reversal is completed. The input data stored in the array at location 4 will be put in array location 1. The input data stored in locations 0, 2, 5 and 7 stay in those locations. Note that this is only true for an 8 point FFT. Other sizes of FFT will have different reordering of the data though it is still based on the bit reversed pattern. For example, in a 16 point FFT, the input data stored in location 1 (binary 0001) will be relocated into location 8 (binary 1000).

You should create an architecture that, efficiently as possible, transforms the input data into a bit reversed order. Note that there are many “software” implementations of this that will not effectively map to “hardware”. While the first goal is to get a working function, you should also consider the performance of the architecture.

We have given you a set of files that allows you to develop and test this bit reversal code in isolation. This includes a simple testbench that exercises this function directly. You should develop and optimize your bit reversed code here. You will later copy this code into the FFT code.

This code is in subfolder 1_bit_reverse in the folder 1_Subcomponents. You should develop your code here to insure that it matches the expected result. Note that this testbench is exercising only one input/output result. In other words, even if it passes this, it may not pass all results. Feel free to add additional testbenches to insure your code is correct.

The bit reverse function has the following prototype: void bit_reverse(DTYPE X_R[SIZE], DTYPE X_I[SIZE])

You should perform the swapping “in place” on the data in both of the real and imaginary portions of the data. That is the input data in both X_R and X_I will be reordered when the function completes. Focus on how you modified your code in order to make it more “hardware friendly”.


**Hint:** Logical operations map well to hardware. Calculating the indices of the arrays that should be swapped can be done with logical operations.

**Optimizing the “Software” Version of the FFT**
##################################################

The next portion of this project performs optimization on a typical software implementation of the FFT. You are given typical three nested loop implementation of the FFT in the folder 0_Initial. First, you should understand in detail what this code is doing. It is worth spending time on this now as you will have to rewrite the FFT in a more hardware friendly manner in the next steps. You can reuse some of this code in those steps.

You should optimize this code as much as possible. The results of the code will be poor; it will likely have > 250 million cycles. The throughput here is likely much worse than running this in software on a microprocessor. This often happens when we put the initial software versions of an application into a high level synthesis tool. And it should not be all that surprising. The code is optimized to run quickly in software, which runs largely in a sequential model of computation. The code must typically be carefully optimized with the final hardware architecture in mind to get good results. This involves exploiting parallelism and pipelining.

You will also notice that the first loop has function calls to sine and cosine. This code will synthesize quickly with these function calls. However, you may wish to replace these function calls (which will synthesize into CORDIC cores), into table lookups. We have provided two tables in the header file, W_real and W_imag which contain the precomputed twiddle factors for our 1024 FFT, i.e., W_real[i] = cos(2.0 * pi * i/SIZE) and W_imag[i] = sin(2.0 * pi * i/SIZE) where i = [0,512).

Some potential optimizations include:


* Using the W_real and W_imag tables
* Pipelining
* Loop unrolling
* Memory partitioning

**Hardware Friendly FFT Implementation**
#########################################

A good architecture will selectively expose and take advantage of parallelism, and allow for pipelining. Your final FFT architecture will restructure the code such that each stage is computed in a separate function or module. There will be one module for bit reversal that you have already developed, and then log N stages (10 in our case) for the butterfly computations corresponding to the 2-point, 4-point, 8-point, 16-point, … FFT stages.

The skeleton code for this final FFT implementation can be found in the 2_Skeleton_Restructured folder. This creates code connects a number of functions in a staged fashion with arrays acting as buffers between the stages. Figure 1 provides a graphical depiction of this process.

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/project4_2.png

Figure 1: A staged implementation of a 1024 FFT. Bit reversal is followed by 10 stages of butterfly computations. This architecture is capable of pipeline both within the stages and across the stages.

The first step in this process is to create code that computes the first and last stages of the FFT. The hope is that this will allow you to get a better understanding of exactly how memory accesses and the butterfly computations are performed in a general case. You can develop these two functions fft_stage_first and fft_stage_last in isolation. They both have subfolders in the 1_Subcomponents folder. Once these are working correctly, you can copy and paste the code directly in the same functions in the 2_Skeleton_Restructured project.

The next task is to create code that can implement “generic” function, i.e., one that can compute any stage of the FFT. This is the function fft_stages which also has its own project in the 1_Subcomponents folder. Note that this function prototype is similar to fft_stage_first and fft_stage_last with one major difference: it has a stage argument. This code will used to implement stages 2 through 9 in the 2_Skeleton_Restructured project.

**Hints:**


* These stages are performing the same calculation as one iteration of the outer for loop in the 0_Initial project.
* The major difference between the stages is what data elements you are performing the butterfly functions on, i.e., in what order do you pull data from X_R and X_I.
* Test each of the functions in isolation with the provided projects. Make sure that the code compiles and passes the testbench before attempting any optimizations.

Once you have a correctly functioning set of functions, you should copy and paste them in the 2_Skeleton_Restructured project and make sure that it passes the testbench. Since our testbenches on perform one check, which is far from comprehensive, it is possible, though hopefully unlikely, that you have some error that the 2_Skeleton_Restructured testbench exposes and was not exercised in the individual testbench. If your code passes the 2_Skeleton_Restructured project you can assume it is correct (though again since it is only one test, it may be wrong; you would need to perform significantly more testing in any “non-class” situation).

Now onto the final part of the project, optimizing of this restructured code. You should perform the typical tricks here: pipelining, memory partitioning, unrolling, etc. Some of these may not make sense depending on how you wrote your code. This final architecture should be orders of magnitude better than the 0_Initial project. Highly optimized FFT architectures can easily have less than 10000 cycles.

5.QPSK Decoder
--------------

The decoder takes the output of the FFT (complex values) and translates them into data. This is essentially undoing the effect of the QPSK encoder which takes input data for transmission and encodes it into into a complex exponential i.e., an I/Q complex number. You can think of this as a translation from the input data into a complex number.

We used the QPSK encoding scheme shown in the below figure. The plot shows four points in the complex plane at (+- 0.707, +- 0.707). This is called a constellation. Each of these points is labeled with an integer value 0, 1, 2 or 3. These integer values correspond to the input data being encoded. You can also think of these as two bit values if you want to consider binary input data. The complex values are the I/Q data that is encoded onto a specific frequency (e.g., one of 1024 frequencies when using a 1024 point FFT). The decoder performs the opposite -- it takes a complex number and translates it into an integer. You can look at the Simulink file for more information. This figure is taken directly from that file. The output of your encoder should be the exact data that was given to the OFDM receiver in the Simulink file.

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/project4_3.png

**Receiver Integration**

You should connect the FFT and the QPSK decoder together to form the complete OFDM receiver. The input to the receiver is the data from the channel. The output of the receiver should match the transmitted data.

**Optimization Guidelines**

* You must always use a clock period of 10 ns.

* The output of the various architectures that you generate must match the golden output. We have broken down the project into subcomponents to allow you to develop and test them individually. You would be wise to do it in such a manner.

* You should not change the data types as given to you. You do not need to perform bitwidth optimization of this project.

* It is ok to rewrite the code if it helps you with optimizations. For example, you can change the function interfaces. There are some variable defined in the header files for you convenience. These include SIZE = 1024, SIZE2 = 512, and M = 10 (log SIZE). Feel free to use these in your code. They are defined in every header file across all of the different folders. The software version has a nested for loop structure that does not allow Vivado HLS to provide an exact number of cycles. The tripcount directive can help with this. You should be able to understand the reported results. For example, while Vivado may give you a best, worst and average case numbers, your algorithm for a fixed size FFT should be a fixed number of cycles.

6. Demo on PYNQ
---------------

The final part is to integrate the receiver onto the PYNQ using a proper interface to transmit data to the OFDM receiver, and receive the decoded data back from your hardware implementation in the programmable logic.

We provided the general framework for creating different PL-PS interfaces and Jupyter Notebook host applications in previous labs. You should use that to create this demo. We will not be providing you with anything more than what was given in previous labs.

**The end of your Jupyter notebook must contain code that verifies your output**. Your can either use the provided input/output, and plot the received data against the golden output, or compare custom signals against a software version of OFDM (similar to what is done in the previous project).


7. Submission Procedure
-----------------------

You must also submit your code (and only your code, not other files, not HLS project files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment (fft.cpp, fft.h, etc.). You must follow the file structure below. We use automated scripts to pull your data, so DOUBLE CHECK your file/folder names to make sure it corresponds to the instructions. Your repo must contains a folder named "project4" at the top-level. This folder must be organized as follows (similar as previous projects):

**Contents:**

* Report.pdf

* Folder fft1024_best
  - Source code and reports (rpt and xml).

* Folder OFDM_receiver
  - Folder containing all of the HLS files necessary to build the complete OFDM receiver.
  - You are welcome to include multiple architectures if you please.

* Folder Demo

  - HLS source code and reports (rpt and xml).
  - bit and .tcl files
  - .ipynb host file

**Report :**

For project 4, you need to submit an 1-page report to explain only your final architecture. You can add figure, diagram, table, or chart to describe your architecture with a short paragraph explaining them. A 2-page report at max is allowed if it is necessary. No questions, or no answers. Just explain your design. We will check if (1) your final FFT and OFDM design are functionally correct and (2) your final FFT design achieves the target performance. The report will help us to understand your design.







