# This makefile was tested with Vivado HLS 2019.2
# and Vitis v2024.1
# 
#

# select the HLS compiler to use (vivado_hls or vitis)
TOP = cordiccart2pol
# -------------------------------------------------------

EXAMPLES_CPP = $(shell ls *_test.cpp)
EXAMPLES_BIN = $(patsubst %.cpp,%,$(EXAMPLES_CPP))
EXAMPLES_LOG = $(patsubst %.cpp,%.log,$(EXAMPLES_CPP))

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

%_test.bin: %_test.cpp %.cpp 
	LD_LIBRARY_PATH=$(LD_LIBRARY_PATH) $(CXX) -I$(VHLS)/include $? -g -o $@

#  missing cos_table and sin_table definition. No testbench files available
#	dft.c \
#	dft_precompute.c \

%.log: %.bin
	./$< > $@ 2>&1 || { s=$$?; echo "./$< > $@ failed $$s" >&2; exit $$s; }

test: $(EXAMPLES_LOG)

.PHONY: clean hls test report ip

# Prevent make from deleting the .bin intermediate files
.PRECIOUS: %.bin %.tcl
