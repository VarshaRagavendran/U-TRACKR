%% ENG 4000% SPACE RESECTION, 2D-3D POSITIONING

clc; 
clear all; 
close all;

%% Importing data sets
% Importing data as table to be easily manipulated 
SR1 = readtable('ImageCoords1.xlsx');
SR2 = readtable('ImageCoords2.xlsx');
SR3 = readtable('ImageCoords3.xlsx');
SR4 = readtable('ImageCoords4.xlsx');

%SR1
cam1_pixel_X = mean(table2array(SR1(:,2)));
cam1_pixel_Y = mean(table2array(SR1(:,3)));

cam2_pixel_X = mean(table2array(SR1(:,4)));
cam2_pixel_Y = mean(table2array(SR1(:,5)));

cam3_pixel_X = mean(table2array(SR1(:,6)));
cam3_pixel_Y = mean(table2array(SR1(:,7)));

cam4_pixel_X = mean(table2array(SR1(:,8)));
cam4_pixel_Y = mean(table2array(SR1(:,9)));

%SR2
cam1_pixel_X2 = mean(table2array(SR2(:,2)));
cam1_pixel_Y2 = mean(table2array(SR2(:,3)));

cam2_pixel_X2 = mean(table2array(SR2(:,4)));
cam2_pixel_Y2 = mean(table2array(SR2(:,5)));

cam3_pixel_X2 = mean(table2array(SR2(:,6)));
cam3_pixel_Y2 = mean(table2array(SR2(:,7)));

cam4_pixel_X2 = mean(table2array(SR2(:,8)));
cam4_pixel_Y2 = mean(table2array(SR2(:,9)));

%SR3
cam1_pixel_X3 = mean(table2array(SR3(:,2)));
cam1_pixel_Y3 = mean(table2array(SR3(:,3)));

cam2_pixel_X3 = mean(table2array(SR3(:,4)));
cam2_pixel_Y3 = mean(table2array(SR3(:,5)));

cam3_pixel_X3 = mean(table2array(SR3(:,6)));
cam3_pixel_Y3 = mean(table2array(SR3(:,7)));

cam4_pixel_X3 = mean(table2array(SR3(:,8)));
cam4_pixel_Y3 = mean(table2array(SR3(:,9)));

%SR4
cam1_pixel_X4 = mean(table2array(SR4(:,2)));
cam1_pixel_Y4 = mean(table2array(SR4(:,3)));

cam2_pixel_X4 = mean(table2array(SR4(:,4)));
cam2_pixel_Y4 = mean(table2array(SR4(:,5)));

cam3_pixel_X4 = mean(table2array(SR4(:,6)));
cam3_pixel_Y4 = mean(table2array(SR4(:,7)));

cam4_pixel_X4 = mean(table2array(SR4(:,8)));
cam4_pixel_Y4 = mean(table2array(SR4(:,9)));


% Taking array data in strings and finding the numbers in double
%cam1_pixel_X = regexp(cam1_pixel_X,'\d+(\.)?(\d+)?','match');
%cam1_pixel_Y = regexp(cam1_pixel_Y,'\d+(\.)?(\d+)?','match');

% Converting string to double 
%cam1_pixel_X = str2double([cam1_pixel_X{:}])';
%cam1_pixel_Y = str2double([cam1_pixel_Y{:}])';


%% Pixel Coordinates to Image Coordinates 

f = 3.04;
pixSize = 0.00112;
width_Of_Image = 1280/2;
height_Of_Image = 720/2; 

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
