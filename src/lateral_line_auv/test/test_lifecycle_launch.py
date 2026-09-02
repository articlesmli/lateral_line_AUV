import unittest
import launch
import launch_ros.actions
import launch_testing.actions
import pytest
import rclpy
from lifecycle_msgs.srv import GetState, ChangeState
from lifecycle_msgs.msg import Transition

@pytest.mark.rostest
def generate_test_description():
    controller_node = launch_ros.actions.LifecycleNode(
        package='lateral_line_auv',
        executable='controller_node',
        name='controller_node',
        namespace='',
        output='screen'
    )

    return launch.LaunchDescription([
        controller_node,
        launch_testing.actions.ReadyToTest()
    ])

class TestAuvLifecycle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.node = rclpy.create_node('test_lifecycle_client')

    def tearDown(self):
        self.node.destroy_node()

    def trigger_transition(self, get_state_client, change_state_client, transition_id, expected_state):
        req_change = ChangeState.Request()
        req_change.transition.id = transition_id
        future_change = change_state_client.call_async(req_change)
        rclpy.spin_until_future_complete(self.node, future_change, timeout_sec=3.0)
        
        result = future_change.result()
        self.assertIsNotNone(result, f"Service call for transition ID {transition_id} timed out or returned None")
        self.assertTrue(
            result.success, 
            f"Transition ID {transition_id} failed. Node rejected the transition (did on_configure/on_activate return FAILURE?)"
        )

        req_state = GetState.Request()
        future_state = get_state_client.call_async(req_state)
        rclpy.spin_until_future_complete(self.node, future_state, timeout_sec=3.0)
        
        current_state = future_state.result().current_state.label
        self.assertEqual(current_state, expected_state, f"Expected state '{expected_state}', but got '{current_state}' after transition ID {transition_id}")

    def test_node_lifecycle_transitions(self):
        get_state_client = self.node.create_client(GetState, '/controller_node/get_state')
        change_state_client = self.node.create_client(ChangeState, '/controller_node/change_state')

        self.assertTrue(get_state_client.wait_for_service(timeout_sec=5.0))
        self.assertTrue(change_state_client.wait_for_service(timeout_sec=5.0))

        # 1. Query initial state
        req_state = GetState.Request()
        future = get_state_client.call_async(req_state)
        rclpy.spin_until_future_complete(self.node, future, timeout_sec=2.0)
        initial_state = future.result().current_state.label
        self.assertIn(initial_state, ['unconfigured', 'inactive', 'active'])

        # 2. Bring node to active state based on initial state
        if initial_state == 'unconfigured':
            self.trigger_transition(get_state_client, change_state_client, Transition.TRANSITION_CONFIGURE, 'inactive')
            self.trigger_transition(get_state_client, change_state_client, Transition.TRANSITION_ACTIVATE, 'active')
        elif initial_state == 'inactive':
            self.trigger_transition(get_state_client, change_state_client, Transition.TRANSITION_ACTIVATE, 'active')

        # 3. Deactivate -> Inactive
        self.trigger_transition(get_state_client, change_state_client, Transition.TRANSITION_DEACTIVATE, 'inactive')

        # 4. Cleanup -> Unconfigured
        self.trigger_transition(get_state_client, change_state_client, Transition.TRANSITION_CLEANUP, 'unconfigured')

        # 5. Shutdown from Unconfigured -> Finalized
        self.trigger_transition(get_state_client, change_state_client, Transition.TRANSITION_UNCONFIGURED_SHUTDOWN, 'finalized')