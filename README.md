# REPLIOT

REPLIOT is an automatic tool for testing replay attacks in a smart home environment. The tool is designed to be *agnostic* and works with any type of device that communicates with the companion app through the local network. REPLIOT includes a detection module that analyzes the device's responses to automatically determine the success of an attack.
Through REPLIOT, we performed thousands of automated experiments on 41 commercial IoT devices spanning various vendors and categories. We found that, among these, 15 devices are vulnerable to replay attacks. Details about our study can be found at [Is Your Kettle Smarter Than a Hacker? A Scalable Tool for Assessing Replay Attack Vulnerabilities on Consumer IoT Devices (https://arxiv.org/pdf/2401.12184.pdf).

    

## Usage in the Laboratory

We utilized REPLIOT in a laboratory environment to assess replay attack vulnerabilities in 41 commercial IoT devices. To replicate our results, you need the physical device connected to an access point (AP) where the tool runs.

For each device under test, follow these steps:

### Setup
- Copy the REPLIOT Folder on the AP. We used a laptop with Ubuntu 20.
- Install the companion app of the device on a smartphone (Google Pixel 3a was used in our tests).
- Select an OBVERSE and the related REVERSE state of the device (e.g., the OBVERSE state is "device ON", while the REVERSE state is "device OFF")
- Create a folder named with the MAC address of the device inside "REPLIOT/Test/Result"
- Within the above folder, create three files: `Fun_coordinates.txt`, `Reverse_coordinates.txt`, `Ground_coordinates.txt`. In `Fun_coordinates.txt`, insert the coordinates to lead the device into the OBVERSE state after the app is open. Similarly, insert coordinates into `Reverse_coordinates.txt` to lead the device into the REVERSE state after the app is open. Often, these two files have the same content. Finally, insert coordinates into `Ground_coordinates.txt` to lead the device into the screen before submitting the OBSERVE command. If you use a Google Pixel 3a and one of our devices, you can copy the coordinates from the folder of the device we used in our laboratory.
- Within the folder "REPLIOT/Test/Result/MAC", create the folder 'Capture'. Insert the screenshot of the smartphone as `Fun_reference.png` when it is in the OBSERVE state. Insert the screenshot of the smartphone as `Reverse_reference.png` when it is in the REVERSE state. If you use a Google Pixel 3a and one of our device, you can copy the screenshot from the folder of the device we used in our laboratory.
- Crop `Fun_reference.png` and `Reverse_reference.png` by selecting a proper area of each screen. Save the crop area in `Fun_crop.txt` and `Reverse_crop.txt` in the folder 'Capture'. If you use a Google Pixel 3a, you can copy the crop files from the folder of the device we used in our laboratory.
- Connect the smartphone to the access point to control it via adb.

### Training Phase

Lunch the following command: 
```bash 
bash Training_device.sh `SERIAL_NUMBER` `MAC_DEVICE` `INTERFACE` `PACKAGE` `MAC_SMARTPHONE`
```
where:
  - SERIAL_NUMBER: Serial number of the phone in ADB.
  - MAC_DEVICE: MAC address of the IoT device.
  - INTERFACE: Network interface on which the traffic is sniffed.
  - PACKAGE: Package name of the companion app.
  - MAC_SMARTPHONE: MAC address of the smartphone.

### Test Phase

Lunch the following command: 
```bash 
bash Test_device.sh `SERIAL_NUMBER` `MAC_DEVICE` `INTERFACE` `PACKAGE` `MAC_SMARTPHONE`
```
where:
  - SERIAL_NUMBER: Serial number of the phone in ADB.
  - MAC_DEVICE: MAC address of the IoT device.
  - INTERFACE: Network interface on which the traffic is sniffed.
  - PACKAGE: Package name of the companion app.
  - MAC_SMARTPHONE: MAC address of the smartphone.


## Usage in Home Environment

### Training Phase

Lunch the following command: 
```bash 
bash Training_device_home.sh `MAC_DEVICE` `INTERFACE` `MAC_SMARTPHONE` `SNIFF_TIME`
```
where:
  - MAC_DEVICE: MAC address of the IoT device.
  - INTERFACE: Network interface on which the traffic is sniffed.
  - MAC_SMARTPHONE: MAC address of the smartphone.
  - SNIFF_TIME: time (seconds) during which the tool sniffs the traffic

When the tool displays in console "Start triggering the device", the user needs to set the device in the OBVERSE and REVERSE state alternatively. This procedure should be repeated at least five times.


### Test Phase

Lunch the following command: 
```bash 
bash Test_device_home.sh `MAC_DEVICE` `INTERFACE` `MAC_SMARTPHONE` `SNIFF_TIME` `DELAY_TIME`
```
where:
  - MAC_DEVICE: MAC address of the IoT device.
  - INTERFACE: Network interface on which the traffic is sniffed.
  - MAC_SMARTPHONE: MAC address of the smartphone.
  - SNIFF_TIME: time (seconds) during which the tool sniffs the traffic
  - DELAY_TIME: time (seconds) after which the tool starts the replay attack
  - DETECTION: can be ``YES'' or ``NO''. If ``YES'', REPLIOT uses the detection module based on the ML model.

    
When the tool displays in console "Start triggering the device", the user needs to set the device in the OBVERSE state. <br />
When the tool displays in console "Sniffing completed. The attack will start in `DELAY_TIME` seconds", the user needs to set the device in the REVERSE state. <br />
If DETECTION is ``YES'', REPLIOT shows in console if the attack has worked or not.

<!---[![Anteprima del mio video](https://img.youtube.com/vi/TXSQ9XJ8Rpc/0.jpg)](https://www.youtube.com/watch?v=TXSQ9XJ8Rpc)--->

