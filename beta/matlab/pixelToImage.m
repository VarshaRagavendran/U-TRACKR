%% pixelToImage Coordinates

clc; 
clear all; 
close all;

%% 1. Input Data
% interior camera orientation params (mm)
f = 3.04; % focal length (mm)
xo = 0;
yo = 0;

% camera pixel size (m) https://www.raspberrypi.org/documentation/hardware/camera/README.md
pixSizeX = 0.00000112;
pixSizeY = 0.00000112;

% image width and height (pix)
imgWidth = 3280;
imgHeight = 2464; 

% pixel coordinates of the 13 points in cam2.jpg: [x,y] (pix)
cam_Pixel_Coords=[
    1556    979;
    1915    1209];

%% 2. Pixel Coordinates to Image Coordinates
% Based off of ESSE3650_03_CamerasImageMeas_16JAN2017.pdf slide 54

% x = [c - w/2 - 0.5] * px 
% y = [(h/2) - r + 0.5] * py
% output: cam_image_coords[x,y] in mm
for i = 1:length(cam_Pixel_Coords)
    cam_Image_Coords(i,1) = ((cam_Pixel_Coords(i,1) - (imgWidth/2) - 0.5) * pixSizeX) * 1000;
    cam_Image_Coords(i,2) = (((imgHeight/2) - cam_Pixel_Coords(i,2) + 0.5) * pixSizeY) * 1000;
end

cam_Image_Coords