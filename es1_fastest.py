import quadrotor.command as cmd
from math import sqrt

def plan_mission(mission):

    DELTA = 0.125
    VDELTA = 0.45
    commands  = [
        cmd.up(1-VDELTA),
        cmd.forward(5-DELTA),
        cmd.left(2-DELTA),
        cmd.backward(4-2*DELTA),
        cmd.right(4-2*DELTA),
        cmd.forward(6),
    ]

    mission.add_commands(commands)
