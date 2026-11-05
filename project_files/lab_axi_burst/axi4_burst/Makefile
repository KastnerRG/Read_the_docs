# Vitis HLS 2024.2
TOP = axi4_sqrt
PYTHON ?= python3
HLS_COMPILER ?= vitis-run --mode hls --tcl
GEN_TCL = $(CURDIR)/../../scripts/gen_hls_runner_script.py
HLS_CONFIG_FILE = $(CURDIR)/__hls_config__.ini
HLS_COMPONENT = $(TOP).comp
HLS_REPORT = $(HLS_COMPONENT)/hls/syn/report/$(TOP)_csynth.rpt
RUN_CHECKED = sh $(dir $(GEN_TCL))run_checked.sh

.DEFAULT_GOAL := hls

$(TOP).tcl: $(wildcard *.cpp *.h *.hpp) $(HLS_CONFIG_FILE) $(GEN_TCL) Makefile
	$(PYTHON) $(GEN_TCL) -c $(HLS_CONFIG_FILE) -i $(TOP).cpp -o $@ --m-axi-addr32

$(HLS_COMPONENT)/.csynth: $(TOP).tcl
	$(RUN_CHECKED) "$(HLS_REPORT)" "HLS synthesis" $(HLS_COMPILER) $<
	touch $@

hls: $(HLS_COMPONENT)/.csynth

report: hls
	cp -f $(HLS_REPORT) $(CURDIR)

sim: HLS_COMMAND = csim_design
sim: HLS_OUTPUT = $(HLS_COMPONENT)/hls/csim/report/$(TOP)_csim.log
cosim: HLS_COMMAND = cosim_design
cosim: HLS_OUTPUT = $(HLS_COMPONENT)/hls/sim/report/$(TOP)_cosim.rpt
ip: HLS_COMMAND = export_design -format ip_catalog -rtl verilog -vendor xilinx.com -library hls -version 1.0 -ipname $(TOP)
ip: HLS_OUTPUT = $(HLS_COMPONENT)/hls/impl/ip/component.xml

sim cosim ip: hls
	@printf '%s\n' 'open_component $(HLS_COMPONENT)' '$(HLS_COMMAND)' 'exit' > $@_$(TOP).tcl
	$(RUN_CHECKED) "$(HLS_OUTPUT)" "HLS $@" $(HLS_COMPILER) $@_$(TOP).tcl

clean:
	rm -rf $(HLS_COMPONENT) logs .Xil
	rm -f $(TOP).tcl sim_$(TOP).tcl cosim_$(TOP).tcl ip_$(TOP).tcl *.log *.jou *.rpt

.PHONY: hls report sim cosim ip clean
