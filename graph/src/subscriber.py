#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist 

def callback(msg):
    pass

rospy.init_node('velocity_subscriber')
pub = rospy.Subscriber('/custom_topic', Twist, callback)

rospy.spin()