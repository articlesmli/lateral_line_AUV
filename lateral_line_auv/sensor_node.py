import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from visualization_msgs.msg import Marker, MarkerArray
import random

class SensorNode(Node):
    def __init__(self):
        super().__init__('lateral_line_sensor_node')
        self.publisher_ = self.create_publisher(Float32MultiArray, '/lateral_line/pressures', 10)
        self.marker_pub_ = self.create_publisher(MarkerArray, '/visualization_marker_array', 10)
        self.timer = self.create_timer(0.2, self.timer_callback)
        self.get_logger().info('Lateral Line Sensor Node with RViz Markers Initialized.')

    def timer_callback(self):
        pressures = [random.uniform(0.1, 1.0) for _ in range(8)]
        
        msg = Float32MultiArray()
        msg.data = pressures
        self.publisher_.publish(msg)
        
        marker_array = MarkerArray()
        for i, p in enumerate(pressures):
            marker = Marker()
            marker.header.frame_id = 'base_link'
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = 'lateral_line_sensors'
            marker.id = i
            marker.type = Marker.CYLINDER
            marker.action = Marker.ADD
            marker.pose.position.x = 0.5 - (i * 0.1)
            marker.pose.position.y = 0.2 * (i - 3.5)
            marker.pose.position.z = 0.0
            marker.scale.x = 0.05
            marker.scale.y = 0.05
            marker.scale.z = float(p) * 0.5
            marker.color.r = float(p)
            marker.color.g = 0.2
            marker.color.b = 1.0 - float(p)
            marker.color.a = 0.8
            marker_array.markers.append(marker)
            
        self.marker_pub_.publish(marker_array)
        self.get_logger().info(f'Published pressure array & markers, obstacle ~{pressures[0]:.2f}m')

def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()