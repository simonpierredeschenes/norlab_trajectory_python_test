import norlab_trajectory
import numpy as np
import copy
import matplotlib.pyplot as plt
import csv


def main():
    pose_list = []
    traj_estim = []
    timestamps_set = set()

    with open('/home/effie/ros2_ws/src/norlab_trajectory_python_test/norlab_trajectory_python_test/odom_data copy.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        next(reader)

        for row in reader:
            timestamp, x, y, z, qx, qy, qz, qw = row
            timestamp, x, y, z, qx, qy, qz, qw = map(float, [timestamp, x, y, z, qx, qy, qz, qw])

            if timestamp in timestamps_set:
                continue
            timestamps_set.add(timestamp)

            T = np.array([
                [1 - 2 * qy ** 2 - 2 * qz ** 2, 2 * qx * qy - 2 * qz * qw, 2 * qx * qz + 2 * qy * qw, x],
                [2 * qx * qy + 2 * qz * qw, 1 - 2 * qx ** 2 - 2 * qz ** 2, 2 * qy * qz - 2 * qx * qw, y],
                [2 * qx * qz - 2 * qy * qw, 2 * qy * qz + 2 * qx * qw, 1 - 2 * qx ** 2 - 2 * qy ** 2, z],
                [0, 0, 0, 1]])

            pose_list.append((timestamp, copy.deepcopy(T)))

    traj = norlab_trajectory.Trajectory(pose_list)

    print(pose_list[0])
    print(traj.getPose(pose_list[0][0]))

    time_stamps = np.linspace(pose_list[0][0], pose_list[-1][0], 100)
    for time in time_stamps:
        traj_estim.append(traj.getPose(time))

    values_x = [pose[1][0][3] for pose in pose_list]
    values_y = [pose[1][1][3] for pose in pose_list]
    values_x_estim = [pose[0][3] for pose in traj_estim]
    values_y_estim = [pose[1][3] for pose in traj_estim]

    plt.plot(values_x, values_y, '.', label='measured values')
    plt.plot(values_x_estim, values_y_estim, '-', label='interpolated values')
    plt.legend()
    plt.show()
