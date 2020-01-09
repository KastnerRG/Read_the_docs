Lab4
====================

Interrupt Controller
********************

In this example we implement :math:`f(x)=x!` as an IP for PYNQ with interrupt controller.

1)Vivado HLS: C/C++ to RTL
--------------------------

In this section, you will write your code in C/C++ and convert it to RTL using Vivado_HLS.

1.1)Create a project
####################

Open Vivado_HLS tool, create a new project, and name it **pynq_fact**.

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3438488411-fact1.png

Set top function to **fact_intrpt**.

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/2082111028-fact2.png

Select **xc7z020clg400-1** as your part number.

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/2893940654-fact3.png

1.2)Write your code
###################

In **Explorer** section, right click on **Source**, and select new file. Create a **new file** and name it **fact_intrpt.cpp**. Complete your code as following:

.. code-block :: c

	void fact_intrpt(int* out, int in){
	    int i, k=1;
	    for(i=1; i<=in; i++){
		k = k*i;
	    }
	    *out = k;
	}

Open **Directive** tab and set **in**, **out**, and **return** ports as *s_axilite* interfaces. Your code should look like this:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/1951382475-fact4.png

1.3) Synthesize your code and export RTL
########################################

You can synthesize your code by clicking on **C Synthesis**. After finishing C synthesis, click on **Export RTL**.

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/1632797711-fact5.png

Now that you exported your RTL, you can close Vivado_HLS.

2) Vivado: RTL to Bitstream
---------------------------

In this section we generate a bitstream for our IP.

2.1)Create a new project
########################

Open Vivado tool and create a new project. Select an appropriate directory for your project and leave the project name as is, **project_1**.

Select **RTL Project** and check **Do not specify sources** at this time.

Set your part number to **xc7z020clg400-1**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3425856850-fact6.png

2.2) Import RTL
###############

In **Flow Navigator**, under **Project Manager**, click on **IP Catalog**.

On the newly opened window, right click and select **Add Repository**.

Navigate to your Vivado_HLS project directory and select **solution1 > impl > ip**.

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/1764593390-fact7.png

2.3) Add blocks to your design
##############################

In **Flow Navigator**, under **IP Integrator**, click on **Create Block Design**. Leave the name as is, **design_1**.

You can add IPs to your design by clicking on the **+** sign. Add the following IPs:

Add **ZYNQ7 Processing System** to your design:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/2209037604-fact8.png

Double click on **ZYNQ7 IP** to customize it. Under page navigator, got to **interrupts**, and enable **IRQ_F2P[15:0]**

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/117709731-fact8.png

Add **fact_intrpt** and rename it to **fact_intrpt**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3779835952-fact9.png

Add **AXI Interrupt Controller** and rename it to **axi_intc**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/4151956562-fact10.png

Double click on **axi_intc** to customize it. Set **Interrupt Output Connection** to **Single**.

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/2935182167-fact11.png

Add two **Concat IPs** to your design, double click on them for **customization**, and **set Number of Ports** to **1**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/538208086-fact12.png

2.4) Connect your blocks
########################

Connect the following ports:

**fact_intrpt::interrupt** to **xlconcat_0::in0**

**xlconcat_0::dout** to **axi_intc::intr[0:0]**

**axi_intc::irq** to **xlconcat_1::in0**

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/2495777624-fact13.png

That is all the manual labor you have to do for the connections. Now, you can use the tool for the rest of the blocks and connections.

In the **Diagram window**, in the highlighted are, click on **Run Block Automation**. Then click on **Run Connection Automation** and **select all**:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/667624785-fact14.png

Your design should look like the following:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/68504461-fact15.png

2.5) Generating bitstream
#########################

Save your block diagram and check your design from **Tools > Validate Design**. If it passed successfully, under **Sources**, **right click** on **design_1**, and select **Create HDL Wrapper** with default settings.

Now you can click on **Generate Bitstream** in **Flow Navigator** with default settings to generate your bitstream.

2.6) Export .tcl file and addresses
###################################

After finishing your bitstream generation, export your block design from **File > Export > Export Block Design**, and name it *fact_intrpt.tcl*:

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/3372073042-fact16.png

Copy **your_vivado_project_directory > project_1.runs > impl_1 > design_1_wrapper.bit** to **your_vivado_project_directory > fact_intrpt.bit** next to *fact_intrpt.tcl*.

In **Sources**, open **fact_intrpt_cntrl_io_s_axi.v** and note the port addresses. We need these addresses in our python code.

.. image :: https://bitbucket.org/repo/x8q9Ed8/images/2508179436-fact17.png

3)Host program
--------------

In this section we use a Jupyter notebook to interact with our IP.

3.1) Move files to PYNQ
#######################

Connect to your PYNQ board and create a new folder. Copy fact_intrpt.tcl and fact_intrpt.bit to this folder. Create a new Jupyter notebook and complete it as following to interact with your design:

.. code-block :: python3

	from pynq import Overlay
	import asyncio
	from psutil import cpu_percent

	ol = Overlay("fact_intrpt.bit")
	ol.download()

.. code-block :: python3

	# IP's addresses
	IP_CTRL = 0x00
	AP_START = 0x1
	GIER = 0x04
	IP_IER = 0x08
	IP_ISR = 0x0C
	INTRPT_AP_DONE = 0x1
	INTRPT_AP_READY = 0x2
	OUT_REG = 0x10
	INP_REG = 0x18

	_INTRPT = INTRPT_AP_DONE

	fact_ip = ol.fact_intrpt
	fact_ip.write(GIER, 0x1)
	fact_ip.write(IP_IER, _INTRPT)


.. code-block :: python3

	# Coroutine that waits for an IP to be done.
	async def read_ip(ip):
	    while True:
		# Wait for the IP to finish.
		await ip.interrupt.wait()
		# Clear the interrupt and then print output's value.
		if (ip.read(IP_ISR) & _INTRPT):
		    ip.write(IP_ISR, _INTRPT)
		    print('interrupt received, out = {}'.format(ip.read(OUT_REG)))

	# Task for IP using the coroutine
	ip_task = asyncio.ensure_future(read_ip(fact_ip))

	# Coroutine for writing input and starting the IP with delay
	async def write_wait(interval):
	    await asyncio.sleep(interval)
	    # write to input
	    fact_ip.write(INP_REG, 10) 
	    print("input = ", fact_ip.read(INP_REG))
	    fact_ip.write(IP_CTRL, AP_START) # You can comment it out to test the interrupt
	    print("IP started")
	    await asyncio.sleep(interval)

	# Run the event loop until the time interval expires
	time_interval = 2  # time in seconds
	loop = asyncio.get_event_loop()
	write_task = asyncio.ensure_future(write_wait(time_interval))

	# Using psutil to record CPU utilization.
	cpu_percent(percpu=True)  # Initializing the CPU monitoring.
	loop.run_until_complete(write_task)
	cpu_used = cpu_percent(percpu=True)

	# Printing the CPU utilization
	print('CPU Utilization = {cpu_used}'.format(**locals()))

	# Removing the IP task from the event loop.
	ip_task.cancel()


