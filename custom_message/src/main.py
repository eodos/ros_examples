#! /usr/bin/env python

import rospy
from custom_message.msg import Age

pub = rospy.Publisher("age_topic", Age, queue_size=1)
rospy.init_node("custom_message")
age = Age()
age.years = 21
age.months = 12.23
age.days = 545
rate = rospy.Rate(0.5)
while not rospy.is_shutdown():
   pub.publish(age)
   rate.sleep() 