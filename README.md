# ECE470_BOBOTS

This repo stores the code for the ECE470 Team BOBOTS project. These source files used in conjunction with UR3 drivers allow for the simulation of a UR3 robot in ROS. The Team BOBOTS robot will serve as a pick and place robot, detecting colored straws and placing them into the appropriate boba drinks.

**Project Update 1:**
- Installed ROS and other neccessary packages on personal Ubuntu 16.04 system
- Created and successfully built catkin workspace with the UR3 drivers and code from previous labs
- Integrated previous lab code to successfully control the movements of the robot through forward kinematics

*Update 1 Video:* https://youtu.be/7ch9c7PPKJs


**Delivrable 2 Update:**
- Fixed various integration issued that were left unaddressed from the last deliverable
- Integrated inverse kinematics using code from previous labs
- Added camera sensor input functionality to allow for decision making based on the robot's surroundings
- Connected all added components to allow for basic pick and place operations on simple blocks

*Update 2 Video:* https://youtu.be/7m8aVT873a8

**Final Submission Update:**
- Tuned block detection parameters to detect blocks more optimally
- Created URDF files of various additional block colors
- Updated blob search script to detect new block colors and return multiple sets of keypoints
- Adjusted move block function to fix precision issues when placing blocks
- Rewrote main robot logic to identify similar block colors and stack the blocks appropriately
- Modified block spawning script to randomize block placement within constrained area
- Added commented code to print relevant data for error analysis
- Refactored/cleaned code and cleaned up terminal output

*Final Submssion Video:* https://www.youtube.com/watch?v=-Hr9zdLKsNA