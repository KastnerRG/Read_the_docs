# Small wrapper for projects previously built only through script.tcl.
include $(dir $(GEN_TCL))boards.mk

NON_TEST_CPP = $(filter-out %_test.cpp,$(wildcard *.cpp))
%_test.bin: %_test.cpp $(NON_TEST_CPP) $(wildcard *.h *.hpp)
	$(CXX) -I$(VHLS)/include $< $(NON_TEST_CPP) -g -o $@
%.log: %.bin
	./$< > $@ 2>&1
test: $(patsubst %.cpp,%.log,$(wildcard *_test.cpp))

.PHONY: test
.PRECIOUS: %.bin
