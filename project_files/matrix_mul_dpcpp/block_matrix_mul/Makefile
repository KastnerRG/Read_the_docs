DPCPP_CXX = dpcpp
DPCPP_CXXFLAGS = -std=c++17 -g -o
DPCPP_LDFLAGS = 
DPCPP_EXE_NAME = block_matrix_mul_dpcpp
DPCPP_SOURCES = src/block_matrix_mul_dpcpp.cpp


all:
	$(DPCPP_CXX) $(DPCPP_CXXFLAGS) $(DPCPP_EXE_NAME) $(DPCPP_SOURCES) $(DPCPP_LDFLAGS)

build_dpcpp:
	$(DPCPP_CXX) $(DPCPP_CXXFLAGS) $(DPCPP_EXE_NAME) $(DPCPP_SOURCES) $(DPCPP_LDFLAGS)


fpga_emulator:
	dpcpp -fintelfpga -DFPGA_EMULATOR $(DPCPP_SOURCES) -o $(DPCPP_EXE_NAME).fpga_emu

fpga_report:
	dpcpp -fintelfpga -Xshardware -fsycl-link=early $(DPCPP_SOURCES) -o fpga_compile_report.a

fpga_hardware:
	dpcpp -fintelfpga -Xshardware $(DPCPP_SOURCES) -o $(DPCPP_EXE_NAME).fpga


run:
	./$(DPCPP_EXE_NAME)

run_dpcpp:
	./$(DPCPP_EXE_NAME)
    
run_fpga_emulator:
	./$(DPCPP_EXE_NAME).fpga_emu

clean: 
	rm -rf $(DPCPP_EXE_NAME) 
