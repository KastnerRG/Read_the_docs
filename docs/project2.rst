.. PhaseDetector documentation master file, created by
   sphinx-quickstart on Fri Mar  8 19:12:45 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project 2: CORDIC
=========================================

If you are in UCSD's WES 237C, you will also need to complete :doc:`Project 2.5: Phase Detector <project2.5>` for this assignment.

1) Introduction
--------------

The goal of this project is to design a  COordinate Rotation DIgital Computer (CORDIC). 
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

* Demo Folder: Demo folder for Cordic.

        - Cordic.ipynb - Jupyter notebook host file

3) Tasks
---------
1. Design and verify a functionally complete CORDIC IP core using HLS: **cordic_baseline**. You are provided a testbench that you can use though that the testbench does not cover all cases. You are encouraged to create a more extensive testbench to ensure that your code is correct.

2. The ultimate goal is to create an efficient CORDIC that only uses simple operations, i.e., add and shift. You should not be using divide, multiply, etc. in your CORDIC core. First design your code using float variables. Once you have a functionally correct CORDIC, then change data types to fixed-point types incrementally while checking to see that the test-bench still passes. This should result in your multiplications being synthesized into shifts and adds (you should verify that this is indeed happening). Do not change your function header/definition/interface (the input and output variables and their datatypes), only change variables inside the body of your cordiccart2pol function. You may use new typedefs if you wish. Try to perform as few operations with float as possible, meaning there will likely be a lot of typecasting involved.

3. Explore the architectural tradeoffs of a CORDIC core architecture based upon a lookup table. We have provided a fully functional base implementation of this. You should read and understand this CORDIC code. You should analyze the design-space of this lookup table IP core by changing the parameters of the look-up tables, e.g., by varying the data type of the input data, and changing the number of entries. This should allow you to find architectures with different resource usage, performance, and accuracy results.

4. A major design tradeoff for the CORDIC revolves around the precision or accuracy of the results. For example, changing the number of rotations effects the accuracy, performance, and resource usage. Another important tradeoff is the data type of the variables. Using large, complex data types (like floating point) is typically most accurate, but not good with respect to performance and resource usage. Using fixed-point types is more performant, but may reduce the accuracy of the results. Perform design-space exploration to create a wide range of implementations using various data types for different variables, modifying the number of rotations, and performing other optimizations to find the Pareto optimal designs. 

        
4) PYNQ Demo
---------
The final task integrates a CORDIC IP core onto the programmable logic (PL) using PYNQ. The provided notebook gives a skeleton for running the CORDIC using memory mapped IO for communication. The :doc:`Lab 1: Pynq Memory Mapped IO <PYNQ-example>` serves as an example you can follow. The notebook passes data to the CORDIC IP, starts the process, reads the result, and compares it with the result computed in Python.

5) Report
----------

Your report should answer the following questions. Make it very clear where you are answering each of these questions (e.g., make each question a header or separate section or copy/paste the questions in your report and add your answer or simply put a bold or emphasized **Question X** before your answer). Your report will be graded based on your responses. 

* **Question 1:** One important design parameter is the number of rotations. Change that number to numbers between 10 and 20 and describe the trends. What happens to performance? Resource usage? Accuracy of the results? Why does the accuracy stop improving after some number of iterations? Can you precisely state when that occurs? 


* **Question 2:** Another important design parameter is the data type of the variables. Is one data type sufficient for every variable or is it better for each variable to have a different type? Does the best data type depend on the input data?  What is the best technique for the designer to determine the data type(s)?


* **Question 3:** What is the effect of using simple operations (add and shift) in the CORDIC as opposed to multiply and divide? How does the resource usage change? Performance? Accuracy?


* **Question 4:** Thinking from a logic-design hardware perspective, what operation does the ternary operator '?' perform? What function would you expect this operator to synthesize as? Do you notice a difference between using it and an if-else block? Is it useful in this project?

	
* **Question 5:** These questions all refer to the LUT-based CORDIC: Summarize the design-space exploration that you performed as you modified the data types of the input variables and the LUT entries. In particular, what are the trends with regard to accuracy (measured as error)? How about resources? What about the performance? Is there a relationship between accuracy, resource usage, and performance? What advantages/disadvantages does the regular CORDIC approach have over an LUT-based approach? 

* **Note**: You should use ap_int or ap_fixed types if necessary for required bit width. You can read about ap_int and ap_fixed from `here <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis.pdf>`_. 

6) Submission Procedure
-------------------------

If you are in UCSD's WES 237C, you will also need to complete :doc:`Project 2.5: Phase Detector <project2.5>` for this assignment.

You must submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (*.cpp, *.h files, and *.tcl) and directly synthesize it. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment (cordic_test.cpp, cordic.h, etc.).

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "cordic" at the top-level. This folder must be organized as follows (similar to project1):

* **Report.pdf**

* Folder **cordic_baseline**: cordiccart2pol.h | cordiccart2pol.cpp | script.tcl | <report rpt/xml> 

* Folder **cordic_optimized1**: cordiccart2pol.h | cordiccart2pol.cpp | script.tcl | <report rpt/xml>

* Folder **cordic_optimized2**: cordiccart2pol.h | cordiccart2pol.cpp | script.tcl | <report rpt/xml>

* ...

* Folder **cordic_LUT**: cordiccart2pol.h | cordiccart2pol.cpp | cordiccart2pol_test.cpp | script.tcl | <report rpt/xml>

* Folder **Demo**: Cordic.ipynb | .bit | .hwh

* **Note**: <report rpt/xml> references both the .rpt and the .xml files in the /syn/report folder. Please include both.

* **Note**: Provide the architectures that you used to answer the questions.

7) Grading Rubric
-------------------

Unlike project 1, it is not explicitly necessary to come up with an optimally efficient solution for the CORDIC core using pipelining, unrolling, and other HLS directives to meet a certain frequency. This project is more about precision and accuracy of data using bit widths. However, the larger goal of this class is to understand how to obtain resource-efficient designs while still achieving the level of functionality you desire. So there's no performance target to hit, but do your best.

The provided cordic_LUT does not pass the test. This is expected and fine. The idea is for this portion of the project is design-space exploration. It is possible to run synthesis for a design that doesn't pass c-sim, but for this question alone you may modify the threshold to make it pass. **Do not do this for other designs or projects without checking with us first**; we want to be able to compare all your designs as if they met or surpassed a certain standard of accuracy.

In this project and in future projects, you may find it necessary to edit the test-bench. Either the test-bench doesn't cover enough cases, or (as in the case of cordic_LUT) the threshold for error of theta may be too high. We may even instruct you to edit the test-bench. In these cases, you are welcome to change this file, and if you do, please **submit the altered test-bench file** too, and explicitly state in your report what changes you made and why.

The cordiccart2pol.cpp file in the cordic_LUT project has a comment asking what happens if you direct HLS to use RAM_1P_LUTRAM for the my_LUT_r and my_LUT_th variables. This question isn't on this page. **You don't have to answer them in the report**, but please do try them out for an understanding of LUTRAMs.

**50 points:** Response to the questions in your report. Points will be deducted based upon poor presentation, grammar, formatting, spelling, etc. Results should be discussed succinctly but with a enough detail to understand your architectures and tradeoffs. Tables and figures should be properly labeled, well thought out, and described in the text with comments on both the design that produced each entry, and the observable trends between entries. Spelling errors are unacceptable.

**50 points:** Correct working project on PYNQ.

