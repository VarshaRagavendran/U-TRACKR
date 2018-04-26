import numpy as np
import math

class intersection(object):

    def __init__(self, xarg1, yarg1, xarg2, yarg2, xarg3, yarg3):
        self.x1 = xarg1
        self.y1 = yarg1
        self.x2 = xarg2
        self.y2 = yarg2
        self.x3 = xarg3
        self.y3 = yarg3
        self.f = 3.04 # focal length (mm)
        self.xo = 0
        self.yo = 0
        self.pixSizeX = 0.00000112
        self.pixSizeY = 0.00000112
        self.imgWidth = 820
        self.imgHeight = 616

    def pixel_to_imageX(self, xarg):
        return ((xarg - (self.imgWidth/2) - 0.5) * self.pixSizeX) * 1000;

    def pixel_to_imageY(self, yarg):
        return (((self.imgHeight / 2) - yarg + 0.5) * self.pixSizeY) * 1000;

    def position_calculation(self):
        # pixel coordinates of the 4 points in image: [x,y] (pix)
        cam_Image_Coords = np.array([[self.pixel_to_imageX(self.x1), self.pixel_to_imageY(self.y1)],
                                     [self.pixel_to_imageX(self.x2), self.pixel_to_imageY(self.y2)],
                                     [self.pixel_to_imageX(self.x3), self.pixel_to_imageY(self.y3)]])

        # camera space coordinates [X,Y,Z] (m)
        cam_Ground_Control_Coords = np.array([[0.06157099169, 0.07060934851, 1.04458976],
                                              [0.7966293212, 0.0816795553, 1.029443323],
                                              [0.7849643986, 0.7972458901, 1.022318113]])

        omega = np.array([[0.3629692572], [0.3729153968], [-0.3631335769]])
        phi = np.array([[-0.3560831591], [0.3562903306], [0.3144897345]])
        kappa = np.array([[-2.303993867], [-0.8475068616], [-5.331991633]])

        # Image Coords (mm)
        x  = cam_Image_Coords[:,0]
        y  = cam_Image_Coords[:,1]

        # Space/Ground Control coords (m)
        X  = cam_Ground_Control_Coords[:,0]
        Y  = cam_Ground_Control_Coords[:,1]
        Z  = cam_Ground_Control_Coords[:,2]

        # Initial orientation parameters
        DELTA = np.array([1, 1, 1])

        # Iterative solution coordinates (m)
        XL = 0
        YL = 0
        ZL = 0

        # Counter to count number of iterations
        counter = 1

        # Count is the size of the matrix
        count = len(cam_Image_Coords)

        # 4. Space Intersection by Collinearity - Iterative Solution---------#

        # Based off of ESSE3650_08_Colinearity_01FEB2017.pdf slide 35, 2.1.

        m11 = []
        m12 = []
        m13 = []
        m21 = []
        m22 = []
        m23 = []
        m31 = []
        m32 = []
        m33 = []

        dX = []
        dY = []
        dZ = []
        Q = []
        R = []
        S = []

        for i in range (0,count):
            m11.append(math.cos(phi[i])*math.cos(kappa[i]))
            m12.append(math.sin(omega[i])*math.sin(phi[i])*math.cos(kappa[i])+math.cos(omega[i])*math.sin(kappa[i]))
            m13.append(-math.cos(omega[i])*math.sin(phi[i])*math.cos(kappa[i])+math.sin(omega[i])*math.sin(kappa[i]))
            m21.append(-math.cos(phi[i])*math.sin(kappa[i]))
            m22.append(-math.sin(omega[i])*math.sin(phi[i])*math.sin(kappa[i])+math.cos(omega[i])*math.cos(kappa[i]))
            m23.append(math.cos(omega[i])*math.sin(phi[i])*math.sin(kappa[i])+math.sin(omega[i])*math.cos(kappa[i]))
            m31.append(math.sin(phi[i]))
            m32.append(-math.sin(omega[i])*math.cos(phi[i]))
            m33.append(math.cos(omega[i])*math.cos(phi[i]))

        # Based off of Elements of Photogrammetry with Applications in GIS (4th edition) Chapter 11 & Appendix B,D
        while (counter < 20):
            counter = counter + 1

        # Elements of Photogrammetry... - Appendix D.5. (D-12) Linerization of Collinearity Equations
        # ESSE3650_08_Colinearity_01FEB2017.pdf slide 35, 2.2.1.

            for i in range(0,count):
                dX.append(X[i]-XL)
                dY.append(Y[i]-YL)
                dZ.append(Z[i]-ZL)
                Q.append((m31[i]*dX[i]) + (m32[i]*dY[i]) + (m33[i]*dZ[i]))
                R.append((m11[i]*dX[i]) + (m12[i]*dY[i]) + (m13[i]*dZ[i]))
                S.append((m21[i]*dX[i]) + (m22[i]*dY[i]) + (m23[i]*dZ[i]))

            # Elements of Photogrammetry... - Appendix D.5. (D-11) Linerization of Collinearity Equations
            eps = [0 for m in range(count*2)]
            for i in range(0,count):
                eps[2*i] = x[i] + (self.f*(R[i]/Q[i]))
                eps[(2*i)+1] = y[i] + (self.f*(S[i]/Q[i]))

            # Elements of Photogrammetry... - Appendix D.5. (D-16) B-Matrix Eqns
            b = [[0 for j in range(6)] for k in range(count)]
            B = [[0 for j in range(2)] for k in range(count*2)]

            for i in range(0,count):
                b[i][0] = -(self.f/Q[i]**2)*(R[i]*m31[i]-Q[i]*m11[i])
                b[i][1] = -(self.f/Q[i]**2)*(R[i]*m32[i]-Q[i]*m12[i])
                b[i][2] = -(self.f/Q[i]**2)*(R[i]*m33[i]-Q[i]*m13[i])
                b[i][3] = -(self.f/Q[i]**2)*(S[i]*m31[i]-Q[i]*m21[i])
                b[i][4] = -(self.f/Q[i]**2)*(S[i]*m32[i]-Q[i]*m22[i])
                b[i][5] = -(self.f/Q[i]**2)*(S[i]*m33[i]-Q[i]*m23[i])

                B[2*i][0:2] = [b[i][0], b[i][1], b[i][2]]
                B[(2*i)+1][0:2] = [b[i][3], b[i][4], b[i][5]]

            # Elements of Photogrammetry... - Appendix B.9. (B-13) Matrix Methods in Least Squares Adjustment Solution
            DELTA = np.dot(np.linalg.inv(np.dot(np.array(B).transpose(),np.array(B))), np.dot(np.array(B).transpose(), eps))
            # DELTA = np.dot(np.dot(np.linalg.inv(np.array(np.dot(B.transpose(), B))), B.transpose()), eps)
            XL = DELTA[0] + XL
            YL = DELTA[1] + YL
            ZL = DELTA[2] + ZL
            dX = []
            dY = []
            dZ = []
            Q = []
            R = []
            S = []

        # 5. Output----------------------------------------------------------#
        XT = XL
        YT = YL
        ZT = ZL

        #print counter
        return XT, YT, ZT