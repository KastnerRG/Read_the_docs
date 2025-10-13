/*
	Filename: fir.cpp
		FIR lab wirtten for WES/CSE237C class at UCSD.
		Match filter
	INPUT:
		x: signal (chirp)

	OUTPUT:
		y: filtered output

*/

#include "fir.h"



void fir (
  data_t *y,
  data_t x
  )
{

	coef_t c[N] = {10, 11, 11, 8, 3, -3, -8, -11, -11, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -11, -11, -8, -3, 3, 8, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 8, 3, -3, -8, -11, -11, -10, -10, -10, -10, -10, -10, -10, -10, -11, -11, -8, -3, 3, 8, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 8, 3, -3, -8, -11, -11, -10, -10, -10, -10, -10, -10, -10, -10, -11, -11, -8, -3, 3, 8, 11, 11, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10};
	
	// Write your code here
	
	static
	data_t shift_reg[N];
	acc_t acc;
	int i;
	
	// Q6
	// #pragma HLS array_partition variable=shift_reg factor=2 block
	// #pragma HLS array_partition variable=y factor=2 block

	// #pragma HLS array_partition variable=shift_reg factor=2 cyclic
	// #pragma HLS array_partition variable=y factor=2 cyclic
	// #pragma HLS pipeline II=1
	//#pragma HLS array_partition variable=shift_reg complete
	//#pragma HLS array_partition variable=y complete
	acc = 0;
	// Q5)
	Shift_Loop:
	for (i = N - 1; i > 0; i--){
		// #pragma HLS pipeline II=1
		#pragma HLS unroll 
		shift_reg[i] = shift_reg[i - 1];
	}

	Accum_Loop:
	for (i = N - 1; i > 0; i--){
		// #pragma HLS pipeline II=1
		#pragma HLS unroll 
		acc += shift_reg[i] * c[i];
	}

	// Q4a) Last iteration moved outside the loop
	acc += x * c[0];
	shift_reg[0] = x;

	*y = acc;
}

