%% Image Space Resection V1.0
% Calculation of initial camera position and angles 
% final results output into 
% calcOmega, calcPhi, calcKappa, calcXL, calcYL, calc ZL
% Message me if you need any help with knowing the aspects of the code

close all;
clc;
clear all;

cam1 = readtable('ImageCoords1234test.xlsx');
%Setting initial EO parameters finding XL,YL,ZL
omega = 0;
phi = 0;

%% INPUT INITIAL PARAMETERS FOR SPACE RESECTION
% f = 3.04 for our focal length of cameras 
% cam1_Image_Coords = calculated image coordinates from pixel coordinates
% retrieved from cams
% caml_Space_Coordinates = frame space coordinates of fixed points. At
% least 4 with xyz needed in order to perform space resection

cam1_Image_X = table2array(cam1(:,2));
cam1_Image_Y = table2array(cam1(:,3));

%cam1_Image_Coords= [cam1_Image_X(:), cam1_Image_Y(:)];

 cam1_Image_Coords=[    -1.4004    1.0293;
   -1.6686    1.0540;
   -1.6311    1.2614;
   -1.4090    1.2511];

f = 3.04;

cam1_Space_Coords = [0.44 0.176 0.0635;
                    0.704 0.44 0.0635;
                    0.44 0.704 0.0635;
                    0.176 0.44 0.0635];
   
%cam1_Image_Coords = [86.421 -83.977;
  %    -100.916 92.582;
   %   -98.322 -89.161;
    %  78.812 98.123];
  
%f = 152.916;


%cam1_Space_Coords = [1268.101 1455.027 22.606;
 %   732.181 545.344 22.299;
  %  1454.553 731.666 22.649;
   % 545.245 1268.232 22.336];

%% Estimate ZL =
% image coords
x  = cam1_Image_Coords(:,1);
y  = cam1_Image_Coords(:,2); 

% Space coords
X  = cam1_Space_Coords (:,1);
Y  = cam1_Space_Coords (:,2);
Z  = cam1_Space_Coords (:,3);

abSquare = (cam1_Space_Coords(1,1)- cam1_Space_Coords(2,1))^2 + (cam1_Space_Coords(1,2)- cam1_Space_Coords(2,2))^2 ;

syms H 

p = (((x(1)/f)*(H-Z(1)))-((x(2)/f)*(H-Z(2))))^2 + (((y(1)/f)*(H-Z(1)))-((y(2)/f)*(H-Z(2))))^2 - abSquare;

r = vpasolve(p);

for i = 1:length(r)
    if r(i) > 0 
      ZL = double(r(i));
    end 
end

%% Calculate the ground coordinates of the ground control points
for i = 1:1:4
    XC(i) = x(i)*((ZL - Z(i))/f); 
    YC(i) = y(i)*((ZL - Z(i))/f);
end

%% Computing 2D conformal coordinates transformation for LSA
% L matrix

Lmat= [X(1);
    Y(1);
    X(2);
    Y(2);
    X(3);
    Y(3);
    X(4);
    Y(4)];

Amat = [XC(1) -YC(1) 1 0;
         YC(1) XC(1) 0 1;
        XC(2) -YC(2) 1 0;
         YC(2) XC(2) 0 1;
        XC(3) -YC(3) 1 0;
         YC(3) XC(3) 0 1;
        XC(4) -YC(4) 1 0;
         YC(4) XC(4) 0 1 ];
   

Xmat = inv(Amat'*Amat)*Amat'*Lmat;

kappa = atand(Xmat(2)/Xmat(1))+180;

%% First run loop forming the rotation matrix

theta = kappa; 

 m11 = cosd(phi)*cosd(kappa);
 m12 = sind(omega)*sind(phi)*cosd(kappa)+cosd(omega)*sind(kappa);
 m13 = -cosd(omega)*sind(phi)*cosd(kappa)+sind(omega)*sind(kappa);
 m21 = -cosd(phi)*sind(kappa);
 m22 = -sind(omega)*sind(phi)*sind(kappa)+cosd(omega)*cosd(kappa);
 m23 = cosd(omega)*sind(phi)*cosd(kappa)+sind(omega)*sind(kappa);
 m31 = sind(phi);
 m32 = -sind(omega)*cosd(phi);
 m33 = cosd(omega)*cosd(phi);
 
M = [m11 m12 m13;
    m21 m22 m23;
    m31 m32 m33];

for i = 1:1:4
    deltaX(i) = X(i) - Xmat(3);
    deltaY(i) = Y(i) - Xmat(4);
    deltaZ(i) = Z(i) - ZL;
end 

%% forming RSQ matrix
for i = 1:1:4
R(i) = m11*deltaX(i)+m12*deltaY(i)+m13*deltaZ(i);
S(i) = m21*deltaX(i)+m22*deltaY(i)+m23*deltaZ(i);
Q(i) = m31*deltaX(i)+m32*deltaY(i)+m33*deltaZ(i);

end
%% forming B matrix run 1
for i = 1:1:4
b(i,1) = (f/Q(i)^2)*(R(i)*(-m33*deltaY(i)+m32*deltaZ(i))-Q(i)*(-m13*deltaY(i)+m12*deltaZ(i)));
b(i,2) = (f/Q(i)^2)*((R(i)*(cosd(phi)*deltaX(i)+sind(omega)*sind(phi)*deltaY(i)-cosd(omega)*sind(phi)*deltaZ(i))- Q(i)*(-sind(phi)*cosd(kappa)*deltaX(i)+sind(omega)*cosd(phi)*cosd(kappa)*deltaY(i)-cosd(omega)*cosd(phi)*cosd(kappa)*deltaZ(i))));
b(i,3) = (-f/Q(i))*(m21*deltaX(i)+m22*deltaY(i)+m23*deltaZ(i));
b(i,4) = (f/Q(i)^2)*(R(i)*m31-Q(i)*m11);
b(i,5) = (f/Q(i)^2)*(R(i)*m32-Q(i)*m12);
b(i,6) = (f/Q(i)^2)*(R(i)*m33-Q(i)*m13);

b(i,7) = (f/Q(i)^2)*(S(i)*(-m33*deltaY(i)+m32*deltaZ(i))-Q(i)*(-m23*deltaY(i)+m22*deltaZ(i)));
b(i,8) = (f/Q(i)^2)*((S(i)*(cosd(phi)*deltaX(i)+sind(omega)*sind(phi)*deltaY(i)-cosd(omega)*sind(phi)*deltaZ(i))- Q(i)*(-sind(phi)*cosd(kappa)*deltaX(i)+sind(omega)*cosd(phi)*cosd(kappa)*deltaY(i)-cosd(omega)*cosd(phi)*cosd(kappa)*deltaZ(i))));
b(i,9) = (f/Q(i))*(m11*deltaX(i)+m12*deltaY(i)+m13*deltaZ(i));
b(i,10) = (f/Q(i)^2)*(S(i)*m31-Q(i)*m21);
b(i,11) = (f/Q(i)^2)*(S(i)*m32-Q(i)*m22);
b(i,12) = (f/Q(i)^2)*(S(i)*m33-Q(i)*m23);
end
% +b19 change
%B matrix - changes
B = [b(1,1) b(1,2) b(1,3) -b(1,4)  -b(1,5)  -b(1,6);
     b(1,7) b(1,8) b(1,9) -b(1,10) -b(1,11) -b(1,12);
     b(2,1) b(2,2) b(2,3) -b(2,4)  -b(2,5)  -b(2,6);
     b(2,7) b(2,8) b(2,9) -b(2,10) -b(2,11) -b(2,12);
     b(3,1) b(3,2) b(3,3) -b(3,4)  -b(3,5)  -b(3,6);
     b(3,7) b(3,8) b(3,9) -b(3,10) -b(3,11) -b(3,12);
     b(4,1) b(4,2) b(4,3) -b(4,4)  -b(4,5)  -b(4,6);
     b(4,7) b(4,8) b(4,9) -b(4,10) -b(4,11) -b(4,12)];
 
 %% domega dphi dkappa dX dY dZ
DELTA = inv(B'*B)*(B'*Lmat);

%% second run
omega = DELTA(1);
phi = DELTA(2);
kappa = DELTA(3);

 m11r2 = cosd(phi)*cosd(kappa);
 m12r2 = sind(omega)*sind(phi)*cosd(kappa)+cosd(omega)*sind(kappa);
 m13r2 = -cosd(omega)*sind(phi)*cosd(kappa)+sind(omega)*sind(kappa);
 m21r2 = -cosd(phi)*sind(kappa);
 m22r2 = -sind(omega)*sind(phi)*sind(kappa)+cosd(omega)*cosd(kappa);
 m23r2 = cosd(omega)*sind(phi)*cosd(kappa)+sind(omega)*sind(kappa);
 m31r2 = sind(phi);
 m32r2 = -sind(omega)*cosd(phi);
 m33r2 = cosd(omega)*cosd(phi);
 
Mr2 = [m11r2 m12r2 m13r2;
    m21r2 m22r2 m23r2;
    m31r2 m32r2 m33r2];

%% forming RSQ matrix
for i = 1:1:4
R2(i) = m11r2*deltaX(i)+m12r2*deltaY(i)+m13r2*deltaZ(i);
S2(i) = m21r2*deltaX(i)+m22r2*deltaY(i)+m23r2*deltaZ(i);
Q2(i) = m31r2*deltaX(i)+m32r2*deltaY(i)+m33r2*deltaZ(i);

end
%% forming B matrix
for i = 1:1:4
b2(i,1) = (f/Q2(i)^2)*(R2(i)*(-m33r2*deltaY(i)+m32r2*deltaZ(i))-Q2(i)*(-m13r2*deltaY(i)+m12r2*deltaZ(i)));
b2(i,2) = (f/Q2(i)^2)*((R2(i)*(cosd(phi)*deltaX(i)+sind(omega)*sind(phi)*deltaY(i)-cosd(omega)*sind(phi)*deltaZ(i))- Q2(i)*(-sind(phi)*cosd(kappa)*deltaX(i)+sind(omega)*cosd(phi)*cosd(kappa)*deltaY(i)-cosd(omega)*cosd(phi)*cosd(kappa)*deltaZ(i))));
b2(i,3) = (-f/Q2(i))*(m21r2*deltaX(i)+m22r2*deltaY(i)+m23r2*deltaZ(i));
b2(i,4) = (f/Q2(i)^2)*(R2(i)*m31r2-Q2(i)*m11r2);
b2(i,5) = (f/Q2(i)^2)*(R2(i)*m32r2-Q2(i)*m12r2);
b2(i,6) = (f/Q2(i)^2)*(R2(i)*m33r2-Q2(i)*m13r2);

b2(i,7) = (f/Q2(i)^2)*(S2(i)*(-m33r2*deltaY(i)+m32r2*deltaZ(i))-Q2(i)*(-m23r2*deltaY(i)+m22r2*deltaZ(i)));
b2(i,8) = (f/Q2(i)^2)*((S2(i)*(cosd(phi)*deltaX(i)+sind(omega)*sind(phi)*deltaY(i)-cosd(omega)*sind(phi)*deltaZ(i))- Q2(i)*(-sind(phi)*cosd(kappa)*deltaX(i)+sind(omega)*cosd(phi)*cosd(kappa)*deltaY(i)-cosd(omega)*cosd(phi)*cosd(kappa)*deltaZ(i))));
b2(i,9) = (f/Q2(i))*(m11r2*deltaX(i)+m12r2*deltaY(i)+m13r2*deltaZ(i));
b2(i,10) = (f/Q2(i)^2)*(S2(i)*m31r2-Q2(i)*m21r2);
b2(i,11) = (f/Q2(i)^2)*(S2(i)*m32r2-Q2(i)*m22r2);
b2(i,12) = (f/Q2(i)^2)*(S2(i)*m33r2-Q2(i)*m23r2);
end
% +b19 change
%B matrix - changes
B2 = [b2(1,1) b2(1,2) b2(1,3) -b2(1,4)  -b2(1,5)  -b2(1,6);
     b2(1,7) b2(1,8) b2(1,9) -b2(1,10) -b2(1,11) -b2(1,12);
     b2(2,1) b2(2,2) b2(2,3) -b2(2,4)  -b2(2,5)  -b2(2,6);
     b2(2,7) b2(2,8) b2(2,9) -b2(2,10) -b2(2,11) -b2(2,12);
     b2(3,1) b2(3,2) b2(3,3) -b2(3,4)  -b2(3,5)  -b2(3,6);
     b2(3,7) b2(3,8) b2(3,9) -b2(3,10) -b2(3,11) -b2(3,12);
     b2(4,1) b2(4,2) b2(4,3) -b2(4,4)  -b2(4,5)  -b2(4,6);
     b2(4,7) b2(4,8) b2(4,9) -b2(4,10) -b2(4,11) -b2(4,12)];
 
 %% domega dphi dkappa dX dY dZ
DELTA2 = inv(B2'*B)*(B2'*Lmat);



 %% Second Run forming the rotation matrix



 
 
 %% calculated angles omega phi kappa and XYZ
 calcOmega = 0 + DELTA2(1)*(180/pi)
 if calcOmega <= 0 
     calcOmega = calcOmega + 360
 elseif calcOmega >= 360
     calcOmega = calcOmega - 360
 end
 
 calcPhi = 0 + DELTA2(2)*(180/pi) + 360
 if calcPhi <= 0 
     calcPhi = calcPhi+ 360
 elseif calcPhi >= 360
     calcPhi = calcPhi - 360
 end
 
 calcKappa = theta + DELTA2(3) 
 if  calcKappa <= 0 
      calcKappa =  calcKappa+ 360
 elseif  calcKappa >= 360
      calcKappa =  calcKappa - 360
 end
 
 calcXL = DELTA2(4)+Xmat(3)
 calcYL = DELTA2(5)+Xmat(4)
 calcZL = DELTA2(6)+ ZL
 
 tic; toc 
 

 
