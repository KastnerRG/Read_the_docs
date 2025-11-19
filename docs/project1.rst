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

* Vivado: Xilinx tool for RTL, SoC design (excluding firmware), and FPGA prototyping. It is not required for this project if you are not planning to prototype on Zynq FPGA. `Vivado User Guide: Getting Started <https://docs.amd.com/r/en-US/ug910-vivado-getting-started/Vivado-Design-Suite-Overview>`_

You can follow the `lab tutorials <https://pp4fpgas.readthedocs.io/en/latest/PYNQ-example.html>`_ step by step (up to C synthesis and exporting RTL) to complete the Vitis HLS environment setup.



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

Line 44 of the ``Makefile`` reference the  scripts folder. You might need to change it to your local path. The scripts will read the ``__hls_config__.ini`` file to generate the .tcl script for Vitis HLS.

Vitis HLS will then read the generated ``.tcl`` scripts to create project components and run C simulation and synthesis.

Your first step should be to run the C synthesis, this simply checks the functional correctness of your code. You can do this by:
   
   ``cd <your fir11 or fir128 folder>``

   ``make test``


To run C synthesis, do:
   
   ``make hls``
  


This will create the HLS project folder. The synthesized RTL and reports will be generated. You can run this command:
   
   ``make report``

to copy the synthesis report to your source code directory. This file will contain the performance and resource usage that you will be reporting. Note that you only need to report the top level performance and resource consumption. For performance metrics, report the numbers under "Latency: Summary". You should report the max value (worst case scenario) if the min and max values are different. For resource consumption, only report the line "Used" under "Utilization Estimates:Summary".

To delete the generated files for a clean start, do:

   ``make clean``

Though not required, you can also run the project using the GUI of Vitis Unified IDE. The advanced visualization tools might help you better understand your optimizations. The steps are `here <https://pp4fpgas.readthedocs.io/en/latest/vitis_unified.html>`_. Note that submission should still be done in command line, as described in Sections 10 and 11.

5) Project Goal
---------------

The first goal of this project is to generate a functionally correct HLS design for an 11-tap FIR filter. Also, you should start to gain an understanding of different HLS optimizations. For FIR128, you should modify the code to generate several optimized designs. Your goal is to create designs that provide tradeoffs between resource usage and execution time. This will require you to rewrite the code and insert pragmas. More specifically, you must do the following:

* Design an 11-tap FIR filter with HLS. In the rest of this document, we use the term FIR11 to refer to this task.

* Design a 128-tap FIR filter with HLS and optimize it. We call this subtask FIR128.

6) FIR11
--------

The first step for the project is to get a functionally correct design working for an 11-tap FIR filter. For this, you must use the Vivado HLS tool and finish the function body of `void fir()` in the file fir.cpp to implement the filter. You can test the correctness of your code by using the provided testbench. This code does not need to be highly optimized; you will work on creating optimized code later. It just needs to work correctly. Use the provided ``Makefile`` to create your project.

7) FIR128 Instructions
----------------------

You will complete the following tasks:

1. Implement a functionally correct, but not optimized, 128-tap FIR filter. This is your baseline implementation. Use the provided ``Makefile`` to create your project. As you attempt each optimization according to the questions below, think about what other optimizations would work well in conjunction with them.

2. Next, generate one or multiple designs to help you answer your report's questions. You should reference the design you generated for your experiment in your answers. You can reference the same design from multiple answers. Your resulting code must always be functionally correct (i.e., match the golden output). In your report, you must explain the effect of the following optimizations on your design. You can test other optimizations as you'd like, but you can leave these out of your report. For every design you include in your report, you can report the corresponding throughput instead of the estimated clock period and latency.

3. Finally, for Q7, generate your best architecture by combining any number of optimizations that you wish. You can use what you learned from your designs for Q2-Q6.

4. Your report should only include the answers to the following questions.

Please refer to Chapter 2 in the pp4fpga textbook before starting this assignment.

8) Questions
--------------

* **Question 1 - FIR11 Baseline:** Implement a functionally correct 11-tap FIR filter. Do not apply pragmas or other optimizations. You can take reference from the textbook.

  - **(a)** Report latency, initiation interval (II), in clock cycles.
  - **(b)** Report the number of BRAM, DSP, LUT and FFs used.

Questions 2-7 refers to FIR128. You should have a functionally correct design before starting these questions.

* **Question 2 - Variable Bitwidths:** You can specify a precise data type for each variable in your design. There are many different data types including floating point, integer, fixed point, all with varying bitwidths and options. The data type provides a tradeoff between accuracy, resource usage, and performance. 

  Change the bitwidth of the variables inside the function body (namely ``coef_t`` and ``acc_t``) using the ``ap_int<>`` datatype.

  - **(a)** Try 3 combinations of variable bitwidths of your choice. Report the latency, II, and resource usage (BRAM, DSP, LUT, and FF) for each design in a table.
  - **(b)** What is the minimum bitwidth of ``coef_t`` and ``acc_t`` you can use without losing accuracy (i.e., your results still match the golden output)?

* **Question 3 - Pipelining:** Pipelining increases throughput, typically at the cost of additional resources. The initiation interval (II) is an important design parameter that affects performance and resource usage. **Hint**: In this project, pipelining should be applied to the ``for`` loop instead of the entire function.

  - **(a)** Report the latency, II, and resource usage of your baseline FIR128 design.
  - **(b)** Turn off the automatic pipelining by using ``#pragma HLS pipeline off``. Report the latency, II, and resource usage of this design.
  - **(c)** Manually pipeline the design using ``#pragma HLS pipeline II=<value>``. Explicitly set the loop initiation interval (II) starting at 1 and increasing in increments of 1 cycle until the throughput stays unchanged (and/or, reaches the same value of a non-pipelined design). Report the latency, II, and resource usage of each design in a table.
  - **(d)** At some point setting the II to a larger value does not make sense. What is that value in this example? 
  - **(e)** Vitis HLS may automatically pipeline a loop without any specific pragma. Based on your observation, what is the default II for a pipelined loop used in this case? 

* **Question 4 - Removing Conditional Statements:** If/else statements and other conditionals can limit the possible parallelism and often require additional resources. Rewriting the code to remove them can make the resulting design more efficient. This is known as code hoisting.

  Rewrite the code to remove any conditional statements. 
  
  - **(a)** Report the numbers in a table: Compare the latency, II, and resource usage of the automatically pipelined design with / without conditional statements.
  - **(b)** Report the numbers in a table: Compare the latency, II, and resource usage of the non-pipelined design with / without conditional statements.

* **Question 5 - Loop Partitioning:** Dividing the loop into two or more separate loops may allow for each of those loops to be executed in parallel (via unrolling), enable loop-level pipelining, or provide other benefits. This may increase performance and resource usage.
  
  - **(a)** Briefly describe the opportunity for loop partitioning in FIR128. Re-write the code to apply your idea.
  - **(b)** Compare the latency, II, and resource usage of the design with / without loop partitioning.
  - **(c)** Apply loop unrolling to the design with loop partitioning. Report the latency, II, and resource usage of this design.
  - **(d)** What is the relationship between loop unrolling and pipelining? Can they be applied together and benefit the design? Justify your answer with experiments / references to past questions.

* **Question 6 - Memory Partitioning:** The storage of the arrays in memory plays an important role in area and performance. On one hand, you could put an array entirely in one memory (e.g., BRAM). But this limits the number of read and write accesses per cycle. Or you can divide the array into two or more memories to increase the number of ports. Or you could instantiate each variable as a register allowing simultaneous access to all the variables at every clock cycle.

  Read the textbook about the memory partitioning parameters: block, cyclic, and complete. 

  - **(a)** Explore array partitioning options for both arrays in your design from Question 5. Report the latency, II and resource usage. Which partition gives the best performance?
  - **(b)** Loop unrolling and memory partitioning are often used together. Try disabling loop unrolling or array partitioning. Report the effects.

* **Question 7 - Best Design:** Combine any number of optimizations to get your best architecture. A design with high throughput will likely take a lot of resources. A design with small resource usage likely will have lower performance, but that could still be good enough depending the application goals.

  - **(a)** Combine any number of optimizations to get your best throughput. What optimizations did you use to obtain this result? Report the latency, II, throughput (in MHz). It is possible to create a design that outputs a result every cycle, i.e., get one sample per cycle, so a throughput of 100 MHz (assuming a 10 ns clock).
  - **(b)** Report the resource usage of your design with the best throughput. Explain why the resource usage is high compared with the baseline in Question 2.
  
It is possible that some optimizations have little (or no effect). Some optimizations may only work when used in combination with others. This is what makes the design space exploration process difficult (and interesting).

* **Note**: You should use ap_int types if necessary for required bit width. You can read about ap_int from `here <https://docs.amd.com/r/en-US/ug1399-vitis-hls/Overview-of-Arbitrary-Precision-Integer-Data-Types>`_ or from section 2.10 of the `textbook <http://kastner.ucsd.edu/hlsbook/>`_. 

9) PYNQ Demo
------------------------

**UCSD students: this part is optional for project 1**.

The following are steps to implement your FIR11 HLS design on the PYNQ board. You will provide the input data (chirp signal) from the Notebook and get the output from the PL on PYNQ. To do that, you must write a *host_fir.ipynb* program.

The specific things you must do in this section are:

* Download an appropriate image for your board from `here <http://www.pynq.io/boards.html>`_ and write it to your SDCard (`PYNQ-Z2 instructions <https://pynq.readthedocs.io/en/latest/getting_started/pynq_z2_setup.html>`_).

* Go through :doc:`Lab: Pynq Memory Mapped IO <PYNQ-example>` example and learn how to write an IP for PYNQ and interact with it.

* Implement your **11-tap** FIR design on PYNQ board.

* Write a host program *host_fir.ipynb*. The expected output is as shown below:

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/demo1.png

Check `pynq.io <http://www.pynq.io/boards.html>`_ for more info.

10) Report Guidelines
------------------------

You only have to answer the questions in the report. The report should be concise and well-written. Answers to each sub-questions should be cleary marked (e.g., Q1.(a)). You do not need to include any code in the report. Explanation of the code / design is also not required unless the questions explicitly requires so. Report should be submitted to Canvas as a PDF file.

Throughput calculation methods are described below. It is typically best to report performance metrics in terms of seconds (or frequency = 1/seconds) rather than some other interval, e.g., clock cycles. For this reason, we **require** you to state the corresponding throughput for every design instead of the estimated clock period and latency.

You are encouraged to use figures and tables to explain an answer. Figure 1 and Figure 2 provide a typical way to compare different architectures. These can be made better, but they serve as a reference that can be relatively easily generated. You can also consider different figures, e.g., to provide an overview of a particular architecture or help explain how you determined the "best design" (i.e., your design space exploration process).

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


11) Code Submission
------------------------------

You must also submit your code. We should be able to run your code and re-produce the results. 

You will need to submit one folder per question. Also, please keep a copy of the report in the repo.

 - **Report.pdf**
 - Folder **Q1**: A functional correct fir11 design.
 - Folder **Baseline**: A functional correct fir128 design without any optimization / pragmas.
 - Folder **Q2**: The design with minimal bitwidth of ``coef_t`` and ``acc_t``, which is your answer to Q2.(b).
 - Folder **Q3**: The design with pipeline turned off, which is your answer to Q3.(b).
 - Folder **Q4**: The automatically pipelined design without conditional statements, which is your answer to Q4.(a).
 - Folder **Q5&6**: The design with loop partitioning, unrolling and array partitioning, which is your answer to Q6.(a).
 - Folder **Q7**: Your design with the highest throughput.

**Each folder** should contain the following files (and these files only), do **not** push the HLS project folder:

 - fir.h
 - fir.cpp
 - fir_test.cpp
 - Makefile
 - __hls_config__.ini
 - fir_test.log # Generated by ``make test``
 - fir_csynth.rpt # Generated by ``make report``
 - fir.tcl # Generated by ``make hls``
 
You must follow the file structure below. We may use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to ensure they correspond to the instructions.

Your repo must contain a "fir" folder at the top level. This folder must be organized as follows:

* **Report.pdf**

* Folder **Q1**: fir.h | fir.cpp | fir_test.cpp| Makefile| __hls_config__.ini | fir_test.log | fir_csynth.rpt | fir.tcl

* Folder **Baseline**: fir.h | fir.cpp | fir_test.cpp| Makefile| __hls_config__.ini | fir_test.log | fir_csynth.rpt | fir.tcl

* Folder **Q2**: fir.h | fir.cpp | fir_test.cpp| Makefile| __hls_config__.ini | fir_test.log | fir_csynth.rpt | fir.tcl

* Folder **Q3**: fir.h | fir.cpp | fir_test.cpp| Makefile| __hls_config__.ini | fir_test.log | fir_csynth.rpt | fir.tcl

* Folder **Q4**: fir.h | fir.cpp | fir_test.cpp| Makefile| __hls_config__.ini | fir_test.log | fir_csynth.rpt | fir.tcl

* Folder **Q5&6**: fir.h | fir.cpp | fir_test.cpp| Makefile| __hls_config__.ini | fir_test.log | fir_csynth.rpt | fir.tcl

* Folder **Q7**: fir.h | fir.cpp | fir_test.cpp| Makefile| __hls_config__.ini | fir_test.log | fir_csynth.rpt | fir.tcl

* Folder **Demo**: (WES students only) host_fir.ipynb | .bit | .hwh


Submission
~~~~~~~~~~

Place your repo on your private Bitbucket or GitHub repository. Give the instructors collaborator or read-only access. Put separate assignments in separate folders; name each folder according to the project. Place your report directly under your project folder.

12) Grading Rubric
------------------

Your answers to the questions will determine your grade. Your answers should be concise and clearly delineated. Additional points (up to 20) will be subtracted for poor formatting and answers that are hard to understand. We encourage using tables to state results, figures to draw comparisons between different designs, and short summaries about how the different architectures were generated, if asked in the question. A well-written report is informative but not overly verbose. You will be deducted points if you do not follow the instructions for the directory naming and file structure.

If you submit a report made in LaTeX, you might find `this link that generates tables from spreadsheets <https://www.tablesgenerator.com/>`_ helpful.

The report comprises 90% of your grade. The remaining 10% is for the performance of the best version of your fir128 filter. If your design achieves a throughput greater than 1MHz but less than 5MHz, then you will be awarded 5 points. If you achieve 5MHz and higher, you will get full credit. The resource usage must be within the resources provided by the Pynq board. Similarly the timing has to be fulfilled, i.e. the clock achieved should be within 10ns (100 MHz).
