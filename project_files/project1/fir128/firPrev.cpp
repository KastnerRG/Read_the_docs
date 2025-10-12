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
		acc_t acc1;
		acc_t acc2;
		int i;

	acc1 = 0;
	acc2 = 0;
	Shift_Accum_Loop1:
	for (i = N - 1; i > (N - 1) / 2; i--){
		#pragma HLS unroll factor=4
		shift_reg[i] = shift_reg[i - 1];
		acc1 += shift_reg[i] * c[i];
	}

	Shift_Accum_Loop2:
	for (i = (N - 1)/2; i >= 0; i--){
		#pragma HLS unroll factor=4
		if (i == 0) {
		 	acc2 += x * c[0];
		 	shift_reg[0] = x;
		} else {
		shift_reg[i] = shift_reg[i - 1];
		acc2 += shift_reg[i] * c[i];
		}
	}


	*y = acc1+acc2;
}

