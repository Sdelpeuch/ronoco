"""
Implementation of the coverage block allowing to cover the whole surface of a rectangle defined by 4 points
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

import config
import logger
import py_trees

from ronoco_vm.coverage import path_coverage_node


class Coverage(py_trees.behaviour.Behaviour):
    """
    Class inherited from py_tree.behaviour.Behavior allowing to define a new behaviour. Implementation of the coverage
    block allowing to cover the whole surface of a rectangle defined by 4 points
    """

    def __init__(self, name="Coverage", data=0.3):
        super(Coverage, self).__init__(name)
        self.map_drive = None
        self.robot_width = data

    def setup(self, timeout):
        """
        No specific treatment
        :return: True
        """
        self.logger.debug("  %s [Coverage::setup()]" % self.name)
        return True

    def initialise(self):
        """
        No specific treatment
        """
        self.logger.debug("  %s [Coverage::initialise()]" % self.name)

    def update(self):
        """
        Creates an instance of MapDrive and waits for it to complete its execution to return success
        :return: SUCCESS or FAILURE
        """
        self.logger.debug("  %s [Coverage::update()]" % self.name)
        logger.debug("Execute block " + self.name)
        self.map_drive = path_coverage_node.MapDrive(self.robot_width)
        while config.finished != py_trees.Status.SUCCESS and config.finished != py_trees.Status.FAILURE:
            time.sleep(1)
        if config.finished == py_trees.Status.FAILURE:
            self.map_drive.on_shutdown()
        return config.finished

    def terminate(self, new_status):
        """
        Replace the finished value of the configuration file with False
        """
        self.logger.debug("  %s [Coverage::terminate().terminate()][%s->%s]" % (self.name, self.status, new_status))
        config.finished = py_trees.Status.RUNNING
