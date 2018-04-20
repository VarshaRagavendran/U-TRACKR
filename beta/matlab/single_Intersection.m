%% ENG4000 U-TRACKR SPACE INTERSECTION, 3D POSITIONING

clc; 
clear all; 
close all;

%% 1. Input Data
% focal length (mm)
f = 3.04;

% camera pixel size (m) https://www.raspberrypi.org/documentation/hardware/camera/README.md
pixSizeX = 0.00000112;
pixSizeY = 0.00000112;

% image width and height (pix)
imgWidth = 3280;
imgHeight = 2464; 

% pixel coordinates of the 4 points in image: [x,y] (pix)
cam_Pixel_Coords=[
    2000 805;
    1292 936;
    1382 1676;
    2096 1674];

% camera space coordinates [X,Y,Z] (m)
cam_Ground_Control_Coords=[
    0.704 0.44 0;
    0.44 0.704 0;
    0.176 0.44 0;
    0.44 0.176 0];

% initial exterior orientation coords parameters (m)
x0 = 0.05;
y0 = 0.05;
z0 = 0.98;

% initial exterior orientation angle parameters (rads)
omega = 0.785398;
phi = 0.785398; % 45 deg
kappa = 0; % 45 deg

%% 2. Pixel Coordinates to Image Coordinates
% Based off of ESSE3650_03_CamerasImageMeas_16JAN2017.pdf slide 54
% output: cam_image_coords[x,y] in mm
for i = 1:length(cam_Pixel_Coords)
    cam_Image_Coords(i,1) = ((cam_Pixel_Coords(i,1) - (imgWidth/2) - 0.5) * pixSizeX) * 1000;
    cam_Image_Coords(i,2) = (((imgHeight/2) - cam_Pixel_Coords(i,2) + 0.5) * pixSizeY) * 1000;
end

cam_Image_Coords;

%% 3. Space Resection by Collinearity - Initialization

% Image Coords (mm)
x  = cam_Image_Coords(:,1);
y  = cam_Image_Coords(:,2);

% Space/Ground Control coords (m)
X  = cam_Ground_Control_Coords (:,1);
Y  = cam_Ground_Control_Coords (:,2);
Z  = cam_Ground_Control_Coords (:,3);

% Initial orientation parameters
DELTA=[1 1 1 1 1 1 1];

% Iterative solution coordinates (m)
XL = x0;
YL = y0;
ZL = z0;

% Counter to count number of iterations
counter = 1;

% Count for each point
count = size(cam_Image_Coords,1);

%% 4. Space Intersection by Collinearity - Iterative Solution
% Based off of Elements of Photogrammetry with Applications in GIS (4th edition) Chapter 11 & Appendix B,D

while counter < 5 %max(abs(DELTA)) >.00000001
    counter = counter + 1;
    
    % Based off of ESSE3650_08_Colinearity_01FEB2017.pdf slide 35, 2.1.
    m11 = cos(phi)*cos(kappa);
    m12 = sin(omega)*sin(phi)*cos(kappa)+cos(omega)*sin(kappa);
    m13 = -cos(omega)*sin(phi)*cos(kappa)+sin(omega)*sin(kappa);
    m21 = -cos(phi)*sin(kappa);
    m22 = -sin(omega)*sin(phi)*sin(kappa)+cos(omega)*cos(kappa);
    m23 = cos(omega)*sin(phi)*sin(kappa)+sin(omega)*cos(kappa);
    m31 = sin(phi);
    m32 = -sin(omega)*cos(phi);
    m33 = cos(omega)*cos(phi);
    
    M = [m11 m12 m13;
        m21 m22 m23;
        m31 m32 m33];
    
    % Elements of Photogrammetry... - Appendix D.5. (D-12) Linerization of Collinearity Equations
    % ESSE3650_08_Colinearity_01FEB2017.pdf slide 35, 2.2.1.
    for i = 1:1:count
        dX(i)=X(i)-XL;
        dY(i)=Y(i)-YL;
        dZ(i)=Z(i)-ZL;
        
        Q(i) = (m31*dX(i)) + (m32*dY(i)) + (m33*dZ(i));
        R(i) = (m11*dX(i)) + (m12*dY(i)) + (m13*dZ(i));
        S(i) = (m21*dX(i)) + (m22*dY(i)) + (m23*dZ(i));
    end
    
    % Elements of Photogrammetry... - Appendix D.5. (D-11) Linerization of Collinearity Equations
    for i = 1:1:count
        J(i) = x(i) + (f*(R(i)/Q(i)));
        K(i) = y(i) + (f*(S(i)/Q(i)));
    end
    
    eps = [J(1);K(1);J(2);K(2);J(3);K(3);J(4);K(4)];
 
    
    % Elements of Photogrammetry... - Appendix D.5. (D-16) B-Matrix Eqns
    for i = 1:1:count
        b(i,4) = (f/Q(i)^2)*(R(i)*m31-Q(i)*m11);
        b(i,5) = (f/Q(i)^2)*(R(i)*m32-Q(i)*m12);
        b(i,6) = (f/Q(i)^2)*(R(i)*m33-Q(i)*m13);
        
        %b(1,7) = b21, b(1,8) = b22, and so on.
        b(i,10) = (f/Q(i)^2)*(S(i)*m31-Q(i)*m21);
        b(i,11) = (f/Q(i)^2)*(S(i)*m32-Q(i)*m22);
        b(i,12) = (f/Q(i)^2)*(S(i)*m33-Q(i)*m23);
    end
    
    B = [b(1,4)  b(1,5)  b(1,6);
         b(1,10) b(1,11) b(1,12);
         b(2,4)  b(2,5)  b(2,6);
         b(2,10) b(2,11) b(2,12);
         b(3,4)  b(3,5)  b(3,6);
         b(3,10) b(3,11) b(3,12);
         b(4,4)  b(4,5)  b(4,6);
         b(4,10) b(4,11) b(4,12)];
    
    % Elements of Photogrammetry... - Appendix B.9. (B-13) Matrix Methods in Least Squares Adjustment Solution
    DELTA = inv(B'*B)*(B'*eps)
    
    %omega =  DELTA(1) + omega
    %phi = DELTA(2) + phi
    %kappa = DELTA(3) + kappa
    
    XL = DELTA(1) + XL
    YL = DELTA(2) + YL
    ZL = DELTA(3) + ZL
   
end

%% 5. Output

%omegaL = (180/pi) * omega
%phiL = (180/pi) * phi
%kappaL = (180/pi) * kappa

XT = XL
YT = YL
ZT = ZL

intersect_Coords = [XT, YT, ZT]
%orientation_Angles = [omegaL, phiL, kappaL]
counter
