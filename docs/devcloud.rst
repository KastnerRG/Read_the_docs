.. _devcloud:

Lab: DPC++ on Intel DevCloud
====================

Getting Started
********************

To complete this lab, you need access to Intel DevCloud. You can log into DevCloud using `JupyterLab <https://jupyter.oneapi.devcloud.intel.com/hub/login?next=/lab/tree/Welcome.ipynb?reset>`_ It is also possible to `access DevCloud using a command-line interface via ssh <https://devcloud.intel.com/oneapi/documentation/connect-with-ssh-linux-macos/>`_.

Resources
************

oneAPI and DPC++ are open source and there are many resources available online to help you start your project:

* `oneAPI <https://www.oneapi.com/>`_

* `Data Parallel C++ Essentials Jupyter Modules <https://jupyter.oneapi.devcloud.intel.com/hub/login?next=/lab/tree/oneAPI_Essentials/Welcome.ipynb?reset>`_

* `Developer Reference <https://software.intel.com/en-us/oneapi>`_

* `DPC++ book <https://tinyurl.com/book-dpcpp>`_

* `oneAPI Programming Guide <https://www.intel.com/content/www/us/en/develop/documentation/oneapi-programming-guide/top.html>`_

* `oneAPI FPGA Optimization Guide <https://software.intel.com/content/www/us/en/develop/documentation/oneapi-fpga-optimization-guide/top.html>`_

* `SYCL Specifications <https://www.khronos.org/sycl/>`_


Instructions
************

This section walks through some example matrix multiplication code to illustrate how to use dpc++ and the DevCloud environment. This requires access to DevCloud via JupyterLab.

Create a Project in JupyterLab
####################

Start a JupyterLab session and click the + sign to open the *Launcher*.

.. image :: https://i.imgur.com/UmK4kbY.png


Use `oneapi-cli <https://github.com/intel/oneapi-cli>`_ to create the baseline matrix multiplication project. Open a Terminal and launch the tool:

.. code-block :: python

 $ oneapi-cli

This tool has a basic interface that allows you to choose a project based on its various templates. Perform the following:

1) Select *Create a project*

2) Select *cpp*

3) Select *Matrix Multiplication* under *Get Started*

4) Leave *Directory* and *Project Name* with their default paramaters and select *Create*

This creates several files inside the *matrix_mul* folder:

.. image :: https://i.imgur.com/n2q6v8C.png

The source file is in the *src* folder and the *README* provides instructions to compile the code.

Use the terminal to compile and run your code. Be sure to use the Jupyter terminal; SSH doesn't seem to work for this operation:

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


Modify the Project for FPGA
###################

Open the file *src/matrix_mul_dpcpp.cpp*.

Line 55 uses the default_selector for the hardware device. Modify the code to use the FPGA emulator by performing the following:

Include a header file by adding the line

.. code-block :: c++

  #include "CL/sycl/INTEL/fpga_extensions.hpp"

Modify the queue initialization:

.. code-block :: c++

  ext::intel::fpga_emulator_selector device_selector;
  queue q(device_selector, dpc_common::exception_handler);


Re-compile and re-run the code. The device should now be an FPGA emulator.

.. code-block :: python

	$ ./matrix_mul_dpc
	Device: Intel(R) FPGA Emulation Device
	Problem size: c(150,600) = a(150,300) * b(300,600)
	Result of matrix multiplication using DPC++: Success - The results are correct!


Generate the FPGA Report
########################################

Once your code is functionally correct, synthesize it to check your design's performance and resource utilization.

Perform high-level synthesis and create the report using ``dpcpp``:

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

.. image :: image/readable-gemm-resources.png

Analyzing the Report
########################################

Take a deeper look at the report. Under *Views*, open *System Viewer*. The ``Kernel System`` has four items: ``Global memory`` is the interface to the off-chip memory. ``a_init`` and ``b_init`` are kernels that initiate the arrays in global memory. ``c_calc`` performs the matrix multiply. The load operations from arrays ``a`` and ``b`` occur in ``c_calc.B8``, the multiply-accumulate operations are in ``c_calc.B2``, and the store operation into array c is in ``c_calc.B7``. The load and multiply-accumulate operations are from line 125.

.. image :: image/mm-kernel-view.png

Click the menu  *Throughput Analysis* and then the item *Loops Viewer*. This provides detailed information for each step of the process in the kernels:

.. image :: image/mm-base-loop-viewer.png

The **Load Store Unit (LSU) Style** for the **LD** operations is shown as **Burst-coalesced cached**. Intel oneAPI DPC++ compiler generates different types of LSUs to manage data transfer between device and host. The compiler uses the *Burst/coalesced* LSU by default. In *Burst/coalesced* mode, the compiler optimizes for buffering contiguous memory requests for the *largest possible burst*. We can change the LSU type to achieve a lower latency for the load operations. This and other optimizations are part of the :doc:`Matrix Multiplication Project <project6>`.
