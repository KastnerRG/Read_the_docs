#include "ap_axi_sdata.h"
#include "hls_stream.h"

#define LEN 10

typedef hls::axis<float, 0,0,0> transPkt;


void axis_fp_example(
	hls::stream<transPkt>&A, 
	hls::stream<transPkt>&B, 
	hls::stream<transPkt>&C,
	hls::stream<transPkt>&D
);
