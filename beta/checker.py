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
      ZL = float(r[i])	
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


#Xmat = 	np.array(np.dot(Amat.transpose(),Amat))
Xmat = np.dot(np.dot(np.linalg.inv(np.array(np.dot(Amat.transpose(),Amat))),Amat.transpose()),Lmat)

#print Xmat
#print ""
#print np.linalg.inv(Xmat)

kappa = math.degrees(math.atan(Xmat[1]/Xmat[0])) + 180

# forming the rotation matrix
theta = kappa; 

m11 = Xmat[0]
m12 = Xmat[1]
m13 = 0
m21 = -Xmat[1]
m22 = Xmat[0]
m23 = 0
m31 = 0
m32 = 0
m33 = 1

M = np.array([[m11 , m12 , m13],
    [m21 , m22 , m23],
    [m31 , m32 , m33]])

deltaX = []
deltaY = []
deltaZ = []

for i in range(0,4):
    deltaX.append(X[i] - Xmat[2])
    deltaY.append(Y[i] - Xmat[3])
    deltaZ.append(Z[i] - ZL)

R = []
S = []
Q = []
# forming RSQ matrix
for i in range(0,4):
	R.append(m11*deltaX[i]+m12*deltaY[i]+m13*deltaZ[i])
	S.append(m21*deltaX[i]+m22*deltaY[i]+m23*deltaZ[i])
	Q.append(m31*deltaX[i]+m32*deltaY[i]+m33*deltaZ[i])

b=[]

# forming B matrix
for i in range(0,4):

	b[i,1] = (f/Q[i]**2)*(R[i]*(-m33*deltaY[i]+m32*deltaZ[i])-Q[i]*(-m13*deltaY[i]+m12*deltaZ[i]))
	b[i,2] = (f/Q[i]**2)*((R[i]*(math.degrees(math.acos(phi))*deltaX[i]+math.degrees(math.asin(omega))*math.degrees(math.asin(phi))*deltaY[i]-math.degrees(math.acos(omega))*math.degrees(math.asin(phi))*deltaZ[i])- Q[i]*(-math.degrees(math.asin(phi))*math.degrees(math.acos(kappa))*deltaX[i]+math.degrees(math.asin(omega))*math.degrees(math.acos(phi))*math.degrees(math.acos(kappa))*deltaY[i]-math.degrees(math.acos(omega))*math.degrees(math.acos(phi))*math.degrees(math.acos(kappa))*deltaZ[i])))
	b[i,3] = (-f/Q[i])*(m21*deltaX[i]+m22*deltaY[i]+m23*deltaZ[i])
	b[i,4] = (f/Q[i]**2)*(R[i]*m31-Q[i]*m11)
	b[i,5] = (f/Q[i]**2)*(R[i]*m32-Q[i]*m12)
	b[i,6] = (f/Q[i]**2)*(R[i]*m33-Q[i]*m13)

	b[i,7] = (f/Q[i]**2)*(S[i]*(-m33*deltaY[i])+m32*deltaZ[i])-Q[i]*(-m23*deltaY[i]+m22*deltaZ[i])
	b[i,8] = (f/Q[i]**2)*((S[i]*(math.degrees(math.acos(phi))*deltaX[i]+math.degrees(math.asin(omega))*math.degrees(math.asin(phi))*deltaY[0]-math.degrees(math.acos(omega))*math.degrees(math.asin(phi))*deltaZ[i])- Q[i]*(-math.degrees(math.asin(phi))*math.degrees(math.acos(kappa))*deltaX[i]+math.degrees(math.asin(omega))*math.degrees(math.acos(phi))*math.degrees(math.acos(kappa))*deltaY[i]-math.degrees(math.acos(omega))*math.degrees(math.acos(phi))*math.degrees(math.acos(kappa))*deltaZ[i])))
	b[i,9] = (-f/Q[i])*(m11*deltaX[i]+m12*deltaY[i]+m13*deltaZ[i])
	b[i,10] = (f/Q[i]**2)*(S[i]*m31-Q[i]*m11)
	b[i,11] = (f/Q[i]**2)*(S[i]*m32-Q[i]*m12)
	b[i,12] = (f/Q[i]**2)*(S[i]*m33-Q[i]*m13)


B = np.array([
	[b[0,0] , b[0,1] ,b[0,2] ,-b[0,3] ,-b[0,4] ,-b[0,5],
     b[0,6] , b[0,7] ,b[0,8] ,b[0,9] ,b[0,10] ,b[0,11],
     b[1,0] , b[1,1] ,b[1,2] ,-b[1,3] ,-b[1,4] ,-b[1,5],
     b[1,6] , b[1,7] ,b[1,8] ,b[1,9] ,b[1,10] ,b[1,11],
     b[2,0] , b[2,1] ,b[2,2] ,-b[2,3] ,-b[2,4] ,-b[2,5],
     b[2,6] , b[2,7] ,b[2,8] ,b[2,9] ,b[2,10] ,b[2,11],
     b[3,0] , b[3,1] ,b[3,2] ,-b[3,3] ,-b[3,4] ,-b[3,5],
     b[3,6] , b[3,7] ,b[3,8] ,b[3,9] ,b[3,10] ,b[3,11]] 
	])

 # domega dphi dkappa dX dY dZ
DELTA = np.linalg.inv(B.transpose()*B)*B.transpose()*Lmat


 # calculated angles omega phi kappa and XYZ
calcOmega = 0 + DELTA[0]*(180/np.pi)
if calcOmega <= 0: 
    calcOmega = calcOmega + 360
elif calcOmega >= 360:
    calcOmega = calcOmega - 360
 


calcPhi = 0 + DELTA[1]*(180/pi) + 360
if calcPhi <= 0:
    calcPhi = calcPhi + 360
elif calcPhi >= 360:
    calcPhi = calcPhi - 360

calcKappa = theta + DELTA[3] 
if calcKappa <= 0: 
     calcKappa =  calcKappa+ 360
elif calcKappa >= 360:
    calcKappa =  calcKappa - 360
 
calcXL = DELTA[3]+Xmat[2]
calcYL = DELTA[4]+Xmat[3]
calcZL = DELTA[5]+ ZL
 
 
     
