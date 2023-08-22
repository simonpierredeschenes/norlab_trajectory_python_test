import norlab_trajectory
import numpy as np
import copy
import matplotlib.pyplot as plt
import csv
import os
from tqdm import tqdm
from .plot_ellipse import plot_ellipse_2D

def main():
    pose_list = []
    traj_estim = []
    covariance = []

    # with open(os.path.expanduser('~') +'/ros2_ws/src/norlab_trajectory_python_test/norlab_trajectory_python_test/odom_data.csv', newline='') as csvfile:
    with open(os.path.expanduser('~') + '/ros2_ws/src/norlab_trajectory_python_test/norlab_trajectory_python_test/f1tenth_ros_bag_2023_05_11-12_09_52.csv', newline='') as csvfile:
    # with open(os.path.expanduser('~') + '/ros2_ws/src/norlab_trajectory_python_test/norlab_trajectory_python_test/warthog_bag_file_2022-07-15-14-49-32.csv', newline='') as csvfile:

        reader = csv.reader(csvfile, delimiter=',')
        next(reader)

        for row in reader:
            timestamp, x, y, z, qx, qy, qz, qw = map(float, row)
            T = np.array([
                [1 - 2 * qy ** 2 - 2 * qz ** 2, 2 * qx * qy - 2 * qz * qw, 2 * qx * qz + 2 * qy * qw, x],
                [2 * qx * qy + 2 * qz * qw, 1 - 2 * qx ** 2 - 2 * qz ** 2, 2 * qy * qz - 2 * qx * qw, y],
                [2 * qx * qz - 2 * qy * qw, 2 * qy * qz + 2 * qx * qw, 1 - 2 * qx ** 2 - 2 * qy ** 2, z],
                [0, 0, 0, 1]])
            pose_list.append((timestamp, copy.deepcopy(T)))

    traj = norlab_trajectory.Trajectory(pose_list)

    for time in np.linspace(pose_list[0][0], pose_list[-1][0], len(pose_list)*10):
        traj_estim.append(traj.getPose(time))

    for time in tqdm(np.linspace(pose_list[0][0], pose_list[-1][0], len(pose_list))) :
        covariance.append(traj.getPoseCovariance(time))

    values_x = [pose[1][0][3] for pose in pose_list]
    values_y = [pose[1][1][3] for pose in pose_list]
    values_z= [pose[1][2][3] for pose in pose_list]

    values_x_estim = [pose[0][3] for pose in traj_estim]
    values_y_estim = [pose[1][3] for pose in traj_estim]
    values_z_estim = [pose[2][3] for pose in traj_estim]

    #timestamp ,x,
    plt.plot(values_x, values_y, '.', label='measured values', alpha = .5)
    plt.plot(values_x_estim, values_y_estim, '-', label='interpolated values', alpha = .8)
    plt.plot(values_x_estim, values_y_estim, '-', label='interpolated values', alpha = .8)
    for pose, cov in zip(traj_estim, covariance):
        plot_ellipse_2D(plt.gca(),pose[:2,3], cov[:2,:2],n_std=7,color="tab:red", alpha = .2, border=False)
    plt.legend()
    plt.show()