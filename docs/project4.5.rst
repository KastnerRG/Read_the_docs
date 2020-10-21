.. OFDM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: OFDM Receiver
==============================

1) Introduction
---------------

In this project, you will learn the basic idea behind an orthogonal frequency-division multiplexing (OFDM) system by implementing a simple OFDM receiver in programmable logic. A major part of OFDM is a Fast Fourier Transform (FFT), and thus you will be working with your FFT implementation from the previous project. You are given a set of test benches for the different submodules. You should design and test each individual submodule individually and integrate them into the FFT module. In the final part of the project, you will complete the OFDM receiver by combining the FFT module with a QPSK symbol decoder.

2) Goal
------

The OFDM receiver is divided into two parts -- the FFT and the QPSK decoder. You will be working with your FFT module from the FFT project. You must design and implement a QPSK decoder, and integrate it with the FFT to complete the receiver. While the major goal of this project is create a functional core, you will also perform optimizations on the code. 

3) Materials
-----------

`download link <https://github.com/KastnerRG/pp4fpgas/blob/master/labs/project4.zip?raw=true>`_

You are given a zip file with four folders 0_Initial, 1_Subcomponents, 2_Skeleton_Restructured, and 3_OFDM. Folder 0_Initial contains the files corresponding to the “software” version of the FFT. Folder 2_Skeleton_Restructured provides a framework for a more optimized FFT implementation. Folder 3_OFDM gives a basic structure for the OFDM receiver with QPSK decoder. And folder 1_Subcomponents has a number of subfolders that allow you to create projects for individual functions that you will develop over the project. This is largely for your convenience for testing and development. All of the code developed here will eventually be placed into 0_Initial and 2_Skeleton_Restructured.

The structure of each of these folders is largely the same.

* ~.cpp - The place where you write your synthesizable code.

* ~.h - header file with various definitions that may be useful for developing your code.

* ~test.cpp - test bench out.gold.dat - “Golden” output. The testbench (~test.cpp) generates a sample input and calls the function in ~.cpp with that sample input. This output of the function is compared to the expected output. This will indicate PASS or FAIL. If it fails, then the code in ~.cpp is incorrect.

* script.tcl and directive.tcl - These allow you to easily create a project.

4) Design Instructions
----------------------

Your tasks for this part of the lab are:

1. Implement the QPSK decoder.

2. Integrate the FFT and decoder into a complete OFDM receiver.

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

5) PYNQ Demo
---------------
The final part is to integrate the receiver onto the PYNQ using a proper interface to transmit data to the OFDM receiver, and receive the decoded data back from your hardware implementation in the programmable logic.

We provided the general framework for creating different PL-PS interfaces and Jupyter Notebook host applications in previous labs. You should use that to create this demo. We will not be providing you with anything more than what was given in previous labs.

**The end of your Jupyter notebook must contain code that verifies your output**. Your can either use the provided input/output, and plot the received data against the golden output, or compare custom signals against a software version of OFDM (similar to what was done in the previous project).


6) Submission Procedure
-----------------------

You must also submit your code (and only your code, not other files, not HLS project files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment (fft.cpp, fft.h, etc.). 

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "ofdm_receiver" at the top-level. This folder must be organized as follows (similar to previous projects):

**Contents:**

* **Report.pdf**

* Folder **fft1024_best**

  - Source code (*.cpp, *.h, *.tcl only) and reports (.rpt and .xml).

* Folder **OFDM_receiver**

  - Folder containing all of the HLS files necessary to build the complete OFDM receiver.

* Folder **Demo**

  - .bit and .hwh files
  - .ipynb host file
  
* You are welcome to include multiple OFDM architectures if you please, in additional folders.


**Report :**

For project 4, you need to submit an 1-page report to explain only your final architecture. You can add figures, diagrams, tables, or charts to describe your architecture with a short paragraph explaining them. A 2-page report at max is allowed if it is necessary. No questions; no answers. Just explain your design. We will check if (1) your final OFDM design is functionally correct and (2) your final OFDM design achieves the target performance. The report will help us to understand your design.

7) Grading Rubric
-----------	

**50 points:** Functionally correct design

**40 points:** Achieving target performance

**10 points:** Report
