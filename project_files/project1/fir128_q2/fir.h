/*
	Filename: fir.h
		Header file
		FIR lab wirtten for WES/CSE237C class at UCSD.

*/
#ifndef FIR_H_
#define FIR_H_

#include "ap_int.h"

const int N=128;
#define BW_VAL 16

typedef ap_int<BW_VAL>	coef_t;
typedef ap_int<BW_VAL>	acc_t;

typedef int	data_t;

void fir (
  data_t *y,
  data_t x
  );

#endif
