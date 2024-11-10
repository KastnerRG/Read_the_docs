#include <ap_int.h>

typedef float DTYPE;
#define SIZE 1024 		/* SIZE OF DFT */
void dft(DTYPE real_sample[SIZE], DTYPE imag_sample[SIZE],DTYPE real_op[SIZE], DTYPE imag_op[SIZE]);
// Use streaming interface for demo
