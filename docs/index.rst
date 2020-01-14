 .. FIR documentation master file, created by
  sphinx-quickstart on Tue Feb 19 10:03:10 2019. 
	You can adapt this file completely to your liking, but it should at least contain the root `toctree` directive.


Parallel Programming for FPGAs Projects and Labs
===================================================

Parallel Programming for FPGAs is an open-source book aimed at teaching hardware and software developers how to efficiently program FPGAs using high-level synthesis (HLS). The goal is to train people to effectively use HLS tools. The book was developed over many years to serve as a primary reference for UCSD 237C — a hardware design class targeting first-year graduate students and advanced undergraduate students. While writing the book, we developed projects and labs for the students to learn the HLS tools and to build real systems using FPGAs. This serves a general one stop shop for those projects and labs.

2) Vivado Installation 
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

3) PYNQ Setup
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

