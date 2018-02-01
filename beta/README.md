# U-TRACKR

## Running the Program (BETA)

### 1. Installing Dependencies

* 1.1\. Enable SSH on the Pi (if it is not already enabled)
	* 1.1.1\. Enter sudo raspi-config in a terminal window
	* 1.1.2\. Select Interfacing Options
	* 1.1.3\. Navigate to and select SSH
	* 1.1.4\. Choose Yes
	* 1.1.5\. Select Ok
	* 1.1.6\. Choose Finish

The following commands starting from 1.2 are to be run on your local machine, not the Pi.

* 1.2\. Install Python 2.7.13

* 1.3\. Install OpenCV 3.4.0
	
	* 1.3.1\. For Windows, follow this guide to install OpenCV: http://opencvpython.blogspot.ca/2012/05/install-opencv-in-windows-for-python.html
	
	* 1.3.2\. Follow this: https://stackoverflow.com/questions/11699298/opencv-2-4-videocapture-not-working-on-windows
		- copy opencv_ffmpeg340.dll to C:/Python27 (where 340 is the OpenCV version 3.4.0)
		- copy opencv_ffmpeg340_64.dll to C:/Python27 (where 340 is the OpenCV version 3.4.0)

* 1.4\. Install the libraries using the following commands:

```
pip install imutils
pip install flask
pip install picamera[array]
pip install paramiko
```

### 2. Running the command

* 2.1\. Turn on the Pi, and ensure it is connected to the same Wi-Fi network as your local machine.

* 2.2\. Find the IP address by running 'ifconfig' and looking at wlan0 > inet addr

* 2.3\. Replace the IP address in main.py from the one found in step 5.

* 2.4\. Run

```
python main.py
```
