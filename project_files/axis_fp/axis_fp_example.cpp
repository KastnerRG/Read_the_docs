#include "axis_fp_example.h"
#include <math.h>


void axis_fp_example(
	hls::stream<transPkt>&A, 
	hls::stream<transPkt>&B, 
	hls::stream<transPkt>&C, 
	hls::stream<transPkt>&D
){
#pragma HLS INTERFACE mode=axis port=A,B,C,D
#pragma HLS INTERFACE mode=s_axilite port=return
	//fp_int Adata, Bdata, Cdata, Ddata;
	transPkt Apkt, Bpkt, Cpkt, Dpkt;
	float Adata, Bdata, Cdata, Ddata;

	while (true) {
		Apkt = A.read();
		Bpkt = B.read();
		// Use integer type to read from the AXIS packets
		Adata = Apkt.data;
		Bdata = Bpkt.data;
		//// Do the calculation s with floating points
		Cdata = Adata + Bdata;
		Ddata = Adata - Bdata;
		////AXIS output packets are expecting integer type
		Apkt.data = Cdata;
		Bpkt.data = Ddata;
		// Re-use the input packets to preserve side channel signals
		// Write the results to the output streams
		C.write(Apkt);
		D.write(Bpkt);
		if (Apkt.last == 1 || Bpkt.last == 1) {
			break;
		}
	}
	return;
}
