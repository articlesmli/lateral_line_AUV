#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "rclcpp_lifecycle/lifecycle_publisher.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"
#include <algorithm>

using rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface;

class ProductionControllerNode : public rclcpp_lifecycle::LifecycleNode
{
public:
    ProductionControllerNode() : rclcpp_lifecycle::LifecycleNode("controller_node"), filtered_steering_(0.0)
    {
        // Declare production parameters with default values
        this->declare_parameter<double>("alpha", 0.2);
        this->declare_parameter<double>("max_steering", 0.3);
        this->declare_parameter<double>("surge_velocity", 0.5);
    }

    LifecycleNodeInterface::CallbackReturn on_configure(const rclcpp_lifecycle::State &) override
    {
        RCLCPP_INFO(this->get_logger(), "Configuring controller node...");

        alpha_ = this->get_parameter("alpha").as_double();
        max_steering_ = this->get_parameter("max_steering").as_double();
        surge_velocity_ = this->get_parameter("surge_velocity").as_double();

        // Production Sensor QoS Profile (Best Effort reliability)
        rclcpp::SensorDataQoS sensor_qos;

        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);
        subscription_ = this->create_subscription<std_msgs::msg::Float32MultiArray>(
            "/lateral_line/pressures", sensor_qos,
            std::bind(&ProductionControllerNode::pressureCallback, this, std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(), "Production Controller Node configured with alpha: %.2f", alpha_);
        return LifecycleNodeInterface::CallbackReturn::SUCCESS;
    }

    LifecycleNodeInterface::CallbackReturn on_activate(const rclcpp_lifecycle::State & state) override
    {
        RCLCPP_INFO(this->get_logger(), "Activating controller node...");
        publisher_->on_activate();
        LifecycleNode::on_activate(state);
        return LifecycleNodeInterface::CallbackReturn::SUCCESS;
    }

    LifecycleNodeInterface::CallbackReturn on_deactivate(const rclcpp_lifecycle::State & state) override
    {
        RCLCPP_INFO(this->get_logger(), "Deactivating controller node...");
        publisher_->on_deactivate();
        LifecycleNode::on_deactivate(state);
        return LifecycleNodeInterface::CallbackReturn::SUCCESS;
    }

    LifecycleNodeInterface::CallbackReturn on_cleanup(const rclcpp_lifecycle::State &) override
    {
        RCLCPP_INFO(this->get_logger(), "Cleaning up controller node...");
        publisher_.reset();
        subscription_.reset();
        return LifecycleNodeInterface::CallbackReturn::SUCCESS;
    }

    LifecycleNodeInterface::CallbackReturn on_shutdown(const rclcpp_lifecycle::State &) override
    {
        RCLCPP_INFO(this->get_logger(), "Shutting down controller node...");
        return LifecycleNodeInterface::CallbackReturn::SUCCESS;
    }

private:
    void pressureCallback(const std_msgs::msg::Float32MultiArray::SharedPtr msg)
    {
        // Only process data if the node is actively running
        if (this->get_current_state().label() != "active") {
            return;
        }

        try {
            if (msg->data.empty()) {
                RCLCPP_WARN_THROTTLE(this->get_logger(), *this->get_clock(), 1000, "Received empty pressure array!");
                return;
            }

            float raw_signal = msg->data[0];
            
            // Apply EMA filter
            filtered_steering_ = (alpha_ * raw_signal) + ((1.0 - alpha_) * filtered_steering_);

            auto twist = geometry_msgs::msg::Twist();
            twist.linear.x = surge_velocity_;
            twist.angular.z = std::clamp(filtered_steering_, -max_steering_, max_steering_);
            
            publisher_->publish(twist);
        } 
        catch (const std::exception & e) {
            RCLCPP_ERROR(this->get_logger(), "Exception in pressureCallback: %s", e.what());
        }
    }

    std::shared_ptr<rclcpp_lifecycle::LifecyclePublisher<geometry_msgs::msg::Twist>> publisher_;
    rclcpp::Subscription<std_msgs::msg::Float32MultiArray>::SharedPtr subscription_;
    double filtered_steering_;
    double alpha_;
    double max_steering_;
    double surge_velocity_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ProductionControllerNode>();
    rclcpp::spin(node->get_node_base_interface());
    rclcpp::shutdown();
    return 0;
}