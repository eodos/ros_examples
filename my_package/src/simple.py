#! /usr/bin/env python

import rospy

rospy.init_node("ObiWan")
rate = rospy.Rate(2)               # We create a Rate object
while not rospy.is_shutdown():     # We prevent the program to end until Ctrl + C
   print "Help me Obi-Wan Kenobi, you're my only hope"
   rate.sleep() 