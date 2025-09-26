Project: FIR Filter Design
=============================

1) Introduction
---------------

The goal of this project is to learn how the basics of an HLS tool. The learning outcomes are to gain a basic understanding of how the Vivado HLS tool works, to get exposed to HLS optimizations, to perform a guided design space exploration to obtain architectures with different tradeoffs in performance and resource usage, to generate a high-quality FIR architecture, and to demonstrate the integration of that FIR on the Zynq FPGA using the Pynq infrastructure.

This project is designed to be paired with Chapter 2 from `Parallel Programming for FPGAs book <http://kastner.ucsd.edu/hlsbook/>`_. The book covers many aspects of the optimizations in this project, and we strongly recommend this as a reference.

The project is divided into three parts:

* Design an 11-tap FIR filter
* Design and optimize a 128-tap FIR filter
* Prototype an FIR filter architecture on a Zynq FPGA

You should start this assignment by understanding the 11-tap FIR filter and implementing a functionally correct design. Next, you modify the code and experiment with different optimizations specified in the questions. The 128-tap FIR filter is more complex and may have different trade-offs, and in the final report, you need to answer the questions about the 128-tap filter. Your answers should show that you understand different optimization and their effects on throughput, latency, and area. Finally, you will take one of your FIR filter designs, program that onto a Zynq FPGA, and demonstrate its functionality with the Pynq infrastructure.

2) Preparation
--------------

Before you start, we strongly suggest you familiarize yourself with the high-level synthesis tool.

* Vitis HLS: A good option is this `VitisHLS User Guide <https://docs.amd.com/r/en-US/ug1399-vitis-hls/Introduction>`_. You do not need to go through the optimization steps, though they provide a good preview of the optimizations you will find in future projects.

* Vivado: Xilinx tool for RTL, SoC design (excluding firmware), and FPGA prototyping. It is not required for this project if you are not planning to prototype on Zynq FPGA. `Vivado User Guide: Getting Started <https://docs.xilinx.com/r/2022.2-English/ug910-vivado-getting-started/Vivado-Design-Suite-Overview>`_

You can follow the `lab tutorials <https://pp4fpgas.readthedocs.io/en/latest/PYNQ-example.html>`_ step by step (up to C synthesis and exporting RTL) to complete the Vitis HLS enviroment setup.



3) Materials
------------

Starter code for this project is available at:

* `project1 <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/project1>`_

This contains:

* fir11 folder: 11 tap fir filter

  - fir.cpp - Implements top-level function

  - fir.h - header file

  - fir_test.cpp - test bench

  - input.dat - input chirp signal

  - out.gold.dat - “Golden” output. When the testbench (from fir_test.cpp) is run through the file fir.cpp it should generate this result. If it does not, you did something wrong.

  - __hls_config__.ini - Record important HLS project settings including target clock period and board part. Also specify the name of the top function.

  - Makefile - Makefile to run the HLS tool from the command line.


* fir128 folder: 128 tap fir filter

  - Contain the same starter code.

Target Board Part: xc7z020clg400-1 (Pynq-Z2 board), or xck26-sfvc784-2lv-c (Kria KV260 board).

Software: Vitis HLS 2024.1 or 2024.2 

Clock Period: 10 ns or 100MHz




4) How to Run the project
--------------------------
Vitis HLS is the EDA tool that allows you to write C/C++ program and generate optimized RTL module. Vitis HLS can be used in two ways: GUI and command line. For simplicity and portability, we will use command line in this project. 

We have provided a Makefile and config.ini file to facilitate the C simulation and synthesis.

It is necessary to have the `scripts <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/scripts>`_ folder ready. 

Line 34 of the ``Makefile`` reference the  scripts folder. You might need to change it to your local path. The scripts will read the ``__hls_config__.ini`` file to generate the .tcl script for Vitis HLS.

Vitis HLS will then read the generated ``.tcl`` scripts to create project components and run C simulation and synthesis.

Your first step should be to run the C synthesis, this simply checks the functional correctness of your code. You can do this by:
.. code-block:: sh

   cd <your fir11 or fir128 folder>
   make test

To run C synthesis, do:
.. code-block:: sh

   make hls

This will create the HLS project folder. The synthesized RTL and reports will be generated. You can run this command:
.. code-block:: sh

   make report

to copy the synthesis report to your source code directory. This file will contain the performance and resource usage that you will be reporting.

To delete the generated files for a clean start, do:
.. code-block:: sh

   make clean

5) Project Goal
---------------

The first goal of this project is to generate a functionally correct HLS design for an 11-tap FIR filter. Also, you should start to gain an understanding of different HLS optimizations. For FIR128, you should modify the code to generate several optimized designs. Your goal is to create designs that provide tradeoffs between resource usage and execution time. This will require you to rewrite the code and insert pragmas. More specifically, you must do the following:

* Design an 11-tap FIR filter with HLS. In the rest of this document, we use the term FIR11 to refer to this task.

* Design a 128-tap FIR filter with HLS and optimize it. We call this subtask FIR128.

5) FIR11
--------

The first step for the project is to get a functionally correct design working for an 11-tap FIR filter. For this, you must use the Vivado HLS tool and finish the function body of `void fir()` in the file fir.cpp to implement the filter. You can test the correctness of your code by using the provided testbench. This code does not need to be highly optimized; you will work on creating optimized code later. It just needs to work correctly. Use the provided ``Makefile`` to create your project.

6) FIR128 Instructions
----------------------

You will complete the following tasks:

1. Implement a functionally correct, but not optimized, 128-tap FIR filter. This is your baseline implementation. Use the provided ``Makefile`` to create your project. As you attempt each optimization according to the questions below, think about what other optimizations would work well in conjunction with them.

2. Next, generate one or multiple designs to help you answer your report's questions. You should reference the design you generated for your experiment in your answers. You can reference the same design from multiple answers. Your resulting code must always be functionally correct (i.e., match the golden output). In your report, you must explain the effect of the following optimizations on your design. You can test other optimizations as you'd like, but you can leave these out of your report. For every design you include in your report, you can report the corresponding throughput instead of the estimated clock period and latency.

3. Finally, for Q6, generate your best architecture by combining any number of optimizations that you wish. You can use what you learned from your designs for Q1-Q5.

4. Your report should only include the answers to the following questions.

You must reference a design or multiple designs for the following questions. The source code in your design should have all the necessary pragmas. Please refer to Chapter 2 in the pp4fpga textbook before starting this assignment.

Questions:

* **Question 1 - FIR11 Baseline:** Implement a functionally correct 11-tap FIR filter. Do not apply pragmas or other optimizations. You can take reference from the textbook.

  - **(a)** Report latency, initiation interval (II), in clock cycles.
  - **(b)** Report the number of BRAM, DSP, LUT and FFs used.

Questions 2-7 refers to FIR128. You should have a functionally correct design before starting these questions.

* **Question 2 - Variable Bitwidths:** You can specify a precise data type for each variable in your design. There many different data types including floating point, integer, fixed point, all with varying bitwidths and options. The data type provides a tradeoff between accuracy, resource usage, and performance. 

  Change the bitwidth of the variables inside the function body (namely ``coef_t`` and ``acc_t``) using the ``ap_int<>`` datatype.

  - **(a)** Try 3 combinations of variable bitwidths of your choice. Report the latency, II, and resource usage (BRAM, DSP, LUT, and FF) for each design in a table.
  - **(b)** What is the minimum bitwidth of ``coef_t`` and ``acc_t`` you can use without losing accuracy (i.e., your results still match the golden output)?

* **Question 3 - Pipelining:** Pipelining increases throughput, typically at the cost of additional resources. The initiation interval (II) is an important design parameter that affects performance and resource usage.

  - **(a)** Report the latency, II, and resource usage of your baseline FIR128 design.
  - **(b)** Turn off the automatic pipelining by using ``#pragma HLS pipeline off``. Report the latency, II, and resource usage of this design.
  - **(c)** Manually pipeline the design using ``#pragma HLS pipeline II=<value>``. Explicitly set the loop initiation interval (II) starting at 1 and increasing in increments of 1 cycle until the throughput stays unchanged. Report the latency, II, and resource usage of each design in a table.
  - **(d)** At some point setting the II to a larger value does not make sense. What is that value in this example? 
  - **(e)** Vitis HLS may automatically pipeline a loop without any specific pragma. Based on your observation, what is the default II for a pipelined loop used in this case? 

* **Question 4 - Removing Conditional Statements:** If/else statements and other conditionals can limit the possible parallelism and often require additional resources. Rewriting the code to remove them can make the resulting design more efficient. This is known as code hoisting.

  Rewrite the code to remove any conditional statements. 
  
  - **(a)** Compare the latency, II, and resource usage of the automatically pipelined design with / without conditional statements.
  - **(b)** Compare the latency, II, and resource usage of the non-pipelined design with / without conditional statements.

* **Question 4 - Loop Partitioning:** Dividing the loop into two or more separate loops may allow for each of those loops to be executed in parallel (via unrolling), enable loop-level pipelining, or provide other benefits. This may increase performance and resource usage.
  
  - **(a)** Briefly describe the opportunity for loop partitioning in FIR128. Re-write the code to apply your idea.
  - **(b)** Compare the latency, II, and resource usage of the design with / without loop partitioning.
  - **(c)** Apply loop unrolling to the design with loop partitioning. Report the latency, II, and resource usage of this design.
  - **(d)** What is the relationship between loop unrolling and pipelining? Can they be applied together and benefit the design? Justify you answer with experiments / references to past questions.

  Is there an opportunity for loop partitioning in FIR filters? Compare your hardware designs before and after loop partitioning. What is the difference in performance? How does the number of resources change? Why?

* **Question 5 - Memory Partitioning:** The storage of the arrays in memory plays an important role in area and performance. On one hand, you could put an array entirely in one memory (e.g., BRAM). But this limits the number of read and write accesses per cycle. Or you can divide the array into two or more memories to increase the number of ports. Or you could instantiate each variable as a register allowing simultaneous access to all the variables at every clock cycle.

  Read the textbook about the memory partitioning parameters: block, cyclic, and complete. 

  - **(a)** Explore array partitioning options for both arrays in your design from Question 4. Report the latency, II and resource usage. Which partition gives the best performance?
  - **(b)** Loop unrolling and memory partitioning are often used together. Try disabling loop unrolling or array partitioning. Report the effects.

* **Question 6 - Best Design:** Combine any number of optimizations to get your best architecture. A design with high throughput will likely take a lot of resources. A design with small resource usage likely will have lower performance, but that could still be good enough depending the application goals.

  - **(a)** Combine any number of optimizations to get your best throughput. What optimizations did you use to obtain this result? Report the latency, II, throughput (in MHz). It is possible to create a design that outputs a result every cycle, i.e., get one sample per cycle, so a throughput of 100 MHz (assuming a 10 ns clock).
  - **(b)** Report the resource usage of your design with the best throughput. Explain why the resource usage is high compared with the baseline in Question 2.
  
It is possible that some optimizations have little (or no effect). Some optimizations may only work when used in combination with others. This is what makes the design space exploration process difficult (and interesting).

* **Note**: You should use ap_int types if necessary for required bit width. You can read about ap_int from `here <https://docs.amd.com/r/en-US/ug1399-vitis-hls/Overview-of-Arbitrary-Precision-Integer-Data-Types>`_ or from section 2.10 of the `textbook <http://kastner.ucsd.edu/hlsbook/>`_. 

7) PYNQ Demo (Optional)
------------------------

The following are steps to implement your FIR11 HLS design on the PYNQ board. You will provide the input data (chirp signal) from the Notebook and get the output from the PL on PYNQ. To do that, you must write a *host_fir.ipynb* program.

The specific things you must do in this section are:

* Download an appropriate image for your board from `here <http://www.pynq.io/board.html>`_ and write it to your SDCard (`PYNQ-Z2 instructions <https://pynq.readthedocs.io/en/latest/getting_started/pynq_z2_setup.html>`_).

* Go through :doc:`Lab: Pynq Memory Mapped IO <PYNQ-example>` example and learn how to write an IP for PYNQ and interact with it.

* Implement your **11-tap** FIR design on PYNQ board.

* Write a host program *host_fir.ipynb*. The expected output is as shown below:

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/demo1.png

Check `pynq.io <http://www.pynq.io/board.html>`_ for more info.

8) Report Guidelines
--------------------

FIR11
~~~~~

* Submit your code (only source code for synthesis) and tcl script.

* Submit synthesis reports (fir_csynth.rpt file **and** fir_csynth.xml document files, you can find them in "<your solution folder>/syn/report").

Demo
~~~~

* Submit your code (only host code)

* Submit a screenshot of the results

* Submit your bitstream

FIR128
~~~~~~

* For each "interesting" architecture:

  - Submit your code and tcl script

  - Submit synthesis reports (.rpt **and** .xml)

  - "Interesting" is imprecise, but it is often difficult to say definitively that one design is the best. Typically, there are different designs that Pareto optimal. Submit any design that you discuss in the answers to your questions. Often, one performs a lot of design space exploration by changing values, leading to many architectures, many of which are "bad" or "uninteresting". We don't need details on those. A good target is more than five and less than twenty "interesting" designs. Your report should only include the answers to the questions. Please clearly indicate where each question is answered in your report.

For each question, explicitly mention which design(s) you used in your answers. You are asked to discuss different performance and resource metrics. Ensure the method used to calculate the performance and resource metrics is described. Throughput calculation methods are described below. It is typically best to report performance metrics in terms of seconds (or frequency = 1/seconds) rather than some other interval, e.g., clock cycles. For this reason, we **require** you to state the corresponding throughput for every design instead of the estimated clock period and latency.

You are strongly encouraged to use figures and tables to explain an answer. Figure 1 and Figure 2 provide a typical way to compare different architectures. These can be made better, but they serve as a reference that can be relatively easily generated. You can also consider different figures, e.g., to provide an overview of a particular architecture or help explain how you determined the "best design" (i.e., your design space exploration process).

Throughput Calculation
~~~~~~~~~~~~~~~~~~~~~~

The throughput is reported in Hz using the formula from Equation 2. Note that you should use the "Estimated Clock Period (ns)" from HLS report instead of the specified clock period. The former is more accurate (though not totally accurate - to do that, you must perform complete synthesis to bitstream) than the latter, which is the user-specified target rate clock period. Often, the tools can do better than the estimated clock period.

The throughput in Hertz can be calculated as:

.. math::
  \text{Throughput (Hz)} = 1/(\text{Clock Period (s)} * \# \text{Clock Cycles})

The throughput in Mhz can be calculated as:

.. math::
  \text{Throughput (MHz)} = 1000/(\text{Clock Period(ns)} * \# \text{Clock Cycles})

You should always present your results using units (Hz, KHz, MHz, etc.) that make “sense.” For example, you should not do 10000 Hz instead 10 KHz. Or not 0.02 MHz but rather 20 KHz

Example Figures
~~~~~~~~~~~~~~~

Figure 1 shows an example graph of resource usage for eight designs. Figure 2 shows their throughput performance.

.. image:: FIRArea.svg
    :width: 640px
    :height: 395px

*Figure 1. Area results of different FIR designs. Note that these are only for reference and do not correspond exactly to the results you can/should obtain.*

.. image:: FIRThroughput.svg
    :width: 640px
    :height: 395px

*Figure 2. Example throughput results for different FIR designs. Note that these are only for reference and do not correspond exactly to the results you can/should obtain.*

9) Submission Procedure
-----------------------

You should submit a report as described in the report instructions.

You must also submit your code (\*.cpp, \*.h files, and \*.tcl, but nothing else). Your code should have everything in it so we can synthesize it directly. This means you should use pragmas in your code and not use the GUI to insert optimization directives. We must be able to only import your fir.cpp/h file and directly synthesize it. You can assume we have correctly set up the design environment (fir_test.cpp, etc.). **DO NOT SUBMIT THE ENTIRE HLS FOLDER.**

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to ensure they correspond to the instructions.

Your repo must contain a "fir" folder at the top level. This folder must be organized as follows:

* **Report.pdf**

* Folder **fir11_baseline**: fir.h | fir.cpp | script.tcl | fir_csynth.rpt | fir_csynth.xml

* Folder **fir128_baseline**: fir.h | fir.cpp | script.tcl | fir_csynth.rpt | fir_csynth.xml

* Folder **fir128_optimized1**: fir.h | fir.cpp | script.tcl | fir_csynth.rpt | fir_csynth.xml

* Folder **fir128_optimized2**: fir.h | fir.cpp | script.tcl | fir_csynth.rpt | fir_csynth.xml

* Folder **fir128_optimized3**: fir.h | fir.cpp | script.tcl | fir_csynth.rpt | fir_csynth.xml

* Folder **fir128_optimized4**: fir.h | fir.cpp | script.tcl | fir_csynth.rpt | fir_csynth.xml

* Folder **fir128_optimized5**: fir.h | fir.cpp | script.tcl | fir_csynth.rpt | fir_csynth.xml

* Folder **fir128_best**: fir.h | fir.cpp | script.tcl | fir_csynth.rpt | fir_csynth.xml

* Folder **Demo**: (WES students only) host_fir.ipynb | .bit | .hwh

* *fir128_optimizedN* corresponds to the architectures you generated to answer the questions. You can have one or multiple. Ensure the code is readable (i.e., do not put multiple optimizations commented out in the same file).

* *fir128_best* is the folder containing your best architecture.

You are not restricted to five optimized folders; for example, you could submit 10. A good rule of thumb is that if you refer to an architecture in your report, you should include a folder of that architecture. 

Submission
~~~~~~~~~~

Place your code on your private Bitbucket or GitHub repository. Give the instructors collaborator or read-only access. Put separate assignments in separate folders; name each folder according to the project. Place your report directly under your project folder.

10) Grading Rubric
------------------

Your answers to the questions will determine your grade. Your answers should be well-written and clearly delineated (for example, copying the questions into the report before answering them or placing each question under a separate subheading). Additional points (up to 20) will be subtracted for poor formatting and answers that are hard to understand. Example issues include spelling errors, multiple/egregious grammar errors, poor presentation of results, lack of written comparison of the results, etc. Report throughput and resource usage for each design you discuss in your report, and include the files for these designs in your submission. We encourage using tables to state results, figures to draw comparisons between different designs, and short summaries about how the different architectures were generated. A well-written report is informative but not overly verbose. You will be deducted points if you do not follow the instructions for the directory naming and file structure.

If you submit a report made in LaTeX, you might find `this link that generates tables from spreadsheets <https://www.tablesgenerator.com/>`_ helpful.

The report comprises 80% of your grade. The remaining 20% is for the performance of the best version of your fir128 filter. If your design achieves a throughput greater than 0.5MHz but less than 1MHz, then you will be awarded 10 points. If you achieve 1MHz and higher, you will get full credit. Try to make resource usage as small as possible. The resource usage must be within the resources provided by the Pynq board. Similarly the timing has to be fulfilled, i.e. the clock achieved should be within 10ns (100 MHz).  
