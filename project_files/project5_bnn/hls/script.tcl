open_project bnn
set_top bnn
add_files bnn.cpp
add_files bnn.h
add_files -tb bnn_test.cpp
open_solution "solution1"
set_part {xc7z020clg400-1}
create_clock -period 10 -name default
source "./directives.tcl"
