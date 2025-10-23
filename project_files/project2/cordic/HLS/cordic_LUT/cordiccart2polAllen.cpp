#include "cordiccart2pol.h"
#include <math.h>

// Use the pre-populated LUT arrays from cordic_LUTs.hpp
#include "cordic_LUTs.hpp"


void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta)
{
    // Convert the inputs to internal fixed point representation
    ap_fixed<W, I, AP_RND, AP_WRAP, 1> fixed_x = x;
    ap_fixed<W, I, AP_RND, AP_WRAP, 1> fixed_y = y;

    // Build the index to find the entries in the LUT.
    ap_uint<2*W> index;

    // Concatenate x and y to create the index into the LUTs. x is upper half; y is lower half.
    for(int i = 0; i < W; i++)
    {
		#pragma HLS UNROLL
        index[2*W-1-i] = fixed_x[W-1-i];
        index[W-1-i]   = fixed_y[W-1-i];
    }

    // Get the result from the LUTs and write it back to the outputs
    *r     = my_LUT_r[index];
    *theta = my_LUT_th[index];
}