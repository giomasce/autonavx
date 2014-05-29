class UserCode:
    def compute_control_command(self, t, dt, x_measured, x_desired):
        '''
        :param t: time since simulation start
        :param dt: time since last call to compute_control_command
        :param x_measured: measured position (scalar)
        :param x_desired: desired position (scalar)
        :return - control command u
        '''
        duration = 32
        power = 97.5
        step = int(t/dt)
        if step < duration:
            return power
        elif step < 2*duration:
            return -power
        else:
            return 0
