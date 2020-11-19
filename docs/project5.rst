.. OFDM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: FM Demodulator
=========================

1) Introduction
---------------
In this project we will build an FM Demodulator and implement it on the Pynq Board.

2) Project Goal
---------------

In this project, you will use your knowledge from previous projects to implement a FM Demodulator in programmable logic. The project is divided into two parts. In the first part, you develop different functions for a FM Demodulator using HLS. A FM Demodulator consists of a linear filter, downsampler and a discriminator.The second part is to integrate the Demodulator onto the Pynq Board using "RTL2832" USB tuners. You should be able to listen to local FM radio channel using your MonoFM implementation in programmable logic. For more detail about the mono FM implementation have a look at it's source code `here <https://github.com/mwickert/scikit-dsp-comm/blob/master/sk_dsp_comm/rtlsdr_helper.py>`_.

3) Materials
------------

`Download <https://bitbucket.org/akhodamoradiUCSD/237c_draft/downloads/fm.zip>`_.

This contains a Python notebook which explains the working of a Mono FM Demodulator.

For this project the following will not be provided:

* ~.cpp - The place where you write synthesizable code
* ~.h - header file with various definitions that may be useful for developing the code 
* ~test.cpp - testbench

You will have to build the entire project from scratch

4) Design Instructions
----------------------
The FM Demodulator has 3 main parts: downsampler, linear filter and discriminator.

**downsampler**
###############
This part consists of a straight forward downsampler. We have to downsample by a factor of N, i.e. keep every Nth sample. The implementation of downsampler can be found `here <https://github.com/mwickert/scikit-dsp-comm/blob/master/sk_dsp_comm/sigsys.py#L2673>`_.

**linear filter**
#################
Build a linear filter whose function is implemented as a direct II transposed structure.

This means that the filter implements:
   a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[M]*x[n-M] - a[1]*y[n-1] - ... - a[N]*y[n-N]
   
 More information about the linear filter implementation can be found `here <https://github.com/scipy/scipy/blob/v1.5.4/scipy/signal/signaltools.py#L1719-L1909>`_.

**discriminator**
#################
To demodulate FM radio, we require a discriminator circuit which gives an output that is proportional to the input frequency deviation. 


.. code-block :: python3

   function disdata = discrim(x)
   // x is the received signal in complex baseband form
   // Mark Wickert
   // xI is the real part of the received signal
   // xQ is the imaginary part of the received signal
   // N is the length of x
   // b filter coefficients
   // a for discrete derivative
   der_xI = linear_filter(b,a,xI)
   der_xQ = linear_filter(b,a,xQ)
   // normalize by the squared envelop acts as a limiter
   disdata = (xI*der_xQ-xQ*der_xI)./(xI^2+xQ^2)
   
More information about the discriminator can be found `here <http://www.eas.uccs.edu/~mwickert/ece5625/lecture_notes/N5625_4.pdf#page=23>`_ in page 4-23.

**Optimization Guidelines**

* You must always use a clock period of 10 ns.

* It is your task to ensure functional correctness in your synthesized design. Therefore, you must write each test bench carefully.

5) PYNQ Demo
------------

This project is different from your previous projects in the sense that it has an immediate and observable impact on you. The effect of the latency and throughput of your implementation can be observed by listening to your audio output, and the feelings of frustration you obtain when a song keeps getting cut. You are highly encouraged to modify the code to achieve a better performance and observe the throughput by changing the way you transmit data between PS and PL. Make use of the "RTL 2832" USB tuner in-order to receive the input RF Samples.

6) Submission Procedure
-----------------------

You need to demonstrate your functional hardware implementation FM Demodulator in class. We will post schedule of each team’s demonstration later on Piazza.

You must also submit your code (and only your code, not other files, not HLS project files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to only import your source file and directly synthesize it. If you change test benches to answer questions, please submit them as well. You can assume that we have correctly set up the design environment. 

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "mono_fm" at the top-level. This folder must be organized as follows (similar to previous projects):

**Contents:**

* **Report.pdf**

* Folder **fm-demodulator**

  - Source code (*.cpp, *.h, *.tcl only) and reports (.rpt and .xml).
  
* Folder **Demo**

  - .bit and .hwh files
  - FM.ipynb host file

**Report:** For this project, you must submit a report the throughput with 1 page for each function from section 4. You may add figures, diagrams, tables, or charts to describe your architectures with a short paragraph explaining them. No questions; no answers. Just explain your design. We will check if your final FM Demodulation functions are functionally correct (they pass their test benches). The report will help us to understand your design. You also can use this report to explain your work for bonus part (check the grading section).

7) Grading Rubric
-----------------

**30 points:** Functionally correct design. You will get full credit if we are able to build your blocks without any effort. All functions must pass their test benches, and the test benches must show some amount of careful thought. You need to report your throughput for each function in your report.

**60 points:** Pynq Demo. You will get full credit for clear audio output.

**10 points:** Report.

**Bonus:** Implement audio output through the Pynq board's 3.5mm audio output. The Pynq board only plays audio through the FPGA fabric. If you are interested in this, you should look at the Pynq Base Overlay.
