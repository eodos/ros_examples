#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist 

rospy.init_node('velocity_publisher')
pub = rospy.Publisher('/custom_topic', Twist, queue_size=1)
velocity = Twist()
velocity.linear.x = 1
velocity.angular.z = 1
rate = rospy.Rate(2)

running = True

def shutdown():
    velocity.linear.x = 0
    velocity.angular.z = 0
    pub.publish(velocity)
    running = False
    print('Shutdown')

# while not rospy.is_shutdown(): 
rospy.on_shutdown(shutdown)
while running:
#   velocity.linear.x += 0.1
#   if (velocity.linear.x  > 1):
#       velocity.linear.x = 0
    velocity.angular.z *= -1
    pub.publish(velocity)
    rate.sleep()
    