import quadrotor.command as cmd
from math import sqrt

def plan_mission(mission):

    # this is an example illustrating the different motion commands,
    # replace them with your own commands and activate all beacons
    commands  = [
        cmd.up(1),
        cmd.forward(5),
        cmd.left(2),
        cmd.backward(4),
        cmd.turn_right(90),
        cmd.forward(4),
        cmd.left(4),
    ]

    mission.add_commands(commands)
