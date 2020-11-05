.. OFDM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project 5: WBFM Receiver
==============================

1) Introduction
---------------
Please go through the `project slides <https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/WES237C%20-%20Lab%205.pdf>`_.

2) Project Goal
---------------

In this project, you will use your knowledge from previous projects to implement a Wide-Band FM (WBFM) receiver in programmable logic. The project is divided into two parts. In the first part, you develop different functions for a WBFM receiver (from GNU Radio) using HLS. A WBFM receiver consists of a vector multiplication (from the volk library), phase detector, FIR filter and an IIR filter. The second part is to integrate the receiver onto the Zedboard using Xillybus and GNU Radio to transmit data to the WBFM receiver, and receive the decoded data back from your hardware implementation in the programmable logic. You should use the provided setup (SD Card) to interact with the PL. You should be able to listen to local FM radio channels using your WBFM implementation in programmable logic. For more detail about the GNU Radio and functions please check the lab slides.

3) Materials
------------

`Download <https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/WESProject5_student.zip>`_.

Test benches for all four functions are provided for you. You are required to implement your hardware-friendly code for each function and pass the test bench. All of the code developed here will eventually placed into wbfm() function and will be called by xillybus_wrapper().

The structure of each of these folders is largely the same.

* ~.cpp - The place where you write your synthesizable code.

* ~.h - header file with various definitions that may be useful for developing your code.

* ~test.cpp - test bench out.gold.dat - “Golden” output. The testbench (~test.cpp) generates a sample input and calls the function in ~.cpp with that sample input. This output of the function is compared to the expected output. This will indicate PASS or FAIL. If it fails, then the code in ~.cpp is incorrect.

* script.tcl and directive.tcl - These allow you to easily create a project.

4) Design Instructions
----------------------
The WBFM receiver implementation in GNU Radio has 4 main parts in its Python wrapper: fm_demod, audio_coeffs, audio_filter and deemph.

.. image :: https://i.imgur.com/VbT7qDk.png

You need to report each function’s throughput for this part. The number of optimizations will not affect your grade. However, each block’s throughput will effect your total throughput and thus will impact audio output quality.

**fm_demod**
##########
This part consists of two functions: volk_32fc_xt_multiply_conjugate_32fc() that we will call volk() and fast_atan2f() that we will call fast_atan(). Both of these functions are implemented in C++ and can be found in GNU Radio source code or on online cross references. You will implement both of these functions in HLS.

**audio_coeffs**
################
This part calculates the coefficients for the following FIR filter. These coefficients are calculated once and will not change during each run. They are provided in your HLS test bench, and you will not need to calculate them.

**audio_filter**
################
This part has one function: fir_filter_fff(); we will call it fir(). You can find the C++ implementation in GNU Radio source code or on online cross references. You will implement this function in HLS.

**deemph**
##########
This part is a wrapper in Python that calculates coefficients for an IIR filter and then calls a C++ function, iir_filter_ffd(). We will call this function iir(). You can find the implementation in GNU Radio source or on online cross references. The coefficients for this IIR filter are also calculated once and will not change during a run. These coefficients are provided in your HLS test bench and you don’t need to calculate them. But you need to implement the iir() in HLS.

**Optimization Guidelines**

* You must always use a clock period of 10 ns.

* The output of the various architectures that you generate must match the golden output. We have broken down the project into subcomponents to allow you to develop and test them individually. You would be wise to do it in such a manner.

* You should not change the data types as given to you. You do not need to perform bitwidth optimization of this project.

* It is OK to rewrite the code if it helps you with optimizations. For example, you can change the function interfaces. There are some variable defined in the header files for you convenience. Feel free to use these in your code.

5) PYNQ Demo
------------

`How to set up WBFM in GNU Radio <https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/WESProject5_student.zip>`_.

This project is different from your previous projects in the sense that it works in real time. Effect of latency and throughput of your implementation can be observed by listening to your audio output and monitoring GNU Radio’s overrun and underrun messages. GNU Radio produces these two warnings if a block receives more or less samples than it needs to consume. Another important factor in performance for FPGA applications is memory access that heavily affects the end-to-end throughput. Xillybus, same as other interfaces, has its own limits for memory access. It is quite sensitive to the size of the transmitted data. You are highly encouraged to modify the code to achieve a better performance and observe the throughput by changing the way you transmit data between PS and PL.

You must implement the WBFM receiver block on the PL part of Pynq. You should use the provided image to interact with your PL. This image includes Linux, GNU Radio, Xillybus and necessary blocks in GNU Radio to interact with PL.

Integration of HLS code
#######################
Xillybus wrapper for this part is provided, and you need to integrate your functions from last part to make a complete WBFM block. You should be able to listen to local FM radio stations using your WBFM implemented in programmable logic.

6) Submission Procedure
-----------------------

You need to demonstrate your functional hardware implementation WBFM receiver in the class. We will post schedule of each team’s demonstration later on piazza.

You must also submit your code (and only your code, not other files, not HLS project files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment. 

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "wbfm_receiver" at the top-level. This folder must be organized as follows (similar to previous projects):

**Contents:**

* **Report.pdf**

* Folder **atan**

  - Source code (*.cpp, *.h, *.tcl only) and reports (.rpt and .xml).
  
* Folder **fir**

  - Source code (*.cpp, *.h, *.tcl only) and reports (.rpt and .xml).
  
* Folder **iir**

  - Source code (*.cpp, *.h, *.tcl only) and reports (.rpt and .xml).
  
* Folder **volk**

  - Source code (*.cpp, *.h, *.tcl only) and reports (.rpt and .xml).

* Folder **wbfm**

  - fast_atan.cpp | wbfm.cpp | wbfm.h
  
* Folder **Demo**

  - .bit and .hwh files
  - WBFM.ipynb host file

**Report:**

For project 5, you must submit a report the throughput with 1 page for each function from section 4. You may add figures, diagrams, tables, or charts to describe your architectures with a short paragraph explaining them. No questions; no answers. Just explain your design. We will check if (1) your final WBFM functions are functionally correct (they pass their test benches) and (2) your final WBFM design achieves the target performance. The report will help us to understand your design. You also can use this report to explain your work for bonus part (check the grading section).

7) Grading Rubric
-----------------

**30 points:** Functionally correct design. You will get full credit if we are able to build your blocks without any effort. All four functions must pass their test benches. You need to report your throughput for each function in your report.

**60 points:** Pynq Demo. You will get full credit for clear audio output; system must operate for at least 1 minute (continuous audio output).

**10 points:** Report.

**Bonus:** You are free to explore and improve the existing project as you wish. The amount of extra credit will depend upon the work. Contact the professor and TAs beforehand if you wish to know how many additional points that a project enhancement will provide. Some examples of improvement are:

* You can add audio quality measurement module 

* You can play with HLS throughput of different modules, and study how HLS optimizations affect audio quality. 

* SDSoC integration.