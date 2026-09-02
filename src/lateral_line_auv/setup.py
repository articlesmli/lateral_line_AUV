import os
from glob import glob
from setuptools import setup

package_name = 'lateral_line_auv'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.xacro')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ivanovaml',
    maintainer_email='ivanovaml@todo.todo',
    description='Bio-inspired lateral line sensing and navigation for AUVs',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_node = lateral_line_auv.sensor_node:main',
            'controller_node = lateral_line_auv.controller_node:main',
        ],
    },
)