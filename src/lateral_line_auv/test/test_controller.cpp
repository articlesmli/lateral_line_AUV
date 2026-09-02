#include <gtest/gtest.h>
#include "rclcpp/rclcpp.hpp"
#include "lifecycle_msgs/msg/transition.hpp"
#include "lifecycle_msgs/srv/change_state.hpp"
#include "lifecycle_msgs/srv/get_state.hpp"

class LifecycleIntegrationTest : public ::testing::Test {
protected:
    static void SetUpTestCase() {
        rclcpp::init(0, nullptr);
    }

    static void TearDownTestCase() {
        rclcpp::shutdown();
    }

    void SetUp() override {
        node_ = rclcpp::Node::make_shared("test_lifecycle_client");
    }

    rclcpp::Node::SharedPtr node_;
};

TEST_F(LifecycleIntegrationTest, CheckLifecycleServicesExist) {
    auto get_state_client = node_->create_client<lifecycle_msgs::srv::GetState>("/controller_node/get_state");
    auto change_state_client = node_->create_client<lifecycle_msgs::srv::ChangeState>("/controller_node/change_state");

    // Ensure the lifecycle service servers are active (requires the node to be running)
    // Note: Run this test alongside your launch file or within a launch-based test framework.
    EXPECT_TRUE(get_state_client->wait_for_service(std::chrono::seconds(1)));
    EXPECT_TRUE(change_state_client->wait_for_service(std::chrono::seconds(1)));
}