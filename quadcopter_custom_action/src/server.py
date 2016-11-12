#! /usr/bin/env python

import rospy
import actionlib
from actionlib.msg import TestFeedback, TestResult, TestAction
from geometry_msgs.msg import Twist
import time

class QuadcopterClass(object):
    _feedback = TestFeedback()
    _result   = TestResult()
    _velocities = Twist()

    def __init__(self):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
          
        self._as = actionlib.SimpleActionServer("quadcopter_as", TestAction, self.goal_callback, False)
        self._as.start()
    
    def goal_callback(self, goal):
    
        r = rospy.Rate(1)
        success = True
        
        rospy.loginfo("Take of...")
        self._velocities.linear.x = 0
        self._velocities.linear.y = 0
        self._velocities.linear.z = 1
        self.pub.publish(self._velocities)
        time.sleep(3)
        
        rospy.loginfo('"quadcopter_as": Executing, square path with %i repetitions' % goal.goal)
        
        for i in xrange(1, goal.goal+1):
            for j in xrange(1, 5):
                if self._as.is_preempt_requested():
                    rospy.loginfo('The goal has been cancelled/preempted')
                    self._as.set_preempted()
                    success = False
                    break
                
                if j==1:
                    self._velocities.linear.x = 1
                    self._velocities.linear.y = 0
                    self._velocities.linear.z = 0
                elif j==2:
                    self._velocities.linear.x = 0
                    self._velocities.linear.y = 1
                    self._velocities.linear.z = 0
                elif j==3:
                    self._velocities.linear.x = -1
                    self._velocities.linear.y = 0
                    self._velocities.linear.z = 0
                else:
                    self._velocities.linear.x = 0
                    self._velocities.linear.y = -1
                    self._velocities.linear.z = 0
                    
                self.pub.publish(self._velocities)
                time.sleep(2)

            self._feedback.feedback = True
            self._as.publish_feedback(self._feedback)
            r.sleep()
          
        self._velocities.linear.x = 0
        self._velocities.linear.y = 0
        self._velocities.linear.z = -1
        self.pub.publish(self._velocities)
        time.sleep(3)
        
        if success:
            self._result.result = self._feedback.feedback
            rospy.loginfo('Succeeded completing %i repetitions' % goal.goal )
            self._as.set_succeeded(self._result)
      
if __name__ == '__main__':
    rospy.init_node('quadcopter_server')
    QuadcopterClass()
    rospy.spin()