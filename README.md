# A Simple Alternative for function moveToPositionAsync in AirSim

I found the moveToPositionAsync function in AirSim not accurate enough, while moveByVelocityAsync seemed more reliable, so I came up of a substitution.

This is just a simple and naive solution, please only use when there's no critical demand to the performance.

I also referred to discussions on this page: https://github.com/Microsoft/AirSim/issues/1677
