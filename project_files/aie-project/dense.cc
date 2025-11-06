#include <aie_api/aie.hpp>
#include <aie_kernels/aie_kernel_utils.h>
#define DTYPE int8

// Make sure the following tile and intrinsic sizes match the sizes in the
// data layout transformations described in
// matrix_multiplication_single_core.py.
constexpr unsigned m = 64;
constexpr unsigned k = 64;
constexpr unsigned n = 64;
constexpr unsigned r = 2;
constexpr unsigned s = 8;
constexpr unsigned t = 8;

using MMUL = aie::mmul<r, s, t, DTYPE, DTYPE>;

extern "C" {

//

// Multiply A and B, and add the result onto the values already in C.
// A, B, and C must be tiled into tiles of size r*s, s*t, and r*t,
// respectively (in our design, the DMA performs this tiling).
void matmul(const DTYPE *__restrict A, const DTYPE *__restrict B, DTYPE *__restrict C) {
  AIE_PREPARE_FOR_PIPELINING
  AIE_LOOP_MIN_ITERATION_COUNT(4)
  for (unsigned row = 0; row < m / r; row += 2) {
    for (unsigned col = 0; col < n / t; col += 2) {

      // The following pointers point to the start of two rows of A and
      // tow columns of B, respectively.
      const DTYPE *__restrict A0_ptr = A + ((row + 0) * (k / s) + 0) * MMUL::size_A;
      const DTYPE *__restrict A1_ptr = A + ((row + 1) * (k / s) + 0) * MMUL::size_A;
      const DTYPE *__restrict B0_ptr = B + (0 * (n / t) + (col + 0)) * MMUL::size_B;
      const DTYPE *__restrict B1_ptr = B + (0 * (n / t) + (col + 1)) * MMUL::size_B;

      const aie::vector<DTYPE, MMUL::size_C> C00_in = aie::load_v<MMUL::size_C>(C + ((row + 0) * (n / t) + (col + 0)) * MMUL::size_C);
      const aie::vector<DTYPE, MMUL::size_C> C01_in = aie::load_v<MMUL::size_C>(C + ((row + 0) * (n / t) + (col + 1)) * MMUL::size_C);
      const aie::vector<DTYPE, MMUL::size_C> C10_in = aie::load_v<MMUL::size_C>(C + ((row + 1) * (n / t) + (col + 0)) * MMUL::size_C);
      const aie::vector<DTYPE, MMUL::size_C> C11_in = aie::load_v<MMUL::size_C>(C + ((row + 1) * (n / t) + (col + 1)) * MMUL::size_C);
      MMUL C00(C00_in);
      MMUL C01(C01_in);
      MMUL C10(C10_in);
      MMUL C11(C11_in);

      // The following loop iterates over the k dimension of the
      // input matrices, i.e., over each tile in the same row of
      // A and each tile in the same column of B.
      for (unsigned i = 0; i < k / s; i += 1, A0_ptr += MMUL::size_A,
                    A1_ptr += MMUL::size_A, B0_ptr += (n / t) * MMUL::size_B,
                    B1_ptr += (n / t) * MMUL::size_B) {
        const aie::vector<DTYPE, MMUL::size_A> A0 = aie::load_v<MMUL::size_A>(A0_ptr);
        const aie::vector<DTYPE, MMUL::size_A> A1 = aie::load_v<MMUL::size_A>(A1_ptr);
        const aie::vector<DTYPE, MMUL::size_B> B0 = aie::load_v<MMUL::size_B>(B0_ptr);
        const aie::vector<DTYPE, MMUL::size_B> B1 = aie::load_v<MMUL::size_B>(B1_ptr);
        C00.mac(A0, B0);
        C01.mac(A0, B1);
        C10.mac(A1, B0);
        C11.mac(A1, B1);
      }
        
      aie::store_v(C + ((row + 0) * (n / t) + (col + 0)) * MMUL::size_C, C00.template to_vector<DTYPE>());
      aie::store_v(C + ((row + 0) * (n / t) + (col + 1)) * MMUL::size_C, C01.template to_vector<DTYPE>());
      aie::store_v(C + ((row + 1) * (n / t) + (col + 0)) * MMUL::size_C, C10.template to_vector<DTYPE>());
      aie::store_v(C + ((row + 1) * (n / t) + (col + 1)) * MMUL::size_C, C11.template to_vector<DTYPE>());
    }
  }
}

}