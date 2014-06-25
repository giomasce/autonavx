import math
import numpy as np
from plot import plot, plot_trajectory, plot_covariance_2d

class UserCode:
    def __init__(self):
        #process noise
        pos_noise_std = 0.005
        yaw_noise_std = 0.005
        self.Q = np.array([
            [pos_noise_std*pos_noise_std,0,0],
            [0,pos_noise_std*pos_noise_std,0],
            [0,0,yaw_noise_std*yaw_noise_std]
        ])

        #measurement noise
        z_pos_noise_std = 0.005
        z_yaw_noise_std = 0.03
        self.R = np.array([
            [z_pos_noise_std*z_pos_noise_std,0,0],
            [0,z_pos_noise_std*z_pos_noise_std,0],
            [0,0,z_yaw_noise_std*z_yaw_noise_std]
        ])

        # state vector [x, y, yaw] in world coordinates
        self.x = np.zeros((3,1))

        # 3x3 state covariance matrix
        self.sigma = 0.01 * np.identity(3)

        self.Kp_psi = 1.0
        self.Kp_xy = 2.0
        self.Kp_xy_sq = 0.1
        self.Kd_xy = 0.4

        self.wp_idx = 0
        self.wp_dist = 0.5
        self.t = 0.0

        self.waypoints = [
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
        self.wp_vel = [
            # M
            [1.0, 0.0],
            [1.0, 0.0],
            [0.0, 0.0],
            [-0.7, 0.7],
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 0.0],

            # U
            [0.0, 0.0],
            [-1.0, 0.0],
            [0.0, 0.5],
            [1.0, 0.0],
            [0.5, 0.0],
            [1.0, 0.0],
            [0.8, 0.1],

            # T
            [0.0, 0.5],
            [0.0, 1.0],
            [-0.5, 0.0],
            [-1.0, 0.0],
            [0.0, 0.0],
        ]

    def get_markers(self):
        '''
        place up to 30 markers in the world
        '''
        markers = self.waypoints + [
            [0.0, 0.0],

            [5.0, 4.0],
            [6.0, 4.5],

            [8.0, 9.0],
            [9.0, 9.0],
        ]
        return markers

    def next_wp(self):
        if self.wp_idx < len(self.waypoints):
            return self.waypoints[self.wp_idx]
        else:
            return None

    def next_vel(self):
        if self.wp_idx < len(self.waypoints):
            return self.wp_vel[self.wp_idx]
        else:
            return None

    def verify_wp(self):
        wp = self.next_wp()
        if wp is None:
            return
        if (self.x[0] - wp[0])**2 + (self.x[1] - wp[1])**2 <= self.wp_dist**2:
            print "Time %f: found waypoint %f, %f" % (self.t, wp[0], wp[1])
            self.wp_idx += 1

    def rotation(self, yaw):
        '''
        create 2D rotation matrix from given angle
        '''
        s_yaw = math.sin(yaw)
        c_yaw = math.cos(yaw)

        return np.array([
            [c_yaw, -s_yaw],
            [s_yaw,  c_yaw]
        ])

    def normalizeYaw(self, y):
        '''
        normalizes the given angle to the interval [-pi, +pi]
        '''
        while(y > math.pi):
            y -= 2 * math.pi
        while(y < -math.pi):
            y += 2 * math.pi
        return y

    def normalizeVect(self, x):
        return x / math.sqrt(np.dot(x.T, x)[0, 0])

    def visualizeState(self):
        # visualize position state
        plot_trajectory("kalman", self.x[0:2])
        plot_covariance_2d("kalman", self.sigma[0:2,0:2])

    def predictState(self, dt, x, u_linear_velocity, u_yaw_velocity):
        '''
        predicts the next state using the current state and
        the control inputs local linear velocity and yaw velocity
        '''
        x_p = np.zeros((3, 1))
        x_p[0:2] = x[0:2] + dt * np.dot(self.rotation(x[2]), u_linear_velocity)
        x_p[2]   = x[2]   + dt * u_yaw_velocity
        x_p[2]   = self.normalizeYaw(x_p[2])

        return x_p

    def calculatePredictStateJacobian(self, dt, x, u_linear_velocity, u_yaw_velocity):
        '''
        calculates the 3x3 Jacobian matrix for the predictState(...) function
        '''
        s_yaw = math.sin(x[2])
        c_yaw = math.cos(x[2])

        dRotation_dYaw = np.array([
            [-s_yaw, -c_yaw],
            [ c_yaw, -s_yaw]
        ])
        F = np.identity(3)
        F[0:2, 2] = dt * np.dot(dRotation_dYaw, u_linear_velocity)

        return F

    def predictCovariance(self, sigma, F, Q):
        '''
        predicts the next state covariance given the current covariance,
        the Jacobian of the predictState(...) function F and the process noise Q
        '''
        return np.dot(F, np.dot(sigma, F.T)) + Q

    def calculateKalmanGain(self, sigma_p, H, R):
        '''
        calculates the Kalman gain
        '''
        return np.dot(np.dot(sigma_p, H.T), np.linalg.inv(np.dot(H, np.dot(sigma_p, H.T)) + R))

    def correctState(self, K, x_predicted, z, z_predicted):
        '''
        corrects the current state prediction using Kalman gain, the measurement and the predicted measurement

        :param K - Kalman gain
        :param x_predicted - predicted state 3x1 vector
        :param z - measurement 3x1 vector
        :param z_predicted - predicted measurement 3x1 vector
        :return corrected state as 3x1 vector
        '''
        x = x_predicted + np.dot(K, z - z_predicted)
        x[2] = self.normalizeYaw(x[2])

        return x

    def correctCovariance(self, sigma_p, K, H):
        '''
        corrects the sate covariance matrix using Kalman gain and the Jacobian matrix of the predictMeasurement(...) function
        '''
        return np.dot(np.identity(3) - np.dot(K, H), sigma_p)

    def predictMeasurement(self, x, marker_position_world, marker_yaw_world):
        '''
        predicts a marker measurement given the current state and the marker position and orientation in world coordinates
        '''
        z_predicted = Pose2D(self.rotation(x[2]), x[0:2]).inv() * Pose2D(self.rotation(marker_yaw_world), marker_position_world);

        return np.array([[z_predicted.translation[0], z_predicted.translation[1], z_predicted.yaw()]]).T

    def calculatePredictMeasurementJacobian(self, x, marker_position_world, marker_yaw_world):
        '''
        calculates the 3x3 Jacobian matrix of the predictMeasurement(...) function using the current state and
        the marker position and orientation in world coordinates

        :param x - current state 3x1 vector
        :param marker_position_world - x and y position of the marker in world coordinates 2x1 vector
        :param marker_yaw_world - orientation of the marker in world coordinates
        :return - 3x3 Jacobian matrix of the predictMeasurement(...) function
        '''

        mat = np.zeros((3,3))

        xc = x[0]
        yc = x[1]
        psi = x[2]
        xm = marker_position_world[0]
        ym = marker_position_world[1]

        mat[0, 0] = -math.cos(psi)
        mat[0, 1] = -math.sin(psi)
        mat[0, 2] = -math.sin(psi)*(xm-xc) + math.cos(psi)*(ym-yc)
        mat[1, 0] = math.sin(psi)
        mat[1, 1] = -math.cos(psi)
        mat[1, 2] = -math.cos(psi)*(xm-xc) - math.sin(psi)*(ym-yc)
        mat[2, 2] = -1.0

        return mat

    def state_callback(self, t, dt, linear_velocity, yaw_velocity):
        '''
        called when a new odometry measurement arrives approx. 200Hz

        :param t - simulation time
        :param dt - time difference this last invocation
        :param linear_velocity - x and y velocity in local quadrotor coordinate frame (independet of roll and pitch)
        :param yaw_velocity - velocity around quadrotor z axis (independent of roll and pitch)

        :return tuple containing linear x and y velocity control commands in local quadrotor coordinate frame (independent of roll and pitch), and yaw velocity
        '''
        self.t = t
        self.x = self.predictState(dt, self.x, linear_velocity, yaw_velocity)

        F = self.calculatePredictStateJacobian(dt, self.x, linear_velocity, yaw_velocity)
        self.sigma = self.predictCovariance(self.sigma, F, self.Q);

        self.verify_wp()

        self.visualizeState()

        wp = self.next_wp()
        if wp is not None:
            target = np.array([wp]).T
            target_vel = np.array([self.next_vel()]).T
            rot = self.rotation(-self.x[2, 0])
            #xy_P = self.Kp_xy * np.dot(rot, self.normalizeVect(target - self.x[0:2, 0]))
            xy_vect = np.dot(rot, target - self.x[0:2, 0])
            xy_norm = math.sqrt(np.dot(xy_vect.T, xy_vect)[0, 0])
            xy_dir = xy_vect / xy_norm
            xy_P = (self.Kp_xy + self.Kp_xy_sq * xy_norm) * xy_vect
            xy_D = self.Kd_xy * np.dot(rot, target_vel - linear_velocity)
            return xy_P + xy_D, 0.0  # self.Kp_psi * (-self.x[2, 0])
        else:
            return np.zeros(2,1), 0.0

    def measurement_callback(self, marker_position_world, marker_yaw_world, marker_position_relative, marker_yaw_relative):
        '''
        called when a new marker measurement arrives max 30Hz, marker measurements are only available if the quadrotor is
        sufficiently close to a marker

        :param marker_position_world - x and y position of the marker in world coordinates 2x1 vector
        :param marker_yaw_world - orientation of the marker in world coordinates
        :param marker_position_relative - x and y position of the marker relative to the quadrotor 2x1 vector
        :param marker_yaw_relative - orientation of the marker relative to the quadrotor
        '''
        z = np.array([[marker_position_relative[0], marker_position_relative[1], marker_yaw_relative]]).T
        z_predicted = self.predictMeasurement(self.x, marker_position_world, marker_yaw_world)

        H = self.calculatePredictMeasurementJacobian(self.x, marker_position_world, marker_yaw_world)
        K = self.calculateKalmanGain(self.sigma, H, self.R)

        self.x = self.correctState(K, self.x, z, z_predicted)
        self.sigma = self.correctCovariance(self.sigma, K, H)

        self.visualizeState()


class Pose2D:
    def __init__(self, rotation, translation):
        self.rotation = rotation
        self.translation = translation

    def inv(self):
        '''
        inversion of this Pose2D object

        :return - inverse of self
        '''
        inv_rotation = self.rotation.transpose()
        inv_translation = -np.dot(inv_rotation, self.translation)

        return Pose2D(inv_rotation, inv_translation)

    def yaw(self):
        from math import atan2
        return atan2(self.rotation[1,0], self.rotation[0,0])

    def __mul__(self, other):
        '''
        multiplication of two Pose2D objects, e.g.:
            a = Pose2D(...) # = self
            b = Pose2D(...) # = other
            c = a * b       # = return value

        :param other - Pose2D right hand side
        :return - product of self and other
        '''
        return Pose2D(np.dot(self.rotation, other.rotation), np.dot(self.rotation, other.translation) + self.translation)
