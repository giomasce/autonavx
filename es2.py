import numpy as np
from plot import plot_trajectory

from numpy import *
from math import *

def rot_trans_mat(x, y, psi):
    return array(
        [[cos(psi), -sin(psi), x],
         [sin(psi), cos(psi), y],
         [0, 0, 1]])

class UserCode:
    def __init__(self):
        self.position = np.array([[0], [0]])

    def measurement_callback(self, t, dt, navdata):
        '''
        :param t: time since simulation start
        :param dt: time since last call to measurement_callback
        :param navdata: measurements of the quadrotor
        '''
        cur_mat = rot_trans_mat(self.position[0], self.position[1], navdata.rotZ)
        new_pos = dot(cur_mat, array([[navdata.vx * dt], [navdata.vy * dt], [1.0]]))
        #print new_pos
        self.position = array([[new_pos[0]], [new_pos[1]]])
        plot_trajectory("odometry", self.position)
