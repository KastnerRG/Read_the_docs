# block matrix multiplication
block_matrix_mul is a simple program that multiplies together two large matrices and
verifies the results.  This program is implemented using Data Parallel C++ (DPC++) targeted towards FPGAs

For comprehensive instructions regarding DPC++ Programming, go to https://software.intel.com/en-us/oneapi-programming-guide and search based on relevant terms noted in the comments.

### Purpose
block_matrix_mul is an optimized version of matrix multiplication.  The code is written to compile to FPGA. The size of the
computation can be adjusted for heavier workloads (defined below). If
successful, the name of the offload device and a success message are
displayed.

The code is set to execute using the fpga emulator or target an fpga. Compiling to fpga performs a full bitstream generation and can take hours. The device used for compilation is displayed in the output.

## License  
This code sample is licensed under MIT license. 

## Building the `block_matrix_mul` Program for DPC++ 


### How to build for DPC++  

   * Run using FPGA emulator
    make fpga_emulator 
    
   * Compile to FPGA bitstream
    make fpga_hardware
    
   * Generate reports
    make fpga_report

   * Clean up 
    make clean 



## Running the Sample

### Application Parameters 
You can modify the size of the computation by adjusting the size parameter
(must be in multiples of 8) in the dpcpp file. The configurable parameters include:
   size = m_size = 128*8; // Must be a multiple of 8.
   M = m_size / 8;
   N = m_size / 4;
   P = m_size / 2;
