# Usage: vivado -mode batch -source build_bitstream.tcl -tclargs
#        target part board_part board_repo ip_repo top output_dir jobs bd_tcl mode board_cache python
if {$argc != 12} {
    error "Expected: target part board_part board_repo ip_repo top output_dir jobs bd_tcl mode board_cache python"
}
lassign $argv target part board_part board_repo ip_repo top output_dir jobs bd_tcl build_mode board_cache python
if {$target ni {pynq zu3}} { error "Unsupported target: $target" }
if {$build_mode ni {block-design bitstream}} { error "Unsupported build mode: $build_mode" }
if {![string is integer -strict $jobs] || $jobs < 1} { error "JOBS must be a positive integer" }
source [file join [file dirname [info script]] ensure_board.tcl]
pp4fpga::ensure_board $target $board_part $board_repo $board_cache $python
if {![file exists [file join $ip_repo component.xml]]} {
    error "HLS IP not found at $ip_repo; run make ip TARGET=$target first."
}
if {![file isfile $bd_tcl]} { error "Block-design script not found: $bd_tcl" }

file mkdir $output_dir
create_project -force overlay [file join $output_dir vivado] -part $part
set_property board_part $board_part [current_project]
set_property ip_repo_paths [list [file normalize $ip_repo]] [current_project]
update_ip_catalog

# The script creates design_1 using target, top, and the exported HLS IP.
source $bd_tcl
assign_bd_address
validate_bd_design
save_bd_design
if {$build_mode eq "block-design"} {
    puts "Validated block design: [file join $output_dir vivado overlay.xpr]"
    return
}
set bd_file [get_files */design_1.bd]
generate_target all $bd_file
add_files -norecurse [make_wrapper -files $bd_file -top]
set_property top design_1_wrapper [current_fileset]
update_compile_order -fileset sources_1
launch_runs impl_1 -to_step write_bitstream -jobs $jobs
wait_on_run impl_1
if {[get_property PROGRESS [get_runs impl_1]] ne "100%" ||
    ![string match "*write_bitstream Complete*" [get_property STATUS [get_runs impl_1]]]} {
    error "Implementation failed: [get_property STATUS [get_runs impl_1]]"
}
set bit_file [file join [get_property DIRECTORY [get_runs impl_1]] design_1_wrapper.bit]
set hwh_file [file join [get_property DIRECTORY [current_project]] overlay.gen sources_1 bd design_1 hw_handoff design_1.hwh]
if {![file isfile $bit_file] || ![file isfile $hwh_file]} {
    error "Vivado did not produce both the bitstream and hardware handoff."
}
file copy -force $bit_file [file join $output_dir $top.bit]
file copy -force $hwh_file [file join $output_dir $top.hwh]
puts "Overlay ready: [file join $output_dir $top.bit] and [file join $output_dir $top.hwh]"
