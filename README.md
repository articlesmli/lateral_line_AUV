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

### It is production-ready for an advanced simulation environment, but deploying it to physical AUV hardware requires several critical additions to ensure absolute safety and reliability in the field. What is Missing for Real-World Deployment:

- **ROS 2 Lifecycle Management (rclcpp_lifecycle):** Real robots require managed nodes with distinct states (Unconfigured, Inactive, Active, Finalized) so ground control can safely configure and activate systems sequentially.

- **Hardware Abstraction Layer (ros2_control or custom drivers):** The current simulation uses a dummy sensor node and standard Twist commands. Production hardware requires physical serial/UDP drivers, thruster allocation matrices, and actual sensor feedback integration.

- **Watchdog & Safety Interrupters:** A physical deployment needs a dedicated safety node to monitor node heartbeats and trigger an immediate emergency stop (/safety_stop) if communication drops or sensor data freezes.

- **Diagnostics & Health Monitoring:** Integrating diagnostic_updater to stream CPU loads, internal temperature, and sensor health metrics back to the surface station.

- **CI/CD Automation:** Setting up a GitHub Actions workflow to automatically run your Google Test suite and build checks on every push to catch regressions early


# Lateral Line AUV

A ROS 2 package engineered for Autonomous Underwater Vehicle (AUV) systems, featuring a fully managed lifecycle controller and automated integration test suites.

## System Architecture

The core of this package is **`controller_node`**, implemented as a managed **ROS 2 Lifecycle Node**. This ensures safe initialization, resource allocation, and controlled degradation or shutdown during mission execution.

**Supported Lifecycle States & Transitions:**

* **Unconfigured**: Initial state upon node startup.
* **Inactive**: Configured state where hardware resources are allocated but execution loops are dormant (reached via `Configure`).
* **Active**: Fully operational state where controllers and actuators execute (reached via `Activate`).
* **Finalized**: Terminal state after clean shutdown sequences.

## Automated Testing Suite

System robustness is verified using **`launch_testing`** and **`pytest`** integration tests (`test_lifecycle_launch.py`). The test runner dynamically inspects initial node states, handles adaptation paths, triggers forward transitions (Configure, Activate), reverse transitions (Deactivate, Cleanup), and terminal shutdown protocols while validating responses via ROS 2 services (`/get_state` and `/change_state`).

## Repository Structure

```text
lateral_line_auv/
├── src/                        # Lifecycle controller node source implementation
├── test/                       # Launch testing and pytest lifecycle integration scripts
├── CMakeLists.txt              # Build configuration with test hooks enabled
└── package.xml                 # ROS 2 package dependencies (lifecycle_msgs, launch_ros, etc.)

```

## Build and Installation

Place this package inside your ROS 2 workspace source directory:

```bash
cd ~/ros2_ws/src
# (If cloned already, navigate to package root)
cd lateral_line_auv

```

Build the package with testing options enabled:

```bash
cd ~/ros2_ws
colcon build --packages-select lateral_line_auv --cmake-args -DBUILD_TESTING=ON

```

## Running Tests

Execute the complete lifecycle integration test suite:

```bash
colcon test --packages-select lateral_line_auv --ctest-args -R test_lifecycle_launch
colcon test-result --verbose

```
