#include "axis_fp_example.h"


void axis_fp_example(
	hls::stream<transPkt>&A, 
	hls::stream<transPkt>&B, 
	hls::stream<transPkt>&C, 
	hls::stream<transPkt>&D
){
#pragma HLS INTERFACE mode=axis port=A,B,C,D
#pragma HLS INTERFACE mode=s_axilite port=return
	// A and B must contain the same nonzero number of complete float samples.
	while (true) {
		const transPkt Apkt = A.read();
		const transPkt Bpkt = B.read();
		const float Adata = Apkt.data;
		const float Bdata = Bpkt.data;
		const bool last = (Apkt.last == 1 || Bpkt.last == 1);

		transPkt Cpkt, Dpkt;
		Cpkt.data = Adata + Bdata;
		Cpkt.keep = 0xf; 
		Cpkt.strb = 0xf; 
		Cpkt.last = last;

		Dpkt.data = Adata - Bdata;
		Dpkt.keep = 0xf;
		Dpkt.strb = 0xf;
		Dpkt.last = last;

		C.write(Cpkt);
		D.write(Dpkt);
		
		if (last) {
			break;
		}
	}
	return;
}
