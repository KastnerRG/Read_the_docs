.. FM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: FM Demodulator
=========================

1) Introduction
---------------
The project develops a mono FM receiver that can be used to listen to the radio through your Pynq board. We use the `RTL2832 <https://www.rtl-sdr.com/tag/rtl2832/>`_ software defined as to sample RF signals.

2) Project Goal
---------------
Your overall goal is to perform real-time demodulation. This means that the demodulation of 1 second of sampled data takes less than one second including the I/O time to transfer data to/from the demodulator on the programmable logic.

The first goal is to use your knowledge from previous projects to implement an FM demodulator IP core. The second goal is to develop an interface between the hardware-accelerated FM demodulator and the Jupyter notebook. The end goal is to perform real-time FM demodulation which requires careful optimization in both the hardware implementation of the demodulator and the interfacing between the processing system (PS) and programmable logic (PL).

The project is divided into two parts.

1) In the first part, you develop a hardware-accelerated version of the `scikit-dsp-comm mono_FM demodulator <https://github.com/scikit-dsp-comm/sdr_helper/blob/master/sk_dsp_comm/sdr_helper/sdr_helper.py#L24>`_ function using HLS. This FM demodulator consists of a linear filter, downsampler, and a discriminator.

2) The second part integrates the demodulator IP core onto the Pynq Board. You should be able to listen to local FM radio channel using your M implementation in programmable logic.

3) Materials
------------
The starter files for the project can be found at in `fm-demodulation <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/fm-demodulation>`_.

This contains two Python notebooks:

1) `mono-fm-demodulation-prerecorded-file.ipynb <https://github.com/KastnerRG/Read_the_docs/blob/master/project_files/fm-demodulation/mono-fm-demodulation-prerecorded-file.ipynb>`_ explains how the Mono FM Demodulator. It uses a prerecorded set of samples from the RTL SDR and can be run on any computer.

2) `rtl2832.ipynb <https://github.com/KastnerRG/Read_the_docs/blob/master/project_files/fm-demodulation/rtl2832.ipynb>`_ provides a more comphrehensive discussion of the project. It includes code that can interface directly with the RTL SDR to sample live data and change the radio settings. It also provides some hints and discussion on how to develop the FM demodulator and interfacing it with the notebook.

We will not provide skeleton, code, testbenches, or any other scaffolding as you have gotten in the previous projects. A major learning outcome for this project is for you to completely develop a hardware accelerated system given only functionally correct Python. You must develop testbenches, correct functionally correct HLS code, decide on the I/O strategy, and optimize the system to achieve real-time performance.

4) Design Instructions
----------------------
The FM Demodulator has three primary functions: ``downsampler``, ``linear filter`` and ``discriminator``.

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

A frequency discriminator computes the derivative of the modulated phase.

Recall that the phase is calculated for a given complex sample ``S`` can be calculated as:

.. math::
  \phi(t) = \tan^{-1}\frac{S_I(t)}{S_R(t)}

where :math:`S` is a sample that is a complex data type consisting of a real :math:`S_R(t)` and imaginary :math:`S_I(t)` values (or equivalently I and Q).

We can calculate the :math:`\phi'(t)`  as

.. math::
  \phi'(t) = \frac{S_R(t)S_I'(t)-S_R'(t)S_I(t)}{S_R^2(t)+S_I^2(t)}

``mono_fm`` uses a simple approximation for the derivative which simply calculates the difference between the current and previous samples.

.. math::
  S_R'(t) = S_R(t) - S_R(t-1)
  S_I'(t) = S_I(t) - S_I(t-1)

This is done for both the real and imaginary parts. Substituting these equations yields the final computation that is done for the discriminator.

.. math::
  \phi'(t) = \frac{S_R(t)(S_I(t) - S_I(t-1))-(S_R(t) - S_R(t-1))S_I(t)}{S_R^2(t)+S_I^2(t)}

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
