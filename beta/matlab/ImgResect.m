function [XT,YT,ZT,omegaL, phiL, kappaL] = ImgResect(x0,y0,z0,omega,phi,kappa)
%% retriving data
%cam1 = readtable('ImageCoords1234test.xlsx');

%cam1_Image_X = table2array(cam1(:,2));
%cam1_Image_Y = table2array(cam1(:,3));

%cam1_Image_Coords= [cam1_Image_X(:), cam1_Image_Y(:)];

cam1_Image_Coords=[
86.421 -83.977;
-100.916 92.582;
-98.322	-89.161;
78.812	98.123
    ];
%{    
0.1011   -0.0300;
   -1.6686    1.0540;
   -1.6311    1.2614;
   -1.4090    1.2511
%}

f = 152.916;

cam1_Space_Coords = [
1268.102 1455.027 22.606;
732.181	545.344	22.299;
1454.553 731.666 22.649;
545.245 1268.232 22.336
];
    %{
    440 176 0;
    704 440 0;
    440 704 0;
    176 440 0
%}



%% Estimate ZL =
% image coords
x  = cam1_Image_Coords(:,1);
y  = cam1_Image_Coords(:,2);

% Space coords
X  = cam1_Space_Coords (:,1);
Y  = cam1_Space_Coords (:,2);
Z  = cam1_Space_Coords (:,3);

%% initial orientation parameters
DELTA=[1 1 1 1 1 1 1];

XL = x0;
YL = y0;
ZL = z0;

%% b matrix
count = size(cam1_Image_Coords,1);
counter = 1;
% setting the tolerance
tor = 0.00000000056;

while  counter < 3
    %min(abs(DELTA)) > 0.01
    %counter = counter+1;
    
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
    
    for i = 1:1:count
        % difference
        dX(i)=X(i)-XL;
        dY(i)=Y(i)-YL;
        dZ(i)=Z(i)-ZL;
        
        % RSQ
        R(i) = m11*(X(i)-XL)+m12*(Y(i)-YL)+m13*(Z(i)-ZL);
        S(i) = m21*(X(i)-XL)+m22*(Y(i)-YL)+m23*(Z(i)-ZL);
        Q(i) = m31*(X(i)-XL)+m32*(Y(i)-YL)+m33*(Z(i)-ZL);
    end
    
    %% Calculate the ground coordinates of the ground control points J,K from image coordinates
    for i = 1:1:count
        J(i) = -x(i) +(R(i)*f)/Q(i);
        K(i) = -y(i) +(S(i)*f)/Q(i);
    end
    
    eps = [J(1);K(1);J(2);K(2);J(3);K(3);J(4);K(4)];
    
    %% B matrix
    for i = 1:1:count
        b(i,1) = (f/Q(i)^2)*(R(i)*(-m33*dY(i)+m32*dZ(i))-Q(i)*(-m13*dY(i)+m12*dZ(i)));
        b(i,2) = (f/Q(i)^2)*((R(i)*(cos(phi)*dX(i)+sin(omega)*sin(phi)*dY(i)-cos(omega)*sin(phi)*dZ(i))- Q(i)*(-sin(phi)*cos(kappa)*dX(i)+sin(omega)*cos(phi)*cos(kappa)*dY(i)-cos(omega)*cos(phi)*cos(kappa)*dZ(i))));
        b(i,3) = (-f/Q(i))*(m21*dX(i)+m22*dY(i)+m23*dZ(i));
        b(i,4) = (f/Q(i)^2)*(R(i)*m31-Q(i)*m11);
        b(i,5) = (f/Q(i)^2)*(R(i)*m32-Q(i)*m12);
        b(i,6) = (f/Q(i)^2)*(R(i)*m33-Q(i)*m13);
        
        b(i,7) = (f/Q(i)^2)*(S(i)*(-m33*dY(i)+m32*dZ(i))-Q(i)*(-m23*dY(i)+m22*dZ(i)));
        b(i,8) = (f/Q(i)^2)*((S(i)*(cos(phi)*dX(i)+sin(omega)*sin(phi)*dY(i)-cos(omega)*sin(phi)*dZ(i))- Q(i)*(-sin(phi)*cos(kappa)*dX(i)+sin(omega)*cos(phi)*cos(kappa)*dY(i)-cos(omega)*cos(phi)*cos(kappa)*dZ(i))));
        b(i,9) = (f/Q(i))*(m11*dX(i)+m12*dY(i)+m13*dZ(i));
        b(i,10) = (f/Q(i)^2)*(S(i)*m31-Q(i)*m21);
        b(i,11) = (f/Q(i)^2)*(S(i)*m32-Q(i)*m22);
        b(i,12) = (f/Q(i)^2)*(S(i)*m33-Q(i)*m23);
    end
    
    B = [b(1,1) b(1,2) b(1,3) b(1,4)  b(1,5)  b(1,6);
        b(1,7) b(1,8) b(1,9) b(1,10) b(1,11) b(1,12);
        b(2,1) b(2,2) b(2,3) b(2,4)  b(2,5)  b(2,6);
        b(2,7) b(2,8) b(2,9) b(2,10) b(2,11) b(2,12);
        b(3,1) b(3,2) b(3,3) b(3,4)  b(3,5)  b(3,6);
        b(3,7) b(3,8) b(3,9) b(3,10) b(3,11) b(3,12);
        b(4,1) b(4,2) b(4,3) b(4,4)  b(4,5)  b(4,6);
        b(4,7) b(4,8) b(4,9) b(4,10) b(4,11) b(4,12)];
    
    %B matrix - changes
    DELTA = inv(B'*B)*(B'*eps)
    counter = rssq(DELTA);
    
    omega =  DELTA(1)+ omega
    phi = DELTA(2)+ phi
    kappa = DELTA(3)+ kappa
    XL = DELTA(4)+ XL
    YL = DELTA(5)+ YL
    ZL = DELTA(6)+ ZL
    
    
end

omegaL = (180/pi)*omega
phiL = (180/pi)*phi
kappaL = (180/pi)*kappa
XT = XL
YT = YL
ZT = ZL/3

end
