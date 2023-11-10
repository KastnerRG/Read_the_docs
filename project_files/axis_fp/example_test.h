#include "ap_axi_sdata.h"
#include "hls_stream.h"

#define LEN 10

typedef ap_axis<32,2,5,6> transPkt;

union fp_int {
	int i;
	float fp;
};

//void example(hls::stream<ap_axis<32,2,5,6>> &A, hls::stream<ap_axis<32,2,5,6>>&B, hls::stream<ap_axis<32,2,5,6>>&C);
void example(hls::stream<transPkt> &A, hls::stream<transPkt>&B, hls::stream<transPkt>&C);
