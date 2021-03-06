"""
Class inherited from py_tree.behaviour.Behavior allowing to define a new behaviour. The behaviour is navigate, i.e.
the movement between the current position and a position given in the constructor parameter.
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import logger
import py_trees

import rospy
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseGoal
from std_msgs.msg import Header


class Navigate(py_trees.behaviour.Behaviour):
    """
    Class inherited from py_tree.behaviour.Behavior allowing to define a new behaviour. The behaviour is navigate, i.e.
    the movement between the current position and a position given in the constructor parameter.
    """

    def __init__(self, name="Navigate", data=None):
        super(Navigate, self).__init__(name)
        self.commander = config.commander
        self.point = data['point']
        self.timeout = data['timeout']
        self.move_base = None
        self.goal = None
        self.header = None

    def setup(self, timeout):
        """
        No specific treatment
        :return: True
        """
        self.logger.debug("  %s [Navigate::setup()]" % self.name)

        return True

    def initialise(self):
        """
        Set target goal as a PoseStamped()
        """
        self.logger.debug("  %s [Navigate::initialise()]" % self.name)
        self.goal = MoveBaseGoal()
        self.header = Header()
        self.header.stamp = rospy.Time.now()
        self.header.frame_id = 'map'
        self.goal.target_pose.header = self.header
        self.goal.target_pose.pose.position.x = self.point['position']['x']
        self.goal.target_pose.pose.position.y = self.point['position']['y']
        self.goal.target_pose.pose.position.z = self.point['position']['z']
        self.goal.target_pose.pose.orientation.x = self.point['orientation']['x']
        self.goal.target_pose.pose.orientation.y = self.point['orientation']['y']
        self.goal.target_pose.pose.orientation.z = self.point['orientation']['z']
        self.goal.target_pose.pose.orientation.w = self.point['orientation']['w']

    def update(self):
        """
        Compute path then execute it.
        :return: SUCCESS or FAILURE
        """
        self.logger.debug("  %s [Navigate::update()]" % self.name)
        logger.debug("Execute block " + self.name)
        self.commander.send_goal(self.goal)
        try:
            self.commander.wait_for_result(rospy.Duration(int(self.timeout)))
        except ValueError:
            self.commander.wait_for_result(rospy.Duration(60))
        state = self.commander.get_state()
        if state in [GoalStatus.PREEMPTED, GoalStatus.ABORTED, GoalStatus.REJECTED, GoalStatus.RECALLED]:
            return py_trees.Status.FAILURE
        elif state == GoalStatus.SUCCEEDED:
            return py_trees.Status.SUCCESS
        else:
            return py_trees.Status.FAILURE

    def terminate(self, new_status):
        """
        Cancel goal if execution fail
        """
        self.logger.debug("  %s [Navigate::terminate().terminate()][%s->%s]" % (self.name, self.status, new_status))
        if self.commander.get_state() not in [GoalStatus.PREEMPTED, GoalStatus.ABORTED, GoalStatus.REJECTED,
                                              GoalStatus.RECALLED, GoalStatus.SUCCEEDED]:
            self.commander.cancel_goal()
