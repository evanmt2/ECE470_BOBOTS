#!/usr/bin/env python

'''
We get inspirations of Tower of Hanoi algorithm from the website below.
This is also on the lab manual.
Source: https://www.cut-the-knot.org/recurrence/hanoi.shtml
'''

import os
import argparse
import copy
import time
import rospy
import rospkg
import numpy as np
import yaml
import sys
from math import pi
from lab2_header import *

# 20Hz
SPIN_RATE = 20

# UR3 home location
home = np.radians([144, -116, 109, -84, -90, 24])
# home = np.radians([120, -90, 90, -90, -90, 0])

# Hanoi tower location 1
Q11 = [134.63*pi/180.0, -61.8*pi/180.0, 139.4*pi/180.0, -167.6*pi/180.0, -89.9*pi/180.0, 14.63*pi/180.0]
Q12 = [134.6*pi/180.0, -72.5*pi/180.0, 138.2*pi/180.0, -155.7*pi/180.0, -90.07*pi/180.0, 14.62*pi/180.0]
Q13 = [134.6*pi/180.0, -82*pi/180.0, 135.5*pi/180.0, -143.5*pi/180.0, -90.2*pi/180.0, 14.63*pi/180.0]
Q21 = [149.7*pi/180.0, -62.7*pi/180.0, 144.7*pi/180.0, -172*pi/180.0, -89.9*pi/180.0, 29.7*pi/180.0]
Q22 = [149.7*pi/180.0, -75.27*pi/180.0, 143.4*pi/180.0, -158.1*pi/180.0, -90.1*pi/180.0, 29.7*pi/180.0]
Q23 = [149.7*pi/180.0, -86.1*pi/180.0, 140.3*pi/180.0, -144.2*pi/180.0, -90.2*pi/180.0, 29.7*pi/180.0]
Q31 = [168.1*pi/180.0, -62.7*pi/180.0, 142.9*pi/180.0, -170.2*pi/180.0, -89.9*pi/180.0, 48.1*pi/180.0]
Q32 = [168.1*pi/180.0, -74.1*pi/180.0, 141.7*pi/180.0, -157.5*pi/180.0, -90.0*pi/180.0, 48.1*pi/180.0]
Q33 = [168.1*pi/180.0, -84.5*pi/180.0, 138.7*pi/180.0, -144.1*pi/180.0, -90.2*pi/180.0, 48.1*pi/180.0]

thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

digital_in_0 = 0
analog_in_0 = 0

suction_on = True
suction_off = False
current_io_0 = False
current_position_set = False

# UR3 current position, using home position for initialization
current_position = copy.deepcopy(home)

############## Your Code Start Here ##############
"""
TODO: Initialize Q matrix
"""

Q = [ [Q11, Q12, Q13], \
      [Q21, Q22, Q23], \
      [Q31, Q32, Q33] ]
############### Your Code End Here ###############

############## Your Code Start Here ##############

"""
TODO: define a ROS topic callback funtion for getting the state of suction cup
Whenever ur3/gripper_input publishes info this callback function is called.
"""

def gripper_callback(msg):
    global digital_in_0

    digital_in_0 = msg.DIGIN

############### Your Code End Here ###############


"""
Whenever ur3/position publishes info, this callback function is called.
"""
def position_callback(msg):

    global thetas
    global current_position
    global current_position_set

    thetas[0] = msg.position[0]
    thetas[1] = msg.position[1]
    thetas[2] = msg.position[2]
    thetas[3] = msg.position[3]
    thetas[4] = msg.position[4]
    thetas[5] = msg.position[5]

    current_position[0] = thetas[0]
    current_position[1] = thetas[1]
    current_position[2] = thetas[2]
    current_position[3] = thetas[3]
    current_position[4] = thetas[4]
    current_position[5] = thetas[5]

    current_position_set = True


def gripper(pub_cmd, loop_rate, io_0):

    global SPIN_RATE
    global thetas
    global current_io_0
    global current_position

    error = 0
    spin_count = 0
    at_goal = 0

    current_io_0 = io_0

    driver_msg = command()
    driver_msg.destination = current_position
    driver_msg.v = 1.0
    driver_msg.a = 1.0
    driver_msg.io_0 = io_0
    pub_cmd.publish(driver_msg)

    while(at_goal == 0):

        if( abs(thetas[0]-driver_msg.destination[0]) < 0.0005 and \
            abs(thetas[1]-driver_msg.destination[1]) < 0.0005 and \
            abs(thetas[2]-driver_msg.destination[2]) < 0.0005 and \
            abs(thetas[3]-driver_msg.destination[3]) < 0.0005 and \
            abs(thetas[4]-driver_msg.destination[4]) < 0.0005 and \
            abs(thetas[5]-driver_msg.destination[5]) < 0.0005 ):

            at_goal = 1

        loop_rate.sleep()

        if(spin_count >  SPIN_RATE*5):

            pub_cmd.publish(driver_msg)
            rospy.loginfo("Just published again driver_msg")
            spin_count = 0

        spin_count = spin_count + 1

    return error


def move_arm(pub_cmd, loop_rate, dest, vel, accel):

    global thetas
    global SPIN_RATE

    error = 0
    spin_count = 0
    at_goal = 0

    driver_msg = command()
    driver_msg.destination = dest
    driver_msg.v = vel
    driver_msg.a = accel
    driver_msg.io_0 = current_io_0
    pub_cmd.publish(driver_msg)

    loop_rate.sleep()

    while(at_goal == 0):

        if( abs(thetas[0]-driver_msg.destination[0]) < 0.0005 and \
            abs(thetas[1]-driver_msg.destination[1]) < 0.0005 and \
            abs(thetas[2]-driver_msg.destination[2]) < 0.0005 and \
            abs(thetas[3]-driver_msg.destination[3]) < 0.0005 and \
            abs(thetas[4]-driver_msg.destination[4]) < 0.0005 and \
            abs(thetas[5]-driver_msg.destination[5]) < 0.0005 ):

            at_goal = 1
            rospy.loginfo("Goal is reached!")

        loop_rate.sleep()

        if(spin_count >  SPIN_RATE*5):

            pub_cmd.publish(driver_msg)
            rospy.loginfo("Just published again driver_msg")
            spin_count = 0

        spin_count = spin_count + 1

    return error


############## Your Code Start Here ##############

def move_block(pub_cmd, loop_rate, start_loc, start_height, \
               end_loc, end_height):
    global Q
    global home
    global current_position
    global current_position_set
    global digital_in_0

    ### Hint: Use the Q array to map out your towers by location and "height".

    # Check if at home position
    # if current_position_set:
    #     for i in range(0, len(current_position)):
    #         if current_position[i] != home[i]:
    #             move_arm(pub_cmd, loop_rate, home, 1, 1)
    #             break
    # else:
    #     return 1
    
    move_arm(pub_cmd, loop_rate, Q[start_loc - 1][start_height - 1], 1, 1)
    gripper(pub_cmd, loop_rate, True) # may need to adjust how we do this
    time.sleep(1)
    # suction on -> verify block grabbed else return ERROR = 1
    if not digital_in_0:
        gripper(pub_cmd, loop_rate, False)
        move_arm(pub_cmd, loop_rate, home, 1, 1)
        return 1

    move_arm(pub_cmd, loop_rate, home, 1, 1)
    # maybe verify block is still grabbed?

    move_arm(pub_cmd, loop_rate, Q[end_loc - 1][end_height - 1], 1 ,1)

    gripper(pub_cmd, loop_rate, False) # may need to adjust how we do this

    move_arm(pub_cmd, loop_rate, home, 1, 1)



    # error = 0



    # return error
    return 0


############### Your Code End Here ###############


def main():

    global home
    global Q
    global SPIN_RATE

    # Initialize ROS node
    rospy.init_node('lab2node')

    # Initialize publisher for ur3/command with buffer size of 10
    pub_command = rospy.Publisher('ur3/command', command, queue_size=10)

    # Initialize subscriber to ur3/position and callback fuction
    # each time data is published
    sub_position = rospy.Subscriber('ur3/position', position, position_callback)

    ############## Your Code Start Here ##############
    # TODO: define a ROS subscriber for ur3/gripper_input message and corresponding callback function

    sub_gripper = rospy.Subscriber('ur3/gripper_input', gripper_input, gripper_callback)

    ############### Your Code End Here ###############


    ############## Your Code Start Here ##############
    # TODO: modify the code below so that program can get user input

    # input_done = 0
    # loop_count = 0

    # while(not input_done):
    #     input_string = raw_input("Enter number of loops <Either 1 2 3 or 0 to quit> ")
    #     print("You entered " + input_string + "\n")

    #     if(int(input_string) == 1):
    #         input_done = 1
    #         loop_count = 1
    #     elif (int(input_string) == 2):
    #         input_done = 1
    #         loop_count = 2
    #     elif (int(input_string) == 3):
    #         input_done = 1
    #         loop_count = 3
    #     elif (int(input_string) == 0):
    #         print("Quitting... ")
    #         sys.exit()
    #     else:
    #         print("Please just enter the character 1 2 3 or 0 to quit \n\n")

    # input_done = 0
    # start_pos = 0
    # end_pos = 0
    # empty_pos = 0

    # while(not input_done):
    #     input_string = raw_input("Enter the start position of the tower <Either 1, 2, 3, or 0 to quit> ")

    #     if int(input_string) == 1:
    #         input_done = 1
    #         start_pos = 1
    #     elif int(input_string) == 2:
    #         input_done = 1
    #         start_pos = 2
    #     elif int(input_string) == 3:
    #         input_done = 1
    #         start_pos = 3
    #     elif int(input_string) == 0:
    #         print("Quitting... ")
    #         sys.exit()
    #     else:
    #         print("Invalid input \n")

    # print("Start position set to position " + str(start_pos) + ".\n")
    # input_done = 0
    # remaining_pos = [1,2,3]
    # remaining_pos.remove(start_pos)

    # while(not input_done):
    #     input_string = raw_input("Enter the end position of the tower <Either " + str(remaining_pos[0]) + ", " + str(remaining_pos[1]) + ", or 0 to quit> ")

    #     if int(input_string) == remaining_pos[0]:
    #         input_done = 1
    #         end_pos = remaining_pos[0]
    #         empty_pos = remaining_pos[1]
    #     elif int(input_string) == remaining_pos[1]:
    #         input_done = 1
    #         end_pos = remaining_pos[1]
    #         empty_pos = remaining_pos[0]
    #     elif int(input_string) == 0:
    #         print("Quitting... ")
    #         sys.exit()
    #     else:
    #         print("Invalid input \n")

    # print("End position set to position " + str(end_pos) + ".\n")




    ############### Your Code End Here ###############

    # Check if ROS is ready for operation
    while(rospy.is_shutdown()):
        print("ROS is shutdown!")

    rospy.loginfo("Sending Goals ...")

    loop_rate = rospy.Rate(SPIN_RATE)

    ############## Your Code Start Here ##############
    # TODO: modify the code so that UR3 can move tower accordingly from user input

    # while(loop_count > 0):

    #     move_arm(pub_command, loop_rate, home, 4.0, 4.0)

    #     rospy.loginfo("Sending goal 1 ...")
    #     move_arm(pub_command, loop_rate, Q[0][0], 4.0, 4.0)

    #     gripper(pub_command, loop_rate, suction_on)
    #     # Delay to make sure suction cup has grasped the block
    #     time.sleep(1.0)

    #     rospy.loginfo("Sending goal 2 ...")
    #     move_arm(pub_command, loop_rate, Q[1][1], 4.0, 4.0)

    #     rospy.loginfo("Sending goal 3 ...")
    #     move_arm(pub_command, loop_rate, Q[2][0], 4.0, 4.0)

    #     loop_count = loop_count - 1

    # gripper(pub_command, loop_rate, suction_off)

    # global home
    # move_arm(pub_command, loop_rate, home, 1, 1)

    # res = move_block(pub_command, loop_rate, start_pos, 3, end_pos, 1)
    # if res:
    #     print("1 PROBLEM YOU LOSER!\n")
    #     return
    # res = move_block(pub_command, loop_rate, start_pos, 2, empty_pos, 1)
    # if res:
    #     print("2 PROBLEM YOU LOSER!\n")
    #     return
    # res = move_block(pub_command, loop_rate, end_pos, 1, empty_pos, 2)
    # if res:
    #     print("3 PROBLEM YOU LOSER!\n")
    #     return
    # res = move_block(pub_command, loop_rate, start_pos, 1, end_pos, 1)
    # if res:
    #     print("4 PROBLEM YOU LOSER!\n")
    #     return
    # res = move_block(pub_command, loop_rate, empty_pos, 2, start_pos, 1)
    # if res:
    #     print("5 PROBLEM YOU LOSER!\n")
    #     return
    # res = move_block(pub_command, loop_rate, empty_pos, 1, end_pos, 2)
    # if res:
    #     print("6 PROBLEM YOU LOSER!\n")
    #     return
    # res = move_block(pub_command, loop_rate, start_pos, 1, end_pos, 3)
    # if res:
    #     print("7 PROBLEM YOU LOSER!\n")
    #     return

    print("Demo movements... ")

    global Q
    move_arm(pub_command, loop_rate, home, .5, 1)
    move_arm(pub_command, loop_rate, Q[0][0], .5, 1)
    move_arm(pub_command, loop_rate, home, .5, 1)
    move_arm(pub_command, loop_rate, Q[1][0], .5, 1)
    move_arm(pub_command, loop_rate, home, .5, 1)
    move_arm(pub_command, loop_rate, Q[2][0], .5, 1)
    move_arm(pub_command, loop_rate, home, .5, 1)
    move_arm(pub_command, loop_rate, Q[1][1], .5, 1)
    move_arm(pub_command, loop_rate, home, .5, 1)
    move_arm(pub_command, loop_rate, Q[1][2], .5, 1)
    move_arm(pub_command, loop_rate, home, .5, 1)
    move_arm(pub_command, loop_rate, Q[2][1], .5, 1)
    move_arm(pub_command, loop_rate, home, .5, 1)
    move_arm(pub_command, loop_rate, Q[2][2], .5, 1)
    move_arm(pub_command, loop_rate, home, .5, 1)

    print("Done!\n")

    ############### Your Code End Here ###############


if __name__ == '__main__':

    try:
        main()
    # When Ctrl+C is executed, it catches the exception
    except rospy.ROSInterruptException:
        pass
