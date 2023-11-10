Lab: Axistream Multiple DMAs (axis)
===================================

Simple streaming example with multiple inputs
*********************************************
In this example we learn how to use `Xilinx AXI_DMA <https://docs.xilinx.com/r/en-US/pg021_axi_dma>`_ to create a simple floating point adder with two streaming inputs and one streaming output.

1) Vitis HLS: Generating RTL code from C/C++ code
--------------------------------------------------

The first section is to create a project in Vitis HLS, synthesize your code, and generate RTL.

1.1) Download code and create a Vivado HLS project
#################################################

Download the code from `here <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/axis_fp>`_ 

Follow the same procedure of creating a Vitis HLS project as `lab 1: MMIO <https://pp4fpgas.readthedocs.io/en/latest/PYNQ-example.html>`_ You can either use .tcl script or manually add the source files and specify top function.

Now you can open your project in Vivado HLS. It should look like this:

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/0_header.jpg

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/1_dut.jpg

Check `here <https://docs.xilinx.com/r/en-US/ug1399-vitis-hls/AXI4-Stream-Interfaces>`_ for the AXI4-Stream interface and how the AXI4-Stream protocol works. In this example, we conform to the more formal version of AXIS interface required by Vitis, which requires a special data type ``hls::axis``. We define our custom data type ``ap_axis<32,2,5,6>`` as ``transPkt``. 32 means we the data we are sending is of 32 bit wide, the rest are for side channels and is not very useful for this project, it is safe to set them to other numbers, e.g. 1,1,1.

However the ``ap_axis`` struct requires the data gets transferred to be signed intergers (and ``ap_axiu`` requires unsigned integers). Since we are using floating points, we use ``union`` data type to allow the tool to interpret our data as integers when interacting with AXIS interfaces, without corrupting our floating point data. Read more about the union data type `here <https://docs.xilinx.com/r/en-US/ug1399-vitis-hls/Unions>`_ from the Xilinx user manual. `Here <https://support.xilinx.com/s/question/0D52E00007DnHxuSAF/streaming-floats-with-tlast?language=en_US>`_ is an example design that uses AXI4-Stream with floating point data.

Using the union data type improperly can lead to various problems. Keep in mind that the union data type does not do type casting, it simply interprete the same bits with differet protocols. In this lab, we do all the arithmetics in floating point, and the "integer version" of the data is used for interaction with the AXIS only, and make no sense if used for arithmetic operations.

Another issue worth noticing is that we are reusing the input AXIS ``transPkt`` for output. The ``transPkt`` contains not only the data but also the necessary side channels. In other projects, you might choose not to reuse the packets, in these cases, you have to manually take care of the side channels, especially ``last``, ``strb`` and ``keep``. Here is an example from another project,

.. code-block :: c++

	out_pkt.data = out_imag_buffer.idata;
	out_pkt.keep = in_Pkt.keep;
	out_pkt.strb = in_Pkt.strb;
	out_pkt.last = (i==LEN-1)?1:0;


1.2) Generate RTL code and export it
####################################

Follow the same step of running C synthesis and exporting RTL as `lab 1 <https://pp4fpgas.readthedocs.io/en/latest/PYNQ-example.html>`_.

2) Vivado: Generating bitstream from RTL code
---------------------------------------------

In this section we import our RTL code from last section, add some required IPs, and generate our bitstream

2.1) Create a new Vivado project and import RTL code
################################

Follow the same steps for creating a Vivado project and add the ip folder in the Vitis HLS project to Vivado IP catalog as in `lab 1 <https://pp4fpgas.readthedocs.io/en/latest/PYNQ-example.html>`_.

Open your Vivado tool and create a new project. Select an appropriate location for your project and leave the default project name as is (**project_1**).

Select **RTL Project** and check **Do specify not sources** at this time.

Select **xc7z020clg400-1** for your part

Under **Flow Navigator**, click on **IP Catalog**. Right click on the opened window and select **Add Repository**. Navigate to your **Vitis HLS project > solution1 > impl > ip** and select it:

2.3) Add IPs to your design
###########################
Under **Flow Navigator**, click on **Create Block Design**. Leave the design name as is (*design_1*). In the newly opened window you can add IPs by clicking on the plus sign.

Add **ZYNQ7 Processing System** and our HLS ip core to your design:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3814633603-pynq6.png

Double click on **ZYNQ7 IP** to customize it. In the opened window, double click on **High Performance AXI 32b/64b Slave Parts**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/148617913-pynq7.png

Select and check **S AXI HP0 interface**:

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/2_zynq.jpg

Add **AXI Direct Memory Access** to your design, you can rename the IPs if you prefer,

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/3_add_dma.jpg

Double click the DMA and change the following parameters: 1) uncheck **Enable Scatter Gather** Engine. 2) Change **Width of Buffer Length Register** to the maximum:

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/4_dma_config0.jpg

Create another DMA, disable Scatter Gather Engine, and disable the write channel. The first DMA will be used for both read and write, but the second DMA will be used for read only, as there are 2 read ports but only 1 write port in our HLS IP.

2.4) Manual connections
#######################

Maunally connect the following ports:
 
**example_0::A** to **axi_dma_0::M_AXIS_MM2S**

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/5_connect_axis.jpg

**example_0::B** to **axi_dma_1::M_AXIS_MM2S**

**example_0::C** to **axi_dma_0::S_AXIS_S2MM**

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/6_connect_axis.jpg

2.5) Automatic connections
##########################

Now you can leave the rest of the connections to the tool. There should be a highlighted strip on top of your diagram window.

1. Click on **Run Block Automation** to enable the external FIXED_IO and DDR interfaces:

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/7_block_auto.jpg

2. Click on **Run Connection Automation** and select all.

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/8_connect_auto.jpg

3. **IMPORTANT!** you have to click again on **Run Connection Automation**

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/9_connect_auto2.jpg

At this point, your design should contain 2 AXI-interconnects. One of them connects the M_AXI port of the PS with the S_AXI_LITE ports of the 2 DMAs and our HLS IP. This enables the PS to configure these IPs:

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/10_axi_inter0.jpg

The other connect the M_AXI ports of the DMAs to the high performance S_AXI port(s) of the PS. DMAs use this channel to perform read and write with the memory.

2.6) Generate bitstream
#######################

Follow the same step as as `lab 1 <https://pp4fpgas.readthedocs.io/en/latest/PYNQ-example.html>`_.

1. Save your design **CTRL+S** or **File > Save Block Design.**

2. Validate your design: **Tools > Validate Design**

3. In Sources, right click on **design_1**, and **Create HDL Wrapper**. Now you should have **design_1_wrapper.**

4. Generate bitstream by clicking on **Generate Bitstream** in **Flow Navigator**

Keep your **project directory > project_1 > project_1.runs > impl_1 > design_1_wrapper.bit** and **project directory > project_1 > project_1.gen > sources_1 > bd > design_1 > hw_handoff > design_1.hwh** for Pynq implementation. You should make sure that the bitstream and the hardware handoff files have the same name.

You can close and exit from Vivado tool.

3) Host program
---------------

In this section we use Python to test our design.

3.1) Move your files
####################

Create a new folder in your PYNQ board and move both bitstream and hardware handoff into it.

3.2) Python code
################

Create a new Jupyter notebook and run code in ``./simple_add_float.ipynb`` under the `source code folder <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/axis_fp>`_ to test your design.

You should be able to see all the components of the overlay by checking its IP dictionary
.. code-block :: python3

	ol = Overlay("./design_1_demofp.bit")
	ol.ip_dict

In this lab, we are only using ``axi_dma_0``, ``axi_dma_1`` and ``example_0``, our HLS IP.

You can check the register map of the HLS IP, and start the IP by writing to the corresponding register:
.. code-block :: python3

	CONTROL_REGISTER = 0x0
	hls_ip.write(CONTROL_REGISTER, 0x1) # 0x81 will set bit 0
	hls_ip.register_map

It is recommended to start the receive process first.

.. code-block :: python3

	dma0_recv.transfer(output_buffer)
	dma0_send.transfer(input_buffer0)
	dma1_send.transfer(input_buffer1)
	dma0_send.wait()
	dma1_send.wait()
	dma0_recv.wait()

Check the register map of DMAs to find out whether the transfer has finished without error, which is very useful in debugging.

.. code-block :: python3

	dma0.register_map
