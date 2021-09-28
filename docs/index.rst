 .. FIR documentation master file, created by
  sphinx-quickstart on Tue Feb 19 10:03:10 2019. 
	You can adapt this file completely to your liking, but it should at least contain the root `toctree` directive.


Parallel Programming for FPGAs: Projects and Labs
===================================================

`Parallel Programming for FPGAs book <http://kastner.ucsd.edu/hlsbook/>`_ is an open-source book aimed at teaching hardware and software developers how to efficiently program FPGAs using high-level synthesis (HLS). The goal is to train people to effectively use HLS tools. The book was developed over many years to serve as a primary reference for UCSD's 237C — a hardware design class targeting first-year graduate students and advanced undergraduate students. 

While writing the book, we developed projects and labs for the students to learn the HLS tools and to build real systems using FPGAs. This serves a general one stop shop for those projects and labs. The projects and labs have a direct correspondance to the chapters in this book and were written to accompany each other.

The projects and labs use the `Xilinx PYNQ infrastructure <https://github.com/Xilinx/PYNQ>`_ and `Intel's DevCloud <https://software.intel.com/content/www/us/en/develop/tools/devcloud.html>`_ to deploy HLS code onto an FPGA. The Xilinx labs/projects target the `PYNQ-Z2 board <http://www.pynq.io/board.html>`_. Please follow this `link <https://pynq.readthedocs.io/en/latest/getting_started/pynq_z2_setup.html>`_ for the Pynq setup. If needed, it is possible `wirelessly access the Pynq-Z2 <https://www.nengo.ai/nengo-pynq/connect.html#via-a-computer>`_. DevCloud provides access to the tools and FPGAs remotely as described in Lab :ref:`devcloud`

.. toctree::
   :maxdepth: 2
   :hidden:
   
   self
   project1
   project2
   project2.5
   project3
   project4
   project4.5
   project6
   project7
   PYNQ-example
   axidma
   axidma2
   axi4
   interrupts
   microblaze.ipynb
   devcloud

