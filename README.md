# Lateral Line AUV Simulation

A production-grade ROS 2 Humble C++ (`ament_cmake`) architecture for an Autonomous Underwater Vehicle (AUV) simulation. This project processes simulated lateral line pressure arrays through an exponential moving average (EMA) filter and publishes optimized velocity commands (`geometry_msgs/msg/Twist`).

## Features

- **High-Performance C++ Architecture:** Refactored from Python for production-grade speed, exception safety, and deterministic memory management.
- **Dynamic Configuration:** Live-tunable parameters (`alpha`, `max_steering`, `surge_velocity`) via YAML configuration files.
- **Optimized QoS Profiles:** Leverages `rclcpp::SensorDataQoS` for robust, low-latency sensor data handling.
- **Unified Launch System:** Spin up the entire simulation pipeline with a single launch file.
- **Automated Unit Testing:** Integrated Google Test (`gtest`) suite validating core signal processing and mathematical constraints.

---

## Prerequisites

- **OS:** Ubuntu 22.04 LTS
- **Middleware:** ROS 2 Humble Hawksbill
- **Build Tool:** Colcon & CMake

---

## Installation & Build

1. Clone or place this package inside your ROS 2 workspace `src/` directory:
   ```bash
   cd ~/ros2_ws/src
   # (Assuming lateral_line_auv is already located here)
