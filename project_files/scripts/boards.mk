# Shared HLS and board build rules; define TOP and GEN_TCL before including.
TARGET ?= pynq
PYTHON ?= python3
VIVADO ?= vivado
JOBS ?= 4
BOARD_REPO ?=
ZU3_DDR ?= 4gb
USE_VITIS ?= 1
ifeq ($(USE_VITIS),1)
HLS_COMPILER ?= vitis-run --mode hls --tcl
# Vitis 2025 bundles HLS without exposing a vitis_hls launcher on PATH.
VITIS_HLS_PATH ?= $(shell command -v vitis_hls 2>/dev/null || command -v vitis-run 2>/dev/null)
VITIS_RUN_PATH ?= $(shell command -v vitis-run 2>/dev/null)
# HLS headers live in Vitis/<ver>/include, but 2024.x launches vitis_hls from
# Vitis_HLS/<ver>/bin, so probe each candidate root for ap_int.h.
VITIS_HLS_ROOT := $(abspath $(dir $(VITIS_HLS_PATH))/..)
VHLS_CANDIDATES := $(XILINX_HLS) $(VITIS_HLS_ROOT) \
  $(abspath $(VITIS_HLS_ROOT)/../../Vitis/$(notdir $(VITIS_HLS_ROOT))) \
  $(if $(VITIS_RUN_PATH),$(abspath $(dir $(VITIS_RUN_PATH))/..)) $(XILINX_VITIS)
VHLS ?= $(or $(firstword $(foreach d,$(VHLS_CANDIDATES),$(if $(wildcard $(d)/include/ap_int.h),$(d)))),$(VITIS_HLS_ROOT))
ifeq ($(wildcard $(VHLS)/include/ap_int.h),)
ifeq ($(strip $(VITIS_HLS_PATH)),)
$(warning Could not find "vitis_hls" or "vitis-run" on PATH; C++ testbenches will not find HLS headers)
else ifneq ($(wildcard $(VITIS_HLS_PATH)),)
$(warning No include/ap_int.h under VHLS=$(VHLS); set VHLS=<Vitis install dir>)
endif
endif
else
HLS_COMPILER ?= vivado_hls -f
VHLS ?= $(shell vivado_hls -r)
endif
HLS_INPUT ?= $(TOP).cpp
HLS_CONFIG_FILE ?= $(CURDIR)/__hls_config__.ini

ifeq ($(TARGET),pynq)
FPGA_PART := xc7z020clg400-1
BOARD_PART ?= tul.com.tw:pynq-z2:part0:1.0
HLS_SUFFIX :=
else ifeq ($(TARGET),zu3)
FPGA_PART := xczu3eg-sfvc784-2-e
BOARD_PART ?= realdigital.org:aup-zu3-$(ZU3_DDR):part0:1.0
HLS_SUFFIX := _zu3
else
$(error Unsupported TARGET '$(TARGET)'; use TARGET=pynq or TARGET=zu3)
endif

BOARD_SCRIPTS := $(dir $(abspath $(GEN_TCL)))
BOARD_CACHE ?= $(abspath $(BOARD_SCRIPTS)/../../board_files)
# Keep the caller's Python executable when Vivado changes PATH internally.
BOARD_PYTHON := $(shell command -v "$(PYTHON)" 2>/dev/null)
HLS_COMPONENT := $(TOP)$(HLS_SUFFIX).comp
HLS_STAMP := $(HLS_COMPONENT)/.csynth
HLS_SCRIPT := $(TOP)$(HLS_SUFFIX).tcl
HLS_EXPORT := export_$(TOP)$(HLS_SUFFIX).tcl
OVERLAY_DIR := $(CURDIR)/build/$(TARGET)
BD_TCL ?= $(BOARD_SCRIPTS)overlay.tcl
.DEFAULT_GOAL := hls

$(HLS_SCRIPT): $(wildcard *.cpp *.h *.hpp directives.tcl) $(HLS_CONFIG_FILE) $(GEN_TCL) $(MAKEFILE_LIST)
	$(PYTHON) $(GEN_TCL) -c $(HLS_CONFIG_FILE) -i $(HLS_INPUT) -o $@ --part $(FPGA_PART) --component $(HLS_COMPONENT) $(HLS_FLAGS)

$(HLS_STAMP): $(HLS_SCRIPT)
	$(HLS_COMPILER) $<
	touch $@

hls: $(HLS_STAMP)

report: hls
	cp -f $(HLS_COMPONENT)/hls/syn/report/$(TOP)_csynth.rpt $(CURDIR)

# One IP export path for both manual imports and the Vivado board build.
ip: hls
	@printf '%s\n' 'open_component $(HLS_COMPONENT)' \
	  'export_design -format ip_catalog -rtl verilog -vendor xilinx.com -library hls -version 1.0 -ipname $(TOP)' \
	  'exit' > $(HLS_EXPORT)
	$(HLS_COMPILER) $(HLS_EXPORT)

board-ip: ip

block-design bitstream: ip
	PP4FPGA_HOST_LD_LIBRARY_PATH="$${LD_LIBRARY_PATH-}" $(VIVADO) -mode batch -source "$(BOARD_SCRIPTS)build_bitstream.tcl" \
	  -tclargs "$(TARGET)" "$(FPGA_PART)" "$(BOARD_PART)" "$(BOARD_REPO)" \
	  "$(CURDIR)/$(HLS_COMPONENT)/hls/impl/ip" "$(TOP)" "$(OVERLAY_DIR)" "$(JOBS)" "$(BD_TCL)" "$@" \
	  "$(BOARD_CACHE)" "$(BOARD_PYTHON)"

clean-board:
	rm -rf "$(OVERLAY_DIR)"

# Remove only generated Tcl and the selected board's component.
clean: clean-board
	rm -rf "$(HLS_COMPONENT)" "$(HLS_SCRIPT)" "$(HLS_EXPORT)" export_board_$(TOP)$(HLS_SUFFIX).tcl logs hls
	rm -f *.o *_test.bin *.log *.rpt out.dat *.jou

.PHONY: hls report ip board-ip block-design bitstream clean-board clean
