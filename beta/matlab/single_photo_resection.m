%% ENG4000 U-TRACKR SPACE RESECTION, 2D-3D POSITIONING

clc; 
clear all; 
close all;

%% 1. Input Data
% interior camera orientation params (mm)
f = 2.616; % focal length (mm)
xo = 0.2154;
yo = -0.4175;

% camera pixel size (m) https://www.raspberrypi.org/documentation/hardware/camera/README.md
pixSizeX = 0.00000112;
pixSizeY = 0.00000112;

% image width and height (pix)
imgWidth = 3280;
imgHeight = 2464; 

% pixel coordinates of the 13 points in cam1.jpg: [x,y] (pix)
cam_Pixel_Coords=[
    2006	705;
    1502	603;
    1226	820;
    1069	1240;
    1287	1619;
    1585	1806;
    2057	1644;
    2137	1138;
    1375	217;
    712		1256;
    1515	2183;
    2440	1181;
    1451	1207];

% % pixel coordinates of the 4 points in cam2.jpg: [x,y] (pix)
% cam_Pixel_Coords=[
%     2099 1729;
%     2095 858;
%     1401 914;
%     1392 1654];
 
% ground control coordinates [X,Y,Z] (m)
cam_Ground_Control_Coords=[
	0.44	0.176	0;
	0.616	0.264	0.057;
	0.704	0.44	0;
	0.616	0.616	0.060;
	0.44	0.704	0;
	0.264	0.616	0.060;
	0.176	0.44	0;
	0.264	0.264	0.061;
	0.704	0.176	0.142;
	0.704	0.704	0.144;
	0.176	0.704	0.143;
	0.176	0.176	0.144;
	0.44	0.44	0.141];

% initial exterior orientation coords parameters cam1.jpg (m)
x0 = 0.05;
y0 = 0.05;
z0 = 0.98;

% % initial exterior orientation coords parameters cam2.jpg (m)
% x0 = 0.90;
% y0 = 0.01;
% z0 = 1.10;

% initial exterior orientation angle parameters cam1.jpg (rads)
omega = 0.785398; % 45 deg
phi = 0.785398; % 45 deg
kappa = 0;

% % initial exterior orientation angle parameters cam2.jpg (rads)
% omega = 0.785398; % 45 deg
% phi = 0.785398; % 45 deg
% kappa = 1.5708; % 90 deg 

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

%% 4. Space Resection by Collinearity - Iterative Solution
% Based off of Elements of Photogrammetry with Applications in GIS (4th edition) Chapter 11 & Appendix B,D

while max(abs(DELTA)) >.00000001
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
        eps(2*i-1,1) = x(i) + (f*(R(i)/Q(i)));
        eps(2*i,1) = y(i) + (f*(S(i)/Q(i)));
        % J(i) = x(i)-xo + (f*(R(i)/Q(i)));
        % K(i) = y(i)-yo + (f*(S(i)/Q(i)));
        % J(i) = -x(i) +(R(i)*f)/Q(i);
        % K(i) = -y(i) +(S(i)*f)/Q(i);
    end
       
    % Elements of Photogrammetry... - Appendix D.5. (D-16) B-Matrix Eqns
    for i = 1:1:count
        b(i,1) = (f/Q(i)^2)*(R(i)*(-m33*dY(i)+m32*dZ(i))-Q(i)*(-m13*dY(i)+m12*dZ(i)));
        b(i,2) = (f/Q(i)^2)*((R(i)*(cos(phi)*dX(i)+sin(omega)*sin(phi)*dY(i)-cos(omega)*sin(phi)*dZ(i))- Q(i)*(-sin(phi)*cos(kappa)*dX(i)+sin(omega)*cos(phi)*cos(kappa)*dY(i)-cos(omega)*cos(phi)*cos(kappa)*dZ(i))));
        b(i,3) = (-f/Q(i))*(m21*dX(i)+m22*dY(i)+m23*dZ(i));
        b(i,4) = -(f/Q(i)^2)*(R(i)*m31-Q(i)*m11);
        b(i,5) = -(f/Q(i)^2)*(R(i)*m32-Q(i)*m12);
        b(i,6) = -(f/Q(i)^2)*(R(i)*m33-Q(i)*m13);
        
        %b(1,7) = b21, b(1,8) = b22, and so on.
        b(i,7) = (f/Q(i)^2)*(S(i)*(-m33*dY(i)+m32*dZ(i))-Q(i)*(-m23*dY(i)+m22*dZ(i)));
        b(i,8) = (f/Q(i)^2)*((S(i)*(cos(phi)*dX(i)+sin(omega)*sin(phi)*dY(i)-cos(omega)*sin(phi)*dZ(i))- Q(i)*(sin(phi)*sin(kappa)*dX(i)-sin(omega)*cos(phi)*sin(kappa)*dY(i)+cos(omega)*cos(phi)*sin(kappa)*dZ(i))));
        b(i,9) = (f/Q(i))*(m11*dX(i)+m12*dY(i)+m13*dZ(i));
        b(i,10) = -(f/Q(i)^2)*(S(i)*m31-Q(i)*m21);
        b(i,11) = -(f/Q(i)^2)*(S(i)*m32-Q(i)*m22);
        b(i,12) = -(f/Q(i)^2)*(S(i)*m33-Q(i)*m23);
        
        % assembling B design matrix 
        B(2*i-1,1:6) = [b(i,1) b(i,2) b(i,3) b(i,4) b(i,5) b(i,6)];
        B(2*i,1:6) = [b(i,7) b(i,8) b(i,9) b(i,10) b(i,11) b(i,12)];
    end
    
    % Elements of Photogrammetry... - Appendix B.9. (B-13) Matrix Methods in Least Squares Adjustment Solution
    DELTA = inv(B'*B)*(B'*eps)
    
    % Iterative parameters 
    omega =  DELTA(1) + omega
    phi = DELTA(2) + phi
    kappa = DELTA(3) + kappa
    XL = DELTA(4) + XL
    YL = DELTA(5) + YL
    ZL = DELTA(6) + ZL   
end

%% 5. Output
omegaL = (180/pi) * omega
phiL = (180/pi) * phi
kappaL = (180/pi) * kappa
XT = XL
YT = YL
ZT = ZL

resection_Coords = [XT, YT, ZT]
orientation_Angles = [omegaL, phiL, kappaL]

counter
