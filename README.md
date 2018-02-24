# U-TRACKR
Detects an object's location using photogrammetry. Currently utilizes the Raspberry Pi with a camera module running Open-CV for object detection. Runs a server that provides a live video stream.

## Setup

### How to setup the camera on the pi:

	"sudo apt-get update"
	"sudo apt-get upgrade"
	1. sudo raspi-config > 5 Enable Camera > Enable > Reboot
	2. put camera module towards the closer end of the ethernet cable on pi, with the blue facing the ethernet.

	"vcgencmd get_camera": Checks if the camera is supported or detected
	pull up the pin connectors, put in the camera, then push it back down.

	3. "raspistill -o image.jpg" for pics
	4. "raspivid" -o video.h264 -t 10000" for videos

Select `Interface Options`, then `Pi Camera` and toggle on. Press `Finish` and exit.

You can verify that the camera works by running

```
raspistill -o image.jpg
```
which will save a image from the camera in your current directory. You can open up the file inspector and view the image.

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

## Running the Program (ALPHA)

### Installing Dependencies

1. https://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/
2. https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
3. Install the libraries using the following commands:

```
pip install imutils
pip install flask
pip install picamera[array]
```

### Running the command

Run the following commands:
```
source ~/.profile
workon cv
sudo modprobe bcm2835-v4l2
```

Note: The modprobe bcm2835-vl2 command prevents a common OpenCV assertion error when using the Pi Camera.

Go to the folder where this repository is stored, go to /alpha and run the following:

```
python main.py
```

You can view a live stream by visiting the ip address of your pi in a browser on the same network. You can find the ip address of your Raspberry Pi by typing `ifconfig` in the terminal and looking for the `inet` address. 

Visit `<raspberrypi_ip>:5000` in your browser to view the stream.

Alternatively, you can run a simple tracking app in /alpha/test to ensure the proper HSV values for object tracking.

```
python tracking.py
```

## Useful Commands

### Checking OpenCV version on Python
```
source ~/.profile
workon cv
python
>>> import cv2
>>> cv2.__version__
```
