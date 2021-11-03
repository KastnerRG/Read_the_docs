//==============================================================
// Copyright © 2020 Intel Corporation
//
// SPDX-License-Identifier: MIT
// =============================================================

/**
 * Matrix_mul multiplies two large matrices both the CPU and the offload device,
 * then compares results. If the code executes on both CPU and the offload
 * device, the name of the offload device and a success message are displayed.
 *
 * For comprehensive instructions regarding DPC++ Programming, go to
 * https://software.intel.com/en-us/oneapi-programming-guide and search based on
 * relevant terms noted in the comments.
 */

#include <CL/sycl.hpp>
#include <iostream>
#include <limits>

#include <CL/sycl/INTEL/fpga_extensions.hpp>

// dpc_common.hpp can be found in the dev-utilities include folder.
// e.g., $ONEAPI_ROOT/dev-utilities/<version>/include/dpc_common.hpp
#include "dpc_common.hpp"

using namespace std;
using namespace sycl;

class a_init;
class b_init;
class c_calc;

/**
 * Each element of the product matrix c[i][j] is computed from a unique row and
 * column of the factor matrices, a[i][k] and b[k][j]
 */

// Matrix size constants.
constexpr int m_size = 128 * 8;  // Must be a multiple of 8.
constexpr int M = m_size / 8;
constexpr int N = m_size / 8;
constexpr int P = m_size / 8;
constexpr int BL = 16;

/**
 * Perform matrix multiplication on host to verify results from device.
 */
int VerifyResult(float (*c_back)[P]);

double GetExecutionTime(const event &e) {
  double start_k = e.get_profiling_info<info::event_profiling::command_start>();
  double end_k = e.get_profiling_info<info::event_profiling::command_end>();
  double kernel_time = (end_k - start_k) * 1e-9; // ns to s
  return kernel_time;
}

int main() {
  // Host memory buffer that device will write data back before destruction.
  float(*c_back)[P] = new float[M][P];

  // Intialize c_back
  for (int i = 0; i < M; i++)
    for (int j = 0; j < P; j++) c_back[i][j] = 0.0f;

  // Initialize the device queue with the default selector. The device queue is
  // used to enqueue kernels. It encapsulates all states needed for execution.
  try {
    // Select either:
    //  - the FPGA emulator device (CPU emulation of the FPGA)
    //  - the FPGA device (a real FPGA)
    #if defined(FPGA_EMULATOR)
         ext::intel::fpga_emulator_selector device_selector;
    #else
         ext::intel::fpga_selector device_selector;
    #endif
    ext::intel::fpga_emulator_selector _device;
    queue q(_device, dpc_common::exception_handler, property::queue::enable_profiling{});

    cout << "Device: " << q.get_device().get_info<info::device::name>() << "\n";

    // Create 2D buffers for matrices, buffer c is bound with host memory c_back

    // These are all Global Memory
    buffer<float, 2> a(range(M, N));
    buffer<float, 1> aa(range(M*N));
    buffer<float, 2> b(range(N, P));
    buffer<float, 1> bb(range(N*P));
    buffer c(reinterpret_cast<float *>(c_back), range(M, P));

    cout << "Problem size: c(" << M << "," << P << ") = a(" << M << "," << N
         << ") * b(" << N << "," << P << ")\n";

    // Using three command groups to illustrate execution order. The use of
    // first two command groups for initializing matrices is not the most
    // efficient way. It just demonstrates the implicit multiple command group
    // execution ordering.

    // Submit command group to queue to initialize matrix a
    auto e_a = q.submit([&](handler &h) {
      // Get write only access to the buffer on a device.
      auto accessor = a.get_access<access::mode::write>(h);
      auto accessor2 = aa.get_access<access::mode::write>(h);

      // Execute kernel.
      h.template parallel_for<a_init>(range(M, N), [=](id<2> index) {
        // Each element of matrix a is 1.
        accessor[index] = 1.0f;
        accessor2[index[0]*M+index[1]] = 1.0f;        
      });
    });

    // Submit command group to queue to initialize matrix b
    auto e_b = q.submit([&](handler &h) {
      // Get write only access to the buffer on a device
      auto accessor = b.get_access<access::mode::write>(h);
      auto accessor2 = bb.get_access<access::mode::write>(h);

      // Execute kernel.
      h.template parallel_for<b_init>(range(N, P), [=](id<2> index) {
        // Each column of b is the sequence 1,2,...,N
        accessor[index] = index[0] + 1.0f;
        accessor2[index[0]*N+index[1]] = index[0] + 1.0f;
      });
    });
    
    // Submit command group to queue to multiply matrices: c = a * b
    auto e_c = q.submit([&](handler &h) {
      // Read from a and b, write to c
      auto A = aa.get_access<access::mode::read>(h);
      auto B = bb.get_access<access::mode::read>(h);
      auto C = c.get_access<access::mode::write>(h);
      
      accessor<float, 2, access::mode::read_write, access::target::local> A_local(range<2>{BL, BL}, h);
      accessor<float, 2, access::mode::read_write, access::target::local> B_local(range<2>{BL, BL}, h);
        
      range<2> num_groups(M, P);
      range<2> num_items(BL, BL);
      
      //sycl::stream out(1024, 256, h);
      h.template parallel_for<c_calc>(nd_range<2>(num_groups, num_items), [=](nd_item<2> item) {
          
          int block_x = item.get_group().get_id(0);
          int block_y = item.get_group().get_id(1);
          
          int local_x = item.get_local_id(0);
          int local_y = item.get_local_id(1);
          
          int a_start = N * BL * block_y;
          int a_end   = a_start + N - 1;
          int b_start = BL * block_x;
                          
          float sum = 0.0f;
          
          for (int a = a_start, b = b_start; a <= a_end; a += BL, b += (BL * P)){

              A_local[local_y][local_x] = A[a + N * local_y + local_x];
              B_local[local_x][local_y] = B[b + P * local_y + local_x];
                  
              item.barrier(access::fence_space::local_space);
                  
              for (int k = 0; k < BL; ++k){
                   sum += A_local[local_y][k] * B_local[local_x][k];
              }
            
              item.barrier(access::fence_space::local_space);
              
          }
        
          C[item.get_global_id(1)][item.get_global_id(0)] = sum;
          
      });
        
        
    });
    double a_time = GetExecutionTime(e_a);
    double b_time = GetExecutionTime(e_b);
    double c_time = GetExecutionTime(e_c);
    double input_size_kb = (2*N)*sizeof(float)/(1024);
    std::cout << "Kernel throughput initializing a: " 
              << (input_size_kb/a_time) << " KB/s \n"; // this one is larger and not accurate. Some device initialization is included here.
    std::cout << "Kernel throughput initializing b: " 
              << (input_size_kb/b_time) << " KB/s \n";
    std::cout << "Kernel throughput calculating c: " 
              << (input_size_kb/c_time) << " KB/s \n";
    
  } catch (sycl::exception const &e) {
    cout << "An exception is caught while multiplying matrices.\n";
    terminate();
  }

  int result;
  cout << "Result of matrix multiplication using DPC++: ";
  result = VerifyResult(c_back);
  delete[] c_back;

  return result;
}

bool ValueSame(float a, float b) {
  return fabs(a - b) < numeric_limits<float>::epsilon();
}

int VerifyResult(float (*c_back)[P]) {
  // Check that the results are correct by comparing with host computing.
  int i, j, k;

  // 2D arrays on host side.
  float(*a_host)[N] = new float[M][N];
  float(*b_host)[P] = new float[N][P];
  float(*c_host)[P] = new float[M][P];

  // Each element of matrix a is 1.
  for (i = 0; i < M; i++)
    for (j = 0; j < N; j++) a_host[i][j] = 1.0f;

  // Each column of b_host is the sequence 1,2,...,N
  for (i = 0; i < N; i++)
    for (j = 0; j < P; j++) b_host[i][j] = i + 1.0f;

  // c_host is initialized to zero.
  for (i = 0; i < M; i++)
    for (j = 0; j < P; j++) c_host[i][j] = 0.0f;

  for (i = 0; i < M; i++) {
    for (k = 0; k < N; k++) {
      // Each element of the product is just the sum 1+2+...+n
      for (j = 0; j < P; j++) {
        c_host[i][j] += a_host[i][k] * b_host[k][j];
      }
    }
  }

  bool mismatch_found = false;

  // Compare host side results with the result buffer from device side: print
  // mismatched data 5 times only.
  int print_count = 0;

  for (i = 0; i < M; i++) {
    for (j = 0; j < P; j++) {
      if (!ValueSame(c_back[i][j], c_host[i][j])) {
        cout << "Fail - The result is incorrect for element: [" << i << ", "
             << j << "], expected: " << c_host[i][j]
             << ", but found: " << c_back[i][j] << "\n";
        mismatch_found = true;
        print_count++;
        if (print_count == 50) break;
      }
    }

    if (print_count == 50) break;
  }

  delete[] a_host;
  delete[] b_host;
  delete[] c_host;

  if (!mismatch_found) {
    cout << "Success - The results are correct!\n";
    return 0;
  } else {
    cout << "Fail - The results mismatch!\n";
    return -1;
  }
}