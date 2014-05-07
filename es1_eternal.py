import quadrotor.command as cmd
from math import sqrt

def plan_mission(mission):

    # this is an example illustrating the different motion commands,
    # replace them with your own commands and activate all beacons
    commands  = [
        cmd.up(1),
        cmd.left(2+sqrt(0.5)),
        cmd.turn_right(45),
        cmd.forward(5*sqrt(2)),
        cmd.turn_left(45),
        cmd.backward(6),
        cmd.turn_left(45),
        cmd.forward(6*sqrt(2)),
        cmd.turn_right(45),
        cmd.right(6),
    ]

    mission.add_commands(commands)
