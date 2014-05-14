
from numpy import *
from math import *

def rot_trans_mat(x, y, psi):
    return matrix(
        [[cos(psi), -sin(psi), x],
         [sin(psi), cos(psi), y],
         [0, 0, 1]])

def write_array(array):
    return ", ".join(["%f" % (x) for x in array])

def write_mat(mat):
    return "; ".join([", ".join(["%s" % (x) for x in y.A1]) for y in mat])

if __name__ == '__main__':
    print write_array(array([1, 2, 3]))
    print write_mat(matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))
