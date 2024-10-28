
Lab: Pynq Memory Mapped IO (s_axilite)
=====================================

This lab describes how to use Pynq to develop an application on the Zynq SoC. The application performs a simple hardware accelerated function on the programmable logic. We first create the IP core that performs the function :math:`f(x) = 2x` using high level synthesis. We synthesize it to the programmable logic using the Vivado tools.  Using the PYNQ infrastructure, we talk to the IP core from ARM processor using memory mapped I/O. We develop a Pynq notebook that sends data to the IP core, executes the core, and receives the computed results. 

0) Vivado Design suite installation
---------------------------

Check `here <https://kastner.ucsd.edu/ryan/vivado-installation/>`_ for installation and UCSD license server guide, though you probably would not need the license server for the projects in this course.

We need Vitis HLS for C synthesis and generating the RTL, and Vivado for FPGA prototyping and generating the bitstream. Vitis is primarily for firmware design, thus not required.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/install0.png

Select Standard edition.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/install1.png

To save disk space, you do not need to install the simulation dependencies for all supported devices since we are only using PYNQ-Z2.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/install2.png

The following tutorials are for pynq-z2 board. The steps are very relatable, though not exactly the same, for Kria boards. Please refer to section 3 if you are using a Kria board.

1) Vitis HLS: C/C++ to RTL
---------------------------

In this section, you will write your code in C/C++, test it, and convert it to RTL using Vitis HLS.

1.1) Write your code
~~~~~~~~~~~~~~~~~~~~

Open Vitis HLS, create a new project, and name it **pynq_mul**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq27.png

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq28.png

Set top function name to **mul_test**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq29.png

Do not add any files to your project and proceed to **part selection** and select **xc7z020clg400-1**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq30.png

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq31.png

In **Explorer** section, right click on **Source**, select **New file** and create **mul_test.cpp**. Complete the body of **mul_test.cpp** as following:

.. code-block:: c++

  void mul_test(int* out, int in){
	*out = 2*in;
  }

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq32.png

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq33.png


Create a test bench file by right clicking on **Test Bench** in **Explorer** section and create a new file named **mul_tb.cpp**. Complete the body of this file as following:

.. code-block:: c++

  #include <iostream>

  using namespace std;

  void mul_test(int* out, int in);

  int main(int argc, char *argv[]){
	int x=5;
	int y;
	mul_test(&y, x);
	if(y!=2*x){
		cout << "Test Failed: output(" << y << ") is not equal to 2x" << x << endl;
	}else{
		cout << "Test Passed" << endl;
	}
	return 0;
  }

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq34.png

1.2) Test your code
~~~~~~~~~~~~~~~~~~~

Run C simulation and make sure your code passes your test bench. 

1.3) Set port types
~~~~~~~~~~~~~~~~~~~

You can set the ports with GUI. Make sure that **mul_test.cpp** is open. Open **Directive**. In the directive window, right click on the the testbench module itself (in our case, mul_test), and select **Modify Directive** (or **Insert Directive**). In the drop down, select **INTERFACE** and set all the ports to **s_axilite** by right clicking on available options. Repeat the same for all its ports (right click on **out** and **in**). In this example, you should configure the ports for 3 times. 

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/0.png

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/1.png

Carefully check your directive tab with the picture below after setting your ports. Make sure that **return**, **out** and **in** ports are all set to s_axilite.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/2.png

An alternate (and better) way of setting the ports is by making HLS pragma declerations in mul_test.cpp. Simply add 3 lines of commands, and you don't have to go through the steps with GUI above.

.. code-block:: c++

  void mul_test(int* out, int in){
	#pragma HLS INTERFACE mode=s_axilite port=return
	#pragma HLS INTERFACE mode=s_axilite port=in
	#pragma HLS INTERFACE mode=s_axilite port=out
	*out = 2*in;
  }

1.4) Synthesis and export your design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run C Synthesis. After the synthesis is complete, you should see the following synthesis summary report-

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/3.png

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/4.png

and after finished, click on **export RTL** and export your design.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/5.png

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/6.png

At this point, you can exit and close Vitis HLS.

2) Vivado: RTL to bitstream
---------------------------

In this section, you will import your RTL code to Vivado and generate a bitstream.

2.1) Create a new project
~~~~~~~~~~~~~~~~~~~~~~~~~

Open Vivado and create a new project and Name your project as **pynq_mul**

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/10.png

Select **RTL Project** and check **Do not specify sources at this time**

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/11.png

Set default part to **xc7z020clg400-1**

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/12.png

Under **IP Integrator**, click on **Create Block Design**

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/13.png

2.2) Import your design
~~~~~~~~~~~~~~~~~~~~~~~

Under **Project Manager**, click on **IP Catalog**. Right click inside the newly open 'IP Catalog' tab and select **Add Repository**. In the open window navigate to your Vivado HLS project folder and select **<path_to_vivado_hls_folder>/solution1/impl/ip**

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/14.png

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/15.png

You can see **Mul_test** under **IP Catalog**.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/16.png

Click **Open block design**, then click **+**, add **Mul_test** IP block into our block design.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/17.png


2.3) Add connections
~~~~~~~~~~~~~~~~~~~~

In the same window, search for "zynq" and add **ZYNQ7 Processing System** to your block design.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/18.png

Your diagram should look like the following:

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/19.png

On top of **Diagram** window, first click and complete **Run Block Automation** and then **Run Connection Automation** with default settings. Your diagram should change and show connections and a couple of extra IPs:

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/20.png

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/21.png

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/22.png

2.4) Generate bitstream
~~~~~~~~~~~~~~~~~~~~~~~

In **Sources**, right click on **design_1** and select **Create HDL Wrapper**

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/23.png

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/24.png

Under **Program and Debug**, click on **Generate Bitstream** and follow instructions to complete synthesis, implementation and bitstream generation.


2.5) Bitstream, .hwh, and addresses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before closing Vivado, we need to note our IP and its ports addresses. 

Under **Sources**, open **mul_test_control_s_axi.v** (the exact name may vary across different versions of Vivado), scroll down and note addresses for in and out ports. We need these addresses for our host program.

In the example below for the streamMul, the addresses to pay attention to are 0x00 (control bus ap_ctrl), 0x10 (output), and 0x20 (input). These are the addresses you will need to use to write data to the fabric from the ARM core, start the fabric to run your design and generate your outputs, and then read your outputs from the fabric into the ARM core on the Pynq board.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/25.png

Under **Address Editor** note IP's address

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/26.png

3) PYNQ board and Host program
------------------------------

Download an appropriate image for your board from `here <http://www.pynq.io/board.html>`_ and write it to your micro SD Card (`PYNQ-Z2 setup instructions <https://pynq.readthedocs.io/en/latest/getting_started/pynq_z2_setup.html>`_). It is recommended to use a dedicated software, e.g. Win32 Disk Imager to burn the .img file to the SD card instead of a simple copy-paste operation, if you find the board cannot booted properly. If you set the jumpers correctly, the boot process should not take more than **a few minutes**.

Use the ethernet cable to connect the board to your machine, and set the static address as stated in the `PYNQ-Z2 tutorial <https://pynq.readthedocs.io/en/latest/getting_started/pynq_z2_setup.html>`_. Connect the JTAG port on the board with your machine using MicroUSB line, and use serial communication software (like PuTTY or Serial Port Unility) to access the command-line-tools (The picture below is for demo only, you don't need to run those commands). This is especially useful for fixing Linux-related issues of the board.

.. image:: https://github.com/KastnerRG/Read_the_docs/raw/master/docs/image/lab0_screenshot/ubuntu_config.png

You can access jupyter notebook through the ipv4 address via a web browser. Create a new folder and notebook. Upload **design_1_wrapper.bit** from **vivado_project_path/pynq_mul.runs/impl1** and copy **design_1.hwh** from **vivado_project_path/pynq_mul.gen/sources_1/bd/design_1/hw_handoff** to the folder you just created in Jupyter.

Make sure the .bit file and the .hwh file have the same name. In this case, we name them "design_1_wrapper.bit" and "design_1_wrapper.hwh".

In the notebook, run the following code to test your IP

.. code-block:: python

	from pynq import Overlay
	from pynq import MMIO

	ol = Overlay("./design_1_wrapper.bit") # designate a bitstream to be flashed to the FPGA
	ol.download() # flash the FPGA

	mul_ip = MMIO(0x40000000, 0x10000) # (IP_BASE_ADDRESS, ADDRESS_RANGE), told to us in Vivado
	inp = 5 # number we want to double

	mul_ip.write(0x20, inp) # write input value to input address in fabric
	print("input:", mul_ip.read(0x20)) # confirm that our value was written correctly to the fabric
	mul_ip.write(0x00, 1) # set ap_start to 1 which initiates the process we wrote to the fabric
	print("output:", mul_ip.read(0x10)) # read corresponding output value from the output address of the fabric 

4) Kria board
-------------
If you are working with a Kria board, there are several necessary changes you have to make. Instead of selecting **xc7z020clg400-1** as the part or **pynq-z2** as the board, you will have to select **xck26-sfvc784-2LV-c** as the part or select **Kria KV260 Vision AI Starter Kit SOM** as the board. This is necessary both for **Vitis HLS** and **Vivado**. As the EDA tools must know what hardware they are targeting. The hardware must also match the board we are eventually using. If the bitstream and hwh generated by Vivado (in which the board is specified) is used in a different kind of board, the pynq software system will have trouble recognizing it.

In Vivado, the steps for adding IPs are the same, but Kria has a different PS (processing system, the ARM core on board) with pynq-z2. In "Add IP" window, select **Zynq Ultrascale+ MPSoC** instead of **ZYNQ7 Processing System**.

Then follow the green designer assistance and let the tool do "block automation" and "connection automation". You probably have to run connection automation twice. Your block diagram should look like this (from project 2: CORDIC):

Note that there should be no ports named x, y, r, theta, as they all become some address in the s_axi_control bus.

You should also be able to find the module named control_s_axi_U under the file tree, and locate the address as the lab tutorial.

Basics of FPGA & PS-PL interaction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
At architecture level, an FPGA is divided into 2 domains: PS and PL.

PS, or processing system, is an Arm core, in charge of controlling everything, managing memory, creating clock, etc. Consider this as the CPU. The big IP block in your diagram starting with "Zynq" is the PS.

PL, or programming logic, is basically everything else. The most important one is the IP you just designed in Vitis HLS, an efficient hardware dedicated for some task, or usually referred to as the "accelerator". Some are auxiliary modules that are typically auto-managed by tools. 

The accelerator cannot access data directly. The PS has to move the data between the memory and your accelerator. Thus the accelerator and the PS must be connected by some on-chip bus protocol. The easiest protocol is axi_lite. If you wish to put an accelerator on an FPGA, you must specify its port type during the design phase in Vitis HLS. Check Step 1.3 for the commands. 
