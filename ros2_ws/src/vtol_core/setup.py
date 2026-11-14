from setuptools import setup

package_name = 'vtol_core'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/sim_launch.py',
            'launch/real_launch.py',
        ]),
        ('share/' + package_name + '/config', ['config/global_params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='SkyEdge Team',
    maintainer_email='team@example.com',
    description='VTOL mission core for competition',
    license='MIT',
    entry_points={
        'console_scripts': [
            'px4_bridge_node = vtol_core.px4_bridge_node:main',
            'mission_manager_node = vtol_core.mission_manager_node:main',
            'guidance_node = vtol_core.guidance_node:main',
            'safety_manager = vtol_core.safety_manager:main',
        ],
    },
)
