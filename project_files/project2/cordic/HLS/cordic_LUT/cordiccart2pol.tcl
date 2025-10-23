open_component cordiccart2pol.comp -reset
add_files [list cordiccart2pol.cpp]
add_files -tb [list cordiccart2pol_test.cpp]
set_top cordiccart2pol
puts "Running: set_top cordiccart2pol"
set_part xc7z020-clg400-1
puts "Running: set_part xc7z020-clg400-1"
create_clock -period 10
csynth_design

exit