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

class checker(object):

    def __init__(self, xarg1, yarg1, xarg2, yarg2, xarg3, yarg3, xarg4, yarg4):
        self.x1 = xarg1
        self.y1 = yarg1
        self.x2 = xarg2
        self.y2 = yarg2
        self.x3 = xarg3
        self.y3 = yarg3
        self.x4 = xarg4
        self.y4 = yarg4

    def position_calculation(self):
        omega = 0
        phi = 0

        # INPUT INITIAL PARAMETERS FOR SPACE RESECTION
        # f = 3.04 for our focal length of cameras
        # cam1_Image_Coords = calculated image coordinates from pixel coordinates
        # retrieve from cams
        # caml_Space_Coordinates = frame space coordinates of fixed points. At
        # least 4 with xyz needed in order to perform space resection

        f = 3.04 #focal length
        pixSize = 1.12; #pixel size of camera
        width_Of_Image = 1280/2;
        height_Of_Image = 720/2;

        # X,Y of 4 cameras of object
        # 1st pass: the markers on the frame
        # 2nd pass: object
        cam1_Image_Coords = np.array([[self.x1 , self.y1],
             [self.x2 , self.y2],
             [self.x3 , self.y3],
             [self.x4, self.y4]])

        # X,Y,Z of markers on the frame, predetermined, never changes
        # 4 markers on the frame, these coordinates will always be the same for each camera
        # cam1_Space_Coords = np.array([[1268.101 , 1455.027 , 22.606],
        #      [732.181 , 545.344 , 22.299],
        #      [1454.553 , 731.666 , 22.649],
        #      [545.245 , 1268.232 , 22.336]])

        # X,Y,Z of markers on the frame, predetermined, never changes
        # 4 markers on the frame, these coordinates will always be the same for each camera
        cam1_Space_Coords = np.array([[6.6817 , 84.9129 , 106.9060],
             [0.9649 , 0.3729 , 106.8558],
             [77.3635 , 3.2707 , 106.9076],
             [83.8137 , 87.8490 , 106.8561]])

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

        kappa = math.radians(math.degrees(math.atan(Xmat[1]/Xmat[0])) + 180)

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

        b= [[0 for x in range(12)] for y in range(4)]

        # forming B matrix
        for i in range(0,4):

            b[i][0] = (f/Q[i]**2)*(R[i]*(-m33*deltaY[i]+m32*deltaZ[i])-Q[i]*(-m13*deltaY[i]+m12*deltaZ[i]))
            b[i][1] = (f/Q[i]**2)*((R[i]*(math.cos(math.degrees(phi))*deltaX[i]+math.sin(math.degrees(omega))*math.sin(math.degrees(phi))*deltaY[i]-math.cos(math.degrees(omega))*math.sin(math.degrees(phi))*deltaZ[i])- Q[i]*(-math.sin(math.degrees(phi))*math.cos(kappa)*deltaX[i]+math.sin(math.degrees(omega))*math.cos(math.degrees(phi))*math.cos(kappa)*deltaY[i]-math.cos(math.degrees(omega))*math.cos(math.degrees(phi))*math.cos(kappa)*deltaZ[i])))
            b[i][2] = (-f/Q[i])*(m21*deltaX[i]+m22*deltaY[i]+m23*deltaZ[i])
            b[i][3] = (f/Q[i]**2)*(R[i]*m31-Q[i]*m11)
            b[i][4] = (f/Q[i]**2)*(R[i]*m32-Q[i]*m12)
            b[i][5] = (f/Q[i]**2)*(R[i]*m33-Q[i]*m13)

            b[i][6] = (f/Q[i]**2)*(S[i]*(-m33*deltaY[i]+m32*deltaZ[i])-Q[i]*(-m23*deltaY[i]+m22*deltaZ[i]))
            b[i][7] = (f/Q[i]**2)*((S[i]*(math.cos(math.degrees(phi))*deltaX[i]+math.sin(math.degrees(omega))*math.sin(math.degrees(phi))*deltaY[0]-math.cos(math.degrees(omega))*math.sin(math.degrees(phi))*deltaZ[i])- Q[i]*(-math.sin(math.degrees(phi))*math.cos(kappa)*deltaX[i]+math.sin(math.degrees(omega))*math.cos(math.degrees(phi))*math.cos(kappa)*deltaY[i]-math.cos(math.degrees(omega))*math.cos(math.degrees(phi))*math.cos(kappa)*deltaZ[i])))
            b[i][8] = (-f/Q[i])*(m11*deltaX[i]+m12*deltaY[i]+m13*deltaZ[i])
            b[i][9] = (f/Q[i]**2)*(S[i]*m31-Q[i]*m11)
            b[i][10] = (f/Q[i]**2)*(S[i]*m32-Q[i]*m12)
            b[i][11] = (f/Q[i]**2)*(S[i]*m33-Q[i]*m13)


        B = np.array([
            [b[0][0].item() , b[0][1].item() ,b[0][2].item() ,-b[0][3].item() ,-b[0][4].item() ,-b[0][5].item()],
            [b[0][6].item() , b[0][7].item() ,b[0][8].item() ,b[0][9].item() ,b[0][10].item() ,b[0][11].item()],
            [b[1][0].item() , b[1][1].item() ,b[1][2].item() ,-b[1][3].item() ,-b[1][4].item() ,-b[1][5].item()],
            [b[1][6].item() , b[1][7].item() ,b[1][8].item() ,b[1][9].item() ,b[1][10].item() ,b[1][11].item()],
            [b[2][0].item() , b[2][1].item() ,b[2][2].item() ,-b[2][3].item() ,-b[2][4].item() ,-b[2][5].item()],
            [b[2][6].item() , b[2][7].item() ,b[2][8].item() ,b[2][9].item() ,b[2][10].item() ,b[2][11].item()],
            [b[3][0].item() , b[3][1].item() ,b[3][2].item() ,-b[3][3].item() ,-b[3][4].item() ,-b[3][5].item()],
            [b[3][6].item() , b[3][7].item() ,b[3][8].item() ,b[3][9].item() ,b[3][10].item() ,b[3][11].item()]
            ])

         # domega dphi dkappa dX dY dZ
        DELTA = np.dot(np.dot(np.linalg.inv(np.array(np.dot(B.transpose(),B))),B.transpose()),Lmat)


         # calculated angles omega phi kappa and XYZ
        calcOmega = 0 + DELTA[0]*(180/np.pi)
        if calcOmega <= 0:
            calcOmega = calcOmega + 360
        elif calcOmega >= 360:
            calcOmega = calcOmega - 360



        calcPhi = 0 + DELTA[1]*(180/np.pi) + 360
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
        return calcXL, calcYL, calcZL