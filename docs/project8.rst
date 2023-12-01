.. FM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: Binary Neural Network 
=========================

1) Introduction
---------------

In this project, we develop a binary neural network for MNIST digit classification. Binary neural networks only use 0s or 1s (or -1s or 1s).
The main goal of this project is to implement a neural network using XNOR and popcount operators instead of multiplications.  



2) Materials
------------
The starter files for the project can be found at `bnn_project <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/bnn_project.zip>`_.
In the bnn_project folder contains:
 - python: this folder contains dataset, weights and python file for running BNN in python. The python file implements BNN_MNIST class which can be used for learning how BNN works in python. To run the python code, we only need to use numpy.
 - hls: hls testbench  ==> This is where you are going to write your code 
 - README.md and also use the 



3) Design Instructions
----------------------
The Python code provides a functionally correct implementation of the BNN written in Python.  The ``feed_forward_quantized`` function takes input (see the python code for details), 
and it runs the BNN based on XNOR. 

	
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

.. code-block :: python3

	# After running the code, we should get an accuracy as follows: 
	Running BNN which uses XNOR
	The shape of the input: (10000, 784)
	Accuracy: 89.39

	

4) Specific tasks for the project
------------

* Design the binary neural network using XNOR and popcount.
* Optimize your design using dataflow or using optimizations such as unroll or pipeline
* Your HLS design must match the golden outputs given in the testbench
* Demo the project on pyqn board. We do not provide jupyter notebooks. You are supposed to create necessary python jupyter notebooks for the demo.

Note: For the demo, feel free to change the interface of the top level HLS code.   

5) Submission Procedure
-----------------------

You have to submit your code (and only your code, not other files, not HLS project files). Your code should have everything in it so that we can synthesize it directly. 
This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to only import your source file and directly synthesize it.

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure it corresponds to the instructions.

Your repo must contain a folder named "bnn_project" at the top-level. This folder must be organized as follows (similar to previous projects):

**Contents:**

* **Report.pdf**

* Folder **bnn_project**

  - Source code (``*.cpp``, ``*.h``, ``*.tcl``) and reports (``.rpt`` and ``.xml``).

* Folder **Demo**

  - ``.bit`` and ``.hwh`` files
  - ``bnn.ipynb`` host file

**Report:** For this project, you must submit a report that describes the implementation of your design. You may add figures, diagrams, tables, or charts to describe your 
architectures with a short paragraph explaining them. There are no specific questions to answer. Just explain your design. 
We will check if (1) your final bnn project functions are functionally correct (they pass their test benches) and (2) uses XNOR. 
