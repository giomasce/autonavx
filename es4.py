class UserCode:
    def __init__(self):
        self.Kp = 5
        self.Kd = 5
        self.last_pos = None

    def compute_control_command(self, t, dt, x_measured, x_desired):
        '''
        :param t: time since simulation start
        :param dt: time since last call to compute_control_command
        :param x_measured: measured position (scalar)
        :param x_desired: desired position (scalar)
        :return - control command u
        '''
        if self.last_pos is None:
            self.last_pos = x_measured
        dist = x_desired - x_measured
        vel_dist = (x_measured - self.last_pos) / dt
        self.last_pos = x_measured
        u = dist * self.Kp - vel_dist * self.Kd

        return u

