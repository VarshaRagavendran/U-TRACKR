import numpy as np
from numpy.linalg import inv
import math
from sympy import Symbol
from sympy.solvers import solve

class intersection(object):

	# 1. Input Data----------------------------------------------------------#

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

        # focal length (mm)
		f = 3.04

        # pixel size X,Y
		# camera pixel size (m) https://www.raspberrypi.org/documentation/hardware/camera/README.md

        pixSizeX = 0.00000112
        pixSizeY = 0.00000112

        # dimension of image: width and height
        width_Of_Image = 3280
        height_Of_Image = 2464

        # pixel coordinates of the 4 points in image: [x,y] (pix)
		#cam_Image_Coords = np.array([[-12.843, -54.155],[-87.550, -51.157]])
		cam_Image_Coords = np.array([[-0.0946, 0.2839], [0.3074, 0.0263]])

        # camera space coordinates [X,Y,Z] (m)
		#cam_Ground_Control_Coords = np.array([[9577.252, 10214.285, 555.192], [9803.241, 10219.622, 556.601]])

		cam_Ground_Control_Coords = np.array([[0.0494, 0.0534, 1.0195], [0.8066, 0.0431, 0.9870]])

        # cam1 resection
		# XT = 0.0494
		# YT = 0.0534
		# ZT = 1.0195
		# omegaL = 19.1668
		# phiL = -19.6642
		# kappaL = -130.3060

		# cam2 resection
		# XT = 0.8066
		# YT = 0.0431
		# ZT = 0.9870
		# omegaL = 21.9053
		# phiL = 19.6120
		# kappaL = -49.7987

		# cam1 object IMCO: [-0.0946, 0.2839]
		# cam2 object IMCO: [0.3074, 0.0263]

		# initial exterior orientation angle parameters (rads)
		# omega = np.array([[1.4022], [-0.1557]])
		# phi = np.array([[-0.3112], [-1.7063]])
		# kappa = np.array([[0.6470], [0.5513]])

		omega = np.array([[0.3345237671], [0.3823196086]])
        phi = np.array([[-0.3432050348], [0.342293973]])
        kappa = np.array([[-2.274268735], [-0.8691512782]])

		# 2. Pixel Coordinates to Image Coordinates--------------------------#

		# Based off of ESSE3650_03_CamerasImageMeas_16JAN2017.pdf slide 54
		# output: cam_image_coords[x,y] in mm
		# for i in range(0,len(cam_Pixel_Coords)):
			# cam_Image_Coords[i,0] = ((cam_Pixel_Coords[i,0] - (imgWidth/2) - 0.5) * pixSizeX) * 1000
			# cam_Image_Coords[i,1] = (((imgHeight/2) - cam_Pixel_Coords[i,1] + 0.5) * pixSizeY) * 1000

		# print cam_Image_Coords

		# 3. Space Intersection by Collinearity - Initialization-------------#

		# Image Coords (mm)
		x  = cam_Image_Coords[:][0]
		y  = cam_Image_Coords[:][1]

		# Space/Ground Control coords (m)
		X  = cam_Ground_Control_Coords[:][0]
		Y  = cam_Ground_Control_Coords[:][1]
		Z  = cam_Ground_Control_Coords[:][2]

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

			dX = []
			dY = []
			dZ = []
			Q = []
			R = []
			S = []

    		for i in range(0,count):
        		dX.append(X[i]-XL)
        		dY.append(Y[i]-YL)
        		dZ.append(Z[i]-ZL)

        		Q[i] = (m31[i]*dX[i]) + (m32[i]*dY[i]) + (m33[i]*dZ[i])
        		R[i] = (m11[i]*dX[i]) + (m12[i]*dY[i]) + (m13[i]*dZ[i])
        		S[i] = (m21[i]*dX[i]) + (m22[i]*dY[i]) + (m23[i]*dZ[i])

    		# Elements of Photogrammetry... - Appendix D.5. (D-11) Linerization of Collinearity Equations
			eps = [[0 for x in range(1)] for y in range(count)] ######################################################
			for i in range(0,count):
        		eps[2*i][0] = x[i] + (f*(R[i]/Q[i]))
        		eps[2*i+1][0] = y[i] + (f*(S[i]/Q[i]))

    		# Elements of Photogrammetry... - Appendix D.5. (D-16) B-Matrix Eqns
        	b = [[0 for x in range(6)] for y in range(count)] ######################################################
			B = [[0 for x in range(6)] for y in range(count)] ######################################################

			for i in range(0,count):
        		b[i,0] = -(f/Q[i]**2)*(R[i]*m31[i]-Q[i]*m11[i])
        		b[i,1] = -(f/Q[i]**2)*(R[i]*m32[i]-Q[i]*m12[i])
        		b[i,2] = -(f/Q[i]**2)*(R[i]*m33[i]-Q[i]*m13[i])
        		b[i,3] = -(f/Q[i]**2)*(S[i]*m31[i]-Q[i]*m21[i])
        		b[i,4] = -(f/Q[i]**2)*(S[i]*m32[i]-Q[i]*m22[i])
        		b[i,5] = -(f/Q[i]**2)*(S[i]*m33[i]-Q[i]*m23[i])

				#B[2*i][0] = b[i][0]
				#B[2*i][1] = b[i][1]
				#B[2*i][2] = b[i][2]
				#B[2*i+1][0] = b[i][3]
				#B[2*i+1][1] = b[i][4]
				#B[2*i+1][2] = b[i][5]

        		B[2*i][0:2] = [b[i,0], b[i,1], b[i,2]] ############################################################
        		B[2*i][0:3] = [b[i,3], b[i,4], b[i,5]] ############################################################

			# Elements of Photogrammetry... - Appendix B.9. (B-13) Matrix Methods in Least Squares Adjustment Solution
			DELTA = np.dot(np.linalg.inv(np.dot(B.transpose(),B)), np.dot(B.transpose(), eps))

    		XL = DELTA[0] + XL
    		YL = DELTA[1] + YL
    		ZL = DELTA[2] + ZL

		# 5. Output----------------------------------------------------------#
		XT = XL
		YT = YL
		ZT = ZL
		#intersect_Coords = np.array([XT, YT, ZT])

		print counter
		return XT, YT, ZT
