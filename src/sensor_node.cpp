#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"
#include "visualization_msgs/msg/marker_array.hpp"
#include <vector>
#include <random>

class SensorNode : public rclcpp::Node
{
public:
    SensorNode() : Node("sensor_node"), num_sensors_(8)
    {
        pressure_pub_ = this->create_publisher<std_msgs::msg::Float32MultiArray>("/lateral_line/pressures", 10);
        marker_pub_ = this->create_publisher<visualization_msgs::msg::MarkerArray>("/lateral_line/markers", 10);
        
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&SensorNode::publishSensors, this));
    }

private:
    void publishSensors()
    {
        // Simulate lateral line pressure values across array
        auto pressure_msg = std_msgs::msg::Float32MultiArray();
        pressure_msg.data.resize(num_sensors_);
        
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_real_distribution<float> dist(0.1f, 1.0f);

        for (int i = 0; i < num_sensors_; ++i) {
            pressure_msg.data[i] = dist(gen);
        }
        pressure_pub_->publish(pressure_msg);

        // Publish RViz2 visualization markers
        visualization_msgs::msg::MarkerArray marker_array;
        for (int i = 0; i < num_sensors_; ++i) {
            visualization_msgs::msg::Marker marker;
            marker.header.frame_id = "base_link";
            marker.header.stamp = this->now();
            marker.ns = "lateral_line";
            marker.id = i;
            marker.type = visualization_msgs::msg::Marker::CYLINDER;
            marker.action = visualization_msgs::msg::Marker::ADD;
            marker.pose.position.x = 0.2 - (i * 0.05);
            marker.pose.position.y = 0.2;
            marker.pose.position.z = 0.0;
            marker.scale.x = 0.02;
            marker.scale.y = 0.02;
            marker.scale.z = pressure_msg.data[i];
            marker.color.r = 0.0;
            marker.color.g = 0.5;
            marker.color.b = 1.0;
            marker.color.a = 0.8;
            marker_array.markers.push_back(marker);
        }
        marker_pub_->publish(marker_array);
    }

    rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr pressure_pub_;
    rclcpp::Publisher<visualization_msgs::msg::MarkerArray>::SharedPtr marker_pub_;
    rclcpp::TimerBase::SharedPtr timer_;
    int num_sensors_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<SensorNode>());
    rclcpp::shutdown();
    return 0;
}
