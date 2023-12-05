#include "bnn.h"
#include <stdio.h>


void verify_output(string name, const int golden[10], int predicted[10]){
    cout<<"-----------------------------------------------------------"<<endl;
	cout<<"Verifying the sample: "<<name<<endl;
    int PASS = 1;
	for(int i=0;i<10;i++) {
		if (golden[i]!=predicted[i]) {
			PASS=0;
			cout<<"Wrong output: Expected: "<<golden[i]<<" Obtained: "<<predicted[i]<<endl;
		}
	}

	if(PASS==0) {
		cout<<"Sample: "<<name<<" FAILED"<<endl;
	} else {
		cout<<"Sample: "<<name<<" PASSED"<<endl;
	}

}

int main ()
{
    const unsigned int sample1[25] ={4294967295, 4294967295, 4294967295, 4294967295, 4294967295,
    	       4294967295, 4290838527, 4227859455, 3221241855, 3758358527,
    	       4232052735, 2281701368, 2147483407, 4294963455, 4294844415,
    	       4293132287, 4232052735, 2281701360, 2147483407, 4294959359,
    	       4294844415, 4290904063, 4229955583, 3288334335, 4294901760};
    // true label: 7
    const int sample1_golden_output[10] = {-2,   4,  -8,  14,  -4,   0, -42,  48,  -4,   2};

    const unsigned int sample2[25] ={4294967295, 4294967295, 4294967292,  134217600, 1073737731,
    	       4294837311, 4292985855, 4282138623, 4286840831, 4034920447,
    	        268435424, 4294966303, 4294951935, 4294459391, 4278714367,
    	       4034920447,  268435440,   67239680,    2093056,   33521671,
    	       4294967295, 4294967295, 4294967295, 4294967295, 4294901760};
     // true label:2
    const int sample2_golden_output[10] = {2,   0,  48,  10, -20,   4,   2, -16,   4, -14};

    const unsigned int sample3[25] ={4294967295, 4294967295, 4294967295, 4294967295,  536870897,
    	       4294967103, 4294960127, 4294852607, 4293132287, 4236247039,
    	       3355443196, 2147483527, 4294965503, 4294938623, 4294049791,
    	       4280287231, 4060086271,  536870881, 4294966815, 4294951935,
    	       4294721535, 4294967295, 4294967295, 4294967295, 4294901760};
    // true label:1
    const int sample3_golden_output[10] = {-16,  42,   2,   4,  -2, -14,   8,   2,  14,  -8};


	ITYPE out1[10];
	ITYPE out2[10];
	ITYPE out3[10];
	for(int i=0;i<10;i++) {
		out1[i] = 0;
		out2[i] = 0;
		out3[i] = 0;
	}


	bnn(sample1, out1);
	bnn(sample2, out2);
	bnn(sample3, out3);

	verify_output("Sample 1", sample1_golden_output, out1);
	verify_output("Sample 1", sample2_golden_output, out2);
	verify_output("Sample 1", sample3_golden_output, out3);

	return 0;

}

