.. PhaseDetector documentation master file, created by
   sphinx-quickstart on Fri Mar  8 19:12:45 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: Cordic
=========================================

1) Introduction
--------------

The goal of this project is to design a  a COordinate Rotation DIgital Computer (CORDIC). 

You are tasked with building one version of the CORDIC from scratch. This will likely take the majority of the time spent working on this project. A CORDIC is an efficient method for calculating trigonometric and hyperbolic functions. CORDIC can do a lot of different functions; we will use it to convert Cartesian coordinates (x, y) to the polar coordinates (r, theta).

2) Materials
-----------

You can download the project files here:

* `cordic.zip <https://github.com/KastnerRG/pp4fpgas/blob/master/labs/cordic.zip?raw=true>`_
 
The provided zip file has a number of subfolders and files corresponding to the different parts of the phase detector. This contains the documents necessary to build the project. You will start from HLS folder to design your phase detector using Vivado HLS. Use the provided script.tcl to create your project.


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
-------
1. Implement the CORDIC HLS code and verify it with the given testbench. Note that the testbench may not cover all cases; in fact, it may be poor. You are encouraged to create a more extensive testbench to ensure that your code is correct.

2. The ultimate goal of the CORDIC is to use only simple operations, i.e., add and shift. You should not be using divide, multiply, etc. in your CORDIC core. First design your code using float. Once you have a functionally correct CORDIC, then change data types to fixed point types and this should change your multiplications into shifts and adds. You should verify that this is indeed happening.

3. Develop a CORDIC core using a lookup table-based technique. We have provided a fully functional base implementation of this. You should read and understand this provided lookup table CORDIC code. You should analyze the design space of this lookup table IP core by changing the resolution of the look-up tables and varying the width of the input data. This will give you different resource, performance andaccuracy results.

.. Note:: You are encouraged to modify this implementation code to gain better utilization or throughput.                                                                                              	 Remember to submit modified .cpp and .h files
        
4) Demo
------
Again, the final task integrates the Cordic onto a PYNQ.Use the memory mapped IO lab tutorial and run the given notebook. The output you obtain from HLS IP is compared with a python implementation of the same.

5) Report
--------

Your report should answer the following questions. Make it very clear where you are answering each of these questions (e.g., make each question a header or separate section or copy/paste the questions in your report and add your answer or simply put a bold or emphasized **Question X** before your answer). Your report will be graded based on your responses. 

 * **Question 1:** These questions all refer to the CORDIC design. Why does the accuracy stop improving after so many iterations? What is the minimal amount of bits required for each variable? Does this   depend  on the input data? If so, can you characterize the input data to help you restrict the number of required bits? Do different variables require different number of bits? You should use ap_int or ap _fixed types if necessary for required bit width. You can read about ap_int and ap_fixed from `here <https://www.xilinx.com/support/documentation/sw_manuals/xilinx2019_1/ug902-vivado-high-level-synthesis .pdf>`_.  


 * **Question 2**: What is the effect of using simple operations (add and shift) in the CORDIC as opposed to floating-point multiply and divide?


 * **Question 3**: How does the ternary operator ‘?’ synthesize? Is it useful in this project?

	
 * **Question 4**: These questions all refer to the LUT-based CORDIC: Summarize the design space exploration that you performed as you modified the data types of the input variables and the LUT entries.   In particular, what are the trends with regard to accuracy (measured as error)? How about resources? What about the performance? Is there a relationship between accuracy, resources, and performance? What advantages/disadvantages does the regular CORDIC approach have over an LUT-based approach? 


6) Submission Procedure
----------------------

You must also submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to only import your *.cpp file and directly synthesize it. You can assume that we have correctly set up the design environment (cordic_test.cpp, cordic.h, etc.).

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



 
