#! /usr/bin/env python

import rospy
import actionlib
from quadcopter_custom_action.msg import QuadcopterFeedback, QuadcopterAction
from geometry_msgs.msg import Twist
import time

class QuadcopterClass(object):
    _feedback = QuadcopterFeedback()
    _velocities = Twist()

    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
          
        self._as = actionlib.SimpleActionServer("quadcopter_custom_as", QuadcopterAction, self.goal_callback, False)
        self._as.start()
    
    def goal_callback(self, goal):
    
        r = rospy.Rate(1)
        success = True
        
        if goal.direction.data == "UP":
            self._velocities.linear.x = 0
            self._velocities.linear.y = 0
            self._velocities.linear.z = 1
            self.pub.publish(self._velocities)
            self._feedback.current_direction.data = "UP"
        
        elif goal.direction.data == "DOWN":
            self._velocities.linear.x = 0
            self._velocities.linear.y = 0
            self._velocities.linear.z = -1
            self.pub.publish(self._velocities)
            self._feedback.current_direction.data = "DOWN"
            
        else:
            self._velocities.linear.x = 0
            self._velocities.linear.y = 0
            self._velocities.linear.z = 0
            self.pub.publish(self._velocities)
            self._feedback.current_direction.data = "UNDEFINED"
        
        for _i in xrange(0, 5):
            
            if self._as.is_preempt_requested():
                rospy.loginfo('The goal has been cancelled/preempted')
                self._as.set_preempted()
                success = False
                break
            
            self._as.publish_feedback(self._feedback)
            r.sleep()
            
        self._velocities.linear.x = 0
        self._velocities.linear.y = 0
        self._velocities.linear.z = 0
        self.pub.publish(self._velocities)
        
        if success:
            #self._result.result = self._feedback.feedback
            rospy.loginfo('Succeeded')# completing %i repetitions' % goal.goal )
            self._as.set_succeeded()#(self._result)
      
if __name__ == '__main__':
    rospy.init_node('quadcopter_custom_server')
    QuadcopterClass()
    rospy.spin()