open_component mul.comp -reset
add_files [list mul.cpp]
add_files -tb [list mul_test.cpp]
set_top mul
puts "Running: set_top mul"
set_part xc7z020clg400-1
puts "Running: set_part xc7z020clg400-1"
create_clock -period 10
csynth_design

exit