#! /usr/bin/env python

import rospy
from custom_srv_msg.srv import CustomServiceMessage, CustomServiceMessageResponse
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
import time

class Bb8Server:
    def __init__(self):
        rospy.Subscriber("/bb8/imu/data", Imu, self.imu_callback)
        self.p = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.my_service = rospy.Service("/bb8_square", CustomServiceMessage , self.callback)
        
        self.velocities = Twist()
        self.response = CustomServiceMessageResponse()
    
    def imu_callback(self, msg):
        #orientation = msg.orientation.
        pass
    
    def callback(self, request):
        if request.radius < 1 or request.repetitions < 1:
            self.response.success = False
            return self.response
        for j in range(1, request.repetitions + 1):
            for i in range(1, 5):
                self.velocities.linear.x = 1
                self.velocities.angular.z = 0
                self.p.publish(self.velocities)
                time.sleep(2*request.radius)
                self.velocities.linear.x = 0
                self.velocities.angular.z = 0
                self.p.publish(self.velocities)
                time.sleep(2*request.radius)
                self.velocities.linear.x = 0
                self.velocities.angular.z = 3
                self.p.publish(self.velocities)
                time.sleep(1)
                self.velocities.linear.x = 0
                self.velocities.angular.z = 0
                self.p.publish(self.velocities)
                time.sleep(2*request.radius)
        
        self.velocities.linear.x = 0
        self.velocities.angular.z = 0
        self.p.publish(self.velocities)
        
        self.response.success = True
        
        return self.response
        #return MyServiceResponse(len(request.words.split())) 

rospy.init_node('bb8_server')
b = Bb8Server()
rospy.spin()