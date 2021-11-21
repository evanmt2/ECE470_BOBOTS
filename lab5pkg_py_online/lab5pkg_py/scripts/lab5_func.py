#!/usr/bin/env python
import numpy as np
from scipy.linalg import expm
from lab5_header import *
import math

"""
Use 'expm' for matrix exponential.
Angles are in radian, distance are in meters.
"""
def Get_MS():
	# =================== Your code starts here ====================#
	# Fill in the correct values for a1~6 and q1~6, as well as the M matrix
	# M = np.eye(4)
	# S = np.zeros((6,6))

	M = [[0.0,-1.0,0.0,390.0],
		 [0.0,0.0,-1.0,401.0],
		 [1.0,0.0,0.0,215.5],
		 [0.0,0.0,0.0,1.0]]


	S = [[0,0,1,150,150,0],
		 [0,1,0,-162,0,-150],
		 [0,1,0,-162,0,94],
		 [0,1,0,-162,0,307],
		 [1,0,0,0,162,-260],
		 [0,1,0,-162,0,390]]

	# ==============================================================#
	return M, S


def skew_sym_helper(i):
	ss = [[0,-1*i[2],i[1],i[3]],
		  [i[2],0,-1*i[0],i[4]],
		  [-1*i[1],i[0],0,i[5]],
		  [0,0,0,0]]
	return ss


"""
Function that calculates encoder numbers for each motor
"""
def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):

	# Initialize the return_value
	return_value = [None, None, None, None, None, None]

	print("Foward kinematics calculated:\n")

	# =================== Your code starts here ====================#
	theta = np.array([theta1,theta2,theta3,theta4,theta5,theta6])
	T = np.eye(4)

	M, S = Get_MS()

	# calculate skew symmetric matricies for each joint
	sm_1 = skew_sym_helper(S[0])
	sm_2 = skew_sym_helper(S[1])
	sm_3 = skew_sym_helper(S[2])
	sm_4 = skew_sym_helper(S[3])
	sm_5 = skew_sym_helper(S[4])
	sm_6 = skew_sym_helper(S[5])
	# print("sm_1: ", sm_1, "\n")

	exp1 = np.multiply(sm_1,theta1)
	exp2 = np.multiply(sm_2,theta2)
	exp3 = np.multiply(sm_3,theta3)
	exp4 = np.multiply(sm_4,theta4)
	exp5 = np.multiply(sm_5,theta5)
	exp6 = np.multiply(sm_6,theta6)
	# print("exp_1: ", exp1, "\n")


	term1 = expm(exp1)
	term2 = expm(exp2)
	term3 = expm(exp3)
	term4 = expm(exp4)
	term5 = expm(exp5)
	term6 = expm(exp6)
	# print("term1: ", term1, "\n")

	T = np.matmul(term1, term2)
	T = np.matmul(T, term3)
	T = np.matmul(T, term4)
	T = np.matmul(T, term5)
	T = np.matmul(T, term6)
	T = np.matmul(T, M)
	# print("T: ", T, "\n")

	# ==============================================================#

	# print(str(T) + "\n")

	return_value[0] = theta1 + PI
	return_value[1] = theta2
	return_value[2] = theta3
	return_value[3] = theta4 - (0.5*PI)
	return_value[4] = theta5
	return_value[5] = theta6

	return return_value


# def adjust_angles(thetas):
#     thetas[0] = thetas[0] + PI
#     thetas[3] = thetas[3] - (0.5*PI)
#     return thetas

"""
Function that calculates an elbow up Inverse Kinematic solution for the UR3
"""
def lab_invk(xWgrip, yWgrip, zWgrip, yaw_WgripDegree):

    # # theta1 to theta6
	# thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	# l01 = 0.152
	# l02 = 0.120
	# l03 = 0.244
	# l04 = 0.093
	# l05 = 0.213
	# l06 = 0.083
	# l07 = 0.083
	# l08 = 0.082
	# l09 = 0.0535
	# l10 = 0.059   # thickness of aluminum plate is around 0.01

	# # xgrip = ?
	# # ygrip = ?
	# # zgrip = ?

	# # xcen = ?
	# # ycen = ?
	# # zcen = ?

	# # theta1
	# thetas[0] = 0        # Default value Need to Change

	# # theta6
	# thetas[5] = PI/2     # Default value Need to Change

	# # x3end = ?
	# # y3end = ?
	# # z3end = ?

	# thetas[1]= -PI/4     # Default value Need to Change
	# thetas[2]= PI/2      # Default value Need to Change
	# thetas[3]= (-PI*3)/4 # Default value Need to Change
	# thetas[4]=-PI/2      # Default value Need to Change

	# print("theta1 to theta6: " + str(thetas) + "\n")

	L1 = 152
	L2 = 120
	L3 = 244
	L4 = 93
	L5 = 213 
	L6 = 83 
	L7 = 83
	L8 = 82 
	L9 = 53.5
	L10 = 59

	new_xWgrip = xWgrip + 150 
	new_yWgrip = yWgrip - 150 
	new_zWgrip = zWgrip - 10 

	x_cen = new_xWgrip - (np.cos(np.radians(yaw_WgripDegree)) * L9)
	y_cen = new_yWgrip - (np.sin(np.radians(yaw_WgripDegree)) * L9)
	z_cen = new_zWgrip

	# print(math.sqrt((x_cen*x_cen)+(y_cen*y_cen)))
	theta_1 = np.arctan2(y_cen,x_cen) - np.arcsin((L2 - L4 + L6)/math.sqrt((x_cen*x_cen)+(y_cen*y_cen)))
	theta_6 = np.radians(90) - np.radians(yaw_WgripDegree) + theta_1
	x3_end = x_cen - (L7 * np.cos(theta_1)) + ((L6+27)*np.sin(theta_1))
	y3_end = y_cen - (L7 * np.sin(theta_1)) - ((L6+27)*np.cos(theta_1))
	z3_end = z_cen + L10 + L8

	La = math.sqrt( (z3_end - L1)*(z3_end - L1) + (x3_end*x3_end) + (y3_end*y3_end))

	theta_c = np.arccos(((L5*L5) - (La*La) - (L3*L3)) / (-2 * La * L3))

	theta_2 = (-1 * theta_c) - np.arcsin((z3_end - L1)/La)

	# theta_a = (np.arcsin(La*np.sin(theta_c)/L5))
	theta_a = np.arccos(((La*La) - (L5*L5) - (L3*L3)) / (-2 * L5 * L3))

	theta_3 = np.pi - theta_a

	theta_4 = (-1 * theta_2) - theta_3

	theta_5 = np.radians(-90)

	thetas = [theta_1, theta_2, theta_3, theta_4, theta_5, theta_6]

	return lab_fk(float(thetas[0]), float(thetas[1]), float(thetas[2]), \
		          float(thetas[3]), float(thetas[4]), float(thetas[5]) )
