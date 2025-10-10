/*
	Filename: fir_test.h
		FIR lab wirtten for WES/CSE237C class at UCSD.
		Testbench file
		Calls fir() function from fir.cpp
		Compares the output from fir() with out.gold.dat
*/

#include <iostream>
#include "mul.h"

using namespace std;

void mul(data_t* out, data_t in);

int main(
  int argc, 
  char *argv[]
  )
{
  data_t x=5;
  data_t y;
  mul(&y, x);
  if(y!=2*x){
    cout << "Test Failed: output(" << y << ") is not equal to 2x" << x << endl;
    return 1;
  }else{
          cout << "Test Passed" << endl;
  }
  return 0;
}