# This makefile was tested with Vivado HLS 2019.2
# and Vitis v2024.1
# 
#

# select the HLS compiler to use (vivado_hls or vitis)
TOP = phasedetector
# -------------------------------------------------------

USE_VITIS=1

ifeq ($(USE_VITIS),1)

VITIS_HLS_PATH := $(shell which vitis_hls 2>/dev/null)
ifeq ($(strip $(VITIS_HLS_PATH)),)
  $(error Could not find "vitis_hls" on PATH.)
endif
VITIS_COMPILER := $(shell dirname "$(VITIS_HLS_PATH)")

ifneq (,$(findstring 2024.2,$(VITIS_HLS_PATH)))
  VHLS := $(VITIS_COMPILER)/../../../Vitis/2024.2
else
  VHLS := $(VITIS_COMPILER)/../../../Vitis_HLS/2024.1
endif

HLS_COMPILER=vitis-run --mode hls --tcl 
else
VHLS := $(shell vivado_hls -r)
HLS_COMPILER=vivado_hls -f
endif


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

#$(warning $(EXAMPLES_LOG))

%.o: %.cpp
	$(CXX) -I$(VHLS)/include -c $< -o $@


%_test.bin: %_test.cpp $(NON_TEST_CPP)
	# Link the test executable against the testbench and all non-test sources.
	LD_LIBRARY_PATH=$(LD_LIBRARY_PATH) $(CXX) -I$(VHLS)/include $^ -g -o $@

#  missing cos_table and sin_table definition. No testbench files available
#	dft.c \
#	dft_precompute.c \



# For HLS: synthesize the design whose top is $(TOP).
# Generate a single $(TOP).tcl from all HLS source files, then run the HLS compiler
# on that tcl to create the $(TOP).comp directory.
CXX_HLS_TARGET_FILES = $(TOP).cpp

# Default HLS targets: the component directory for TOP
HLS_TARGETS = $(TOP).comp

%.comp: %.tcl
	$(HLS_COMPILER) $< || { s=$$?; echo "$(HLS_COMPILER) $< failed $$s" >&2; exit $$s; }

# Generate a single TCL for the top-level HLS build. The gen script expects
# a single input name (the key used to look up the `files` list in the INI).
# It will then write a Tcl that calls add_files with the files listed in the
# INI. If you prefer to manage files entirely from the Makefile, you can add
# them to the INI on-the-fly or modify the generator script.
$(TOP).tcl: $(TOP).cpp $(HLS_CONFIG_FILE)
	$(GEN_TCL) -c $(HLS_CONFIG_FILE) -i $(TOP).cpp -o $@

.PHONY: $(TOP).tcl

%.log: %.bin
	./$< > $@ 2>&1 || { s=$$?; echo "./$< > $@ failed $$s" >&2; exit $$s; }


hls: $(HLS_TARGETS)

test: $(EXAMPLES_LOG)

report: hls
	cp -f $(TOP).comp/hls/syn/report/$(TOP)_csynth.rpt $(CURDIR) || true

$(CURDIR)/export_$(TOP).tcl:
	@{ \
	    echo "open_component $(TOP).comp"; \
		echo "export_design -format ip_catalog -rtl verilog -version 1.0 -ipname $(TOP) "; \
		echo "exit"; \
	} > $(CURDIR)/export_$(TOP).tcl


ip: hls $(CURDIR)/export_$(TOP).tcl
	$(HLS_COMPILER) $(CURDIR)/export_$(TOP).tcl || { s=$$?; echo "$(HLS_COMPILER) -source $(CURDIR)/export_$(TOP).tcl failed $$s" >&2; exit $$s; }

clean:
	rm -rf *.o *.log *.bin *.tcl *.comp *.rpt logs hls out.dat *.jou

.PHONY: clean hls test report ip

# Prevent make from deleting the .bin intermediate files
.PRECIOUS: %.bin %.tcl 

