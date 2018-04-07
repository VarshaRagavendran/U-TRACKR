%% ENG 4000% SPACE RESECTION, 2D-3D POSITIONING

clc; 
clear all; 
close all;

%% Importing data sets
% Importing data as table to be easily manipulated 
SR = readtable('data/NewImageCoords1234.xlsx');


%SR1
cam1_pixel_X = table2array(SR(1,1));
cam1_pixel_Y = table2array(SR(1,2));

cam2_pixel_X = table2array(SR(1,3));
cam2_pixel_Y = table2array(SR(1,4));

cam3_pixel_X = table2array(SR(1,5));
cam3_pixel_Y = table2array(SR(1,6));

cam4_pixel_X = table2array(SR(1,7));
cam4_pixel_Y = table2array(SR(1,8));

%SR2
cam1_pixel_X2 = table2array(SR(2,1));
cam1_pixel_Y2 = table2array(SR(2,2));

cam2_pixel_X2 = table2array(SR(2,3));
cam2_pixel_Y2 = table2array(SR(2,4));

cam3_pixel_X2 = table2array(SR(2,5));
cam3_pixel_Y2 = table2array(SR(2,6));

cam4_pixel_X2 = table2array(SR(2,7));
cam4_pixel_Y2 = table2array(SR(2,8));

%SR3
cam1_pixel_X3 = table2array(SR(3,1));
cam1_pixel_Y3 = table2array(SR(3,2));

cam2_pixel_X3 = table2array(SR(3,3));
cam2_pixel_Y3 = table2array(SR(3,4));

cam3_pixel_X3 = table2array(SR(3,5));
cam3_pixel_Y3 = table2array(SR(3,6));

cam4_pixel_X3 = table2array(SR(3,7));
cam4_pixel_Y3 = table2array(SR(3,8));

%SR4
cam1_pixel_X4 = table2array(SR(4,1));
cam1_pixel_Y4 = table2array(SR(4,2));

cam2_pixel_X4 = table2array(SR(4,3));
cam2_pixel_Y4 = table2array(SR(4,4));

cam3_pixel_X4 = table2array(SR(4,5));
cam3_pixel_Y4 = table2array(SR(4,6));

cam4_pixel_X4 = table2array(SR(4,7));
cam4_pixel_Y4 = table2array(SR(4,8));


% Taking array data in strings and finding the numbers in double
%cam1_pixel_X = regexp(cam1_pixel_X,'\d+(\.)?(\d+)?','match');
%cam1_pixel_Y = regexp(cam1_pixel_Y,'\d+(\.)?(\d+)?','match');

% Converting string to double 
%cam1_pixel_X = str2double([cam1_pixel_X{:}])';
%cam1_pixel_Y = str2double([cam1_pixel_Y{:}])';


%% Pixel Coordinates to Image Coordinates 
% based on Camera Module V2: https://www.raspberrypi.org/documentation/hardware/camera/README.md
% camera focal length (mm)
f = 3.04;

% laptop pixSize with resolution 3840 x 2160, screen size 15.6" = 0.089 http://lcdtech.info/en/data/pixel.size.htm
% pixSize = 0.089;
pixSize = 0.00112;

% screen size measured on the laptop
% width_Of_Image = 600/2;
% height_Of_Image = 340/2; 
% Sensor resolution
width_Of_Image = 3280/2;
height_Of_Image = 2464/2; 

% SR1
for i = 1:length(cam1_pixel_X)
    cam1_Image_X(i) = (cam1_pixel_X(i) - width_Of_Image - 0.5) * pixSize;
    cam1_Image_Y(i) = (height_Of_Image - cam1_pixel_Y(i) + 0.5) * pixSize;
    cam2_Image_X(i) = (cam2_pixel_X(i) - width_Of_Image - 0.5) * pixSize;
    cam2_Image_Y(i) = (height_Of_Image - cam2_pixel_Y(i) + 0.5) * pixSize;
    cam3_Image_X(i) = (cam3_pixel_X(i) - width_Of_Image - 0.5) * pixSize;
    cam3_Image_Y(i) = (height_Of_Image - cam3_pixel_Y(i) + 0.5) * pixSize;
    cam4_Image_X(i) = (cam4_pixel_X(i) - width_Of_Image - 0.5) * pixSize;
    cam4_Image_Y(i) = (height_Of_Image - cam4_pixel_Y(i) + 0.5) * pixSize;
end
cam1_Image_Coords1= [cam1_Image_X(:)'; cam1_Image_Y(:)']';
cam2_Image_Coords1= [cam2_Image_X(:)'; cam2_Image_Y(:)']';
cam3_Image_Coords1= [cam3_Image_X(:)'; cam3_Image_Y(:)']';
cam4_Image_Coords1= [cam4_Image_X(:)'; cam4_Image_Y(:)']';


% SR2
for i = 1:length(cam1_pixel_X)
    cam1_Image_X2(i) = (cam1_pixel_X2(i) - width_Of_Image - 0.5) * pixSize;
    cam1_Image_Y2(i) = (height_Of_Image - cam1_pixel_Y2(i) + 0.5) * pixSize;
    cam2_Image_X2(i) = (cam2_pixel_X2(i) - width_Of_Image - 0.5) * pixSize;
    cam2_Image_Y2(i) = (height_Of_Image - cam2_pixel_Y2(i) + 0.5) * pixSize;
    cam3_Image_X2(i) = (cam3_pixel_X2(i) - width_Of_Image - 0.5) * pixSize;
    cam3_Image_Y2(i) = (height_Of_Image - cam3_pixel_Y2(i) + 0.5) * pixSize;
    cam4_Image_X2(i) = (cam4_pixel_X2(i) - width_Of_Image - 0.5) * pixSize;
    cam4_Image_Y2(i) = (height_Of_Image - cam4_pixel_Y2(i) + 0.5) * pixSize;
end
cam1_Image_Coords2= [cam1_Image_X2(:)'; cam1_Image_Y2(:)']';
cam2_Image_Coords2= [cam2_Image_X2(:)'; cam2_Image_Y2(:)']';
cam3_Image_Coords2= [cam3_Image_X2(:)'; cam3_Image_Y2(:)']';
cam4_Image_Coords2= [cam4_Image_X2(:)'; cam4_Image_Y2(:)']';

% SR3
for i = 1:length(cam1_pixel_X)
    cam1_Image_X3(i) = (cam1_pixel_X3(i) - width_Of_Image - 0.5) * pixSize;
    cam1_Image_Y3(i) = (height_Of_Image - cam1_pixel_Y3(i) + 0.5) * pixSize;
    cam2_Image_X3(i) = (cam2_pixel_X3(i) - width_Of_Image - 0.5) * pixSize;
    cam2_Image_Y3(i) = (height_Of_Image - cam2_pixel_Y3(i) + 0.5) * pixSize;
    cam3_Image_X3(i) = (cam3_pixel_X3(i) - width_Of_Image - 0.5) * pixSize;
    cam3_Image_Y3(i) = (height_Of_Image - cam3_pixel_Y3(i) + 0.5) * pixSize;
    cam4_Image_X3(i) = (cam4_pixel_X3(i) - width_Of_Image - 0.5) * pixSize;
    cam4_Image_Y3(i) = (height_Of_Image - cam4_pixel_Y3(i) + 0.5) * pixSize;
end
cam1_Image_Coords3= [cam1_Image_X3(:)'; cam1_Image_Y3(:)']';
cam2_Image_Coords3= [cam2_Image_X3(:)'; cam2_Image_Y3(:)']';
cam3_Image_Coords3= [cam3_Image_X3(:)'; cam3_Image_Y3(:)']';
cam4_Image_Coords3= [cam4_Image_X3(:)'; cam4_Image_Y3(:)']';

% SR3
for i = 1:length(cam1_pixel_X)
    cam1_Image_X4(i) = (cam1_pixel_X4(i) - width_Of_Image - 0.5) * pixSize;
    cam1_Image_Y4(i) = (height_Of_Image - cam1_pixel_Y4(i) + 0.5) * pixSize;
    cam2_Image_X4(i) = (cam2_pixel_X4(i) - width_Of_Image - 0.5) * pixSize;
    cam2_Image_Y4(i) = (height_Of_Image - cam2_pixel_Y4(i) + 0.5) * pixSize;
    cam3_Image_X4(i) = (cam3_pixel_X4(i) - width_Of_Image - 0.5) * pixSize;
    cam3_Image_Y4(i) = (height_Of_Image - cam3_pixel_Y4(i) + 0.5) * pixSize;
    cam4_Image_X4(i) = (cam4_pixel_X4(i) - width_Of_Image - 0.5) * pixSize;
    cam4_Image_Y4(i) = (height_Of_Image - cam4_pixel_Y4(i) + 0.5) * pixSize;
end
cam1_Image_Coords4= [cam1_Image_X4(:)'; cam1_Image_Y4(:)']';
cam2_Image_Coords4= [cam2_Image_X4(:)'; cam2_Image_Y4(:)']';
cam3_Image_Coords4= [cam3_Image_X4(:)'; cam3_Image_Y4(:)']';
cam4_Image_Coords4= [cam4_Image_X4(:)'; cam4_Image_Y4(:)']';

%% Converted Image Coordinates 
Cam1_IMCO = [cam1_Image_Coords1;
    cam1_Image_Coords2;
    cam1_Image_Coords3;
    cam1_Image_Coords4]

Cam2_IMCO = [cam2_Image_Coords1;
    cam2_Image_Coords2;
    cam2_Image_Coords3;
    cam2_Image_Coords4]

Cam3_IMCO = [cam3_Image_Coords1;
    cam3_Image_Coords2;
    cam3_Image_Coords3;
    cam3_Image_Coords4]

Cam4_IMCO = [cam4_Image_Coords1;
    cam4_Image_Coords2;
    cam4_Image_Coords3;
    cam4_Image_Coords4]


%%
hold on
scatter(cam4_Image_Coords1(1,1),cam4_Image_Coords1(1,2))
scatter(cam4_Image_Coords2(1,1),cam4_Image_Coords2(1,2))
scatter(cam4_Image_Coords3(1,1),cam4_Image_Coords3(1,2))
scatter(cam4_Image_Coords4(1,1),cam4_Image_Coords4(1,2))
hold off
