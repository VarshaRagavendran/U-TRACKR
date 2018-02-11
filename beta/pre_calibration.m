%% ENG 4000% SPACE RESECTION, 2D-3D POSITIONING

clc; 
clear all; 
close all;

%% Importing data sets
% Importing data as table to be easily manipulated 
cam1 = readtable('ImageCoords1234.xlsx');

cam1_pixel_X = mean(table2array(cam1(:,2)));
cam1_pixel_Y = mean(table2array(cam1(:,3)));

cam2_pixel_X = mean(table2array(cam1(:,4)));
cam2_pixel_Y = mean(table2array(cam1(:,5)));

cam3_pixel_X = mean(table2array(cam1(:,6)));
cam3_pixel_Y = mean(table2array(cam1(:,7)));

cam4_pixel_X = mean(table2array(cam1(:,8)));
cam4_pixel_Y = mean(table2array(cam1(:,9)));


% Taking array data in strings and finding the numbers in double
%cam1_pixel_X = regexp(cam1_pixel_X,'\d+(\.)?(\d+)?','match');
%cam1_pixel_Y = regexp(cam1_pixel_Y,'\d+(\.)?(\d+)?','match');

% Converting string to double 
%cam1_pixel_X = str2double([cam1_pixel_X{:}])';
%cam1_pixel_Y = str2double([cam1_pixel_Y{:}])';


%% Pixel Coordinates to Image Coordinates 

f = 3.04;
pixSize = 1.12;
width_Of_Image = 1280/2;
height_Of_Image = 720/2; 

for i = 1:length(cam1_pixel_X)
    cam1_Image_X(i) = (cam1_pixel_X(i) - width_Of_Image - 0.5) * pixSize;
    cam1_Image_Y(i) = (height_Of_Image - cam1_pixel_Y(i) + 0.5) * pixSize;
end
cam1_Image_Coords= [cam1_Image_X(:)'; cam1_Image_Y(:)']'

for i = 1:length(cam1_pixel_X)
    cam2_Image_X(i) = (cam2_pixel_X(i) - width_Of_Image - 0.5) * pixSize;
    cam2_Image_Y(i) = (height_Of_Image - cam2_pixel_Y(i) + 0.5) * pixSize;
end
cam2_Image_Coords= [cam2_Image_X(:)'; cam2_Image_Y(:)']'

for i = 1:length(cam1_pixel_X)
    cam3_Image_X(i) = (cam3_pixel_X(i) - width_Of_Image - 0.5) * pixSize;
    cam3_Image_Y(i) = (height_Of_Image - cam3_pixel_Y(i) + 0.5) * pixSize;
end
cam3_Image_Coords= [cam3_Image_X(:)'; cam3_Image_Y(:)']'

for i = 1:length(cam1_pixel_X)
    cam4_Image_X(i) = (cam4_pixel_X(i) - width_Of_Image - 0.5) * pixSize;
    cam4_Image_Y(i) = (height_Of_Image - cam4_pixel_Y(i) + 0.5) * pixSize;
end
cam4_Image_Coords= [cam4_Image_X(:)'; cam4_Image_Y(:)']'


%%


