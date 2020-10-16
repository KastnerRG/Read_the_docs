.. PhaseDetector documentation master file, created by
   sphinx-quickstart on Fri Mar  8 19:12:45 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: CORDIC
=========================================

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

You must submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (*.cpp, *.h files, and scripts) and directly synthesize it. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment (cordic_test.cpp, cordic.h, etc.).

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

* **Note**: You should use ap_int or ap_fixed types if necessary for required bit width. You can read about ap_int and ap_fixed from `here <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis .pdf>`_. 

7) Grading Rubric
-------------------

**50 points:** Response to the questions in your report. Points will be deducted based upon poor presentation, grammar, formatting, spelling, etc. Results should be discussed succinctly but with a enough detail to understand your architectures and tradeoffs. Tables and figures should be properly labeled, well thought out, and described in the text with comments on both the design that produced each entry, and the observable trends between entries. Spelling errors are unacceptable.

**50 points:** Correct working project on PYNQ.

