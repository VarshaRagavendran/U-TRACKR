clear all;
clc;

% read text files of coordinates

%% READ IMAGE COORDINATE FILE
% [ u, v ] = textread('test1.txt', '%f %f ' );
% x = u;
% y = v;

% cam_Image_Coords (mm) - cam1.jpg
x = [0.41944,-0.11368,-0.45192,-0.68264,-0.4844,-0.16632,0.38696,0.52584,-0.23016,-1.06232,-0.29624,0.85624,-0.25704];
y = [0.46536,0.63336,0.41944,-0.0364,-0.48664,-0.73528,-0.59528,-0.04088,1.04328,-0.0308,-1.15864,-0.08456,-0.03752];

% % cam_Image_Coords (mm) - cam2.jpg
% x = [0.4026, 0.4990, 0.3489, -0.1966, -0.5057, -0.6961, -0.4754, -0.1361, 0.8518, -0.3354, -1.0881, -0.2582, -0.2638];
% y = [-0.5270, 0.0039, 0.5214, 0.6558, 0.4138, -0.0442, -0.4900, -0.7017, 0.0263, 1.0814, -0.0722, -1.1351, -0.0308];

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
c = 3.04;
xo = 0;
yo = 0;
% initial exterior orientation coords parameters (m)
Xo = 0.05;
Yo = 0.05;
Zo = 0.98;
% initial exterior orientation angle parameters (rads)
omega = 0.785398; % 45 deg
phi = 0.785398; % 45 deg
kappa = 0;

% % cam2.jpg
% % interior camera orientation params (mm)
% % focal length
% c = 2.616;
% xo = 0.2154;
% yo = -0.4175;
% % initial exterior orientation coords parameters (m)
% Xo = 0.90;
% Yo = 0.01;
% Zo = 1.10;
% % initial exterior orientation angle parameters (rads)
% omega = 0.785398; % 45 deg
% phi = 0.785398; % 45 deg
% kappa = 0;

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

 