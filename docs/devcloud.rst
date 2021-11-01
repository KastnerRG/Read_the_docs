.. _devcloud:

Lab: DPC++ on Intel DevCloud
====================

Getting Started
********************

To complete this lab, you need access to Intel DevCloud. `Log in to DevCloud <https://devcloud.intel.com/oneapi/>`_ and navigate to Get Started.

DevCloud provides several ways to access the software and hardware. We recommend setting up both JupyterLab and SSH since each has benefits:

* **JupyterLab** provides visual interfaces to navigate through your files and edit your code.

* **SSH** gives a simple command-line interface to the resources. You also can use SSHFS and SCP to access and transfer your files to/from the cloud. We strongly recommend Linux for this lab.

.. image :: https://i.imgur.com/Z2bRl46.png

We suggest reviewing modules 1, 2, and 3 of *Introduction to oneAPI* and *Essentials of Data-Parallel C++*, available on the *Get Started* page.

Resources
************

oneAPI and DPC++ are open source and there are many resources available online to help you start your project:

* `oneAPI <https://www.oneapi.com/>`_

* `Developer Reference <https://software.intel.com/en-us/oneapi>`_

* `DPC++ book (chapters 1 - 4) <https://tinyurl.com/book-dpcpp>`_

* `oneAPI Programming Guide <https://software.intel.com/sites/default/files/oneAPIProgrammingGuide_3.pdf>`_

* `oneAPI FPGA Optimization Guide <https://software.intel.com/content/www/us/en/develop/documentation/oneapi-fpga-optimization-guide/top.html>`_

* `Example Codes <http://tinyurl.com/oneapimodule?1>`_

* `SYCL Specifications <https://www.khronos.org/registry/SYCL/specs/sycl-1.2.1.pdf>`_


1) Instructions
---------------

This section walks through some example matrix multiplication code to illustrate how to use dpc++ and the DevCloud environment. This requires access to JupyterLab (on the cloud) and a SSH connection to your machine.

1.1) Create a Project in JupyterLab
####################

	* Start a JupyterLab session.

	* Click the + sign to open the *Launcher*.

	.. image :: https://i.imgur.com/UmK4kbY.png


	* Use `oneapi-cli <https://github.com/intel/oneapi-cli>`_ to create the baseline matrix multiplication project.

	* Open a *Terminal* and launch the tool:

		.. code-block :: python

			$ oneapi-cli

	* This tool has a basic interface that allows you to choose a project based on its various templates. Perform the following:

		1) Select *Create a project*

		2) Select *cpp*

		3) Select *Matrix Multiplication* under *Get Started*

		4) Leave *Directory* and *Project Name* with their default paramaters and select *Create*

This creates several files inside the *matrix_mul* folder:

.. image :: https://i.imgur.com/n2q6v8C.png

The source file is in the *src* folder and the *README* provides instructions to compile the code.

	* Use the terminal to compile and run your code. Be sure to use the Jupyter terminal; SSH doesn't seem to work for this operation:

		.. code-block :: python

			$ cd matrix_mul
			$ make all
			$ make run

The output should look like this:

.. code-block :: python

	$ ./matrix_mul_dpc
	Device: Intel(R) Xeon(R) Gold 6128 CPU @ 3.40GHz
	Problem size: c(150,600) = a(150,300) * b(300,600)
	Result of matrix multiplication using DPC++: Success - The results are correct!

It shows the device name used for the matrix multiplication, the matrices' size, and the testbench result.


1.2) Modify the Project for FPGA
###################

Open the file *src/matrix_mul_dpcpp.cpp*.

Line 55 uses the default_selector for the hardware device. See Section 4.3.8 of the `Programming Guide <https://software.intel.com/sites/default/files/oneAPIProgrammingGuide_3.pdf>`_ for more details.

Modify the code to select a FPGA device. This can be accomplished in two steps:

# Include a header file by adding the line:

    .. code-block :: c++
      #include "CL/sycl/INTEL/fpga_extensions.hpp"

# Modify the queue initialization:

    .. code-block :: c++
      ext::intel::fpga_emulator_selector _device;
      queue q(_device, dpc_common::exception_handler);

Re-compile and re-run the code. The device should now be an FPGA emulator.

.. code-block :: python

	$ ./matrix_mul_dpc
	Device: Intel(R) FPGA Emulation Device
	Problem size: c(150,600) = a(150,300) * b(300,600)
	Result of matrix multiplication using DPC++: Success - The results are correct!


1.3) Generate the FPGA Report
########################################

Once your code is functionally correct, synthesize it to check your design's performance and resource utilization.

Perform high level synthesis and create the report using *dpcpp*:

.. code-block :: python

	$ cd src
	$ dpcpp -fintelfpga matrix_mul_dpcpp.cpp -c -o matrix_mul_dpcpp.o
	$ dpcpp -fintelfpga matrix_mul_dpcpp.o -fsycl-link -Xshardware

These commands do not perform a full synthesis, i.e., they do not create an FPGA bitstream. They perform high level synthesis and simulate the FPGA design on a processor. This enables estimations of the design performace and resource usage. To generate a bitstream, remove ``-fsycl-link*``. Note that generating a bitstream can take a *long* time and thus should only be done sparingly, i.e., when the design optimizations are finalized.

The report is an HTML file in ``matrix_mul_dpcpp.prj/reports``. At the time of writing this tutorial, JupyterLab has issues with some combinations of operating systems and web browsers. If the reports are not rendering, make sure to "Trust" the HTML. Safari seems to have the best compatibility with this, with Firefox coming second, but neither is guaranteed to work. If they still do not render, use SCP or SSHFS to copy or mount your files (incuding the *lib* folder from which the report draws its components) to your local drive, then open the report locally.

The *report* provides an overview of the design performance. Open *report.html*, click *Summary* button, click **Compile Estimated Kernel Resource Utilization Summary** in the *Summary Content* pane.

This shows the resource usages for the different kernels and other system resources.

.. image :: image/dpcpp-gemm-resources.png

The kernel names look almost random as these compiler generated. To make the report readable modify the code to name to the kernels:

Add three classes in your code as follows:

.. code-block :: c++

	class a_init;
	class b_init;
	class c_calc;

Now you can assign each class to one of your kernels. For example, *a_init* will be assigned to the kernel that initializes buffer *a* as follows:

.. code-block :: c++

	h.template parallel_for<a_init>(range(M, N), [=](auto index) {

Change the other kernels in a similar manner. Repeat the steps to generate a new report. Do not forget to remove the old files before generating a new report:

.. code-block :: python

	$ rm -rf matrix_mul_dpcpp.prj/ matrix_mul_dpcpp.o matrix_mul_dpcpp.a
	$ dpcpp -fintelfpga matrix_mul_dpcpp.cpp -c -o matrix_mul_dpcpp.o
	$ dpcpp -fintelfpga matrix_mul_dpcpp.o -fsycl-link -Xshardware

This will make your report more readable:

.. image :: https://i.imgur.com/u8rjftn.png

2) Analyzing the Report
---------------------------

Let's take a deeper look at the report. Under *System Viewer*, open *Graph Viewer*. On the open page, select *System* under *Graph List*.

This graph shows that your code has three kernels: *a_init* and *b_init* are simple kernels that store values into the global memory. *c_calc* has two blocks: B2 calculates the matrix multiply, and B1 stores the results in the global memory.

Now let's explain the red arrows. Click on the red circle titled *LD (x2)* inside *c_calc.B2*. These two LD operations correspond to line 126 in the source code. They have a latency of 223 cycles to read from DDR memory, which is the bottleneck for the loop iteration.

.. image :: https://i.imgur.com/F5Y9jYm.png

Check the results in *Loop Analysis*: under *Throughput Analysis*, select *Loop Analysis* and click on *c_calc.B2*:

.. image :: https://i.imgur.com/vXlEsMd.png

The *Schedule Viewer* under *System Viewer* provides detailed information for each step of the process in the kernels:

.. image :: https://i.imgur.com/cJmQUhZ.png

Details for the load operation **LD** is available by clicking on their *yellow* bar.

.. image :: https://i.imgur.com/IgN1CVJ.png

The **Load Store Unit (LSU) Style** for the **LD** operations is shown as **Burst-coalesced cached**. Intel oneAPI DPC++ compiler generates different types of LSUs to manage data transfer between device and host. The compiler uses the *Burst/coalesced* LSU by default. In *Burst/coalesced* mode, the compiler optimizes for buffering contiguous memory requests for the *largest possible burst*. We can change the LSU type to achieve a lower latency for the load operations. More details are available at `Intel® oneAPI DPC++ FPGA Optimization Guide <https://software.intel.com/content/www/us/en/develop/download/oneapi-fpga-optimization-guide.html>`_.
