AUP-ZU3 Boards
============================

This page serves as documentation for the AUP-ZU3 boards that will be leant to students of CSE 237C as of Fall 2026. `The official getting started guide is here <https://xilinx.github.io/AUP-ZU3/getting_started.html>`_.

This guide is from October 2026, and the current PYNQ is 3.1 and the image is located at `this link <https://download.amd.com/opendownload/pynq/AUP-ZU3-3.1.1-4gb.zip>`_.

As tested by the writers of this guide, the getting started guide works for Windows and Linux computers properly with a USB-C cable. Below, we have figured out how to get it to work on MacOS.

1) MacOS Setup
--------------------------------------------------

By default, the device doesn't properly work on MacOS due to incompatibility with `RNDIS <https://en.wikipedia.org/wiki/RNDIS>`_. This guide is subject to change if the PYNQ image is updated in some way, but for 3.1 it should work.

First, you want to write the image from the link above to your Micro SD card, as in the guide. Next, plug a USB-C cable into both your computer and the port in the FPGA board labeled **PROG UART**.

Power the board on, and it should power on as normal. Run the following command ::

  $ ls /dev/tty*
  
You will see many entries in the output, but look for some entries like these ::

  /dev/tty.usbserial-8800204102EB0
  /dev/tty.usbserial-8800204102EB1

These will be the board's serial connections. If you happen to have multiple usbserial devices plugged in, try the command above with the board disconnected and reconnected and look for the diff.

In my experience, the board's UART port is the device ending with 1, but to be safe you can open both of them. To open the device, use gnu screen with the command below ::

  screen /dev/cu.usbserial-8800204102EB1 115200
  
Note the `115200`, this is important. This is the baud rate of the UART port. You should see a shell prompt if you press enter and the board has already booted. If you have not yet booted, you should see the boot log showing up as the device boots, and eventually should be put into a shell.

Now, to change the board image to work on Mac, we want to run the following ::

  mkdir -p /tmp/fatfs
  sudo mount /usr/local/share/fatfs /tmp/fatfs
  sudo rm /tmp/fatfs/delete-for-mac.txt

For password prompts, the default password is `xilinx`.

Once you have run these steps, you should be good to go once you reboot the device, so give it one good ::

  sudo reboot

and the USB port should now work for MacOS when plugged into the `USB 3.0 DRP I` port.

2) How did we figure this out?
--------------------------------------------------

At the time of writing, these steps have not been documented by AMD, nor has the out-of-the-box incompatibility with windows. We figured this out by reading the scripts in the board. This information might be useful if the image is changed and these steps need to be updated for the new image.

To view the usbgadget service, run ::

  systemctl cat usbgadget

This gives us the output ::

  # /lib/systemd/system/usbgadget.service
  [Unit]
  Description=USB Gadget for Networking
  Before=network-online.service isc-dhcp-server.service

  [Service]
  Type=oneshot
  RemainAfterExit=yes
  ExecStart=/usr/local/bin/usbgadget
  ExecStop=/usr/local/bin/usbgadget_stop

  [Install]
  WantedBy=basic.target
  
We dug into the script at `usr/local/bin/usbgadget` to find out that there are conditions for when the gadget is created with RNDIS vs ECM. The essence is that it either looks for the `delete-for-windows.txt` file or the `delete-for-mac.txt` file in the fatfs. 