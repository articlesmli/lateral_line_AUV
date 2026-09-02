cmake_minimum_required(VERSION 3.8)
project(lateral_line_auv)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)

add_executable(sensor_node src/sensor_node.cpp)
ament_target_dependencies(sensor_node rclcpp std_msgs visualization_msgs)

add_executable(controller_node src/controller_node.cpp)
ament_target_dependencies(controller_node rclcpp rclcpp_lifecycle std_msgs geometry_msgs)

install(TARGETS
  sensor_node
  controller_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch config urdf resource
  DESTINATION share/${PROJECT_NAME}
)

ament_package()

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  find_package(ament_cmake_pytest REQUIRED)
  find_package(lifecycle_msgs REQUIRED)
  
  ament_add_gtest(test_controller test/test_controller.cpp)
  target_include_directories(test_controller PRIVATE include)
  ament_target_dependencies(test_controller rclcpp lifecycle_msgs)

  ament_add_pytest_test(test_lifecycle_launch test/test_lifecycle_launch.py)
endif()