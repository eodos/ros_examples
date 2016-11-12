#! /usr/bin/env python

import rospy                                          
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from std_srvs.srv import Trigger, TriggerResponse
from actionlib.msg import TestAction, TestFeedback, TestResult
# from random import randint
import math
import actionlib

class Node():
    def __init__(self):
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.callback_odom)
        self.imu_sum = rospy.Subscriber('/sphero/imu/data', Imu, self.callback_imu)
        self.collision_service = rospy.Service("/detect_collision", Trigger , self.callback_collision)
        self._as = actionlib.SimpleActionServer("/check_completion", TestAction, self.callback_action, False)
        self._as.start()
        
        self.count = 0
        self.underCollision = False
        
        self.imu_data = Imu()
        self.odometry_data = Odometry()
        
    def callback_action(self, goal):
        r = rospy.Rate(1)
        running = True
        success = True
        result = TestResult()
        result.result = 0
        
        while running:
            if self._as.is_preempt_requested():
                rospy.loginfo('The goal has been cancelled/preempted')
                self._as.set_preempted()
                success = False
                break
            
            x = self.odometry_data.pose.pose.position.x
            y = self.odometry_data.pose.pose.position.y
            position = [x, y]
            distance = math.sqrt(x**2 + y**2)
            if distance > 2:
                success = True
                running = False
                result.result = 1
                
            # self._as.publish_feedback(self._feedback)
            r.sleep()
    
        if success:
            self._as.set_succeeded(result)
        
    def callback_collision(self, request):
        self.response = TriggerResponse()
        self.response.success = False
        self.response.message = "None"
        
        if self.underCollision and self.count >= 7:
            self.underCollision = False
        
        if self.underCollision:
            self.count += 1
            
        if not self.underCollision:
            # if self.imu_data.linear_acceleration.y > 6 or self.imu_data.linear_acceleration.y < -6 \
            #   or self.imu_data.linear_acceleration.z > 6 or self.imu_data.linear_acceleration.z < -6:
            x = self.imu_data.linear_acceleration.x
            y = self.imu_data.linear_acceleration.y
            z = self.imu_data.linear_acceleration.z
            accelerations = [x, y]#, z]
            max_val = max(accelerations)
            min_val = min(accelerations)
            if abs(max_val) > abs(min_val):
                max_abs_index = accelerations.index(max_val)
            else:
                max_abs_index = accelerations.index(min_val)
            max_abs_acceleration = accelerations[max_abs_index] 
            sign = max_abs_acceleration > 0
            relevant = abs(max_abs_acceleration) > 3
            
            if relevant:
                if max_abs_index == 0:
                    if sign:
                        self.response.message = "+X"
                    else:
                        self.response.message = "-X"
                elif max_abs_index == 1:
                    if sign:
                        self.response.message = "+Y"
                    else:
                        self.response.message = "-Y"
                else:
                    if sign:
                        self.response.message = "+Z"
                    else:
                        self.response.message = "-Z"
            
            # if (self.imu_data.linear_acceleration.y**2 + self.imu_data.linear_acceleration.z**2) > 10:
                self.underCollision = True
                self.count = 0
                self.response.success = True
        return self.response
       
    def callback_odom(self, msg):
        self.odometry_data = msg
        
    def callback_imu(self, msg):
        self.imu_data = msg

if __name__ == "__main__":
    rospy.init_node('sphero_sensors')
    n = Node()
    rospy.spin()
