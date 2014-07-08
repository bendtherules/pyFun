
# Maybe make a non-square rooted function for comparison (faster)
from uniquelist import uniquelist
import math


def atan2_inv(y_diff, x_diff):
    '''Returns atan2 in inverted y-axis in degrees'''
    return math.degrees(math.atan2(-y_diff, x_diff))
# following constants are required for the next function


def distance(point_1, point_2):
    ''' distance between point_1 and point_2, where both are 2 member iterable'''
    if (not len(point_1) == 2) or (not len(point_2) == 2):
        raise TypeError("point_1 and point_2 both must be 2 member iterable")
    diff_x = point_2[0] - point_1[0]
    diff_y = point_2[1] - point_1[1]
    return math.hypot(diff_x, diff_y)


def vel_add(vel_1, vel_2):
    ''' vel_1 and vel_2 both must be in (magnitude,direction_in_degree) format.
        Returns in same format.'''
    if (not len(vel_1) == 2) or (not len(vel_2) == 2):
        raise TypeError("vel_1 and vel_2 both must be 2 member iterable")

    vel_1_x = vel_1[0] * math.cos(math.radians(vel_1[1]))
    vel_1_y = -vel_1[0] * math.sin(math.radians(vel_1[1]))

    vel_2_x = vel_2[0] * math.cos(math.radians(vel_2[1]))
    vel_2_y = -vel_2[0] * math.sin(math.radians(vel_2[1]))

    vel_tot_x = vel_1_x + vel_2_x
    vel_tot_y = vel_1_y + vel_2_y

    vel_tot = (
        math.hypot(vel_tot_x, vel_tot_y), atan2_inv(vel_tot_y, vel_tot_x))

    return vel_tot


def direction(point_1, point_2):
    if (not len(point_1) == 2) or (not len(point_2) == 2):
        raise TypeError("point_1 and point_2 both must be 2 member iterable")
    diff_x = point_2[0] - point_1[0]
    diff_y = point_2[1] - point_1[1]
    return atan2_inv(diff_y, diff_x)

UNION = 1
INTERSECTION = 2
DIFFERENCE = 3
ADD = 4
# for each member (usually objects) in the list, it is replaced by one of
# its variables
MAKE_IT_VARIABLE_LIST = 5


def operation_on_lists(operation, list1, list2=None, variable_name=None):
    ''' operation_on_lists(operation, list1, list2) -> list
        Does operation involving list1 and list2.
        variable_name is required only for MAKE_IT_VARIABLE_LIST operation. It is a string representing the variable name
        Valid operations are UNION, INTERSECTION, DIFFERENCE, ADD, MAKE_IT_VARIABLE_list '''
    def intersection():
        if list2 is None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = []
        for temp1 in list1:
            for temp2 in list2:
                if temp1 == temp2:
                    list_return.append(temp1)
        return list_return

    def union():
        if list2 is None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = uniquelist()
        list_return.extend(list1)
        list_return.extend(list2)
        return list_return

    def add():
        if list2 is None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = []
        list_return.append(list1)
        list_return.append(list2)
        return list_return

    def difference():
        if list2 is None:
            raise TypeError("second argument i.e. list2 should be a list")
        list_return = []
        list_intersection = intersection()
        for temp1 in list1:
            if temp1 not in list_intersection:
                list_return.append(temp1)
        return list_return

    # for each member (usually objects) in the list, it is replaced by one of
    # its variables
    def make_it_variable_list():
        if variable_name is None:
            raise TypeError("variable_name should be a string")
        if not list2 is None:
            raise TypeError("list2 should be None")
        return_list = [getattr(temp, variable_name) for temp in list1]

    if operation == UNION:
        return union()
    elif operation == INTERSECTION:
        return intersection()
    elif operation == DIFFERENCE:
        return difference()
    elif operation == ADD:
        return add()
    elif operation == MAKE_IT_VARIABLE_LIST:
        return make_it_variable_list()
    else:
        raise ValueError(
            "Invalid operation name. Valid operations are UNION, INTERSECTION, DIFFERENCE.")
# end of operation_on_lists()
