.. PhaseDetector documentation master file, created by
   sphinx-quickstart on Fri Mar  8 19:12:45 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: CORDIC
==================

1) Introduction
--------------

The primary goal of this project is to understand how to use arbitrary precision data types and their effects on accuracy, performance, and resource consumption. To do this, the project implements a Cartesian to Polar transform in two different ways: using a COordinate Rotation DIgital Computer (CORDIC) and as a lookup table (LUT).

A CORDIC is an efficient method for calculating trigonometric and hyperbolic functions. The CORDIC control can be modified to perform different functions, e.g., the book describes how to use a CORDIC for calculating sine and cosine. This project focuses on using the CORDIC to translate between Cartesian coordinates (x, y) to the polar coordinates (r, theta).

The lookup table architecture is a generic computational technique that instantiates a memory that holds the output results. The function inputs are used to address into the memory to retrieve the appropriate result. A lookup table in the FPGA logic architecture is one such example that uses very small memories to compute an arbitrary N bit input logic function whose output is 1 bit. These LUTs are small -- a 4-LUT has 16 bits; a 5-LUT has 32 bits. This project has a LUT-based architecture to compute the Cartesian to Polar transform.

2) Materials
--------------

You can download the project files here:

* `CORDIC Project Repo <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/project2/cordic>`_

The repo has a number of subfolders and files related to the project. This contains the documents necessary to build the project. You will start from HLS folder to design a CORDIC using HLS. You can use the provided script.tcl to create your project.

* HLS\/cordic folder:

        - cordiccart2pol.cpp - The place where you write your synthesizable code. Currently, it only contains the function prototype.

        - cordiccart2pol.h - header file with various definitions that may be useful for developing your code.

        - cordiccart2pol_test.cpp - test bench

        - script.tcl - Use this to create your project

* HLS\/cordic_LUT folder:

        - cordiccart2pol.cpp - The place where you can find the synthesizable code. Currently, it contains a simple implementation.

        - cordiccart2pol.h - header file with various definitions that may be useful for developing your code. Here you can modify values and types of the design parameters to explore their impact.

        - cordiccart2pol_test.cpp - test bench

        - script.tcl - Use this to create your project

* Demo folder:

        - Cordic.ipynb - Jupyter notebook host file

3) Tasks
---------
1. Design and verify a functionally complete CORDIC IP core using HLS: **cordic_baseline**. You are provided a testbench that you can use though that the testbench does not cover all cases. You are encouraged to create a more extensive testbench to ensure that your code is correct.

2. The ultimate goal is to create an efficient CORDIC that only uses simple operations, i.e., add and shift. You should not be using divide, multiply, etc. in your CORDIC core. First design a baseline using float variables. Once you have a functionally correct CORDIC, then start experimenting with arbitrary precision data types. This should decrease the usage of DSP and change the type of DSP utilized (you should verify that this is indeed happening). Do not change the function header/definition/interface (the input and output variables and their datatypes), only change variables inside the body of your `cordiccart2pol` function. You may use new typedefs if you wish. Try to perform as few operations with float as possible, meaning there will likely be a lot of typecasting involved.

3. A major design tradeoff for the CORDIC revolves around the precision or accuracy of the results. For example, changing the number of rotations effects the accuracy, performance, and resource usage. Another important tradeoff is the data type of the variables. Using large, complex data types (like floating point) is typically most accurate, but not good with respect to performance and resource usage. Fixed-point types provide better performance and resource usage, but may reduce the accuracy of the results. Perform design-space exploration to create a wide range of implementations using various data types for different variables, modifying the number of rotations, and performing other optimizations to find the Pareto optimal designs.

4. Explore the architectural tradeoffs of a lookup table (LUT) architecture. We have provided a fully functional base implementation of this. You should read and understand this code. You should analyze the design-space of this lookup table IP core by changing the parameters of the look-up tables, e.g., by varying the data type of the input data and the output data types. This should allow you to find architectures with different resource usage, performance, and accuracy results.

4) PYNQ Demo
---------
The final task integrates a CORDIC IP core onto the programmable logic (PL) using PYNQ. The provided notebook gives a skeleton for running the CORDIC using memory mapped IO for communication. The :doc:`Lab: Pynq Memory Mapped IO <PYNQ-example>` serves as an example you can follow. The notebook passes data to the CORDIC IP, starts the process, reads the result, and compares it with the result computed in Python.

5) Report
----------

Your report should answer the following questions. Make it very clear where you are answering each of these questions (e.g., make each question a header or separate section or copy/paste the questions in your report and add your answer or simply put a bold or emphasized **Question X** before your answer). Your report will be graded based on your responses.

For all questions below, use a CORDIC implementation using the starter code in `cordic/cordiccart2pol.cpp` unless otherwise indicated.

* **Question 1:** One important design parameter is the number of rotations. Change that number to numbers between 10 and 20.

        * **a)** Create a table that shows resource usage, throughput, latency, and RMSE for each design you create. You should have at least 6 different designs with different numbers of rotations. Use 10, 12, 14, 16, 18, and 20 rotations.
        * **b)** Plot throughput, resource usage, and RMSE as a function of the number of rotations. Clearly label your axes and each datapoint.
        * **c)** At what number of rotations does the accuracy stop noticeably improving in the plot?

* **Question 2:** Another important design parameter is the data type of the variables.

        * **a)** We will use the `ap_fixed` arbitrary precision data type for each variable. At most how many integer bits are required for each variable? Remember that this is a signed type. (Hint: consider the range of values that each variable can take on. You can use the float implementation to help you determine this. Think of the range of values of the variables `r`, `x`, `y`, and `theta`). Give an answer for each variable. The testbench assumes that `x` and `y` are normalized between [-1, 1].
        * **b)** Now that you have fixed the number of integer bits (use the largest number of integer bits determined in **2a**), experiment with the number of total bits for each variable. Use the same number of total bits for each variable. Create a table that shows resource usage, throughput, latency, and RMSE for each design you create. You should have at least 6 different designs with different numbers of total bits. Use 8, 12, 16, 20, 24, and 32 total bits.
        * **c)** Use `ap_fixed<16,3>` for all variables. Now experiment with changing the type of all internal values of your function (i.e. everything except for input variables `x`, `y` and output variables `r`, `theta`). At the start of the function, declare new variables `new_x` and `new_y` that are initialized to the inputs with these new datatypes and replace all occurrences of `x` and `y` with `new_x` and `new_y`. Also change the datatype of `x_initial`. Create a table that shows resource usage, throughput, latency, and RMSE for each design you create. You should have at least 6 different designs with different types for the internal variables. Use 8, 12, 16, 20, 24, and 32 total bits.

* **Question 3:** What is the effect of using simple operations (add and shift) in the CORDIC as opposed to multiply and divide?
  
        * **a)** Now that you are using `ap_fixed` for all variables, change your implementation to use simple operations like add and shift instead of multiply and divide. Create a table that shows resource usage, throughput, latency, and RMSE for each design you create. You should have at least 6 different designs with different numbers of total bits. Use 8, 12, 16, 20, 24, and 32 total bits. Use the implementation from **2b** as a baseline for comparison.
        * **b)** Create 3 separate plots for LUTs, DSPs, and FFs for each of these data types and each implementation. Clearly label your axes and each datapoint. Use a different color/line style for each implementation.

* **Question 4:** These questions all refer to the lookup table (LUT) implementation of the Cartesian to Polar transformation.

        * **a)** How does the input data type affect the size of the LUT? How does the output data type affect the size of the LUT? Precisely describe the relationship between input/output data types and the number of bits required for the LUT.
        * **b)** Create a table of resource usage, throughput, latency, and error vs number of total bits. Use the same number of integer bits for all data types (as in **2b**).
        * **c)** Plot all types of resource usage (LUTs, FFs, DSPs) as a function of the total number of bits for the data types. Make one plot for resource utilization
        * **d)** Plot RMSE as a function of the total number of bits for the data types.
        * **e)** What advantages/disadvantages of the CORDIC implementation compared to the LUT-based implementation?


6) Submission Procedure
-------------------------

You must submit your code (and only your code, not other files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to use what is provided (*.cpp, *.h files, and *.tcl) and directly synthesize it. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment (cordic_test.cpp, cordic.h, etc.).

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "cordic" at the top-level. This folder must be organized as follows (similar to the structure in other projects):

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

The main goal of this project is to develop a fully functional CORDIC core capable of performing a Cartesian to Polar transformation functioning on a PYNQ board. The major learning goal is to understand how data types can impact the accuracy, performance, and resource usage of a hardware implementation.

Efficient solutions are generally important, the project is not focused on performance optimizations.  Thus, there is no explicit performance target. We encourage you to explore how pipelining, unrolling, and other HLS directives can be used to make the designs higher performance. But you will not be graded on this aspect.

In this project and in future projects, you may want to edit the testbench. If you make any edits, please **submit the altered testbench file** too, and explicitly state in your report what changes you made and why.

**50 points:** Response to the questions in your report. Your answers should be well written and clearly delineated (for example: by copying the questions into the report before answering them, or placing each question under a separate subheading). Additional points (up to 20) will be subtracted for poor formatting and/or answers that are hard to understand. Examples of issues include any spelling errors, multiple/egregious grammar errors, poor presentation of results, lack of written comparison of the results, etc. Report the throughput, resource usage, and accuracy for each design you discuss in your report, and include the files for these designs in your submission. We encourage the use of tables for stating results and the changes that produced them, and figures to draw comparisons between different designs. Use these figures and tables in your discussion. A well-written report is informative but not overly verbose. You will be deducted points if you do not follow the instructions on directory naming and file structure.

**50 points:** Correct working project on PYNQ.
