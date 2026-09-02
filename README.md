# Lateral Line AUV

A production-grade ROS 2 Humble C++ package engineered for Autonomous Underwater Vehicle (AUV) systems, featuring a managed lifecycle controller and automated integration test suites.

## System Architecture

The core of this repository is **`controller_node`**, implemented as a managed **ROS 2 Lifecycle Node** (`rclcpp_lifecycle`) to ensure deterministic state management, resource allocation, and fault-safe handling.

* **Managed States:** Explicitly handles `Unconfigured`, `Inactive`, `Active`, and `Finalized` transitions.
* **Service Interfaces:** Exposes standard lifecycle management services (`/get_state`, `/change_state`).
* **Modular Components:** Integrates complementary C++ nodes, parameter configuration via YAML (`controller_params.yaml`), and simulation launch scripts (`sim.launch.py`).

## Automated Testing Suite

System robustness and state-machine compliance are verified using **`launch_testing`** and **`pytest`** integration tests (`test_lifecycle_launch.py`). The test runner programmatically validates full operational loops—from dynamic startup discovery through activation, deactivation, cleanup, and terminal shutdown.

## Repository Structure

```text
lateral_line_auv/
├── config/                   # Runtime parameter files (YAML configurations)
│   └── controller_params.yaml
├── lateral_line_auv/         # Python module package directory
│   ├── __init__.py           # Python package initializer
│   ├── controller_node.py    # Python controller node implementation
│   └── sensor_node.py        # Python sensor node implementation
├── launch/                   # Launch orchestration scripts
│   └── sim.launch.py         # Simulation launch pipeline script
├── resource/                 # ROS 2 package resource index markers
│   └── lateral_line_auv
├── src/                      # C++ source code files and logic implementation
│   ├── controller_node.cpp   # C++ lifecycle controller node source
│   ├── create_publisher      # Helper publisher implementation component
│   ├── create_subscription   # Helper subscriber implementation component
│   └── sensor_node.cpp       # C++ sensor node source implementation
├── test/                     # Unit and integration test suites
│   ├── test_controller.cpp   # C++ controller test implementation
│   └── test_lifecycle_launch.py # Automated launch testing and pytest suite
├── urdf/                     # Unified Robot Description Format models
│   └── auv.urdf.xacro        # AUV robot description and xacro macros
├── CMakeLists.txt            # CMake build configuration script with test hooks
├── package.xml               # ROS 2 package manifest and dependency declarations
├── .gitignore                # Git exclusion rules for build artifacts and caches
└── README.md                 # Centralized project documentation and architecture guide

```

## Build and Installation

1. Navigate to your ROS 2 workspace source directory and clone or place the package:
```bash
cd ~/ros2_ws/src

```


2. Build the package with testing options enabled using `colcon`:
```bash
cd ~/ros2_ws
colcon build --packages-select lateral_line_auv --cmake-args -DBUILD_TESTING=ON

```



## Running the Test Suite

Execute the automated lifecycle integration tests to verify node behavior and state transitions:

```bash
colcon test --packages-select lateral_line_auv --ctest-args -R test_lifecycle_launch
colcon test-result --verbose

```
