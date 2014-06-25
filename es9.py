import math
import numpy as np
from plot import plot, plot_trajectory, plot_covariance_2d

class UserCode:
    def __init__(self):
        pass

    def get_markers(self):
        '''
        place up to 30 markers in the world
        '''
        waypoints = [
            # M
            [1.5, 0.5],
            [3.0, 0.5],
            [4.5, 0.5],
            [3.5, 2.0],
            [1.5, 3.5],
            [3.0, 3.5],
            [4.5, 3.5],

            # U
            [7.0, 5.5],
            [5.5, 5.5],
            [4.0, 5.5],
            [4.0, 7.0],
            [4.0, 8.5],
            [5.5, 8.5],
            [7.0, 8.5],

            # T
            [9.5, 9.5],
            [9.5, 11.0],
            [9.5, 12.5],
            [8.0, 11.0],
            [6.5, 11.0],
        ]
        markers = waypoints + [
            [5.0, 4.0],
            [6.0, 4.5],

            [8.0, 9.0],
            [9.0, 9.0],
        ]
        return markers

    def state_callback(self, t, dt, linear_velocity, yaw_velocity):
        '''
        called when a new odometry measurement arrives approx. 200Hz

        :param t - simulation time
        :param dt - time difference this last invocation
        :param linear_velocity - x and y velocity in local quadrotor coordinate frame (independet of roll and pitch)
        :param yaw_velocity - velocity around quadrotor z axis (independet of roll and pitch)

        :return tuple containing linear x and y velocity control commands in local quadrotor coordinate frame (independet of roll and pitch), and yaw velocity
        '''

        return np.ones((2,1)) * 0.1, 0

    def measurement_callback(self, marker_position_world, marker_yaw_world, marker_position_relative, marker_yaw_relative):
        '''
        called when a new marker measurement arrives max 30Hz, marker measurements are only available if the quadrotor is
        sufficiently close to a marker

        :param marker_position_world - x and y position of the marker in world coordinates 2x1 vector
        :param marker_yaw_world - orientation of the marker in world coordinates
        :param marker_position_relative - x and y position of the marker relative to the quadrotor 2x1 vector
        :param marker_yaw_relative - orientation of the marker relative to the quadrotor
        '''
        pass
