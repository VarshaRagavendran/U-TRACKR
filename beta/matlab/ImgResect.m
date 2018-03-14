function [XT,YT,ZT,omegaL, phiL, kappaL] = ImgResect(x0,y0,z0,omega,phi,kappa)
%% retriving data
%cam1 = readtable('ImageCoords1234test.xlsx');

%cam1_Image_X = table2array(cam1(:,2));
%cam1_Image_Y = table2array(cam1(:,3));

%cam1_Image_Coords= [cam1_Image_X(:), cam1_Image_Y(:)];

cam1_Image_Coords=[
      0.10038     -0.16012
     -0.16785     -0.13547
     -0.13031     0.071987
     0.091838     0.061661
    ];

f = 3.04;

cam1_Space_Coords = [44 17.6 6.35;
    70.4 44 6.35;
    44 70.4 6.35;
    17.6 44 6.35];

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

%% b matrix
count = size(cam1_Image_Coords,1);
counter = 0
% while max(abs(DELTA)) > 0.01
while counter < 30
    counter = counter+1;
    
    m11 = cos(phi)*cos(kappa);
    m12 = sin(omega)*sin(phi)*cos(kappa)+cos(omega)*sin(kappa);
    m13 = -cos(omega)*sin(phi)*cos(kappa)+sin(omega)*sin(kappa);
    m21 = -cos(phi)*sin(kappa);
    m22 = -sin(omega)*sin(phi)*sin(kappa)+cos(omega)*cos(kappa);
    m23 = cos(omega)*sin(phi)*cos(kappa)+sin(omega)*sin(kappa);
    m31 = sin(phi);
    m32 = -sin(omega)*cos(phi);
    m33 = cos(omega)*cos(phi);
    
    M = [m11 m12 m13;
        m21 m22 m23;
        m31 m32 m33];
    
    for i = 1:1:count
        dx(i)=x0-X(i);
        dy(i)=y0-Y(i);
        dz(i)=z0-Z(i);
        R(i) = m11*(X(i)-x0)+m12*(Y(i)-y0)+m13*(Z(i)-z0);
        S(i) = m21*(X(i)-x0)+m22*(Y(i)-y0)+m23*(Z(i)-z0);
        Q(i) = m31*(X(i)-x0)+m32*(Y(i)-y0)+m33*(Z(i)-z0);
    end
    
    %% Calculate the ground coordinates of the ground control points J,K from image coordinates
    for i = 1:1:count
        J(i) = - x(i) + (R(i)*f)/Q(i);
        K(i) = - y(i) + (S(i)*f)/Q(i);
    end
    
    eps = [J(1);K(1);J(2);K(2);J(3);K(3);J(4);K(4)];
    
    %% B matrix
    for i = 1:1:count
        b(i,1) = (f/Q(i)^2)*(R(i)*(-m33*dy(i)+m32*dz(i))-Q(i)*(-m13*dy(i)+m12*dz(i)));
        b(i,2) = (f/Q(i)^2)*((R(i)*(cos(phi)*dx(i)+sin(omega)*sin(phi)*dy(i)-cos(omega)*sin(phi)*dz(i))- Q(i)*(-sin(phi)*cos(kappa)*dx(i)+sin(omega)*cos(phi)*cos(kappa)*dy(i)-cos(omega)*cos(phi)*cos(kappa)*dz(i))));
        b(i,3) = (-f/Q(i))*(m21*dx(i)+m22*dy(i)+m23*dz(i));
        b(i,4) = (f/Q(i)^2)*(R(i)*m31-Q(i)*m11);
        b(i,5) = (f/Q(i)^2)*(R(i)*m32-Q(i)*m12);
        b(i,6) = (f/Q(i)^2)*(R(i)*m33-Q(i)*m13);
        
        b(i,7) = (f/Q(i)^2)*(S(i)*(-m33*dy(i)+m32*dz(i))-Q(i)*(-m23*dy(i)+m22*dz(i)));
        b(i,8) = (f/Q(i)^2)*((S(i)*(cos(phi)*dx(i)+sin(omega)*sin(phi)*dy(i)-cos(omega)*sin(phi)*dz(i))- Q(i)*(-sin(phi)*cos(kappa)*dx(i)+sin(omega)*cos(phi)*cos(kappa)*dy(i)-cos(omega)*cos(phi)*cos(kappa)*dz(i))));
        b(i,9) = (f/Q(i))*(m11*dx(i)+m12*dy(i)+m13*dz(i));
        b(i,10) = (f/Q(i)^2)*(S(i)*m31-Q(i)*m21);
        b(i,11) = (f/Q(i)^2)*(S(i)*m32-Q(i)*m22);
        b(i,12) = (f/Q(i)^2)*(S(i)*m33-Q(i)*m23);
    end
    
    B = [b(1,1) b(1,2) b(1,3) -b(1,4)  -b(1,5)  -b(1,6);
        b(1,7) b(1,8) b(1,9) -b(1,10) -b(1,11) -b(1,12);
        b(2,1) b(2,2) b(2,3) -b(2,4)  -b(2,5)  -b(2,6);
        b(2,7) b(2,8) b(2,9) -b(2,10) -b(2,11) -b(2,12);
        b(3,1) b(3,2) b(3,3) -b(3,4)  -b(3,5)  -b(3,6);
        b(3,7) b(3,8) b(3,9) -b(3,10) -b(3,11) -b(3,12);
        b(4,1) b(4,2) b(4,3) -b(4,4)  -b(4,5)  -b(4,6);
        b(4,7) b(4,8) b(4,9) -b(4,10) -b(4,11) -b(4,12)];
    
    % +b19 change
    %B matrix - changes
    
    DELTA = inv(B'*B)*(B'*eps);
    
    omega =  DELTA(1)+ omega ;
    phi = DELTA(2)+ phi;
    kappa = DELTA(3)+ kappa;
    XL = DELTA(4)+ x0;
    YL = DELTA(5)+ y0;
    ZL = DELTA(6)+ z0;
    
    
end

omegaL = (180/pi)*omega;
phiL = (180/pi)*phi;
kappaL = (180/pi)*kappa;
XT = XL;
YT = YL;
ZT = ZL;

counter
XT
YT
ZT
omegaL
phiL
kappaL

end