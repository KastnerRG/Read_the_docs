#include "cordiccart2pol.h"
#include <math.h>
#include <stdio.h>


struct Rmse
{
	int num_sq;
	float sum_sq;
	float error;

	Rmse(){ num_sq = 0; sum_sq = 0; error = 0; }

	float add_value(float d_n)
	{
		num_sq++;
		sum_sq += (d_n*d_n);
		error = sqrtf(sum_sq / num_sq);
		return error;
	}

};


Rmse rmse_theta;
Rmse rmse_r;


void run_test(data_t x, data_t y, double golden_theta, double golden_r)
{
	data_t r;
	data_t theta;

	cordiccart2pol(x, y, &r,  &theta);

	printf("Test: x=%.4f, y=%.4f, golden theta=%.4f, golden r=%.4f, your theta=%.4f, your r=%.4f\n",
			(double)x, (double)y, golden_theta, golden_r, (double)theta, (double)r);

	rmse_theta.add_value((float)theta - golden_theta);
	rmse_r.add_value((float)r - golden_r);
}


int main()
{
	data_t x;
	data_t y;
	data_t r;
	data_t theta;


	printf("---Testing results----------------------------------\n");

	// Test1
	run_test(0.8147, 0.1269, 0.154521173805634, 0.824523923242982);

	// Test 2
	run_test(0.6323, -0.2785, -0.414888412375609, 0.690916449362729);

	// Test 3
	run_test(-0.5469, -0.9575, -2.089751217098013, 1.102681214132172);

	// Test 4
	run_test(-0.4854, 0.7003, 2.176897679895152, 0.852075847562880);

	// -------------------------------------------------------------------
    // --- NEW EXTENSIVE TEST CASES --------------------------------------
    // -------------------------------------------------------------------

	// Test 5: Angle 37 deg (Q1); R=0.42
    // X = 0.42 * cos(37 deg), Y = 0.42 * sin(37 deg)
    run_test(0.335427, 0.252762, 0.6457718232, 0.42);

    // Test 6: Angle 112 deg (Q2); R=1.59
    // X = 1.59 * cos(112 deg), Y = 1.59 * sin(112 deg)
    run_test(-0.596094, 1.474160, 1.9547687625, 1.59);

    // Test 7: Angle 179.9 deg (Near -X axis); R=5.12
    // X = 5.12 * cos(179.9 deg), Y = 5.12 * sin(179.9 deg)
    run_test(-5.119992, 0.008933, 3.1398811776, 5.12);

    // Test 8: Angle -15 deg (Q4); R=0.055 (Small R)
    // X = 0.055 * cos(-15 deg), Y = 0.055 * sin(-15 deg)
    run_test(0.053126, -0.014235, -0.2617993878, 0.055);

    // Test 9: Angle -167 deg (Q3); R=7.50 (Large R)
    // X = 7.50 * cos(-167 deg), Y = 7.50 * sin(-167 deg)
    run_test(-7.307775, -1.687133, -2.9147545199, 7.50);

    // Test 10: Angle 285 deg (or -75 deg, Q4); R=2.20
    // X = 2.20 * cos(-75 deg), Y = 2.20 * sin(-75 deg)
    run_test(0.569485, -2.122603, -1.3089969390, 2.20);

    // Test 11: Angle -150 deg (Q3); R=0.90
    // X = 0.90 * cos(-150 deg), Y = 0.90 * sin(-150 deg)
    run_test(-0.779423, -0.450000, -2.6179938780, 0.90);

    // Test 12: Angle 90.5 deg (Near +Y axis); R=3.00
    // X = 3.00 * cos(90.5 deg), Y = 3.00 * sin(90.5 deg)
    run_test(-0.026178, 2.999886, 1.5794101861, 3.00);

	//Test 13: Angle 180, R =  65.00
	// X = 65.00 * cos(180), Y = 65.00 * sin(180)
	run_test(-65.00, 0.00, 3.141593, 65.00);

	//Test 14: Angle 90, R =  7.00
	// X = 7.00 * cos(90), Y = 7.00 * sin(90)
	run_test(0.00, 7.00, 1.570796, 7.00);

	//Test 15: Angle 0.3, R =  12.00
	// X = 12.00 * cos(0.3), Y = 12.00 * sin(0.3)
	run_test(11.999835, 0.062831, 0.005235, 12.00);


	printf("---RMS error----------------------------------\n");
	printf("----------------------------------------------\n");
	printf("   RMSE(R)           RMSE(Theta)\n");
	printf("%0.15f %0.15f\n", rmse_r.error, rmse_theta.error);
	printf("----------------------------------------------\n");


	float error_threshold = 0.001;

    int success = (rmse_r.error < error_threshold) && (rmse_theta.error < error_threshold);

    if (success) return 0;
    else return 1;

}
