# This makefile was tested with Vivado HLS 2019.2
# and Vitis v2024.1
# 
#

# select the HLS compiler to use (vivado_hls or vitis)
TOP = phasedetector
# -------------------------------------------------------

EXAMPLES_CPP = $(shell ls *_test.cpp)
EXAMPLES_BIN = $(patsubst %.cpp,%,$(EXAMPLES_CPP))
EXAMPLES_LOG = $(patsubst %.cpp,%.log,$(EXAMPLES_CPP))

# Collect all non-test C++ sources so we can support multi-file designs.
# Non-test sources are any .cpp files that do not match '*_test.cpp'.
NON_TEST_CPP = $(filter-out %_test.cpp,$(wildcard *.cpp))

# Note: the HLS TCL generator used by this project expects a single input
# file name (the key used to select a section in the INI file). To include
# multiple implementation files in the HLS flow, add a `files = ...` entry
# for the top-level section in `__hls_config__.ini`. Example:
#
# [$(TOP).cpp]
# top = $(TOP)
# files = $(TOP).cpp helper1.cpp helper2.cpp
# tb_files = $(TOP)_test.cpp
#
# The generator will read `files` from the INI and include them in the Tcl
# it writes. We therefore call the generator with -i $(TOP).cpp below.

CC = gcc
CXX = g++

# insert new LD path to the LD_LIBRARY_PATH if it is not already there
# 
LD_PATH_NEW = /usr/lib/x86_64-linux-gnu
LD_LIBRARY_PATH := $(shell echo $(value LD_LIBRARY_PATH) | grep -q $(LD_PATH_NEW) || echo $(LD_PATH_NEW):)$(value LD_LIBRARY_PATH)

# ------------ Set the script path to generate tcl scripts ----------------
GEN_TCL = $(CURDIR)/../../../../scripts/gen_hls_runner_script.py
# -------------------------------------------------------------------------

#HLS_CONFIG_FILE = $(CURDIR)/__hls_config__.ini
HLS_CONFIG_FILE = $(CURDIR)/__hls_config__.ini

include $(dir $(GEN_TCL))boards.mk

#$(warning $(EXAMPLES_LOG))

%.o: %.cpp
	$(CXX) -I$(VHLS)/include -c $< -o $@

%_test.bin: %_test.cpp $(NON_TEST_CPP)
	# Link the test executable against the testbench and all non-test sources.
	LD_LIBRARY_PATH=$(LD_LIBRARY_PATH) $(CXX) -I$(VHLS)/include $^ -g -o $@

#  missing cos_table and sin_table definition. No testbench files available
#	dft.c \
#	dft_precompute.c \

%.log: %.bin
	./$< > $@ 2>&1 || { s=$$?; echo "./$< > $@ failed $$s" >&2; exit $$s; }

test: $(EXAMPLES_LOG)

.PHONY: clean hls test report ip

# Prevent make from deleting the .bin intermediate files
.PRECIOUS: %.bin %.tcl
