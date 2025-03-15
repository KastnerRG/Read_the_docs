/*
 This is traditional 2-radix DIT FFT algorithm implementation.
 INPUT:
 In_R, In_I[]: Real and Imag parts of Complex signal

 OUTPUT:
 Out_R, Out_I[]: Real and Imag parts of Complex signal
 */

#include "fft.h"


/*=======================BEGIN: FFT=========================*/
//stage 1
void fft_stage_first(DTYPE X_R[SIZE], DTYPE X_I[SIZE], DTYPE OUT_R[SIZE], DTYPE OUT_I[SIZE]) {

	//Insert your code here

}

//stages
void fft_stages(DTYPE X_R[SIZE], DTYPE X_I[SIZE], int stage, DTYPE OUT_R[SIZE], DTYPE OUT_I[SIZE]) {

	//Insert your code here
}

//last stage
void fft_stage_last(DTYPE X_R[SIZE], DTYPE X_I[SIZE], DTYPE OUT_R[SIZE], DTYPE OUT_I[SIZE]) {

	//Insert your code here

}

void bit_reverse(DTYPE X_R[SIZE], DTYPE X_I[SIZE], DTYPE X_R_Copy[SIZE], DTYPE X_I_Copy[SIZE])
{

	//Insert your code here
}
/*=======================END: FFT=========================*/
