Lab: AXI4-Burst Mode (m_axi)
============================

Simple example of AXI4-Burst Mode
***********************************

This lab is an example of AXI4 data transfer in burst mode. It takes in a given sample of values and provides the square root. 

1) Vitis HLS: Generating RTL code from C/C++ code
--------------------------------------------------

In this section you learn how to create a project in Vitis HLS, synthesis your code, and generate RTL.

1.1) Download code and create a Vitis HLS project
##################################################

This is the code we will be using:

.. code-block :: c++

	#include "axi4_sqrt.hpp"
	#include <string.h>
	#include <math.h>

	void axi4_sqrt(float *in, float *out, int len)
	{
	#pragma HLS INTERFACE s_axilite port=return bundle=sqrt
	#pragma HLS INTERFACE s_axilite port=len bundle=sqrt
	#pragma HLS INTERFACE m_axi depth=50 port=out offset=slave bundle=output
	#pragma HLS INTERFACE m_axi depth=50 port=in offset=slave bundle=input
	#pragma HLS INTERFACE s_axilite port=in bundle=sqrt
	#pragma HLS INTERFACE s_axilite port=out bundle=sqrt

		float buff[100];
		memcpy(buff, (const float*) in, len * sizeof(float));

		for(int i = 0; i < len; i++)
			buff[i] = sqrt(buff[i]);

		memcpy(out, (const float*) buff, len * sizeof(float));
	}
	
Note that we had to include `string.h` to be able to use `memcpy`. Additionally, we use `memcpy` instead of a for-loop (as used in AXI-streaming) to force Vitis HLS to infer an AXI4-Burst. Sometimes Vitis HLS will not infer this from a for-loop, but will for `memcpy`.

Also note that we had to set the bundles of `s_axilite` ports for `in` and `out` to the same bundle as the `return` port. This is required since Vitis HLS will otherwise assign the `m_axi` ports to a separate interface (instead of a single interface for all variables, which is easier to handle in Jupyter). Please see `this Xilinx docs <https://docs.xilinx.com/r/2020.2-English/ug1399-vitis-hls/Controlling-the-Address-Offset-in-an-AXI4-Interface>`_ page for more information.

Download and unzip `axi4_burst.zip <https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/axi4_burst.zip>`_ that contains the above code. The `.cpp` file in the zip file actually does not match with above code, so please update it with the above code. Generate your project using the provided script.tcl file:

Linux: open a terminal, make sure your environment is set, navigate to streamMul folder, and run the following ::

    $ vitis_hls -f script.tcl

Windows: open vitis_hls command line and run the following ::

    $ vitis_hls -f script.tcl

Now you can open your project in Vitis HLS. It should look like this:

.. image :: https://i.imgur.com/iHkVmWE.png

1.2) Generate RTL code and export it
####################################

Before running C Synthesis, in Vitis HLS, go to the **Solution > Solution Settings**, then under the "General" tab, in `config_interface`, de-select the `m_axi_addr64` option (see screenshot below, specifically the row with the red cross). This is required because 64-bit addresses are used by default when `m_axi`` is used in the pragmas. And in Jupyter with Pynq, it is not clear how to write the values to 64 bit addresses. So de-selecting this option will ensure that 32-bit addresses are used.

.. image :: https://i.imgur.com/o6gpaSv.png

Click on Run **C Synthesis** to generate RTL code. After it is done, you can check your resource utilization and timing report. Your latency is unknown (?) because your loop size (*len*) is a variable.

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq19.png

Note: you can also check the addresses of variables (that you need to write to in Jupyter) in the Synthesis summary under "S_AXILITE Registers".

Now you can export your RTL code by clicking on **Export RTL**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/582121524-pynq3.png

After exporting is done, you can close and exit from Vitis HLS.

2) Vivado: Generating bitstream from RTL code
---------------------------------------------

In this section we import our RTL code from last section, add some required IPs, and generate our bitstream.

2.1) Create a new Vivado project
################################

Open your Vivado tool and create a new project. Select an appropriate location for your project and leave the default project name as is (**project_1**).

Select **RTL Project** and check **Do not specify sources** at this time.

Select **xc7z020clg400-1** for your part:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3090594305-pynq4.png

2.2) Import RTL code
####################

Under **Flow Navigator**, click on **IP Catalog**. Right-click on the opened window and select **Add Repository**. Navigate to your **Vitis HLS project > solution1 > impl > ip** and select it:

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq20.png


2.3) Add IPs to your design
###########################
Under **Flow Navigator**, click on **Create Block Design**. Leave the design name as is (*design_1*). In the newly opened window, you can add IPs by clicking on the plus sign.

Add **ZYNQ7 Processing System** to your design:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3814633603-pynq6.png

Double click on **ZYNQ7 IP** to customize it. In the opened window, double click on **High Performance AXI 32b/64b Slave Parts**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/148617913-pynq7.png

Select and check **S AXI HP0 interface**:

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq21.png

Add the **axi4_sqrt** IP to the design.

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq22.png


2.4) Automatic connections
##########################

1. Click on **Run Block Automation**

2. Click on **Run Connection Automation** and select all. Click OK.

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq23.png

3. Click on **Run Connection Automation** again and select all. Click OK.

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq24.png

This is how the final design should look. Note: in Vivado 2023, it uses AXI Interconnect block instead of AXI SmartConnect, but it works.

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq25.png

2.5) Generate bitstream
#######################

1. Save your design **CTRL+S** or **File > Save Block Design**.

2. Validate your design: **Tools > Validate Design**.

3. In Sources, right click on **design_1**, and **Create HDL Wrapper**. Now you should have **design_1_wrapper**.

4. Generate bitstream by clicking on **Generate Bitstream** in **Program and Debug**.

2.6) Post bitstream Generation
##############################

In sources, expand **design_1_wrapper::design_1_i::design_1::axi4_sqrt_0::design_1_axi4_sqrt_0_0::inst : axi4_sqrt**, double click on **axi4_sqrt_sqrt_s_axi_U** , and note the address for **in_r** , **out_r** , **len** as **0x10** , **0x18** and **0x20** respectively. We need this addresses in our host program. These addresses can also be found in the Vitis HLS C Synthesis summary.

.. image :: https://github.com/KastnerRG/pp4fpgas/raw/master/labs/images/pynq26.png

You can close and exit the Vivado tool.

Copy your **project directory > project_1 > project_1.runs > impl_1 > design_1_wrapper.bit** to your **project directory > project_1** and rename it to **axi4_sqrt.bit**

Copy your **project directory > project_1 > project_1.gen > sources_1 > bd > design_1 > hw_handoff > design_1.hwh** to your **project directory > project_1** and rename it to **axi4_sqrt.hwh**

These files need to have the same name (except for their file extension).

3) Host program
---------------

In this section, we use Python to test our design.

3.1) Move your files
####################

Create a new folder in your PYNQ board and move both **axi4_sqrt.hwh** and **axi4_sqrt.bit** into it.

3.2) Python code
################

Create a new Jupyter notebook and run the following code to test your design:

.. code-block :: python3

	from pynq import Overlay
	from pynq import Xlnk # replace with allocate for Pynq >= 2.7
	import numpy as np

	ol = Overlay('axi4_sqrt.bit')
	sqrt_ip = ol.axi4_sqrt_0 # if you can't find the IP, type 'ol.' and hit Tab to see what options are available
	
.. code-block :: python3

	length = 40
	inpt = Xlnk().cma_array(shape=(length,), dtype=np.float32)
	outpt = Xlnk().cma_array(shape=(length,), dtype=np.float32)
	a = [i*i for i in range(length)]
	np.copyto(inpt, a)
	soft_op = np.sqrt(inpt)

	sqrt_ip.write(0x20, length)
	sqrt_ip.write(0x10, inpt.physical_address)
	sqrt_ip.write(0x18, outpt.physical_address)
	sqrt_ip.write(0x00, 1)

	print("Hardware Output", "Software Output \n")
	for i in range(length):
	    print(outpt[i], "\t\t  ", soft_op[i])











