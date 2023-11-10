Lab: Axistream Single DMA (axis) 
================================

Simple streaming example using AXI 
************************
In this example we learn how to use `Xilinx AXI_DMA <https://www.xilinx.com/products/intellectual-property/axi_dma.html>`_ to create streaming interfaces for and IP.

This class will not go too deep into AXI protocols and Vivado, but a nice tutorial of the AXI Direct Memory Access (DMA) exists `here. <https://www.fpgadeveloper.com/2014/08/using-the-axi-dma-in-vivado.html>`_

1) Vivado HLS: Generating RTL code from C/C++ code
-------------------------------------------------

In this section you learn how to create a project in Vivado HLS, synthesize your code, and generate RTL.

1.1) Download code and create a Vivado HLS project
#################################################

Download and unzip `streamMul.zip. <https://bitbucket.org/akhodamoradi/pynq_interface/downloads/streamMul.zip>`_ Generate your project using the provided script.tcl file:

Linux: open a terminal, make sure your environment is set, navigate to streamMul folder, and run the following ::

    $ vitis_hls script.tcl

Windows: Open Vitis and create a New Project and import **streamMul.cpp** and **streamMul.hpp** and set **smul** as the top function.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/manual_add.png

**Your code is not complete!**, modify your code to become same as the following:

.. code-block :: c++

	#include "ap_axi_sdata.h"
	#include "hls_stream.h"

	typedef ap_axiu<32, 0, 0, 0> trans_pkt;

	void smul(hls::stream< trans_pkt > &INPUT, hls::stream< trans_pkt > &OUTPUT)
	{
	#pragma HLS INTERFACE s_axilite port = return bundle = CTRL

			#pragma HLS INTERFACE axis port=INPUT
			#pragma HLS INTERFACE axis port=OUTPUT
			trans_pkt data_p;

			INPUT.read(data_p);
			data_p.data *= 2;
			OUTPUT.write(data_p);
	}


In this lab, since we are using an ap_axiu struct for out I/O variables, the `last` bit is handled for us. We must interact with them this way because we are dealing with an AXI stream, not an array.

1.2) Generate RTL code and export it
####################################

Click on Run **C Synthesis** to generate RTL code. After it is done, you can check your resource utilization and timing report. 

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/hls1.png

Check your hardware interface as follows: 

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/hls2.png


Now you can export your RTL code by clicking on **Export RTL**:

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/hls3.png

After exporting is done, you can close and exit from Vitis.

2) Vivado: Generating bitstream from RTL code
---------------------------------------------

In this section we import our RTL code from last section, add some required IPs, and generate our bitstream

2.1) Create a new Vivado project
################################

Open your Vivado tool and create a new project. Select an appropriate location for your project and leave the default project name as is (**project_1**).

Select **RTL Project** and check **Do specify not sources** at this time.

Select **xc7z020clg400-1** for your part:

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/vivado2.png

2.2) Import RTL code
####################

Under **Flow Navigator**, click on **IP Catalog**. Right click on the opened window and select **Add Repository**. Navigate to your **Vivado HLS project > solution1 > impl > ip** and select it:

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/vivado3.png

2.3) Add IPs to your design
###########################
Under **Flow Navigator**, click on **Create Block Design**. Leave the design name as is (*design_1*). In the newly opened window you can add IPs by clicking on the plus sign.

Add **ZYNQ7 Processing System** to your design:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3814633603-pynq6.png

Double click on **ZYNQ7 IP** to customize it. In the opened window, double click on **High Performance AXI 32b/64b Slave Parts**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/148617913-pynq7.png

Select and check **S AXI HP0 interface**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3126944786-pynq8.png

Add a **Smul** to your design and rename it to **smul**:

Add a **AXI Direct Memory Access** to your design and rename it to **smul_dma**. 

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/dma5.png

Double click on your **AXI DMA** and change the following parameters: 1) uncheck **Enable Scatter Gather** Engine. 2) Change **Width of Buffer Length Register** to 23:

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/dma6.png



2.4) Manual connections
#######################

Connect the following ports:

**smul::OUTPUT_r to smul_dma::S_AXIS_S2MM**

**smul_dma::M_AXIS_MM2S to smul::INPUT_r**



.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/vivado5.png

2.5) Automatic connections
##########################

Now you can leave the rest of the connections to the tool. There should be a highlighted strip on top of your diagram window.

1. Click on **Run Block Automation**

2. Click on **Run Connection Automation** and select all

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/vivado6.png

3. **IMPORTANT!** you have to click again on **Run Connection Automation**

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/vivado7.png

At this point your design should look like this:

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/axi_single_dma/vivado8.png

2.6) Generate bitstream
#######################

1. Save your design **CTRL+S** or **File > Save Block Design.**

2. Validate your design: **Tools > Validate Design**

3. In Sources, right click on **design_1**, and **Create HDL Wrapper**. (use default options) Now you should have **design_1_wrapper.**

4. Generate bitstream by clicking on **Generate Bitstream** in **Flow Navigator**


Copy your **project directory > project_1 > project_1.runs > impl_1 > design_1_wrapper** to your **project directory > project_1** and rename it to **smul.bit.** 
In my case, axi_single_dma > axi_single_dma.runs >impl_1 > design_1_wrapper.bit** 
 
Copy your **project directory > project_1 > project_1.srcs > sources_1 > bd > design_1 > hw_handoff > design_1.hwh** to your **project directory > project_1** and rename it to **smul.hwh**.
aadddddddasfasdfadsfsdafaddeeedddafadsf

You should have both **smul.bit** and **smul.hwh**.

You can close and exit from Vivado tool.

3) Host program
---------------

In this section we use Python to test our design.

3.1) Move your files
####################

Create a new folder in your PYNQ board and move both **smul.bit** and **smul.hwh** into it.

3.2) Python code
################

Create a new Jupyter notebook and run the following code to test your design:

.. code-block :: python3
    
    import time
	from pynq import Overlay
	import pynq.lib.dma
	import numpy as np
	from pynq import MMIO
	import random

	print("Programming the FPGA")
	ol = Overlay('./smul.bit') # check your path
	ol.download() # it downloads your bit to FPGA
	
	print("Inspect all the IP names")
	ol.ip_dict.keys()

.. code-block :: python3

	print("Inspect the HLS IP registers")
	hls_ip = ol.smul
	print(hls_ip)
	# hls_ip.register_map


	# Setup recv/send DMA 
	dma = ol.smul_dma
	dma_send = ol.smul_dma.sendchannel
	dma_recv = ol.smul_dma.recvchannel

	#dma = ol.axi_dma_0
	#dma_send = ol.axi_dma_0.sendchannel
	#dma_recv = ol.axi_dma_0.recvchannel

	print("Starting HLS IP")
	hls_ip.register_map
	CONTROL_REGISTER = 0x0
	hls_ip.write(CONTROL_REGISTER, 0x81) # 0x81 will set bit 0
	# hls_ip.register_map

	# Prepare data to send 
	from pynq import allocate
	import numpy as np

	data_size = 20
	input_buffer = allocate(shape=(data_size,), dtype=np.uint32)
	output_buffer = allocate(shape=(data_size,), dtype=np.uint32)

	for i in range(data_size):
		input_buffer[i] = i

	print("Starting DMA transfer")
	dma_recv.transfer(output_buffer)
	dma_send.transfer(input_buffer)

	dma_send.wait()
	dma_recv.wait()

	# Print the data 
	for i in range(data_size):
		#print('0x' + format(output_buffer[i], '02x'))
		print(i, input_buffer[i], output_buffer[i])

	del input_buffer
	del output_buffer
	del ol
	print("Finished!")
