#! /usr/bin/env python

import rospy
from custom_srv_msg.srv import CustomServiceMessage, CustomServiceMessageRequest
import time

rospy.init_node('bb8_client')
rospy.wait_for_service('/bb8_square')
call_service = rospy.ServiceProxy('/bb8_square', CustomServiceMessage)

time.sleep(2)

print "Calling service..."
request = CustomServiceMessageRequest()
request.repetitions = 2
request.radius = 2
result=call_service(request)
print "Completed:", result.success

rospy.spin()
