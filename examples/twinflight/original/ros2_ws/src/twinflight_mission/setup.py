from setuptools import setup
from glob import glob
import os

package_name = "twinflight_mission"

setup(
    name=package_name,
    version="0.2.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
        (os.path.join("share", package_name, "launch"), glob("launch/*.py")),
    ],
    install_requires=["setuptools", "PyYAML"],
    zip_safe=True,
    maintainer="TwinFlight Team",
    maintainer_email="example@example.com",
    description="ROS2 PX4 waypoint mission simulator for presentation",
    license="BSD-3-Clause",
    entry_points={
        "console_scripts": [
            "mission_node = twinflight_mission.mission_node:main",
            "mission_preview = twinflight_mission.mission_preview:main",
        ],
    },
)
