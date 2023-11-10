#include "example_test.h"
#include <math.h>

/*
void example(hls::stream<ap_axis<32,2,5,6>> &A, hls::stream<ap_axis<32,2,5,6>>&B, hls::stream<ap_axis<32,2,5,6>>&C){
#pragma HLS INTERFACE mode=axis port=A,B,C
#pragma HLS INTERFACE mode=s_axilite port=return
	ap_axis<32,2,5,6> tmp1, tmp2, tmp3;
	for (int i=0; i<LEN; i ++){
		A.read(tmp1);
		B.read(tmp2);
		tmp3 = tmp1;
		tmp3.data = tmp1.data.to_int() + tmp2.data.to_int() + 5;
		C.write(tmp3);
	}
}
*/

void example(hls::stream<transPkt> &A, hls::stream<transPkt>&B, hls::stream<transPkt>&C){
#pragma HLS INTERFACE mode=axis port=A,B,C
#pragma HLS INTERFACE mode=s_axilite port=return
	fp_int Adata, Bdata, Cdata;
	transPkt Apkt, Bpkt;

	for (unsigned int i = 0; i<LEN; i++){
		Apkt = A.read();
		Bpkt = B.read();
		// Use integer type to read from the AXIS packets
		Adata.i = Apkt.data;
		Bdata.i = Bpkt.data;
		// Do the calculation s with floating points
		Cdata.fp = Adata.fp + Bdata.fp;
		//AXIS output packets are expecting integer type
		Apkt.data = Cdata.i;
		C.write(Apkt);
	}
}
