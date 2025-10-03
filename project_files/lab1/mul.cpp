/*
	Filename: mul.cpp
		MUL lab written for WES/CSE237C class at UCSD.

	INPUT:
		in

	OUTPUT:
		out

*/
#include "mul.h"

void mul(
	data_t* out, 
	data_t in
	)
{
	#pragma HLS INTERFACE mode=s_axilite port=return
    #pragma HLS INTERFACE mode=s_axilite port=in
    #pragma HLS INTERFACE mode=s_axilite port=out
    *out = 2*in;
}

