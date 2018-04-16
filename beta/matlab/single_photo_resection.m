%% ENG4000 U-TRACKR SPACE RESECTION, 2D-3D POSITIONING

clc; 
clear all; 
close all;

%% 1. INPUT
% focal length (mm)
f = 3.04;

% camera pixel size (m) https://www.raspberrypi.org/documentation/hardware/camera/README.md
pixSizeX = 0.00000112;
pixSizeY = 0.00000112;

% image width and height (pix)
imgWidth = 3280;
imgHeight = 2464; 

% pixel coordinates of the 4 points in image: [x,y] (pix)
cam_pixel_coords=[
    2119 1686;
    2072 815;
    1337 897;
    1395 1639];

% ground control coordinates [X,Y,Z] (m)
cam_ground_control_coords=[
    0.44 0.176 0;
    0.704 0.44 0;
    0.44 0.704 0;
    0.176 0.44 0];

% initial exterior orientation coords parameters (m)
x0 = 0;
y0 = 0;
z0 = 0;

% initial exterior orientation angle parameters (rads)
omega = 0;
phi = 0;
kappa = 0;

%% Pixel Coordinates to Image Coordinates
% Based off of ESSE3650_03_CamerasImageMeas_16JAN2017.pdf slide 54

% x = [c - w/2 - 0.5] * px 
% y = [(h/2) - r + 0.5] * py
% output: cam_image_coords[x,y] in mm
for i = 1:length(cam_pixel_coords)
    cam_image_coords(i,1) = ((cam_pixel_coords(i,1) - (imgWidth/2) - 0.5) * pixSizeX) * 1000;
    cam_image_coords(i,2) = (((imgHeight/2) - cam_pixel_coords(i,2) + 0.5) * pixSizeY) * 1000;
end
