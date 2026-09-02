# Bio-Inspired Lateral Line AUV Simulation

A ROS 2 Humble and Gazebo Sim project implementing a bio-inspired lateral line sensor array and reactive navigation controller for an Autonomous Underwater Vehicle (AUV).

## System Overview

This package simulates an underwater vehicle equipped with a simulated lateral line pressure sensing system. It bridges physics simulation in Gazebo Sim (Garden) with real-time visualization in RViz2, featuring reactive obstacle avoidance and custom telemetry nodes.

* **`sensor_node`**: Processes pressure telemetry and publishes marker arrays (`/lateral_line/markers`) and pressure data (`/lateral_line/pressures`).
* **`controller_node`**: Listens to sensor inputs, applies exponential moving average (EMA) filtering, and computes steering commands (`/cmd_vel`).
* **`sim.launch.py`**: Orchestrates the concurrent startup of Gazebo Sim, robot state publishing, and RViz2 visualization.

## Tech Stack

* **ROS 2 Humble**
* **Gazebo Sim (Garden)**
* **RViz2**
* **Python / Xacro / URDF**

## Quick Start Guide

1. Clone the repository into your ROS 2 workspace source directory:
   ```bash
   cd ~/ros2_ws/src
   git clone [https://github.com/articlesmli/lateral_line_AUV.git](https://github.com/articlesmli/lateral_line_AUV.git)
