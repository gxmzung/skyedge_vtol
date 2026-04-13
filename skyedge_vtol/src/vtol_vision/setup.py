from setuptools import setup

package_name = 'vtol_vision'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='SkyEdge Team',
    maintainer_email='team@example.com',
    description='VTOL vision nodes',
    license='MIT',
    entry_points={
        'console_scripts': [
            'line_tracker_node = vtol_vision.line_tracker_node:main',
            'aruco_detector_node = vtol_vision.aruco_detector_node:main',
        ],
    },
)
