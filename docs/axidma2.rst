Lab: Axistream Multiple DMAs (axis)
===================================

Simple streaming example with multiple inputs & outputs
*********************************************
In this example we learn how to use `Xilinx AXI_DMA <https://docs.xilinx.com/r/en-US/pg021_axi_dma>`_ to create a simple floating point adder with two streaming inputs and two streaming outputs.

1) Vitis HLS: Generating RTL code from C/C++ code
--------------------------------------------------


Find the code `here <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/axis_fp>`_. The main body of our design is a simple floating point adder and subtractor. 

We use AXI-Stream, the most common on-chip communication protocol for high performance accelerator design in SoC environments. Unlike the AXI-Lite interfaces, AXI-Stream interfaces do not have address channels, and are designed for high throughput data transfer. 

Defining the interfaces is a bit more complicated here. First we have to define a transaction packet that can be understood by AXI-Stream protocol,

.. code-block :: c++

	typedef hls::axis<float, 0,0,0> transPkt;


``float`` is our 32-bit data type. The three zero parameters disable the optional ``TUSER``, ``TID``, and ``TDEST`` side channels. The packet still includes ``keep`` (``TKEEP``), ``strb`` (``TSTRB``), and ``last`` (``TLAST``).


The interfaces to our top function must be defined as AXI-Stream channels:

.. code-block :: c++

	void axis_fp_example(
		hls::stream<transPkt>&A, 
		hls::stream<transPkt>&B, 
		hls::stream<transPkt>&C,
		hls::stream<transPkt>&D
	);

From a software perspective, you can think of these interfaces as FIFO queues with unkown depth. You can read from an input stream when there is a packet available, and write to an output stream when you have the data ready. For example,

.. code-block :: c++

	Apkt = A.read();
	Bpkt = B.read();
	Adata = Apkt.data;
	Bdata = Bpkt.data;


Construct separate output packets and set their side channels explicitly:

.. code-block :: c++

	const bool last = Apkt.last || Bpkt.last;
	transPkt Cpkt, Dpkt;
	Cpkt.data = Adata + Bdata;
	Dpkt.data = Adata - Bdata;
	Cpkt.keep = 0xf;
	Cpkt.strb = 0xf;
	Dpkt.keep = 0xf;
	Dpkt.strb = 0xf;
	Cpkt.last = last;
	Dpkt.last = last;
	C.write(Cpkt);
	D.write(Dpkt);
	if (last) {
		break;
	}


Each result is a complete four-byte float, so ``keep`` and ``strb`` are set to ``0xf``: all four bytes are present and contain data. ``last`` marks the final beat of a packet. The ``while`` loop stops when either input asserts ``last``, and both output packets use that same end condition. This ensures that both receive DMAs see an output packet boundary when the kernel stops.

This lab requires both input buffers to contain the same nonzero number of complete ``float32`` values, with ``TLAST`` asserted on the same final input pair. Each output buffer has space for that same number of floats. The shared end condition does not provide general support for unequal input lengths: the kernel reads one value from each input on every iteration, and unread data from a longer transfer can leave its send DMA blocked.

PYNQ does not require the output to reuse an input packet object. It requires valid output data, byte qualifiers, and packet boundaries. If another accelerator changes the output width or number of values, construct the output masks and ``TLAST`` for that output format and size the host receive buffers accordingly, rather than copying input metadata.

``axis_fp_example_test.cpp`` is a simple software testbench. Note that since both ``read()`` and ``write()`` functions are blocking, we have to write all the input data to the input stream before calling the function. This is different from hardware execution.

Run ``make test`` to compile and execute the C++ testbench, then ``make ip`` to run C synthesis and export RTL as an IP core for Vivado. The current ``make ip`` flow does not run C simulation or C/RTL co-simulation.


2) Vivado: Generating bitstream from RTL code
---------------------------------------------

In this section we import our RTL code from last section, add some required IPs, and generate our bitstream

2.1) Create a new Vivado project and import RTL code
################################

Follow the same steps for creating a Vivado project and add the ip folder in the Vitis HLS project to Vivado IP catalog as in `lab 1 <https://pp4fpgas.readthedocs.io/en/latest/PYNQ-example.html>`_.

Open your Vivado tool and create a new project. Select an appropriate location for your project and leave the default project name as is (**project_1**).

Select **RTL Project** and check **Do specify not sources** at this time.

Select **xc7z020clg400-1** for your part

Under **Flow Navigator**, click on **IP Catalog**. Right click on the opened window and select **Add Repository**. Navigate to your **Vitis HLS Component > hls > impl > ip** and select it:

2.2) Add IPs to your design
###########################
Under **Flow Navigator**, click on **Create Block Design**. Leave the design name as is (*design_1*). In the newly opened window you can add IPs by clicking on the plus sign.

Add **ZYNQ7 Processing System** and our HLS ip core to your design:

.. image :: image/axi_fp/ip.png

Note that the input and output ports of our HLS IP are all AXI-Stream ports.

Double click on **ZYNQ7 IP** to customize it. In the opened window, double click on **High Performance AXI 32b/64b Slave Parts**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/148617913-pynq7.png

Select and check **S AXI HP0 interface**:

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/2_zynq.jpg

Since AXI-Stream ports do not have address channels, we need to use AXI DMAs to tranfer data between our HLS IP and the DDR memory. One DMA can handle one read and one write channel. Therefore, we need to add 2 DMAs to our design. 

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/3_add_dma.jpg

Double click the DMA to configure: uncheck **Enable Scatter Gather** Engine. Both DMAs will need read and write channels.

.. image :: image/axi_fp/dma.png


2.4) Manual connections
#######################

AXI Stream ports need to be connected manually. We start from the ``M_AXIS_MM2S`` port of ``axi_dma_0``. This channel will **read** data from DDR memory and **send** to our HLS IP. Vivado will automatically show you the elegible ports to be connected to.

.. image :: image/axi_fp/connecting.png

The ``S_AXIS_S2MM`` channels will **receive** data from our HLS IP and **write** to DDR memory. They should connected to the output ports. 

Complete all AXI-Stream connections as below:

.. image :: image/axi_fp/connected.png

2.5) Automatic connections
##########################

Now you can leave the rest of the connections to the tool. There should be a highlighted strip on top of your diagram window.

1. Click on **Run Block Automation** to enable the external FIXED_IO and DDR interfaces:

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/7_block_auto.jpg

2. Click on **Run Connection Automation** and select all.

.. image :: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/dma2/8_connect_auto.jpg

3. **IMPORTANT!** you have to click again on **Run Connection Automation**

.. image :: image/axi_fp/auto2.png

At this point, your design should contain 2 AXI-interconnects. One of them connects the M_AXI port of the PS with the S_AXI_LITE ports of the 2 DMAs and our HLS IP. This enables the PS to configure these IPs. Your entire block diagram should look like this:

.. image :: image/axi_fp/bd.png

The other connect the M_AXI ports of the DMAs to the high performance S_AXI port(s) of the PS. DMAs use this channel to perform read and write with the memory.

2.6) Generate bitstream
#########################

Follow the same step as as `lab 1 <https://pp4fpgas.readthedocs.io/en/latest/PYNQ-example.html>`_.

1. Save your design **CTRL+S** or **File > Save Block Design.**

2. Validate your design: **Tools > Validate Design**

3. In Sources, right click on **design_1**, and **Create HDL Wrapper**. Now you should have **design_1_wrapper.v**

4. Generate bitstream by clicking on **Generate Bitstream** in **Flow Navigator**

After the above steps finish, keep your **project directory > project_1 > project_1.runs > impl_1 > design_1_wrapper.bit** and **project directory > project_1 > project_1.gen > sources_1 > bd > design_1 > hw_handoff > design_1.hwh** for Pynq implementation. You should make sure that the bitstream and the hardware handoff files have the same name.

After changing the HLS source, export the IP again, refresh or upgrade the HLS IP in Vivado, and regenerate the bitstream. Copy the new ``.bit`` and matching ``.hwh`` files to PYNQ before testing the change.

You can close and exit from Vivado tool.

3) Host program
------------------

In this section we use Python to test our design.

3.1) Move your files
####################

Create a new folder in your PYNQ board and move both bitstream and hardware handoff into it.

3.2) Python code
################

Create a new Jupyter notebook and run code in ``./simple_add_float.ipynb`` under the `source code folder <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/axis_fp/demo>`_ to test your design.

You should be able to see all the components of the overlay by checking its IP dictionary

.. code-block :: python3

	ol = Overlay("./design_1.bit")
	ol.ip_dict

In this lab, we are only using ``axi_dma_0``, ``axi_dma_1`` and our HLS IP.

You can check the register map of the HLS IP, and start the IP by writing to the corresponding register:

.. code-block :: python3

	CONTROL_REGISTER = 0x0
	hls_ip.write(CONTROL_REGISTER, 0x1) # AP_START; 0x81 also enables auto-restart
	hls_ip.register_map

The supplied notebook allocates equally sized ``np.float32`` buffers for both inputs and outputs. Keep the receive-before-send order shown below so both output DMAs are ready to accept results. Start the HLS IP again for each new pair of input transfers when using the single-run ``0x1`` control value above.

.. code-block :: python3

	dma0_recv.transfer(output_buffer0)
	dma1_recv.transfer(output_buffer1)
	dma0_send.transfer(input_buffer0)
	dma1_send.transfer(input_buffer1)
	dma0_send.wait()
	dma1_send.wait()
	dma0_recv.wait()
	dma1_recv.wait()

Check the register map of DMAs to find out whether the transfer has finished without error, which is very useful in debugging.

.. code-block :: python3

	dma0.register_map
