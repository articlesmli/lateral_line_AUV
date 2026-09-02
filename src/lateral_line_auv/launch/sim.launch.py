import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg_share = get_package_share_directory('lateral_line_auv')
    
    # Locate and process URDF/Xacro file
    xacro_file = os.path.join(pkg_share, 'urdf', 'auv.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # Start Gazebo Sim Server/Client
    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': 'empty.sdf -r'}.items()
    )

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # Spawn AUV into Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description',
                   '-name', 'lateral_line_auv',
                   '-z', '1.5']
    )

    # Sensor Node
    sensor_node = Node(
        package='lateral_line_auv',
        executable='sensor_node',
        name='lateral_line_sensor_node',
        output='screen'
    )

    # Controller Node
    controller_node = Node(
        package='lateral_line_auv',
        executable='controller_node',
        name='auv_nav_controller',
        output='screen'
    )

    return LaunchDescription([
        gz_sim_launch,
        robot_state_publisher_node,
        spawn_entity,
        sensor_node,
        controller_node
    ])