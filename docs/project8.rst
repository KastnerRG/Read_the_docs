.. FM_Receiver documentation master file, created by
   sphinx-quickstart on Sat Mar 23 13:02:50 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Project: Binary Neural Network (BNN) 
=========================

1) Introduction
---------------

In this project, we develop a binary neural network for MNIST digit classification. Binary neural networks only use -1s or 1s.
The main goal of this project is to implement a neural network using XNOR and popcount operators instead of multiplication and summation.  



2) Materials
------------
The starter files for the project can be found at `bnn_project <https://github.com/KastnerRG/Read_the_docs/tree/master/project_files/bnn_project.zip>`_.
The bnn_project folder contains:
 - python: this folder contains dataset, weights, and Python code that implements a BNN. The Python file implements the BNN_MNIST class, which is useful to understand how a BNN works. 
 - hls: hls testbench  ==> This is where you are going to write your code 
 - README.md 



3) Design Instructions
----------------------
The Python code provides a functionally correct implementation of the BNN.  The ``feed_forward_quantized`` function takes as input an MNIST image, executes the BNN, and outputs the classified result (a digit between 0 and 9. 

The function that you must replicate in HLS is:	
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

	# Executing the Python file will run 10000 MNIST images, each of size 28*28=784, and return a classification. The accuracy is the percentage of correct classifications. 
	Running BNN which uses XNOR
	The shape of the input: (10000, 784)
	Accuracy: 89.39

	

4) Project Tasks
------------

* Design the binary neural network using XNOR and popcount in HLS.
* Optimize your design to increase throughput and minimize latency. Consider optimizations like dataflow, loop unrolling, and pipelining. Provide details and trade-offs of design optimizations in your report.
* Your HLS design must match the golden outputs given in the testbench.
* Demo the project on pynq board. This project does not provide an example Jupyter notebook. You should create to create a notebook that demos your result.
* Provide a report that explains: 1) your different optimizations, describes how you decided to interface your HLS IP core, and provides details of your notebook demo. 

Note: You can change the interface of the top-level HLS code. If you do, you should explain the rationale for these changes in your report. 

5) Submission Procedure
-----------------------

You have to submit your code (and only your code, not other files, not HLS project files). Your code should have everything in it so we can synthesize it directly. 
This means that you should use pragmas in your code, and not use the GUI to insert optimization directives. We must be able to import your source file and directly synthesize it.

You must follow the file structure below. We use automated scripts to pull your data, so **DOUBLE CHECK** your file/folder names to make sure they correspond to the instructions.

Your repo must contain a folder named "bnn_project" at the top level. This folder must be organized as follows (similar to previous projects):

**Contents:**

* **Report.pdf**

* Folder **bnn_project**

  - Source code (``*.cpp``, ``*.h``, ``*.tcl``) and reports (``.rpt`` and ``.xml``).

* Folder **Demo**

  - ``.bit`` and ``.hwh`` files
  - ``bnn.ipynb`` host file

**Report:** For this project, you must submit a report that describes the implementation of your design. You may add figures, diagrams, tables, or charts to describe your 
architectures with a short paragraph explaining them. There are no specific questions to answer. Just explain your design. 
We will check if (1) your final BNN project functions are functionally correct (they pass their test benches) and (2) they use XNOR. 
