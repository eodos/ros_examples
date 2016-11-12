#! /usr/bin/env python

import rospy
from iri_wam_reproduce_trajectory.srv import ExecTraj # import the service message used by the service /gazebo/delete_model
import sys 
import rospkg

rospy.init_node('service_client') # initialise a ROS node with the name service_client
rospy.wait_for_service('/execute_trajectory') # wait for the service client /gazebo/delete_model to be running
traj_service = rospy.ServiceProxy('/execute_trajectory', ExecTraj) # create the connection to the service

rospack = rospkg.RosPack()
traj = rospack.get_path('iri_wam_reproduce_trajectory') + "/config/get_food.txt"

result=traj_service(traj)

rospy.spin()
