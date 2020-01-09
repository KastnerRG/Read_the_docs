 .. FIR documentation master file, created by
  sphinx-quickstart on Tue Feb 19 10:03:10 2019. 
	You can adapt this file completely to your liking, but it should at least contain the root `toctree` directive.


CSE237C- Validation and Testing of Embedded Systems
===================================================

1)Introduction
--------------

This course is designed to help you be familiar with High Level Synthesis and concepts pertaining to it. It consists of 4 projects and 4 Labs which will help you implement the HLS concepts you have learnt during the class. It will also aims at helping the stduents to learn Vivado flow and control the FPGA using python notebooks on the PYNQ.

2)Vivado Installation 
----------------------

Below are the required steps which help in installing vivado

* Vivado Design Suite Installation
 
    1. Go to: http://www.xilinx.com/support/download/
    2. Download the 2019.1 Web Install Thin Client (if you have fast internet). 
    3. You will need to make a username and password at the Xilinx website.
    4. “Vivado Design Suite - 2019.1 System Edition” for your platform. Both Linux or Windows versions are available, but we highly recommend that you use Windows.
    5. At the end of the installation, it will ask about a license. Click on “Manage License Search Paths” on the left (under “Manage License”) and enter in 2100@cselm2.ucsd.edu into the XILINXD_LICENSE_FILE field.
 
* License Settings (if not set above):
    1. Go to Start->Xilinx Design Tools
    2. Open Vivado 2019.1 -> Manage Xilinx License 
    3. Open Manage Xilinx License Search Paths
    4. Set the XILINXD_LICENSE_FILE to 2100@cselm2.ucsd.edu

3)PYNQ Setup
------------

Please follow this `link <https://pynq.readthedocs.io/en/latest/getting_started/pynq_z2_setup.html>`_ for the pynq setup.

.. toctree::
   :maxdepth: 2
   :hidden:
   
   self
   project1
   project2
   project3
   project4
   PYNQ-example
   axidma
   axidma2
   pl-ps_interrupt
   Lab5.ipynb

