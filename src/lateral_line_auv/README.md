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

---

**Commands to Commit and Push to GitHub**

Run these commands in your terminal to update your GitHub repository with the comprehensive project documentation:

```bash
cd ~/ros2_ws/src/lateral_line_auv
git add README.md
git commit -m "Add comprehensive project README covering architecture, lifecycle flow, and test suite"
git push origin main

```