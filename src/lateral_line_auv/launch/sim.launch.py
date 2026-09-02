from launch import LaunchDescription
from launch.actions import EmitEvent, RegisterEventHandler
from launch_ros.actions import LifecycleNode, Node
from launch_ros.events.lifecycle import ChangeState
from launch_ros.event_handlers import OnStateTransition
import lifecycle_msgs.msg

def generate_launch_description():
    # Define the lifecycle controller node
    controller_node = LifecycleNode(
        package='lateral_line_auv',
        executable='controller_node',
        name='controller_node',
        namespace='',
        output='screen',
        parameters=[{'alpha': 0.2, 'max_steering': 0.3, 'surge_velocity': 0.5}]
    )

    # Standard sensor node
    sensor_node = Node(
        package='lateral_line_auv',
        executable='sensor_node',
        name='sensor_node',
        output='screen'
    )

    # Automatically trigger 'configure' once the node spawns
    to_configure_transition = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=controller_node,
            transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE,
        )
    )

    # Automatically trigger 'activate' once the node reaches the 'inactive' state
    activate_handler = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=controller_node,
            start_state='configuring',
            goal_state='inactive',
            entities=[
                EmitEvent(
                    event=ChangeState(
                        lifecycle_node_matcher=controller_node,
                        transition_id=lifecycle_msgs.msg.Transition.TRANSITION_ACTIVATE,
                    )
                )
            ]
        )
    )

    # Trigger configuration right after startup
    configure_handler = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=controller_node,
            start_state='unconfigured',
            goal_state='unconfigured',
            entities=[]
        )
    )

    return LaunchDescription([
        sensor_node,
        controller_node,
        RegisterEventHandler(
            OnStateTransition(
                target_lifecycle_node=controller_node,
                start_state='unknown',
                goal_state='unconfigured',
                entities=[to_configure_transition]
            )
        ),
        activate_handler
    ])