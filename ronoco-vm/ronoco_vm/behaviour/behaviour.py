"""
This file implements some constants for behaviour like kind of types, leaves and create an instance of CartesianPoint()
commander
"""
import ast
from collections import Counter

import cartesian_point
import config
import py_trees

import behaviour
import rosservice


def selector(name, data, child):
    return True, py_trees.composites.Selector()


def sequence(name, data, child):
    return True, py_trees.composites.Sequence()


def parallel(name, data, child):
    return True, py_trees.composites.Parallel()


def execute(data, child, name):
    if name is None or name == "":
        name = "Execute"
    if data is None:
        return False, None
    state, point = cartesian_point.CartesianPoint().find_db(int(data))
    if not state:
        return False, None
    return True, behaviour.execute.Execute(name, point)


def plan(name, data, child):
    if data is None:
        return False, None
    state, point = cartesian_point.CartesianPoint().find_db(int(data))
    if not state:
        return False, None
    return True, behaviour.plan.Plan(name, point)


def condition(name, data, child):
    if data is None:
        return False, None
    try:
        return True, py_trees.decorators.Condition(name=name, status=states[data], child=child)
    except KeyError:
        return False, None


def inverter(name, data, child):
    try:
        return True, py_trees.decorators.Inverter(child, name)
    except TypeError:
        return False, None


def timeout(name, data, child):
    if data is None:
        return False, None
    try:
        return True, py_trees.decorators.Timeout(name=name, duration=int(data), child=child)
    except TypeError:
        return False, None


def cartesian(name, data, child):
    if name is None or name == "":
        name = "Cartesian"
    if data is None:
        return False, None
    state, point = cartesian_point.CartesianPoint().find_db(int(data['point_id']))
    if not state:
        return False, None
    return True, behaviour.cartesian.Cartesian(name,
                                               {"point": point, "reliability": data['reliability'], "eef": data['eef']})


def record(name, data, child):
    if name is None or name == "":
        name = "Record"
    if data is None:
        return False, None
    return True, behaviour.record.Record(name,
                                         {"identifier": data['identifier'], "time": data['time']})


def replay(name, data, child):
    if name is None or name == "":
        name = "Replay"
    if data is None:
        return False, None
    return True, behaviour.replay.Replay(name, data)


def end_effector(name, data, child):
    if name is None or name == "":
        name = "end effector"
    if data is None:
        return False, None
    if rosservice.get_service_type("/" + config.end_effector) is None:
        return False, None
    return True, behaviour.end_effector.EndEffector(name, data)


def service(name, data, child):
    if name is None or name == "":
        name = "service"
    if data is None:
        return False, None
    return True, behaviour.service.Service(name, data)


def navigate(name, data, child):
    if name is None or name == "":
        name = "navigate"
    if data is None:
        return False, None
    state, point = cartesian_point.CartesianPoint().find_db(int(data['identifier']))
    if not state:
        return False, None
    data = {'point': point, 'timeout': data['timeout']}
    return True, behaviour.navigate.Navigate(name, data)


def coverage(name, data, child):
    if name is None or name == "":
        name = "coverage"
    if data is None:
        return False, None
    if data['points'] != '':
        data['points'] = ast.literal_eval(data['points'])
        if len(Counter(data['points']).values()) < 3:
            return False, None
        points = []
        for i in range(len(data['points'])):
            state, point = cartesian_point.CartesianPoint().find_db(int(data['points'][i]))
            if not state:
                return False, None
            points.append(point)
        data['points'] = points
    return True, behaviour.coverage.Coverage(name, data)


def sleep(name, data, child):
    if name is None or name == "":
        name = "sleep"
    if data is None:
        return False, None
    return True, behaviour.sleep.Sleep(name, data)


types = {'selector': selector,
         'sequence': sequence,
         'parallel': parallel,
         'execute': execute,
         'replay': replay,
         'plan': plan,
         'cartesian': cartesian,
         'condition': condition,
         'inverter': inverter,
         'timeout': timeout,
         'record': record,
         'end effector': end_effector,
         'service': service,
         'navigate': navigate,
         'coverage': coverage,
         'sleep': sleep
         }

composites = {'selector', 'sequence', 'parallel'}
leaf = {'execute', 'plan', 'cartesian', 'record', 'replay', 'end effector', 'service', 'navigate', 'coverage', 'sleep'}
decorators = {'condition', 'inverter', 'timeout'}
data_node = {'execute', 'replay', 'plan', 'cartesian', 'condition', 'timeout', 'record', 'end effector', 'service',
             'navigate', 'coverage', 'sleep'}
states = {"success": py_trees.common.Status.SUCCESS, "failure": py_trees.common.Status.FAILURE,
          "running": py_trees.common.Status.RUNNING}
