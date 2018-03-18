function [XT,YT,ZT] = ImgIntersect(XA,XB,YA,YB,ZA,ZB,omegaA,omegaB,phiA,phiB,kappaA,kappaB)
%% Space Intersection by Collinearity
%% Takes in 2 existing inputs locations to calculated the location of an object

% Defining initial parameters
% 2 initial XYZ space coordinates, XA,YA,ZA and XB,YB,ZB
% 2 initial image coordinates, xA,yA and xB,yB
% 2 intiital rotations omegaA,phiA,kappaA and omegaB,phiB,kappaB

pixSize = 0.00112;
width_Of_Image = 3280/2;
height_Of_Image = 2464/2;


xPix = [1395 2090];
yPix = [1639 808];

% image coordinates
%{
for i = 1:1:2
    x(i) = (xPix(i) - width_Of_Image - 0.5) * pixSize
    y(i) = (height_Of_Image - yPix(i) + 0.5) * pixSize
end
%}

x = [-12.843 -22.720 -0.433 -25.993];
y = [-54.155 -4.828 70.321 -58.086];

%% Computation Parameters
% Focal length
%f = 3.04;
f = 152.057;

% Rotation orientation matrix
omega = [omegaA omegaB];
phi = [phiA phiB];
kappa = [kappaA kappaB];

%% Iterating Parameters

% Count and counter
count = 2;
counter = 0;

% iterator
iter = 1;

% Setting the tolerance
tor = 0.00000000056;

% Empty
dX = 0;
dY = 0;
dZ = 0;

%% Rotation matrix for two rotation parameters
for i = 1:1:count
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

while  iter < 3
    if counter == 0
        dX = XB-XA;
        dY = YB-YA;
        dZ = ZB-ZA;
        
    elseif counter > 0
        dX = dX;
        dY = dY;
        dZ = dZ;
    end
    
    counter = counter + 1;
    %% coefficient RSQ
    for i = 1:1:count
        R(i) = m11(i)*(dX)+m12(i)*(dY)+m13(i)*(dZ);
        S(i) = m21(i)*(dX)+m22(i)*(dY)+m23(i)*(dZ);
        Q(i) = m31(i)*(dX)+m32(i)*(dY)+m33(i)*(dZ);
    end
    
    %% Calculate the ground coordinates of the ground control points J,K from image coordinates
    for i = 1:1:count*2
        J(i) = -x(i) +(R(1)*f)/Q(1);
        K(i) = -y(i) +(S(1)*f)/Q(1);
        
        J(i+4) = -x(i) +(R(2)*f)/Q(2);
        K(i+4) = -y(i) +(S(2)*f)/Q(2);
    end
    
    % L matrix
    eps = [J(1);K(1);J(2);K(2);J(3);K(3);J(4);K(4);J(5);K(5);J(6);K(6);J(7);K(7);J(8);K(8)];
    
    %% B matrix
    % Design b matrix of determing object point location of A(X,Y,Z)
    for i = 1:1:count*2
        b(i,1) = (f/Q(1)^2)*(R(1)*m31(1)-Q(1)*m11(1));
        b(i,2) = (f/Q(1)^2)*(R(1)*m32(1)-Q(1)*m12(1));
        b(i,3) = (f/Q(1)^2)*(R(1)*m33(1)-Q(1)*m13(1));
        
        b(i,4) = (f/Q(1)^2)*(S(1)*m31(1)-Q(1)*m21(1));
        b(i,5) = (f/Q(1)^2)*(S(1)*m32(1)-Q(1)*m22(1));
        b(i,6) = (f/Q(1)^2)*(S(1)*m33(1)-Q(1)*m23(1));
        
        b(i,7) = (f/Q(2)^2)*(R(2)*m31(2)-Q(2)*m11(2));
        b(i,8) = (f/Q(2)^2)*(R(2)*m32(2)-Q(2)*m12(2));
        b(i,9) = (f/Q(2)^2)*(R(2)*m33(2)-Q(2)*m13(2));
        
        b(i,10) = (f/Q(2)^2)*(S(2)*m31(1)-Q(2)*m21(2));
        b(i,11) = (f/Q(2)^2)*(S(2)*m32(1)-Q(2)*m22(2));
        b(i,12) = (f/Q(2)^2)*(S(2)*m33(1)-Q(2)*m23(2));
    end
    
    % B matrix
    B = [b(1,1)  b(1,2)  b(1,3);
        b(1,4) b(1,5) b(1,6);
        b(1,7)  b(1,8)  b(1,9);
        b(1,10) b(1,11) b(1,12);
        b(2,1)  b(2,2)  b(2,3);
        b(2,4) b(2,5) b(2,6);
        b(2,7)  b(2,8)  b(2,9);
        b(2,10) b(2,11) b(2,12);   
        b(3,1)  b(3,2)  b(3,3);
        b(3,4) b(3,5) b(3,6);
        b(3,7)  b(3,8)  b(3,9);
        b(3,10) b(3,11) b(3,12);
        b(4,1)  b(4,2)  b(4,3);
        b(4,4) b(4,5) b(4,6);
        b(4,7)  b(4,8)  b(4,9);
        b(4,10) b(4,11) b(4,12)
        ];
    
    % Least Squares Solution of B matrix
    DELTA = inv(B'*B)*(B'*eps)
    %iter = rssq(DELTA);
    iter = iter + 1;
    
    % iterative parameters
    dX = DELTA(1)+ dX
    dY = DELTA(2)+ dY
    dZ = DELTA(3)+ dZ
end

XT = dX
YT = dY
ZT = dZ

end
