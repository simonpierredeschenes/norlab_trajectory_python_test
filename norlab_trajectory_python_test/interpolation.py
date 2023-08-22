import norlab_trajectory
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial.transform import Rotation as R

from pathlib import Path
BASE_PATH = Path(__file__).absolute().parents[1] / 'norlab_trajectory_python_test'
import argparse

def main(input_file, covariance, points):
    traj_estim = []
    df = pd.read_csv(BASE_PATH / f'{input_file}', names=["Timestamp", "X", "Y", "Z", "qx", "qy", "qz", "qw"], delimiter= ' ')

    timestamps = df['Timestamp'].values
    poses = []

    for i in range(len(timestamps)):
    # for i in range(1000,1100) :
        x = df['X'][i] - df['X'][0]
        y = df['Y'][i] - df['Y'][0]
        z = df['Z'][i] - df['Z'][0]
        qx = df['qx'][i]
        qy = df['qy'][i]
        qz = df['qz'][i]
        qw = df['qw'][i]

        T = np.identity(4)
        Rot = R.from_quat([qx, qy, qz, qw]).as_matrix()
        T[0:3, 0:3] = Rot
        T[0, 3] = x
        T[1, 3] = y
        T[2, 3] = z
        
        poses.append((T))

    covariances = [covariance * np.eye(6) for _ in range(len(timestamps))]

    traj = norlab_trajectory.Trajectory(timestamps, poses, covariances)

    timestamps_interpolation = np.linspace(timestamps[0], timestamps[-1], len(timestamps)*points)

    for time in timestamps_interpolation:
        traj_estim.append(traj.getPose(time))
        
    values_x = [pose[0, 3] for pose in poses]
    values_y = [pose[1, 3] for pose in poses]
    values_z= [pose[2, 3] for pose in poses]

    # nx_u = [pose[0,0] for pose in poses]
    # nx_v = [pose[1,0] for pose in poses]

    # ny_u = [pose[0,1] for pose in poses]
    # ny_v = [pose[1,1] for pose in poses]

    values_x_estim = [pose[0, 3] for pose in traj_estim]
    values_y_estim = [pose[1, 3] for pose in traj_estim]
    values_z_estim = [pose[2, 3] for pose in traj_estim]


    fig, ax = plt.subplots()
    ax.plot(values_x, values_y, '.', label='measured values')
    # ax.quiver(values_x, values_y, nx_u, nx_v, angles = 'xy', scale_units ='xy', scale =1 , headwidth =1, color='r', label='measured values')
    # ax.quiver(values_x, values_y, ny_u, ny_v, angles = 'xy', scale_units ='xy', scale =1 , headwidth =1, color='g', label='measured values')

    plt.scatter(values_x_estim, values_y_estim, label='interpolated values', c=timestamps_interpolation, alpha=0.5)
    ax.set_aspect('equal')
    ax.legend()
    plt.show()
   # plt.savefig('/home/user/ros_ws/src/norlab_trajectory_python_test/norlab_trajectory_python_test/interpolation_4.png')

def init_argparse():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        type=str, required=True,
                        help='Name of input file.')
    parser.add_argument('-cov', '--covariance',
                        type=float, required=False, default=1e-7,
                        help='Covariance value for interpolation, default value is 1e-7.')
    parser.add_argument('-p', '--points',
                        type=int, required=False, default=1,
                        help='Number of points between two timestamps, default value is 1.')
    return parser

if __name__ == '__main__' :
    parser = init_argparse()
    args = parser.parse_args()
    main(args.input, args.covariance, args.points)