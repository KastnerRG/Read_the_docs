.. FM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: FM Demodulator
=========================

1) Introduction
---------------
In this project we use the `RTL2832 <https://www.rtl-sdr.com/tag/rtl2832/>`_ RF tuner to sample RF signals and will build a FM Demodulator and implement it on the Pynq Board.

2) Project Goal
---------------

In this project, you will use your knowledge from previous projects to implement an FM Demodulator in programmable logic. The project is divided into two parts.

In the first part, you develop different functions to implement the `scikit-dsp-comm mono_FM <https://github.com/mwickert/scikit-dsp-comm/blob/master/sk_dsp_comm/rtlsdr_helper.py#L1842>`_ Demodulator in Vivado HLS. This FM Demodulator consists of a linear filter, downsampler, and a discriminator.

The second part is to integrate the Demodulator onto the Pynq Board. You should be able to listen to local FM radio channel using your MonoFM implementation in programmable logic.

3) Materials
------------

`Download <https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/mono_fm.zip>`_.

This contains a Python notebook which explains the working of a Mono FM Demodulator. You can view the contents of the notebook :doc:`here<rtl2832>`.

For this project the following will not be provided:

* ~.cpp - The place where you write synthesizable code
* ~.h - header file with various definitions that may be useful for developing the code 
* ~test.cpp - testbench

You will have to build the entire project from scratch

4) Design Instructions
----------------------
The FM Demodulator has 3 main parts: downsampler, linear filter and discriminator.

**downsampler**
##########
This part consists of a straight forward downsampler. We have to downsample by a factor of N, that is keep every Nth sample. The implementation of downsampler can be found `here <https://github.com/mwickert/scikit-dsp-comm/blob/master/sk_dsp_comm/sigsys.py#L2673>`_.

**linear filter**
################
Build a linear filter whose function is implemented as a direct II transposed structure.

This means that the filter implements:

.. math::

   a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[M]*x[n-M] 
                         - a[1]*y[n-1] - ... - a[N]*y[n-N]
   
More information about the linear filter implementation can be found `here <https://github.com/scipy/scipy/blob/v1.5.4/scipy/signal/signaltools.py#L1719-L1909>`_.

**discriminator**
################
To demodulate FM we require a discriminator circuit, which gives an output which is proportional to the input frequency deviation. 


.. code-block :: python3

   def discrim(x):
    """
    function disdata = discrim(x)
    where x is an angle modulated signal in complex baseband form.
    
    Mark Wickert
    """
    X=np.real(x)        # X is the real part of the received signal
    Y=np.imag(x)        # Y is the imaginary part of the received signal
    b=np.array([1, -1]) # filter coefficients for discrete derivative
    a=np.array([1, 0])  # filter coefficients for discrete derivative
    derY=signal.lfilter(b,a,Y)  # derivative of Y, 
    derX=signal.lfilter(b,a,X)  #    "          X,
    disdata=(X*derY-Y*derX)/(X**2+Y**2)
    return disdata

The above code is the `scikit-dsp-comm implementation <https://github.com/mwickert/scikit-dsp-comm/blob/master/sk_dsp_comm/rtlsdr_helper.py#L1825>`_ of an FM baseband discriminator. 

To understand the operation of *discrim()* start with a general FM modulated signal and obtain the complex envelope:

.. image:: https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/in_signal.png

The complex envelope is:

.. image:: https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/complex_env.png

A frequency discriminator obtains the derivative of the modulated angle:

.. image:: https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/phi.png

And its derivative is:

.. image:: https://bitbucket.org/akhodamoradiUCSD/237c_data_files/downloads/dphi.png

**Optimization Guidelines**

* You must always use a clock period of 10 ns.

* The latency for demodulation should be less than the sample time; i.e. less than 1 second for 1 second sample time.


5) PYNQ Demo
------------

This project is different from your previous projects in the sense that it has to achive a *real time* performance, with a processing time less than the sampling time. You are highly encouraged to modify the code to achieve a better performance and observe the throughput by changing the way you transmit data between PS and PL. Make use of the "RTL 2832" USB tuner in-order to receive the input RF Samples.


6) Submission Procedure
-----------------------

You have to submit your code (and only your code, not other files, not HLS project files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to only import your source file and directly synthesize it.

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "mono_fm" at the top-level. This folder must be organized as follows (similar to previous projects):

**Contents:**

* **Report.pdf**

* Folder **fm-demodulator**

  - Source code (*.cpp, *.h, *.tcl only) and reports (.rpt and .xml).
  
* Folder **Demo**

  - .bit and .hwh files
  - FM.ipynb host file

**Report:** For this project, you must submit a report with 1 page for each function from section 4. You may add figures, diagrams, tables, or charts to describe your architectures with a short paragraph explaining them. No questions; no answers. Just explain your design. We will check if (1) your final FM Demodulation functions are functionally correct (they pass their test benches) and (2) achieves target latency. The report will help us to understand your design. You also can use this report to explain your work for bonus part (check the grading section).

7) Grading Rubric
-----------------

**30 points:** Functionally correct design. You will get full credit if we are able to build your blocks without any effort. You need to report the throughput of the final design.

**60 points:** Pynq Demo. You will get full credit for clear audio output and an RMSE less than 1e-6.

**10 points:** Report.

**Bonus:** Integrate your design with the base overlay to make use of audio instance on the Pynq Board. More information about the audio module on Pynq Z2 can be found `here <https://pynq.readthedocs.io/en/v2.3/pynq_libraries/audio.html>`_ and `here <https://pynq.readthedocs.io/en/v2.3/pynq_package/pynq.lib/pynq.lib.audio.html#pynq-lib-audio>`_. Detailed description of the BaseOverlay can be found  `here <https://pynq.readthedocs.io/en/v2.3/pynq_overlays/pynqz2/pynqz2_base_overlay.html>`_.
