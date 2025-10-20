#ifndef CORDICCART2POL_H
#define CORDICCART2POL_H
#include "ap_fixed.h"

#define NO_ITER 16
#define NUM_BITS 12

typedef int   coef_t;
typedef ap_fixed<NUM_BITS,3> data_t;
//typedef float data_t; // 2b
typedef ap_fixed<NUM_BITS,3> acc_t;

void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta);

#endif
