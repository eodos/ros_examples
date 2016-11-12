#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from actionlib.msg import TestAction, TestGoal
import actionlib
import time

class CommanderNode():
    
    def __init__(self):
        self.p = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.wait_for_service('/detect_collision')
        self.collision_service = rospy.ServiceProxy('/detect_collision', Trigger)
        
        # Action to count 2 minutes
        self.action_client = actionlib.SimpleActionClient('/check_completion', TestAction)
        self.action_client.wait_for_server()
        
        #Action to check if outside maze
        self._as = actionlib.SimpleActionServer("/check_completion", TestAction, self.callback_action, False)
        self._as.start()
        
        self.goal = TestGoal()
        self.action_client.send_goal(self.goal, feedback_cb=self.callback_action)
        self.state_result = 0
        
        self.rate = rospy.Rate(10)
        self.velocities = Twist()
        
    def callback_action():
        pass
        
    def move_forward(self):
        self.velocities.linear.x = 0.1
        self.velocities.angular.z = 0
        self.p.publish(self.velocities)
        
    def move_backward(self):
        self.velocities.linear.x = -0.1
        self.velocities.angular.z = 0
        self.p.publish(self.velocities)
        
    def move_forward_and_turn(self):
        self.velocities.linear.x = 0.1
        self.velocities.angular.z = 0.3
        self.p.publish(self.velocities)

    def main(self):
        # Initial velocity
        time.sleep(1)
        self.move_forward()
        
        
        self.state_result = self.action_client.get_state()
        while self.state_result < 2:
        # while True:
            result = self.collision_service()
            if result.success:
                print "Collision!", result.message
                if result.message == "X-":
                    self.move_forward()
                elif result.message == "X+":
                    self.move_backward()
                else:
                    self.move_forward_and_turn()
            self.rate.sleep()
            self.state_result = self.action_client.get_state()
        
        print self.state_result
        print self.action_client.get_result()
        if self.state_result == 2 or self.state_result == 3:
            print 'COMPLETED'
        else:
            print 'ERROR'

rospy.init_node('sphero_commander')
c = CommanderNode()
c.main()
