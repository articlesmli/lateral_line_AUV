import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist

class ControllerNode(Node):
    def __init__(self):
        super().__init__('auv_nav_controller')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/lateral_line/pressures',
            self.pressure_callback,
            10
        )
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Exponential Moving Average (EMA) filter configurations
        self.alpha = 0.3
        self.filtered_steering = 0.0
        
        self.get_logger().info('AUV Navigation Controller Node with EMA Filter Initialized.')

    def pressure_callback(self, msg):
        if not msg.data:
            return
            
        left_pressure = sum(msg.data[:len(msg.data)//2])
        right_pressure = sum(msg.data[len(msg.data)//2:])
        raw_steering = (right_pressure - left_pressure) * 0.5
        
        # Apply smoothing filter to prevent high-frequency yaw twitching
        self.filtered_steering = (self.alpha * raw_steering) + ((1.0 - self.alpha) * self.filtered_steering)
        
        twist = Twist()
        twist.linear.x = 1.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = float(self.filtered_steering)
        
        self.publisher_.publish(twist)
        self.get_logger().warn(f'Hazard detected! Filtered steering (angular.z): {self.filtered_steering:.2f} rad/s')

def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()