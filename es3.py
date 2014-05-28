import numpy as np

class Pose3D:
    def __init__(self, rotation, translation):
        self.rotation = rotation
        self.translation = translation

    def to_matrix(self):
        comp_matrix = np.hstack([self.rotation, self.translation])
        proj_matrix = np.vstack([comp_matrix, np.array([[0, 0, 0, 1]])])
        return proj_matrix

    def from_matrix(self, mat):
        rotation = mat[:3, :3]
        translation = mat[:3, 3:4]

        return Pose3D(rotation, translation)

    def inv(self):
        '''
        Inversion of this Pose3D object

        :return inverse of self
        '''
        proj_matrix = self.to_matrix()
        proj_inv = np.linalg.inv(proj_matrix)
        return self.from_matrix(proj_inv)

    def __mul__(self, other):
        '''
        Multiplication of two Pose3D objects, e.g.:
            a = Pose3D(...) # = self
            b = Pose3D(...) # = other
            c = a * b       # = return value

        :param other: Pose3D right hand side
        :return product of self and other
        '''
        proj_self = self.to_matrix()
        proj_other = other.to_matrix()
        proj_ret = np.dot(proj_self, proj_other)
        return self.from_matrix(proj_ret)

    def __str__(self):
        return "rotation:\n" + str(self.rotation) + "\ntranslation:\n" + str(self.translation.transpose())

def compute_quadrotor_pose(global_marker_pose, observed_marker_pose):
    '''
    :param global_marker_pose: Pose3D
    :param observed_marker_pose: Pose3D

    :return global quadrotor pose computed from global_marker_pose and observed_marker_pose
    '''
    global_quadrotor_pose = global_marker_pose * observed_marker_pose.inv()

    return global_quadrotor_pose
