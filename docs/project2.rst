.. PhaseDetector documentation master file, created by
   sphinx-quickstart on Fri Mar  8 19:12:45 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: CORDIC
=========================================
This project is divided into two **PARTS**. 

**PART 1 will be CORDIC design and PART 2 will be designing a Phase Detector using CORDIC**.

PART 1: CORDIC
--------------

1) Introduction
--------------
The goal of this part is to design a  a COordinate Rotation DIgital Computer (CORDIC). 
You are tasked with building one version of the CORDIC from scratch. This will likely take the majority of the time spent working on this project. A CORDIC is an efficient method for calculating trigonometric and hyperbolic functions. CORDIC can do a lot of different functions; here we will specifically use it to convert Cartesian coordinates (x, y) to the polar coordinates (r, theta).

2) Materials
--------------

You can download the project files here:

* `cordic.zip <https://github.com/KastnerRG/pp4fpgas/blob/master/labs/cordic.zip?raw=true>`_
 
The provided zip file has a number of subfolders and files related to implementing the CORDIC. This contains the documents necessary to build the project. You will start from HLS folder to design a CORDIC using Vivado HLS. Use the provided script.tcl to create your project.

* HLS \ cordic folder:

        - cordiccart2pol.cpp - The place where you write your synthesizable code. Currently, it only contains the function prototype.

        - cordiccart2pol.h - header file with various definitions that may be useful for developing your code.

        - cordiccart2pol_test.cpp - test bench

        - script.tcl - Use this to create your project

* HLS \ cordic_LUT folder:

        - cordiccart2pol.cpp - The place where you can find the synthesizable code. Currently, it contains a simple implementation.

        - cordiccart2pol.h - header file with various definitions that may be useful for developing your code. Here you can modify values and types of the design parameters to explore their impact.

        - cordiccart2pol_test.cpp - test bench

        - script.tcl - Use this to create your project

* Demo Folder:Demo folder for Cordic.

        - Cordic.ipynb - Jupyter notebook host file

3) Tasks
---------
1. Design and verify a functionally complete CORDIC IP core using HLS. You are provided a testbench that you can use though that the testbench does not cover all cases. You are encouraged to create a more extensive testbench to ensure that your code is correct.

2. The ultimate goal is to create an efficient CORDIC that only uses simple operations, i.e., add and shift. You should not be using divide, multiply, etc. in your CORDIC core. First design your code using float. Once you have a functionally correct CORDIC, then change data types to fixed point types and this should change your multiplications into shifts and adds. You should verify that this is indeed happening.

3. Explore the architectural tradeoffs of a CORDIC core architecture based upon a lookup table. We have provided a fully functional base implementation of this. You should read and understand this CORDIC code. You should analyze the design space of this lookup table IP core by changing the parameters of the look-up tables, e.g., varying by varying the data type of the input data and changing the number of entries. This should allow you to find architectures with different resource, performance, and accuracy results.

4. A major design tradeoff for the CORDIC revolves around the precision or accuracy of the results. For example, changing the number of rotations effects the accuracy, performance, and resource usage. Another important tradeoff is the data type of the variables. Using large, complex data types (like floating point) is typically most accurate, but not good with respect to performance and resource usage. Using fixed point types is more performant, but may reduce the accuracy of the results. Perform design space exploration to create a wide range of implementations using various data types for different variables, modifying the number of rotations, and performing other optimizations to find the Pareto optimal designs. 

        
4) PYNQ Demo
---------
The final task integrates a CORDIC IP core onto the programmable logic (PL) using PYNQ. The provided notebook gives a skeleton for running the CORDIC using memory mapped IO for communication. The notebook passes data to the CORDIC IP, receives the result, and compares it with the result computed in Python.

5) Report
----------

Your report should answer the following questions. Make it very clear where you are answering each of these questions (e.g., make each question a header or separate section or copy/paste the questions in your report and add your answer or simply put a bold or emphasized **Question X** before your answer). Your report will be graded based on your responses. 

* **Question 1:** One important design parameter is the number of rotations. Change that number and describe the results. What happens to performance? Resource usage? Accuracy of the results? Why does the accuracy stop improving after so many iterations? Can you precisely state when that occurs? 

* **Question 2:** Another important design parameter is the data type of the variables. Is one data type sufficient for every variable or is it better for each variable to have a different type? Does the best data type depend on the input data?  What is the best technique for the designer to determine the data type?

* **Question 3:** What is the effect of using simple operations (add and shift) in the CORDIC as opposed to multiply and divide? How does the resource usage change? Performance? Accuracy?


* **Question 4:** How does the ternary operator ‘?’ synthesize? Is it useful in this project?

	
* **Question 5:** These questions all refer to the LUT-based CORDIC: Summarize the design space exploration that you performed as you modified the data types of the input variables and the LUT entries.   In particular, what are the trends with regard to accuracy (measured as error)? How about resources? What about the performance? Is there a relationship between accuracy, resources, and performance? What advantages/disadvantages does the regular CORDIC approach have over an LUT-based approach? 


6) Submission Procedure
-------------------------

You must submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (*.cpp, *h files, and scripts) and directly synthesize it. You can assume that we have correctly set up the design environment (cordic_test.cpp, cordic.h, etc.).

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contains a folder named "project2" at the top-level. This folder must be organized as follows (similar as project1):

* **Report.pdf**

* Folder **cordic_baseline**: cordiccart2pol.h | cordiccart2pol.cpp | script.tcl | <report rpt/xml> 

* Folder **cordic_optimized1**: cordiccart2pol.h | cordiccart2pol.cpp | script.tcl | <report rpt/xml>

* Folder **cordic_optimized2**: cordiccart2pol.h | cordiccart2pol.cpp | script.tcl | <report rpt/xml>

* ...

* Folder **cordic_LUT**: cordiccart2pol.h | cordiccart2pol.cpp | cordiccart2pol_test.cpp | | …

* Folder **Demo** : Cordic.ipynb | .bit | .hwh

* **Note**: change <report rpt/xml> by both the .rpt and the .xml files in the /syn/report folder.

* **Note**: Provide the architectures that you used to answer the questions.

* **Note**: You should use ap_int or ap_fixed types if necessary for required bit width. You can read about ap_int and ap_fixed from `here <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis .pdf>`_. 

7) Grading Rubric
-------------------

**50 points:** Response to the questions in your report. Points will be deducted based upon poor presentation, grammar, formatting, spelling, etc. Results should be discussed succinctly but with a enough detail to understand your architectures and tradeoffs. Figures should be well thought out and described in the text. Spelling errors are unacceptable.

**50 points :** Correct working project on PYNQ.

PART 2: Phase Detector
-----------------

1) Introduction
-----------------

The goal of this part is to design a simple phase detector. This is done by combining a complex FIR filter and a COordinate Rotation DIgital Computer (CORDIC). You build a complex FIR filter by hierarchically instantiating four “real” FIR filters similar to what you developed in the FIR filter project. In this part, you use CORDIC IP core from the previous part.

The complex FIR filter is used to correlate to a known complex signal. We use Golay codes which have some great properties related to orthogonality and auto-correlation. This is not important to this lab, but is some really amazing math. I hope you look into it.

In the end, you will combine all of these modules into a phase detector. This is a common block used in a digital communications receiver. The goal is to do simple synchronization and discover the phase of the signal. The output of the CORDIC (r, theta) gives you these results. It is a simple phase detector, but should provide you with a basic understanding of the problem, and you should come away with knowledge on how to develop two new important hardware blocks (CORDIC and a complex FIR filter).

We provide a Simulink file that models a transmitter, channel, and receiver. You are building an equivalent receiver in HLS in this project. The Simulink file is provided for your information only. You do not have to edit or do anything with this file though it could be useful for understanding the overall application better.

2) Materials
-----------

You can download the project files here:

* `Phase Detector.zip <https://github.com/KastnerRG/pp4fpgas/blob/master/labs/phase_detector.zip?raw=true>`_
 
The provided zip file has a number of subfolders and files corresponding to the different parts of the phase detector. This contains the documents necessary to build the project. You will start from HLS folder to design your phase detector using Vivado HLS. Use the provided script.tcl to create your project.

* HLS \ fir_top folder: This folder contains *.cpp*,*.h*, and script files for a complex FIR filter. This is a particular type of filter called a matched filter. You are matching the incoming signal to complex I and Q Golay codes that are provided for you. In the fir.cpp file, there are four sub functions firI1, firI2, firQ1, and firQ2. These functions are real FIR filters i.e., the same that you designed in Project 1. You can use your favorite code from Project 1 in these four sub functions. In the complex FIR filter, four of these functions are used in the “fir” function. In that function, you need to connect the four FIR filters “firI1, firI2, firQ1, and firQ2” to an adder and subtractor to create the complex matched filter. This structure is demonstrated in the Simulink file.

* HLS \ phasedetector folder: After you design the cordic and the complex fir, you will use them to design the phase detector.

        - fir.cpp - complex fir filter you designed previously.

        - cordiccart2pol.cpp - cordiccart2pol function you designed previously.

        - phasedetector.cpp - Top level skeleton for the phase detector. You use fir.cpp and cordiccart2pol.cpp to design the phasedetector function.

        - phasedetector_test - test bench

        - phasedetector.h - header file

        - script.tcl - Use this to create your project

* Simulink:
        
        - Project2_model.slx: Simulink model file. You do not have to edit or do anything with this file though it could be useful for understanding the overall application better.

* Demo Folder:Demo folder for Phase Detector.

        - host.ipynb - Jupyter notebook host file

        - input_i.dat - input I signal

        - input_q.data - input Q signal

        - out_gold.dat - golden output

3) Tasks
-------
In this project, you will build a phase detector to process the given a complex signal (I and Q or real and imaginary parts) demonstrated in the figure below.

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/project2_1.png

The final goal is to implement this phase detector. To achieve this goal, you will need to finish the following tasks:

1. Implement the complex matched filter and verify it with the given testbench. This matched filter consists of four FIR filter modules which are similar to the ones in your Project 1. For the purpose of debugging, if you plot the outputs of this step, you should expect the waveforms as shown in the figure below. Or more simply just make sure that that testbench passes.

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/project2_3.png

2. Connect the complex matched filter and CORDIC modules to implement the receiver. Verify this overall design with the given testbench. For the purpose of debugging, if you plot the outputs of this step,you should expect the waveforms as shown in the figure below.

.. Note:: You are encouraged to modify this implementation code to gain better utilization or throughput.                                                                                              	 Remember to submit modified .cpp and .h files
        
4) PYNQ Demo
------
Again, the final task integrates the phase detector onto a PYNQ. Implement the receiver design on the board. This process is mostly similar to your second lab, but you need to modify your HLS code for streaming interface.

You also should see these outputs:

.. code-block:: c++

   Thetas at the R peaks are:

   0.015529

   0.047509

   0.079485

   0.111526

   0.143491

   ...

These are the rotated phases that have been detected by your design.

5) Report
--------

Your report should answer the following questions. Make it very clear where you are answering each of these questions (e.g., make each question a header or separate section or copy/paste the questions in your report and add your answer or simply put a bold or emphasized **Question X** before your answer). Your report will be graded based on your responses. 

* **Question 1:** What is the throughput of your Phase Detector? How does that relate to the individual components (FIR, CORDIC, etc.)? How can you make it better?

6) Submission Procedure
----------------------

You must also submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (*.cpp, *h files, and scripts) and directly synthesize it. You can assume that we have correctly set up the design environment (cordic_test.cpp, cordic.h, etc.).

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contains a folder named "project2" at the top-level. This folder must be organized as follows (similar as project1):

* **Report.pdf**

* Folder **fir_top_baseline**: fir.h | fir.cpp | script.tcl | report.rpt and .xml

* Folder **phasedetector_optimized1**: phasedetector.h | phasedetector.cpp | cordiccart2pol.cpp | fir.cpp | script.tcl | <report rpt/xml>

* Folder **phasedetector_optimized2**: phasedetector.h | phasedetector.cpp | cordiccart2pol.cpp | fir.cpp | script.tcl | <report rpt/xml>

* ...

* Folder **Demo** : PhaseDetector.ipynb | .bit | .hwh

* **Note**: change <report rpt/xml> by both the .rpt and the .xml files in the /syn/report folder.

* **Note**: Provide the architectures that you used to answer the questions. You may optimize on individual components (FIR/CORDIC), or on the phase detector directly.

7) Grading Rubric
-------------------

**50 points:** Response to the questions in your report. Points will be deducted based upon poor presentation, grammar, formatting, spelling, etc. Results should be discussed succinctly but with a enough detail to understand your architectures and tradeoffs. Figures should be well thought out and described in the text. Spelling errors are unacceptable.

**50 points :** Correct working project on PYNQ.
