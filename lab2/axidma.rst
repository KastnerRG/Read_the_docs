AXI_DMA
=======

Simple streaming Example
************************
In this example we learn how to use `Xilinx AXI_DMA <https://www.xilinx.com/products/intellectual-property/axi_dma.htm>`_ to create streaming interfaces for and IP.

1)Vivado_HLS: Generating RTL code from C/C++ code
-------------------------------------------------

In this section you learn how to create a project in Vivado_HLS, synthesis your code, and generate RTL.

1.1)Download code and create a Vivado_HLS project
#################################################

Download and unzip `streamMul.zip. <https://bitbucket.org/akhodamoradi/pynq_interface/downloads/streamMul.zip>`_ Generate your project using the provided script.tcl file:

Linux: open a terminal, make sure your environment is set, navigate to streamMul folder, and run the following ::

    $ vivado_hls script.tcl

Windows: open vivado_hls command line and run the following ::

    $ vivado_hls script.tcl

Now can open you your project in Vivado_HLS. **Your code is not complete!**, modify your code to become same as the following:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3975727536-pynq1.png

INPUT and OUTPUT ports are set to *axis* interfaces for streaming and *length* is set to *s_axilite* for a non-streaming interface. *axis_t* is a struct defined in the header file, the 1-bit *last* is required for *axis* interfaces.

1.2) Generate RTL code and export it
####################################

Click on Run **C Synthesis** to generate RTL code. After it is done, you can check your resource utilization and timing report. Your latency is unknown (?) because your loop size (*length*) is a variable.

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/349020321-pynq2.png

Now you can export your RTL code by clicking on **Export RTL**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/582121524-pynq3.png

After exporting is done, you can close and exit from Vivado_HLS.

2) Vivado: Generating bitstream from RTL code
---------------------------------------------

In this section we import our RTL code from last section, add some required IPs, and generate our bitstream

2.1) Create a new Vivado project
################################

Open your Vivado tool and create a new project. Select an appropriate location for your project and leave the default project name as is (**project_1**).

Select **RTL Project** and check **Do specify not sources** at this time.

Select **xc7z020clg400-1** for your part:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3090594305-pynq4.png

2.2) Import RTL code
####################

Under **Flow Navigator**, click on **IP Catalog**. Right click on the opened window and select **Add Repository**. Navigate to your **Vivado_HLS project > solution1 > impl > ip** and select it:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3508043996-pynq5.png

2.3) Add IPs to your design
###########################
Under **Flow Navigator**, click on **Create Block Design**. Leave the design name as is (*design_1*). In the newly opened window you can add IPs by clicking on the plus sign.

Add **ZYNQ7 Processing System** to your design:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3814633603-pynq6.png

Double click on **ZYNQ7 IP** to customize it. In the opened window, double click on **High Performance AXI 32b/64b Slave Parts**:


