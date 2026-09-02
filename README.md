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
   
---

## It is production-ready for an advanced simulation environment, but deploying it to physical AUV hardware requires several critical additions to ensure absolute safety and reliability in the field. What is Missing for Real-World Deployment:

- **ROS 2 Lifecycle Management (rclcpp_lifecycle):** Real robots require managed nodes with distinct states (Unconfigured, Inactive, Active, Finalized) so ground control can safely configure and activate systems sequentially.

- **Hardware Abstraction Layer (ros2_control or custom drivers):** The current simulation uses a dummy sensor node and standard Twist commands. Production hardware requires physical serial/UDP drivers, thruster allocation matrices, and actual sensor feedback integration.

- **Watchdog & Safety Interrupters:** A physical deployment needs a dedicated safety node to monitor node heartbeats and trigger an immediate emergency stop (/safety_stop) if communication drops or sensor data freezes.

- **Diagnostics & Health Monitoring:** Integrating diagnostic_updater to stream CPU loads, internal temperature, and sensor health metrics back to the surface station.

- **CI/CD Automation:** Setting up a GitHub Actions workflow to automatically run your Google Test suite and build checks on every push to catch regressions early

