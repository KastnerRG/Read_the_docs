#include "cordiccart2pol.h"

data_t Kvalues[NO_ITER] = {1,	0.500000000000000,	0.250000000000000,	0.125000000000000,	0.0625000000000000,	0.0312500000000000,	0.0156250000000000,	0.00781250000000000,	0.00390625000000000,	0.00195312500000000,	0.000976562500000000,	0.000488281250000000,	0.000244140625000000,	0.000122070312500000,	6.10351562500000e-05,	3.05175781250000e-05};//, /*17-20*/ 1.525878906250000e-05, 7.629394531250000e-06, 3.814697265625000e-06, 1.907348632812500e-06  };

// radians
data_t angles[NO_ITER] = {0.785398163397448,	0.463647609000806,	0.244978663126864,	0.124354994546761,	0.0624188099959574,	0.0312398334302683,	0.0156237286204768,	0.00781234106010111,	0.00390623013196697,	0.00195312251647882,	0.000976562189559320,	0.000488281211194898,	0.000244140620149362,	0.000122070311893670,	6.10351561742088e-05,	3.05175781155261e-05};//,/*17-20*/  1.525878905776305e-05, 7.629394528881525e-06, 3.8146972644407625e-06, 1.90734863222038125e-06};

void cordiccart2pol(data_t x, data_t y, data_t * r,  data_t * theta)
{
    // Function control signal
    #pragma HLS INTERFACE mode=s_axilite port=return

    // Inputs (x and y)
    #pragma HLS INTERFACE mode=s_axilite port=x
    #pragma HLS INTERFACE mode=s_axilite port=y

    // Outputs (r and theta)
    #pragma HLS INTERFACE mode=s_axilite port=r
    #pragma HLS INTERFACE mode=s_axilite port=theta
    
	// Write your code here
	// input x and y, output r/magnitude and theta/angle
	// acc_t can be the angle accumulating

    /* BASELINE IMPLEMENTATION START */
    // acc_t current_theta = 0.0;  // We will accumulate the angle
    // Precheck to force into quadrants I and IV
    int sigma = (y < 0) ? -1 : 1;
    // // If the y value is positive, we know that we are in either Quadrant I or II.
    //     // A rotation by -90 will put us into Quadrant IV or I, respectively
    //     // x_new = y_old
    //     // y_new = -x_old
    // // If the y value is negative, we know that we are in either Quadrant III or IV.
    //     // A rotation by 90 will put us into Quadrant IV or I, respectively
    //     // x_new = -y_old
    //     // y_new = x_old
    /* BASELINE IMPLEMENTATION end */


    /* ADD AND SHIFT ACCUM VER */
    //acc_t current_theta = sigma * angles[0] * 2; // sigma * 90 degrees
    acc_t current_theta = 0.0;
    data_t current_x = 0.0;
    data_t current_y = 0.0;
    
    if(sigma > 0){
        current_theta += (angles[0] << 1); 
        current_x = y;
        current_y = -x;   
    }
    else if(sigma < 0){
        current_theta -= (angles[0] << 1);
        current_x = -y; 
        current_y = x;
    }
    //acc_t current_theta = sigma * (angles[0] << 1);

    // data_t current_x = sigma * y;
    // data_t current_y = -sigma * x;
    // data_t current_x = y;  // base is x_new = y_old
    // data_t current_y = -x; //         y_new = -x_old
    // if(y < 0) {
    //     current_x = -current_x; 
    //     current_y = current_y;
    //     current_theta = -current_theta;
    // }

    for (int i = 0; i < NO_ITER; i++) {
        sigma = (current_y < 0) ? -1 : 1;
        // starts from allegedly 1/1.6467,0 and goes to x, y 
        // so if we start from x, y and want to go back to 1/1.6467,0 we reverse it

        //current cos = current cos - current sin ∗ sigma ∗ factor;
        


        //data_t temp_x = current_x + (current_y >> i )* sigma;
        //current_y = current_y - (current_x >> i)* sigma;
        //current_x = temp_x;
        //current_theta += sigma * angles[i];
        if(sigma>0){
            data_t temp_x = current_x + (current_y >> i );
            current_y = current_y - (current_x >> i);
            current_theta += angles[i];
            current_x = temp_x;
        }
        else if(sigma < 0){
            data_t temp_x = current_x - (current_y >> i );
            current_y = current_y + (current_x >> i);
            current_theta -= angles[i];
            current_x = temp_x;
        }
        

       
        /////cur_sin = current sin + current cos ∗ sigma ∗ factor;

        

        //// Update the angle (theta) and accumulate it
        //current_theta += sigma * angles[i];
        //// theta = theta - sigma * cordic phase[j];
        //// Instead of going down to 0, we starting from 0

        //// factor = factor / 2;  is done by Kvalues array. 

    }

    // Set the output variables
    data_t scaling_factor = 0.6072529350088812561694;
    *r = current_x * scaling_factor;   // Final magnitude * (K=lim_n->inf K(n))
    *theta = current_theta;  // Final angle
}
