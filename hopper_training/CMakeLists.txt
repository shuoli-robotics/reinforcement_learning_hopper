cmake_minimum_required(VERSION 2.8.3)
project(hopper_training)

find_package(catkin REQUIRED COMPONENTS
  std_msgs
  message_generation
)

add_message_files(
  FILES
  QLearnPoint.msg
  QLearnElement.msg
  QLearnMatrix.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)


catkin_package(
  CATKIN_DEPENDS rospy message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)