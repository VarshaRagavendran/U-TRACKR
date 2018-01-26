# U-TRACKR
Detects an object's location using photogrammetry. Currently utilizes the Raspberry Pi with a camera module running Open-CV for object detection. Runs a server that provides a live video stream.

## Setup

### How to setup the camera:

	"sudo apt-get update"
	"sudo apt-get upgrade"
	1. sudo raspi-config > 5 Enable Camera > Enable > Reboot
	2. put camera module towards the closer end of the ethernet cable on pi, with the blue facing the ethernet.

	"vcgencmd get_camera": Checks if the camera is supported orp detected
	pull up the pin connectors, put in the camera, then push it back down.

	3. "raspistill -o image.jpg" for pics
	4. "raspivid" -o video.h264 -t 10000" for videos

Select `Interface Options`, then `Pi Camera` and toggle on. Press `Finish` and exit.

You can verify that the camera works by running

```
raspistill -o image.jpg
```
which will save a image from the camera in your current directory. You can open up the file inspector and view the image.

### Installing Dependencies

1. https://www.pyimagesearch.com/2015/02/23/install-opencv-and-python-on-your-raspberry-pi-2-and-b/
2. https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
3. Install the libraries using the following commands:

```
pip install imutils
pip install flask
pip install picamera[array]
```

## Running the Program (ALPHA)

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
