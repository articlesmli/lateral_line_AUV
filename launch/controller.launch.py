import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('lateral_line_auv')
    controller_params_path = os.path.join(pkg_share, 'config', 'controller_params.yaml')

    controller_node = Node(
        package='lateral_line_auv',
        executable='controller_node',
        name='controller_node',
        output='screen',
        parameters=[controller_params_path]
    )

    return LaunchDescription([
        controller_node
    ])