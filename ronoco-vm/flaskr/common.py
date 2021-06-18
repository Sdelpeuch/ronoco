"""
This file implements the common endpoint
"""
from flask import Blueprint
from werkzeug.exceptions import NotFound

import rospy
from roscpp.srv import GetLoggers


class Common:
    """
    Definition of common endpoint
    """
    def __init__(self):
        self.bp = Blueprint('common_views', __name__, url_prefix='/')

        self.bp.route('/', methods=['GET'])(self.index)
        self.bp.route('/robot_state')(self.robot_state)

    @staticmethod
    def index():
        """
        GET Method

        TODO : change index behaviour
        :return: if everything is ok : 'Hello World !' else an HttpError
        """
        return 'Hello World from everyone !'

    @staticmethod
    def robot_state():
        """
        Check if you can communicate with a ros master
            + Use rosservice /rosout/get_loggers
            + Node: /rosout
            + Type: roscpp/GetLoggers
            + Args:

        :return: {'robot_state': True} if communication with rosmaster is possible, NotFound exception else
        """
        get_loggers = rospy.ServiceProxy('rosout/get_loggers', GetLoggers)
        try:
            get_loggers()
        except rospy.service.ServiceException:
            raise NotFound()
        return {'robot_state': True}