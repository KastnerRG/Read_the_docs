Project: AMD AI-Engine (AIE) Accelerator
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
