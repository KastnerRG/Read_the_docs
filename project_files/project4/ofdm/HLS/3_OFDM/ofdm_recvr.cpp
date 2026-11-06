#include "fft.h"

// This top level function uses the FFT and qpsk_decode functions
// defined in the other cpp files. Inputs are read and written as described in the
// multiple DMAs lab

void ofdm_receiver(hls::stream<transPkt> &x_real, hls::stream<transPkt> &x_imag, hls::stream<transPkt> &out)
{
#pragma HLS INTERFACE mode=axis port=x_real,x_imag,out
#pragma HLS INTERFACE mode=s_axilite port=return
#pragma HLS DATAFLOW

	fp_int xr[SIZE], xi[SIZE];
	int D[SIZE];
	DTYPE X_R[SIZE], X_I[SIZE];
	transPkt xrPkt, xiPkt;

	// read from input stream
	for (int i = 0; i < SIZE; i += 1) {
		xrPkt = x_real.read();
		xr[i].i = xrPkt.data;
		X_R[i] = xr[i].fp;
		xiPkt = x_imag.read();
		xi[i].i = xiPkt.data;
		X_I[i] = xi[i].fp;
	}

	//Call fft
	DTYPE REV_R[SIZE], REV_I[SIZE];
	DTYPE Stage1_R[SIZE], Stage1_I[SIZE];
	DTYPE Stage2_R[SIZE], Stage2_I[SIZE];
	DTYPE Stage3_R[SIZE], Stage3_I[SIZE];
	DTYPE Stage4_R[SIZE], Stage4_I[SIZE];
	DTYPE Stage5_R[SIZE], Stage5_I[SIZE];
	DTYPE Stage6_R[SIZE], Stage6_I[SIZE];
	DTYPE Stage7_R[SIZE], Stage7_I[SIZE];
	DTYPE Stage8_R[SIZE], Stage8_I[SIZE];
	DTYPE Stage9_R[SIZE], Stage9_I[SIZE];
	DTYPE TEMP_R[SIZE], TEMP_I[SIZE];
	DTYPE OUT_R[SIZE], OUT_I[SIZE];

	bit_reverse(X_R, X_I, REV_R, REV_I);

	fft_stage_first(REV_R, REV_I, Stage1_R, Stage1_I);
	fft_stages(Stage1_R, Stage1_I, 2, Stage2_R, Stage2_I);
	fft_stages(Stage2_R, Stage2_I, 3, Stage3_R, Stage3_I);
	fft_stages(Stage3_R, Stage3_I, 4, Stage4_R, Stage4_I);
	fft_stages(Stage4_R, Stage4_I, 5, Stage5_R, Stage5_I);
	fft_stages(Stage5_R, Stage5_I, 6, Stage6_R, Stage6_I);
	fft_stages(Stage6_R, Stage6_I, 7, Stage7_R, Stage7_I);
	fft_stages(Stage7_R, Stage7_I, 8, Stage8_R, Stage8_I);
	fft_stages(Stage8_R, Stage8_I, 9, Stage9_R, Stage9_I);
	fft_stage_last(Stage9_R, Stage9_I, TEMP_R, TEMP_I);

	bit_reverse(TEMP_R, TEMP_I, OUT_R, OUT_I);
	qpsk_decode(OUT_R, OUT_I, D);

	// write to output stream
	for (int i = 0; i < SIZE; i += 1) {
		xrPkt.data = D[i];
		xrPkt.last = (i==SIZE-1)?1:0;
		out.write(xrPkt);
	}
}
