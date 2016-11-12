#! /usr/bin/env python

import rospy                                          
from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist

class Node():
    def __init__(self):
        self.laser_sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, self.callback)
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.actuator = Twist()
        self.times_turning = 0
        self.wall_avoided = False
    def callback(self, msg):
        middle_laser = len(msg.ranges)/2
        for i in range(middle_laser-100, middle_laser+100):
            if msg.ranges[i] < 1.5:
                self.publish(0.5, 1)
                self.times_turning+=1
                self.wall_avoided = True
                return
        if self.wall_avoided and self.times_turning and msg.ranges[0] > 25 and msg.ranges[len(msg.ranges)-1] > 25:
            self.publish(0.5, -1)
            self.times_turning-=1
        else:
            self.publish(0.5, 0)
    def publish(self, linear_speed, angular_speed):
        self.actuator.linear.x = linear_speed
        self.actuator.angular.z = angular_speed
        self.vel_pub.publish(self.actuator)

rospy.init_node('laser_readings')
n = Node()

rospy.spin()
