"""
This file implements some constants for behavior like kind of types, leaves and create an instance of CartesianPoint()
commander
"""
import py_trees

from flaskr import behavior
from flaskr import cartesian_point


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
    return True, behavior.execute.Execute(name, point)


def plan(name, data, child):
    if data is None:
        return False, None
    state, point = cartesian_point.CartesianPoint().find_db(int(data))
    if not state:
        return False, None
    return True, behavior.plan.Plan(name, point)


def condition(name, data, child):
    if data is None:
        return False, None
    try:
        return True, py_trees.decorators.Condition(name=name, status=states[data], child=child)
    except KeyError:
        return False, None


def inverter(name, data, child):
    return True, py_trees.decorators.Inverter(name=name, child=child)


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
    return True, behavior.cartesian.Cartesian(name,
                                              {"point": point, "reliability": data['reliability'], "eef": data['eef']})


types = {'selector': selector,
         'sequence': sequence,
         'parallel': parallel,
         'execute': execute,
         'plan': plan,
         'cartesian': cartesian,
         'condition': condition,
         'inverter': inverter,
         'timeout': timeout
         }

composites = {'selector', 'sequence', 'parallel'}
leaf = {'execute', 'plan', 'cartesian'}
decorators = {'condition', 'inverter', 'timeout'}
states = {"success": py_trees.common.Status.SUCCESS, "failure": py_trees.common.Status.FAILURE,
          "running": py_trees.common.Status.RUNNING}
commander = cartesian_point.CartesianPoint().commander
