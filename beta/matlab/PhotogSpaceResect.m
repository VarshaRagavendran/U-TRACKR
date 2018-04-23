clear all;
clc;

% read text files of coordinates

%% READ IMAGE COORDINATE FILE
% [ u, v ] = textread('test1.txt', '%f %f ' );
% x = u;
% y = v;

% cam_Image_Coords (mm) - cam1.jpg
x = [0.4094, -0.1551, -0.4642, -0.6401, -0.3959, -0.0622, 0.4665, 0.5561, -0.2974, -1.0399, -0.1406, 0.8954, -0.2122];
y = [0.5908, 0.7050, 0.4620, -0.0084, -0.4329, -0.6423, -0.4609, 0.1058, 1.1374, -0.0263, -1.0646, 0.0577, 0.0286];

% % cam_Image_Coords (mm) - cam2.jpg
% x = [0.5135, 0.5090, -0.2682, -0.2783];
% y = [-0.5561, 0.4194, 0.3567, -0.4721];

%% READ OBJECT COORDINATE FILE
% [ X, Y, Z] = textread('test1_ob.txt', '%f %f %f' );
% Number of Points

% ground control coordinates [X,Y,Z] (m)
X = [0.44, 0.616, 0.704, 0.616, 0.44, 0.264, 0.176, 0.264, 0.704, 0.704, 0.176, 0.176, 0.44];
Y = [0.176, 0.264, 0.44, 0.616, 0.704, 0.616, 0.44, 0.264, 0.176, 0.704, 0.704, 0.176, 0.44];
Z = [0, 0.057, 0, 0.06, 0, 0.06, 0, 0.061, 0.142, 0.144, 0.143, 0.144, 0.141];

n = length(X);


%% INITIAL APPROXIMATIONS

% cam1.jpg
% interior camera orientation params (mm)
% focal length
c = 2.616;
xo = 0.2154;
yo = -0.4175;
% initial exterior orientation coords parameters (m)
Xo = 0.05;
Yo = 0.05;
Zo = 0.98;
% initial exterior orientation angle parameters (rads)
omega = 0.785398; % 45 deg
phi = 0.785398; % 45 deg
kappa = 0;

% % cam2.jpg
% % focal length (mm)
% c = 3.04;
% % initial exterior orientation coords parameters (m)\
% xo = 0;
% yo = 0;
% Xo = 0.90;
% Yo = 0.05;
% Zo = 1.10;
% % initial exterior orientation angle parameters (rads)
% omega = 0.785398; % 45 deg
% phi = -0.785398; % 45 deg
% kappa = 1.5708; % 90 deg

%% BEGINNING ITERATIONS
for iteration = 1:40
    iteration 
    

 
% Rotation matrix
m_11 = cos(phi)*cos(kappa) 
m_12 = -cos(phi)*sin(kappa)
m_13 =  sin(phi)
m_21 = cos(omega )*sin(kappa)+ sin(omega )*sin(phi)*cos(kappa)
m_22 = cos(omega )*cos(kappa)-sin(omega )*sin(phi)*sin(kappa)
m_23 = -sin(omega )*cos(phi)
m_31 = sin(omega )*sin(kappa) - cos(omega )*sin(phi)*cos(kappa)
m_32 = sin(omega )*cos(kappa)+ cos(omega )*sin(phi)*sin(kappa)
m_33 = cos(omega )*cos(phi)

 
   % Abbreviations for simplicity of the collinearity equations'
   % derivatives into the design matrix A

    
 
 %  A is the Design matrix   &   Y is the Observations/Misclosure vector(i.e. Observed - Approximated)
 A = zeros(2*n,6);%preallocated memory for A matrix
 for g = 1:n

     

     nx(g) = (m_11 .* (X(g) - Xo)) + (m_21 .* (Y(g) - Yo)) + (m_31 .* (Z(g) - Zo))
     ny(g) = (m_12 .* (X(g) - Xo)) + (m_22 .* (Y(g) - Yo)) + (m_32 .* (Z(g) - Zo))
     d(g)  = (m_13 .* (X(g) - Xo)) + (m_23 .* (Y(g) - Yo)) + (m_33 .* (Z(g) - Zo))

    
   Nx =nx';
   Ny =ny';
   D = d';




 A(2*g-1,1:6) = [   
     c.*((m_11.*D(g) - m_13.*Nx(g))/D(g).^2)    
     c.*((m_21.*D(g) - m_23.*Nx(g))/D(g).^2)      
     c.*((m_31.*D(g) - m_33.*Nx(g))/D(g).^2)      
     -c .*((D(g).*(-m_31.*(Y(g) - Yo) + m_21.*(Z(g) - Zo))) + (Nx(g).*(m_33.*(Y(g) - Yo) - m_23.*(Z(g) - Zo))))/D(g).^2         
     -c.* (-D(g).^2 .* cos(kappa)+ Nx(g).*(-Nx(g).*cos(kappa) + Ny(g).*sin(kappa)))/D(g).^2      
     -c.*(Ny(g)/D(g))     ] ; 
 
 A(2*g,1:6)   = [   
     c.*((m_12.*D(g)- m_13.*Ny(g))/D(g).^2)     
     c.*((m_22.*D(g) - m_23.*Ny(g))/D(g).^2)      
     c.*((m_32.*D(g) - m_33.*Ny(g))/D(g).^2)      
     -c .*((D(g).*(-m_32.*(Y(g) - Yo) + m_22.*(Z(g) - Zo))) + (Ny(g).*(m_33.*(Y(g) - Yo) - m_23.*(Z(g) - Zo))))/D(g).^2          
     c/D(g).^2 .*(Ny(g).*(cos(phi).*(X(g)-Xo) + sin(omega)*sin(phi).*(Y(g)-Yo) -cos(omega)*sin(phi).*(Z(g)-Zo)) -  D(g).*(sin(phi)*sin(kappa).*(X(g)-Xo)-sin(omega)*cos(phi)*sin(kappa).*(Y(g)-Yo) + cos(omega)*cos(phi)*sin(kappa).*(Z(g)-Zo)))      
     c.*(Nx(g)/D(g))      ];
 
%      c/D(g).^2 .*(Ny(g).*(cos(phi).*(X(g)-Xo) + sin(omega)*sin(phi).*(Y(g)-Yo) -cos(omega)*sin(phi).*(Z(g)-Zo)) -  D(g).*(sin(phi)*sin(kappa).*(X(g)-Xo)-sin(omega)*cos(phi)*sin(kappa).*(Y(g)-Yo) + cos(omega)*cos(phi)*sin(kappa).*(Z(g)-Zo))
 
 
%    -c.* ( D(g).^2 .* sin(kappa)+ Ny(g).*(cos(phi).*(X(g) -Xo) + sin(omega)*sin(phi).*(Y(g)-Yo)-cos(omega)*sin(phi).*(Z(g)-Zo)   )  )/D(g).^2 
 
  
  W(2*g-1,1)  = x(g) - xo + c.*(Nx(g)/D(g));
  W(2*g,1)    = y(g) - yo + c.*(Ny(g)/D(g));
 
 end
 
 
% W is  weight matrix set to the identity matrix 
%  W = eye([2*n 2*n]);

% Using Gauss-Markov Model of Least Squares to Estimate VOU (Gauss Markov
% Equation --->   error(residuals) = Y - A * X_hat........where 
% X_hat =(A'WA)-1 * A'WY

 delta_X = (inv(A'*A)) * (A'*W)
 
 Xo = Xo + delta_X(1)
 Yo = Yo + delta_X(2)
 Zo = Zo + delta_X(3)
 omega = omega + delta_X(4)
 phi = phi + delta_X(5)
 kappa = kappa + delta_X(6)

 residuals = W - (A*delta_X)



 end

 