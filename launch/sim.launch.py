import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('lateral_line_auv')
    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    controller_params_path = os.path.join(pkg_share, 'config', 'controller_params.yaml')
    nav2_params_path = os.path.join(pkg_share, 'config', 'nav2_params.yaml')

    # Custom AUV Lifecycle Controller Node with isolated parameters
    controller_node = Node(
        package='lateral_line_auv',
        executable='controller_node',
        name='controller_node',
        output='screen',
        parameters=[controller_params_path]
    )

    # Nav2 Bringup Navigation Launch Integration
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup_dir, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'True',
            'params_file': nav2_params_path
        }.items()
    )

    return LaunchDescription([
        controller_node,
        nav2_bringup_launch
    ])