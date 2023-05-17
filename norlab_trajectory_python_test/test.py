import norlab_trajectory
import numpy as np
import copy
import matplotlib.pyplot as plt
from tqdm import tqdm
from .plot_ellipse import plot_ellipse_2D


def main():
    pose = np.eye(4)
    poses = []
    covariance = []
    for i in range(10):
        pose[0, 3] = float(i)
        pose[1, 3] = np.sin(pose[0, 3])
        poses.append((float(i), copy.deepcopy(pose)))
    traj = norlab_trajectory.Trajectory(poses)

    time_stamps = np.linspace(poses[0][0], poses[-1][0], 100)
    traj_estim = []
    for time_stamp in time_stamps:
        traj_estim.append(traj.getPose(time_stamp))
    for time in tqdm(np.linspace(poses[0][0], poses[-1][0], 100)) :
        covariance.append(traj.getPoseCovariance(time))
    
    values_x = [pose[1][0][3] for pose in poses]
    values_y = [pose[1][1][3] for pose in poses]

    values_x_estim = [pose[0][3] for pose in traj_estim]
    values_y_estim = [pose[1][3] for pose in traj_estim]

    plt.plot(values_x, values_y, '.', label='measured values')
    plt.plot(values_x_estim, values_y_estim, '-', label='interpolated values')
    for pose, cov in zip(traj_estim, covariance):
        plot_ellipse_2D(plt.gca(),pose[:2,3], cov[:2,:2], n_std=3)
    plt.legend()
    plt.show()
