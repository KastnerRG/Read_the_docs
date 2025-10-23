#ifndef CORDICCART2POL_H
#define CORDICCART2POL_H
#include "ap_fixed.h"

#define NO_ITER 16
#define NUM_BITS 32 // 2b and 3a
#define ROT_BITS 32 // 2c

typedef int   coef_t;
typedef ap_fixed<NUM_BITS,3> data_t;
//typedef float data_t; // 2b
typedef ap_fixed<NUM_BITS,3> acc_t;

typedef ap_fixed<ROT_BITS,3> cordicTableType;

void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta);

#endif
