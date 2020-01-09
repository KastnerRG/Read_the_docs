
Lab 2
======

In this example we implement :math:`f(x) = 2x` as an IP on PYNQ.

1) Vivado HLS: C/C++ to RTL
---------------------------

In this section, you will write your code in C/C++, test it, and convert it to RTL using Vivado HLS.

1.1) Write your code
~~~~~~~~~~~~~~~~~~~~

Open Vivado HLS, create a new project, and name it **pynq_mul**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq1.png

Set top function name to **mul_test**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq2.png

Do not add any files to your project and proceed to **part selection** and select **xc7z020clg400-1**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq3.png

In **Explorer** section, right click on **Source**, select **New file** and create **mul_test.cpp**. Complete the body of **mul.cpp** as following:

.. code-block:: c++

  void mul_test(int* out, int in){
	*out = 2*in;
  }

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

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq4.png

1.2) Test your code
~~~~~~~~~~~~~~~~~~~

Run C simulation and make sure your code passes your test bench.

1.3) Set port types
~~~~~~~~~~~~~~~~~~~

Make sure that **mul_test.cpp** is open. Open **Directive** on right side and set all the ports to **s_axilite** by right clicking on available options in **Directive** window.

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq5.png

1.4) Synthesis and export your design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run C Synthesis and after finished, click on **export RTL** and export your design.

At this point, you can exit and close Vivado HLS.

2) Vivado: RTL to bitstream
---------------------------

In this section, you will import your RTL code to Vivado and generate a bitstream.

2.1) Create a new project
~~~~~~~~~~~~~~~~~~~~~~~~~

Open Vivado and create a new project and Name your project as **mul_test**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq6.png

Select **RTL Project** and check **Do not specify sources at this time**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq7.png

Set default part to **xc7z020clg400-1**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq8.png

Under **IP Integrator**, click on **Create Block Design**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq9.png

2.2) Import your design
~~~~~~~~~~~~~~~~~~~~~~~

Under **Project Manager**, click on **IP Catalog**. Right click inside the newly open 'IP Catalog' tab and select **Add Repository**. In the open window navigate to your Vivado HLS project folder and select **<pass_to_vivado_hls_folder>\solution1\impl\ip**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq10.png

In **IP Catalog** search for **mul_test**, double click on it and add it to your block design

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq11.png

2.3) Add connections
~~~~~~~~~~~~~~~~~~~~

Go back to **IP Catalog** and add **ZYNQ7 Processing System** to your block design.

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq12.png

Your diagram should look like the following:

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq13.png

On top of **Diagram** window, first click and complete **Run Block Automation** and then **Run Connection Automation** with default settings. Your diagram should change and show connections and a couple of extra IPs:

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq14.png

2.4) Generate bitstream
~~~~~~~~~~~~~~~~~~~~~~~

In **Sources**, right click on **design_1** and select **Create HDL Wrapper**

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq15.png

Under **Project Manager**, click on **Generate Bitstream** to build .bit and .tcl files

2.5) Bitstream, tcl, and addresses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before closing Vivado, we need to note our IP and its ports addresses:

Under **Sources**, open **mul_test_mul_io_s_axi.v**, scroll down and note addresses for in and out ports. We need these addresses for our host program.

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq16.png

Under **Address Editor** note IP's address

.. image:: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq17.png

3) PYNQ board and Host program
------------------------------

Using SMB or SCP, copy **design_1_wrapper.bit** and **design_1_wrapper.tcl** from **vivado_project_path\mul_test.runs\impl1** to your PYNQ board at **/home/xilinx/jupyter_notebooks/mul_test**.

Open a new Notebook and run the following code to test your IP

.. code-block:: python

  from pynq import Overlay
  from pynq import MMIO

  ol = Overlay("/home/xilinx/jupyter_notebooks/mul_test/design_1_wrapper.bit")
  ol.download()

  mul_ip=MMIO(0x43C00000, 0x10000)

  inp = 5

  mul_ip.write(0x18, inp)
  print("input:", mul_ip.read(0x18)) 
  mul_ip.write(0x00, 1)
  print("output:", mul_ip.read(0x10)) 


