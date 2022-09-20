from operator import truediv
from airsim.types import ImageRequest, Quaternionr, Vector3r
import airsim
import time
import numpy as np
from scipy.spatial.transform import Rotation as R


class airsim_client:
    # def __init__(self, ip_addr="127.0.0.1") -> None:
    #     print("Try to connect {}...".format(ip_addr))
    #     self.client = airsim.MultirotorClient(ip_addr)
    #     self.client.confirmConnection()
    #     self.client.enableApiControl(True)

    #     self.dhc = dh.drone_func_class()
    #     self.circle_finder = circle_finder.circle_finder(self.client)

    #     self.setpoints = uav_setpoints()

    def moveToPosition(self, x, y, z, max_v):
        currentPos = self.client.getMultirotorState().kinematics_estimated.position
        current_dist = (
            (currentPos.x_val - x) ** 2
            + (currentPos.y_val - y) ** 2
            + (currentPos.z_val - z) ** 2
        ) ** 0.5
        # t = current_dist / max_v

        timer = 0
        timer_on_flag = False
        timer_start = time.time()
        timer_end = time.time()
        iter_times = 0
        delta_t = 0.05
        while current_dist > 0.15 or timer <= 0.8 or timer_on_flag == False:
            iter_times += 1
            # Calculate and move to target
            delta_x = x - currentPos.x_val
            delta_y = y - currentPos.y_val
            delta_z = z - currentPos.z_val
            vx = min(delta_x, max_v)
            vy = min(delta_y, max_v)
            vz = min(delta_z, max_v)
            self.client.moveByVelocityAsync(vx, vy, vz, delta_t)
            time.sleep(delta_t)

            # Update distance
            currentPos = self.client.getMultirotorState().kinematics_estimated.position
            current_dist = (
                (currentPos.x_val - x) ** 2
                + (currentPos.y_val - y) ** 2
                + (currentPos.z_val - z) ** 2
            ) ** 0.5

            # Judge if to start timer
            if current_dist <= 0.1 and timer_on_flag == False:
                timer_on_flag = True
                timer_start = time.time()

            timer_end = time.time()

            # Judge if to cancel timer
            if current_dist > 0.1:
                timer_on_flag = False
                timer_end = timer_start

            # Calculate time span
            timer = timer_end - timer_start

            print(
                iter_times,
                "\tCur_dist =",
                format(current_dist, ".3f"),
                "\tTimer =",
                format(timer, ".3f"),
                "\tTimer_on_flag =",
                timer_on_flag,
            )

        # Make UAV hover stably
        self.client.moveByVelocityAsync(0, 0, 0, 0.2)
        time.sleep(0.2)
        print("=====Arrived at target!=====\n")
        self.client.hoverAsync().join()
