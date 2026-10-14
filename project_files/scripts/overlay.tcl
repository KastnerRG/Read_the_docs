# A single HLS accelerator with AXI-Lite control, optional AXI memory ports,
# and simple-mode DMA channels for AXI streams (axi_dma_0, axi_dma_1, ...).
create_bd_design design_1
set accelerator [create_bd_cell -type ip -vlnv xilinx.com:hls:$top:1.0 ${top}_0]
set controls [get_bd_intf_pins -quiet -of_objects $accelerator -filter {VLNV == xilinx.com:interface:aximm_rtl:1.0 && MODE == Slave}]
set memory_ports [get_bd_intf_pins -quiet -of_objects $accelerator -filter {VLNV == xilinx.com:interface:aximm_rtl:1.0 && MODE == Master}]
set streams [lsort [get_bd_intf_pins -quiet -of_objects $accelerator -filter {VLNV == xilinx.com:interface:axis_rtl:1.0}]]
set supported [concat $controls $memory_ports $streams]
foreach pin [get_bd_intf_pins -of_objects $accelerator] {
    if {$pin ni $supported} {
        error "Unsupported accelerator interface $pin; provide a custom BD_TCL."
    }
}
if {[llength $controls] == 0} {
    error "The accelerator needs an s_axilite control interface. Add the lab's HLS interface pragmas, or provide a custom BD_TCL."
}
set interface_pins [get_bd_pins -of_objects $supported]
foreach pin [get_bd_pins -of_objects $accelerator] {
    if {$pin ni $interface_pins && [get_property TYPE $pin] ni {clk rst intr}} {
        error "Unmapped accelerator port $pin; add AXI interface pragmas or provide a custom BD_TCL."
    }
}

set needs_memory [expr {[llength $memory_ports] + [llength $streams] > 0}]
if {$target eq "pynq"} {
    set ps [create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 processing_system7_0]
    apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 -config \
        {make_external "FIXED_IO, DDR" apply_board_preset "1"} $ps
    set_property -dict [list CONFIG.PCW_USE_M_AXI_GP0 1 CONFIG.PCW_USE_S_AXI_HP0 $needs_memory \
        CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ 100] $ps
    set control_master $ps/M_AXI_GP0
    set memory_slave $ps/S_AXI_HP0
    set clock $ps/FCLK_CLK0
    set ps_reset $ps/FCLK_RESET0_N
} else {
    set ps [create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e:3.5 zynq_ultra_ps_e_0]
    apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1"} $ps
    set_property -dict [list CONFIG.PSU__USE__M_AXI_GP0 0 CONFIG.PSU__USE__M_AXI_GP1 0 \
        CONFIG.PSU__USE__M_AXI_GP2 1 CONFIG.PSU__USE__S_AXI_GP2 $needs_memory \
        CONFIG.PSU__FPGA_PL0_ENABLE 1 CONFIG.PSU__CRL_APB__PL0_REF_CTRL__FREQMHZ 100] $ps
    set control_master $ps/M_AXI_HPM0_LPD
    set memory_slave $ps/S_AXI_HP0_FPD
    set clock $ps/pl_clk0
    set ps_reset $ps/pl_resetn0
}

# Create a shared reset synchronized to the PL clock.
set reset [create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 rst_100m]
connect_bd_net [get_bd_pins $clock] [get_bd_pins $reset/slowest_sync_clk]
connect_bd_net [get_bd_pins $ps_reset] [get_bd_pins $reset/ext_reset_in]
set constant [create_bd_cell -type ip -vlnv xilinx.com:ip:xlconstant:1.1 clock_locked]
set_property CONFIG.CONST_VAL 1 $constant
connect_bd_net [get_bd_pins $constant/dout] [get_bd_pins $reset/dcm_locked]
foreach pin [get_bd_pins -of_objects $ps -filter {TYPE == clk && DIR == I}] {
    connect_bd_net [get_bd_pins $clock] $pin
}
foreach pin [get_bd_pins -of_objects $accelerator -filter {TYPE == clk}] {
    connect_bd_net [get_bd_pins $clock] $pin
}
foreach pin [get_bd_pins -of_objects $accelerator -filter {TYPE == rst}] {
    if {[get_property CONFIG.POLARITY $pin] eq "ACTIVE_HIGH"} {
        connect_bd_net [get_bd_pins $reset/peripheral_reset] $pin
    } else {
        connect_bd_net [get_bd_pins $reset/peripheral_aresetn] $pin
    }
}

# Pair sorted input and output streams to preserve the notebooks' DMA names.
set input_streams {}
set output_streams {}
foreach stream $streams {
    if {![get_property CONFIG.HAS_TLAST $stream]} {
        error "Stream $stream needs TLAST for AXI DMA; use ap_axis/ap_axiu or provide a custom BD_TCL."
    }
    if {[get_property MODE $stream] eq "Slave"} {
        lappend input_streams $stream
    } else {
        lappend output_streams $stream
    }
}
set dma_count [expr {max([llength $input_streams], [llength $output_streams])}]
for {set dma_index 0} {$dma_index < $dma_count} {incr dma_index} {
    set input_stream [lindex $input_streams $dma_index]
    set output_stream [lindex $output_streams $dma_index]
    set has_input [expr {$input_stream ne ""}]
    set has_output [expr {$output_stream ne ""}]
    set dma [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dma:7.1 axi_dma_$dma_index]
    set_property -dict [list CONFIG.c_include_sg 0 CONFIG.c_sg_length_width 26 \
        CONFIG.c_addr_width [expr {$target eq "zu3" ? 64 : 32}] \
        CONFIG.c_include_mm2s $has_input CONFIG.c_include_s2mm $has_output] $dma
    if {$has_input} {
        set width [expr {8 * [get_property CONFIG.TDATA_NUM_BYTES $input_stream]}]
        set_property CONFIG.c_m_axis_mm2s_tdata_width $width $dma
        connect_bd_intf_net [get_bd_intf_pins $dma/M_AXIS_MM2S] $input_stream
        lappend memory_ports [get_bd_intf_pins $dma/M_AXI_MM2S]
    }
    if {$has_output} {
        set width [expr {8 * [get_property CONFIG.TDATA_NUM_BYTES $output_stream]}]
        set_property CONFIG.c_s_axis_s2mm_tdata_width $width $dma
        connect_bd_intf_net $output_stream [get_bd_intf_pins $dma/S_AXIS_S2MM]
        lappend memory_ports [get_bd_intf_pins $dma/M_AXI_S2MM]
    }
    lappend controls [get_bd_intf_pins $dma/S_AXI_LITE]
    foreach pin [get_bd_pins -of_objects $dma -filter {TYPE == clk && DIR == I}] {
        connect_bd_net [get_bd_pins $clock] $pin
    }
    connect_bd_net [get_bd_pins $reset/peripheral_aresetn] [get_bd_pins $dma/axi_resetn]
}

# Explicit AXI interconnects keep clocks and reset wiring identical on both boards.
proc connect_axi {name masters slaves clock reset} {
    set interconnect [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 $name]
    set_property -dict [list CONFIG.NUM_SI [llength $masters] CONFIG.NUM_MI [llength $slaves]] $interconnect
    set index 0
    foreach master $masters {
        connect_bd_intf_net $master [get_bd_intf_pins [format "%s/S%02d_AXI" $name $index]]
        incr index
    }
    set index 0
    foreach slave $slaves {
        connect_bd_intf_net [get_bd_intf_pins [format "%s/M%02d_AXI" $name $index]] $slave
        incr index
    }
    foreach pin [get_bd_pins -of_objects $interconnect -filter {TYPE == clk && DIR == I}] {
        connect_bd_net [get_bd_pins $clock] $pin
    }
    foreach pin [get_bd_pins -of_objects $interconnect -filter {TYPE == rst && DIR == I}] {
        connect_bd_net [get_bd_pins $reset/interconnect_aresetn] $pin
    }
}
connect_axi control_interconnect [list [get_bd_intf_pins $control_master]] $controls $clock $reset
if {$needs_memory} {
    connect_axi memory_interconnect $memory_ports [list [get_bd_intf_pins $memory_slave]] $clock $reset
}
# Interrupts are intentionally unused; the supplied notebooks poll completion.
