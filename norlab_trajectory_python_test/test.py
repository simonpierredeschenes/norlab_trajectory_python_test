import norlab_trajectory
import numpy as np
import copy
import os
import matplotlib.pyplot as plt
from tqdm import tqdm
from .plot_ellipse import plot_ellipse_2D

def main():
    pose = np.eye(4)
    poses = []
    time_stamp_list = []
    covariance = []
    traj_estim = []

    for i in range(10):
        pose[0, 3] = float(i)
        pose[1, 3] = np.sin(pose[0, 3])
        poses.append((copy.deepcopy(pose)))
        cov = np.eye(6)
        covariance.append(cov)
    
    time_stamps = np.linspace(poses[0], poses[-1], 100)
    print(time_stamps)
    for time in time_stamps :
        time_stamp_list.append(time)
    
    traj = norlab_trajectory.Trajectory(time_stamp_list, poses, covariance)

    for time in time_stamps:
        traj_estim.append(traj.getPose(time))

    for time in tqdm(time_stamps) :
        covariance.append(traj.getPoseCovariance(time))

    values_x = [pose[0][3] for pose in poses]
    values_y = [pose[1][3] for pose in poses]

    values_x_estim = [pose[0][3] for pose in traj_estim]
    values_y_estim = [pose[1][3] for pose in traj_estim]

    plt.plot(values_x, values_y, '.', label='measured values')
    plt.plot(values_x_estim, values_y_estim, '-', label='interpolated values')

    for pose, cov in zip(traj_estim, covariance):
        plot_ellipse_2D(plt.gca(),pose[:2,3], cov[:2,:2], n_std=3)

    plt.legend()
    plt.savefig(os.path.expanduser('~') + '/ros2_ws/src/norlab_trajectory_python_test/norlab_trajectory_python_test/Figures/test_py_cov.png')

