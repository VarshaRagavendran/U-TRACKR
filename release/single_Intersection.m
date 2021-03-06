%% ENG4000 U-TRACKR SPACE INTERSECTION, 3D POSITIONING

clc;
clear all;
close all;

%% 1. Input Data
% focal length (mm)
f = 3.04;

% Video feed images
cam_Image_Coords=[
   -0.6778   -0.2794;
   -0.3164    0.4642;
    0.7095    0.3074
];

cam_Ground_Control_Coords= [
   0.0353166681 0.7939111255 0.7933969121;
   0.03684110851 0.1065042173 0.7987291604;
   1.044962932 0.9715076934 1.012035044];

omega = [0.3894798702;	0.3834680869;	-0.3276393065];
phi = [-0.3819569536;	0.332866596;	0.2990655086];
kappa = [-2.283401489;	-0.8981148577;	-5.445299646];

% Image Coords (mm)
x  = cam_Image_Coords(:,1);
y  = cam_Image_Coords(:,2);

% Space/Ground Control coords (m)
X  = cam_Ground_Control_Coords(:,1);
Y  = cam_Ground_Control_Coords(:,2);
Z  = cam_Ground_Control_Coords(:,3);

% Initial orientation parameters
DELTA=[1 1 1];

% Iterative solution coordinates (m)
XL = 0;
YL = 0;
ZL = 0;

% Counter to count number of iterations
counter = 1;

% Count is the size of the matrix
count = size(cam_Image_Coords,1);

%% 4. Space Intersection by Collinearity - Iterative Solution
% Based off of ESSE3650_08_Colinearity_01FEB2017.pdf slide 35, 2.1.
for i=1:1:count
    m11(i) = cos(phi(i))*cos(kappa(i));
    m12(i) = sin(omega(i))*sin(phi(i))*cos(kappa(i))+cos(omega(i))*sin(kappa(i));
    m13(i) = -cos(omega(i))*sin(phi(i))*cos(kappa(i))+sin(omega(i))*sin(kappa(i));
    m21(i) = -cos(phi(i))*sin(kappa(i));
    m22(i) = -sin(omega(i))*sin(phi(i))*sin(kappa(i))+cos(omega(i))*cos(kappa(i));
    m23(i) = cos(omega(i))*sin(phi(i))*sin(kappa(i))+sin(omega(i))*cos(kappa(i));
    m31(i) = sin(phi(i));
    m32(i) = -sin(omega(i))*cos(phi(i));
    m33(i) = cos(omega(i))*cos(phi(i));
    
end

% Based off of Elements of Photogrammetry with Applications in GIS (4th edition) Chapter 11 & Appendix B,D
while counter < 40
    counter = counter + 1;
   
    % Elements of Photogrammetry... - Appendix D.5. (D-12) Linerization of Collinearity Equations
    % ESSE3650_08_Colinearity_01FEB2017.pdf slide 35, 2.2.1.
    
    for i = 1:1:count
        dX(i) = (X(i)-XL);
        dY(i) = (Y(i)-YL);
        dZ(i) = (Z(i)-ZL); 
        
        Q(i) = (m31(i)* dX(i)) + (m32(i)* dY(i)) + (m33(i)*dZ(i));
        R(i) = (m11(i)* dX(i)) + (m12(i)* dY(i)) + (m13(i)*dZ(i));
        S(i) = (m21(i)* dX(i)) + (m22(i)* dY(i)) + (m23(i)*dZ(i));
    end
    
    % Elements of Photogrammetry... - Appendix D.5. (D-11) Linerization of Collinearity Equations
    for i = 1:1:count
        eps(2*i-1,1) = x(i) + (f*(R(i)/Q(i)));
        eps(2*i,1) = y(i) + (f*(S(i)/Q(i)));
    end
    
    % Elements of Photogrammetry... - Appendix D.5. (D-16) B-Matrix Eqns
    for i = 1:1:count
        b(i,1) = -(f/Q(i)^2)*(R(i)*m31(i)-Q(i)*m11(i));
        b(i,2) = -(f/Q(i)^2)*(R(i)*m32(i)-Q(i)*m12(i));
        b(i,3) = -(f/Q(i)^2)*(R(i)*m33(i)-Q(i)*m13(i));
        
        b(i,4) = -(f/Q(i)^2)*(S(i)*m31(i)-Q(i)*m21(i));
        b(i,5) = -(f/Q(i)^2)*(S(i)*m32(i)-Q(i)*m22(i));
        b(i,6) = -(f/Q(i)^2)*(S(i)*m33(i)-Q(i)*m23(i));
        
        B(2*i-1,1:3) = [b(i,1) b(i,2) b(i,3)];
        B(2*i,1:3)= [b(i,4) b(i,5) b(i,6)];
    end
    
    % Elements of Photogrammetry... - Appendix B.9. (B-13) Matrix Methods in Least Squares Adjustment Solution
    DELTA = inv(B'*B)*(B'*eps)
    
    XL = DELTA(1) + XL
    YL = DELTA(2) + YL
    ZL = DELTA(3) + ZL
    
end

%% 5. Output

XT = XL
YT = YL
ZT = ZL

intersect_Coords = [XT, YT, ZT]
counter
