#include "cordiccart2pol.h"

data_t Kvalues[NO_ITER] = {1,	0.500000000000000,	0.250000000000000,	0.125000000000000,	0.0625000000000000,	0.0312500000000000,	0.0156250000000000,	0.00781250000000000,	0.00390625000000000,	0.00195312500000000,	0.000976562500000000,	0.000488281250000000,	0.000244140625000000,	0.000122070312500000,	6.10351562500000e-05,	3.05175781250000e-05};

data_t angles[NO_ITER] = {0.785398163397448,	0.463647609000806,	0.244978663126864,	0.124354994546761,	0.0624188099959574,	0.0312398334302683,	0.0156237286204768,	0.00781234106010111,	0.00390623013196697,	0.00195312251647882,	0.000976562189559320,	0.000488281211194898,	0.000244140620149362,	0.000122070311893670,	6.10351561742088e-05,	3.05175781155261e-05};

// ---Testing results----------------------------------
// Test: x=0.8147, y=0.1269, golden theta=0.1545, golden r=0.8245, your theta=0.1545, your r=1.3578
//                              8.85219793 degrees

// Test: x=0.6323, y=-0.2785, golden theta=-0.4149, golden r=0.6909, your theta=-0.4149, your r=1.1378
//                             -23.7720189 degrees

// Test: x=-0.5469, y=-0.9575, golden theta=-2.0898, golden r=1.1027, your theta=-1.7433, your r=1.7079
//                              -119.73672 degrees

// Test: x=-0.4854, y=0.7003, golden theta=2.1769, golden r=0.8521, your theta=1.7433, your r=1.2733
//                              124.727182 degrees

// ---RMS error----------------------------------
// ----------------------------------------------
//    RMSE(R)           RMSE(Theta)
// 0.506904780864716 0.277535438537598
// ----------------------------------------------
void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta)
{
	// Write your code here
	// input x and y, output r/magnitude and theta/angle
	// acc_t can be the angle accumulating
    data_t current_x = x;  // Start with the input x
    data_t current_y = y;  // Start with the input y
    acc_t current_theta = 0.0;  // We will accumulate the angle

    for (int i = 0; i < NO_ITER; i++) {
        int sigma = (current_y < 0) ? -1 : 1;

        // starts from allegedly 1/1.6467,0 and goes to x, y 
        // so if we start from x, y and want to go back to 1/1.6467,0 we reverse it

        //current cos = current cos - current sin ∗ sigma ∗ factor;
        data_t temp_x = current_x + current_y * sigma * Kvalues[i];
        //cur_sin = current sin + current cos ∗ sigma ∗ factor;
        current_y = current_y - current_x * sigma * Kvalues[i];
        current_x = temp_x;

        // Update the angle (theta) and accumulate it
        current_theta += sigma * angles[i];
        // theta = theta - sigma * cordic phase[j];
        // Instead of going down to 0, we starting from 0

        // factor = factor / 2;  is done by Kvalues array. 

    }

    // Set the output variables
    *r = current_x;  // Final magnitude
    *theta = current_theta;  // Final angle
}
