import rospy
import rospkg
import os
import yaml
import random

from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import DeleteModel
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion

# def spawn_block(config_idx, missing_block=False):
def spawn_block(missing_block=False):

    missing_yellow = False
    missing_green = False

    if missing_block:
        if random.randint(0, 1) == 0:
            missing_yellow = True
        else:
            missing_green = True

    # Initialize ROS pack
    rospack = rospkg.RosPack()

    # Get path to block
    ur_path = rospack.get_path('ur_description')
    # lab5_path = rospack.get_path('lab5pkg_py')

    block_yellow_path = os.path.join(ur_path, 'urdf', 'block_yellow.urdf')
    block_green_path = os.path.join(ur_path, 'urdf', 'block_green.urdf')
    block_red_path = os.path.join(ur_path, 'urdf', 'block_red.urdf')
    block_blue_path = os.path.join(ur_path, 'urdf', 'block_blue.urdf')
    block_purple_path = os.path.join(ur_path, 'urdf', 'block_purple.urdf')
    block_turquoise_path = os.path.join(ur_path, 'urdf', 'block_turquoise.urdf')

    # Wait for service to start
    rospy.wait_for_service('gazebo/spawn_urdf_model')
    spawn = rospy.ServiceProxy('gazebo/spawn_urdf_model', SpawnModel)
    delete = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)

    # Get YAML path
    # yaml_path = os.path.join(lab5_path, 'scripts', 'configs',  'positions.yaml')

    # Load block positions
    # with open(yaml_path, 'r') as f:
    #     positions_dict = yaml.load(f)

    # IF YOU USE THOSE POSITIONS DIRECTLY, YOU WILL GET A ZERO
    # NO EXCUSES, AND WE WILL RUN CHECKS
    # block_yellow_position = positions_dict['block_yellow_positions'][config_idx]

    dests = [(.15, 0), (.15, .05), (.15, .1), (.15, .15), (.15, .2), (.15, .25), (.15, .3),
             (.2, 0),  (.2, .05),  (.2, .1),  (.2, .15),  (.2, .2),  (.2, .25),  (.2, .3),
             (.25, 0), (.25, .05), (.25, .1), (.25, .15), (.25, .2), (.25, .25), (.25, .3), (.25, .35),
             (.3, 0),  (.3, .05),  (.3, .1),  (.3, .15),  (.3, .2),  (.3, .25),  (.3, .3),  (.3, .35),
             (.35, 0), (.35, .05), (.35, .1), (.35, .15), (.35, .2), (.35, .25), (.35, .3)]

    y1_pos = dests.pop(random.randrange(0,36))
    y2_pos = dests.pop(random.randrange(0,35))
    g1_pos = dests.pop(random.randrange(0,34))
    g2_pos = dests.pop(random.randrange(0,33))
    r1_pos = dests.pop(random.randrange(0,32))
    r2_pos = dests.pop(random.randrange(0,31))
    b1_pos = dests.pop(random.randrange(0,30))
    b2_pos = dests.pop(random.randrange(0,29))
    p1_pos = dests.pop(random.randrange(0,28))
    p2_pos = dests.pop(random.randrange(0,27))
    t1_pos = dests.pop(random.randrange(0,26))
    t2_pos = dests.pop(random.randrange(0,25))

    # Uncomment for error analysis
    # print("BLOCK SPAWN LOCATIONS:")
    # print(y1_pos, y2_pos, g1_pos, g2_pos, r1_pos, r2_pos, b1_pos, b2_pos, p1_pos, p2_pos, t1_pos, t2_pos)


    # Spawn block

    # First delete all blocks
    delete('block_yellow1')
    delete('block_yellow2')
    delete('block_green1')
    delete('block_green2')
    delete('block_red1')
    delete('block_red2')
    delete('block_blue1')
    delete('block_blue2')
    delete('block_purple1')
    delete('block_purple2')
    delete('block_turquoise1')
    delete('block_turquoise2')

    # Spawn yellow
    block_name = 'block_yellow1'
    pose = Pose(Point(y1_pos[0], y1_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_yellow:
        spawn(block_name, open(block_yellow_path, 'r').read(), 'block', pose, 'world')

    # Spawn yellow
    block_name = 'block_yellow2'
    pose = Pose(Point(y2_pos[0], y2_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_yellow:
        spawn(block_name, open(block_yellow_path, 'r').read(), 'block', pose, 'world')

    # Spawn green
    block_name = 'block_green1'
    pose = Pose(Point(g1_pos[0], g1_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_green_path, 'r').read(), 'block', pose, 'world')

    # Spawn green
    block_name = 'block_green2'
    pose = Pose(Point(g2_pos[0], g2_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_green_path, 'r').read(), 'block', pose, 'world')

    # Spawn red
    block_name = 'block_red1'
    pose = Pose(Point(r1_pos[0], r1_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_red_path, 'r').read(), 'block', pose, 'world')

    # Spawn red
    block_name = 'block_red2'
    pose = Pose(Point(r2_pos[0], r2_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_red_path, 'r').read(), 'block', pose, 'world')

    # Spawn blue
    block_name = 'block_blue1'
    pose = Pose(Point(b1_pos[0], b1_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_blue_path, 'r').read(), 'block', pose, 'world')

    # Spawn blue
    block_name = 'block_blue2'
    pose = Pose(Point(b2_pos[0], b2_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_blue_path, 'r').read(), 'block', pose, 'world')

    # Spawn purple
    block_name = 'block_purple1'
    pose = Pose(Point(p1_pos[0], p1_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_purple_path, 'r').read(), 'block', pose, 'world')

    # Spawn purple
    block_name = 'block_purple2'
    pose = Pose(Point(p2_pos[0], p2_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_purple_path, 'r').read(), 'block', pose, 'world')
    
    # Spawn turquoise
    block_name = 'block_turquoise1'
    pose = Pose(Point(t1_pos[0], t1_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_turquoise_path, 'r').read(), 'block', pose, 'world')
    
    # Spawn turquoise
    block_name = 'block_turquoise2'
    pose = Pose(Point(t2_pos[0], t2_pos[1], 0), Quaternion(0, 0, 0, 0))
    if not missing_green:
        spawn(block_name, open(block_turquoise_path, 'r').read(), 'block', pose, 'world')


if __name__ == '__main__':
    print("Don't try to run me! Look at the lab manual.")
