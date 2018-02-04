import numpy as np
from numpy.linalg import inv
import math
from sympy import Symbol
from sympy.solvers import solve
# Image Space Resection V1.0
# Calculation of initial camera position and angles 
# final results output into 
# calcOmega, calcPhi, calcKappa, calcXL, calcYL, calc ZL
# Message me if you need any help with knowing the aspects of the code

omega = 0
phi = 0

# INPUT INITIAL PARAMETERS FOR SPACE RESECTION
# f = 3.04 for our focal length of cameras 
# cam1_Image_Coords = calculated image coordinates from pixel coordinates
# retrieve from cams
# caml_Space_Coordinates = frame space coordinates of fixed points. At
# least 4 with xyz needed in order to perform space resection

f = 152.916
cam1_Image_Coords = np.array([[86.421 , -83.977],
     [-100.916 , 92.582],
     [-98.322 , -89.161],
     [78.812 , 98.123]])

cam1_Space_Coords = np.array([[1268.101 , 1455.027 , 22.606],
     [732.181 , 545.344 , 22.299],
     [1454.553 , 731.666 , 22.649],
     [545.245 , 1268.232 , 22.336]])

# Estimate ZL =
# image coords
x  = cam1_Image_Coords[:,0]
y  = cam1_Image_Coords[:,1]


# Space coords
X  = cam1_Space_Coords[:,0]
Y  = cam1_Space_Coords[:,1]
Z  = cam1_Space_Coords[:,2]

abSquare = (cam1_Space_Coords[0,0]- cam1_Space_Coords[1,0])**2 + (cam1_Space_Coords[0,1]- cam1_Space_Coords[1,1])**2

H = Symbol('H')

p = (((x[0]/f)*(H-Z[0]))-((x[1]/f)*(H-Z[1])))**2 + (((y[0]/f)*(H-Z[0]))-((y[1]/f)*(H-Z[1])))**2 - abSquare;

r = solve(p,H); 

for i in range(0, len(r)):
    if r[i] > 0:
      ZL = r[i]	
XC = []
YC = []
#Calculate the ground coordinates of the ground control points
for i in range(0,4):
    XC.append(np.dot(x[i],((ZL - Z[i])/f)))
    YC.append(np.dot(y[i],((ZL - Z[i])/f)))

#Computing 2D conformal coordinates transformation for LSA
# L matrix

Lmat = np.array([[X[0]],
     			[Y[0]],
      			[X[1]],
    			[Y[1]],
    			[X[2]],
    			[Y[2]],
    			[X[3]],
    			[Y[3]]])

Amat = np.array([[XC[0] , -YC[0] , 1 , 0],
     [YC[0] , XC[0] , 0 , 1],
     [XC[1] , -YC[1] , 1 , 0],
     [YC[1] , XC[1] , 0 , 1],
     [XC[2] , -YC[2] , 1 , 0],
     [YC[2] , XC[2] , 0 , 1],
     [XC[3] , -YC[3] , 1 , 0],
     [YC[3], XC[3] , 0 , 1 ]])


Xmat = 	np.linalg.inv(np.dot(Amat.transpose(),Amat))
#kappa = math.degrees(math.atan(Xmat[1]/Xmat[0])) + 180


# forming the rotation matrix
#theta = kappa;



     
