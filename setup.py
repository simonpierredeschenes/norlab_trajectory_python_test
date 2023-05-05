from setuptools import setup

package_name = 'norlab_trajectory_python_test'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'norlab_trajectory'],
    zip_safe=True,
    maintainer='Simon-Pierre Deschênes',
    maintainer_email='simon-pierre.deschenes.1@ulaval.ca',
    description='A package to test the python bindings of norlab_trajectory.',
    license='BSD-2.0',
    entry_points={
        'console_scripts': [
            'test = norlab_trajectory_python_test.test:main',
            'trajectory_ros = norlab_trajectory_python_test.trajectory_ros:main',
        ],
    },
)
