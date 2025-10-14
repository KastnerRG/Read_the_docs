open_component fir.comp -reset
add_files [list fir.cpp]
add_files -tb [list fir_test.cpp]
set_top fir
puts "Running: set_top fir"
set_part xc7z020-clg400-1
puts "Running: set_part xc7z020-clg400-1"
create_clock -period 10
csynth_design

exit