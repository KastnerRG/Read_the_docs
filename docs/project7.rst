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

Recall that the phase is calculated for a given complex sample ``S`` can be calculated as

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

This is done for both the real and imaginary parts. This computation is done using the ``lfilter`` function in the Python code. The ``b`` array is used to calculate the differences between consecutive elements.

Substituting these equations yields the final computation that is done for the discriminator.

.. math::
  \phi'(t) = \frac{S_R(t)(S_I(t) - S_I(t-1))-(S_R(t) - S_R(t-1))S_I(t)}{S_R^2(t)+S_I^2(t)}

This is a fairly simple calculation that can be performed efficiently in hardware.

5) PYNQ Demo
------------

You should integrate your HLS code into a Jupyter notebook and demonstrate *real-time* performance, i.e., the total processing time less is less than the sampling time.

The provided Jupyter notebooks provide methods to sample real-data using the RTL SDR. There is also a prerecorded file. Your system should be able to take data in this format, process it in real-time, output it in the expected format, and play correctly using the provided functions. This must be done in real-time. For example, your system must be able to process 1 second of data in under one second.

You can use any method of interfacing as long as it performs the processing in real-time. This will require that the I/O between the PS and PL is efficient. This can very easily become a bottleneck and limit your ability to perform real-time processing. A real-time HLS IP core is useless if your cannot use it to the best of its performance. You are highly encouraged to modify the code to achieve a better performance and observe the throughput by changing the way you transmit data between PS and PL. Make use of the "RTL 2832" USB tuner in-order to receive the input RF Samples.


6) Optimization Guidelines
------------

* **Hardware / Software Interface:** An important consideration in your overall design will be the way that you exchange data between the ``mono_fm`` IP core on the programmable logic (PL) and the Jupyter notebook running on the processing system (PS). This interface will define the interface to your IP core, so think carefully about the entire system design before diving into the HLS design process.

* **Testing:** You must develop a strategy for testing your HLS code. Perform incremental testing. Design and test the subfunctions before integrating them together.

* **Real-time Performance Constraints:** Your ultimate goal is to perform real-time demodulation. The SDR sampling rate is set at 2.4 million samples per second (MSPS). That requires a real-time ``mono_fm`` to be have an initiation interval less than 417 ns. Using a clock period of 10 ns, that allows for approximately 40 cycles per sample. Given the fairly simplistic nature of the computations, this should be feasible. Do not forget about the potential effects of the HW/SW interface on the overall design.

* **System Design:** You are responsible for understanding the system constraints and delivering a system that meets those constraints. There are many ways to build a system. The best systems are the ones that work reliably. Always work first on developing a functional baseline implementation. Then optimize it to achieve real-time performance.

7) Submission Procedure
-----------------------

You have to submit your code (and only your code, not other files, not HLS project files). Your code should have everything in it so that we can synthesize it directly. This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to only import your source file and directly synthesize it.

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "mono_fm" at the top-level. This folder must be organized as follows (similar to previous projects):

**Contents:**

* **Report.pdf**

* Folder **fm-demodulator**

  - Source code (``*.cpp``, ``*.h``, ``*.tcl``) and reports (``.rpt`` and ``.xml``).

* Folder **Demo**

  - ``.bit`` and ``.hwh`` files
  - ``FM.ipynb`` host file

**Report:** For this project, you must submit a report that describes the implementation of your design. You may add figures, diagrams, tables, or charts to describe your architectures with a short paragraph explaining them. There are no specific questions to answer. Just explain your design. We will check if (1) your final FM Demodulation functions are functionally correct (they pass their test benches) and (2) achieves target latency. The report will help us to understand your design. You also can use this report to explain your work for bonus part (check the grading section).

8) Grading Rubric
-----------------

**30 points:** Functionally correct HLS design. You will get full credit if we are able to build and test your HLS code without any effort. You must provide testbenches that demonstrate the correct functionality of your code. You need to report the throughput of the final design.

**30 points:** Basic Pynq Demo. Demonstrate the ability to demodulate the prerecorded file through your HLS code. You will get full credit for clear audio output and an RMSE less than 1e-6.

**10 points:** Real-time Pynq Demo. Demonstrate the ability to perform real-time demodulation. For example, show that your system can demodulate the 1 second prerecorded file in under 1 second.

**10 points:** Interface with RTL SDR. Demonstrate the ability to directly acquire real-time samples using the RTL SDR.

**20 points:** Report. Detail the system design decisions, HLS code, testbenches, HW/SW interfaces, and other aspects of the system. Talk about challenges. Report should be well formatted, use figures and diagrams to aid explanations, and free of spelling and grammar errors.

**Bonus:**

**30 Points:** Output audio on Pynq board. Modify your design to listen to the audio using the Pynq audio. The Pynq base overlay has the ability to use of audio instance on the Pynq Board. One approach would be to add your system into the base overlay. Another approach would extract the important parts of the base overall into your designs.  More information about the audio module on Pynq Z2 can be found `here <https://pynq.readthedocs.io/en/v2.3/pynq_libraries/audio.html>`_ and `here <https://pynq.readthedocs.io/en/v2.3/pynq_package/pynq.lib/pynq.lib.audio.html#pynq-lib-audio>`_. Detailed description of the BaseOverlay can be found  `here <https://pynq.readthedocs.io/en/v2.3/pynq_overlays/pynqz2/pynqz2_base_overlay.html>`_.
