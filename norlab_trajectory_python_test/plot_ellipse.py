import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D

def plot_ellipse_2D(ax, mean, cov, n_std=2, color="tab:red", alpha=.2, border=False, **kwargs):
    if cov[0,0] < 1e-5**2 or cov[1,1] < 1e-5**2:
        return
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0),
        width=ell_radius_x * 2,
        height=ell_radius_y * 2,
        facecolor= (colors.to_rgba(color, alpha) if border==False else (0,0,0,0)),
        edgecolor= (colors.to_rgba(color, alpha) if border==True else (0,0,0,0)),
        **kwargs)
    # Calculating the stdandard deviation of x from the squareroot of the variance and multiplying with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = mean[0].flatten()
    # calculating the stdandard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = mean[1].flatten()
    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)
    ellipse.set_transform(transf + ax.transData)
    # ax.scatter(*mean, marker='x', color=color)
    return ax.add_patch(ellipse)