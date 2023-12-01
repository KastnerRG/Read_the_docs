.. FM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: Binary Neural Network 
=========================

1) Introduction
---------------
In this project, we develop binary neural network for MNIST digit classification. 

2) Materials
------------
The starter files for the project can be found at in `fm-demodulation <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/fm-demodulation>`_.

Read the README.md 


3) Design Instructions
----------------------
The Python code provides a functionally correct implementation of the FM demodulator written in Python.  The ``mono_fm`` function taken directly from the ``scikit-dsp-comm'' library is:
To run the python code, we only need to use numpy.  

.. code-block :: python3

	unzip pyrtlsdr-master.zip
	cd pyrtlsdr-master
	python setup.py install

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
	
.. code-block :: python3

    def feed_forward_quantized(self, input):
        """This function does BNN

        :param input: MNIST sample input
        :return:
        """
        # layer 1
        X0_input = self.quantize(self.sign(self.adj(input)))
        layer1_output = self.matmul_xnor(X0_input, self.fc1w_qntz.T)
        layer1_activations = (layer1_output * 2 - 784)

        # layer 2
        layer2_input = self.sign(layer1_activations)
        layer2_quantized = self.quantize(layer2_input)
        layer2_output = self.matmul_xnor(layer2_quantized, self.fc2w_qntz.T)
        layer2_activations = (layer2_output * 2 - 128)

        # layer 3
        layer3_input = self.sign(layer2_activations)
        layer3_quantized = self.quantize(layer3_input)
        layer3_output = self.matmul_xnor(layer3_quantized, self.fc3w_qntz.T)

        final_output = (layer3_output * 2 - 64)
        A = np.array([final_output], np.int32)

        return A

Runnign test!
(10000, 784)
89.39
89.39

4) Optimization Guidelines
------------

* Desdign the network using XNOR and popcount

* if necessery design it using  

5) Submission Procedure
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
