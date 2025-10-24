#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "axis_fp_example.h"


int main () {
	printf("-------axis_fp_example Test-------\n");
	hls::stream<transPkt> A, B, C, D;
	transPkt pktA, pktB, pktC, pktD;
	//fp_int dataA, dataB, dataC, dataD;
	float dataA, dataB, dataC, dataD;

	float inputA[LEN];
	float inputB[LEN];

	for (int i = 0; i < LEN; i++) {
		inputA[i] = i;
		inputB[i] = 2*i;
	}

	for (int i = 0; i < LEN; i++) {
		pktA.data = inputA[i];
		pktB.data = inputB[i];
		// Prepare tlast signal
		if (i == LEN -1) {
			pktA.last = 1;
			pktB.last = 1;
		} else {
			pktA.last = 0;
			pktB.last = 0;
		}
		A.write(pktA);
		B.write(pktB);
	}

	axis_fp_example(A, B, C, D);

	for (int i = 0; i < LEN; i++) {
		
		// Read the results from output streams
		pktC = C.read();
		pktD = D.read();
		dataC = pktC.data;
		dataD = pktD.data;
		// Print the results
		if (dataC != inputA[i] + inputB[i] || dataD != inputA[i] - inputB[i]) {
			printf("Test failed at index %d: %.2f + %.2f != %.2f or %.2f - %.2f != %.2f\n", i, inputA[i], inputB[i], dataC, inputA[i], inputB[i], dataD);
			return 1;
		}
		if (i == LEN -1) {
			if (pktC.last != 1 || pktD.last != 1) {
				printf("Test failed: Expecting tlast signal\n");
				return 1;
			}
		} else {
			if (pktC.last != 0 || pktD.last != 0) {
				printf("Test failed at index %d: Not expecting tlast signal\n", i);
				return 1;
			}
		}
	}
	printf("-----------Test passed!-----------\n");
	return 0;
}
