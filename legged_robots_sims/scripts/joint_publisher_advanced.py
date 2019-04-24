import rospy
from std_msgs.msg import String
from xpp_msgs.msg import RobotStateCartesian, RobotStateJoint
from std_msgs.msg import Float64
"""
[xpp_msgs/RobotStateCartesian]
duration time_from_start
xpp_msgs/State6d base
  geometry_msgs/Pose pose
    geometry_msgs/Point position
      float64 x
      float64 y
      float64 z
    geometry_msgs/Quaternion orientation
      float64 x
      float64 y
      float64 z
      float64 w
  geometry_msgs/Twist twist
    geometry_msgs/Vector3 linear
      float64 x
      float64 y
      float64 z
    geometry_msgs/Vector3 angular
      float64 x
      float64 y
      float64 z
  geometry_msgs/Accel accel
    geometry_msgs/Vector3 linear
      float64 x
      float64 y
      float64 z
    geometry_msgs/Vector3 angular
      float64 x
      float64 y
      float64 z
xpp_msgs/StateLin3d[] ee_motion
  geometry_msgs/Point pos
    float64 x
    float64 y
    float64 z
  geometry_msgs/Vector3 vel
    float64 x
    float64 y
    float64 z
  geometry_msgs/Vector3 acc
    float64 x
    float64 y
    float64 z
geometry_msgs/Vector3[] ee_forces
  float64 x
  float64 y
  float64 z
bool[] ee_contact
"""
"""
[xpp_msgs/RobotStateJoint]
duration time_from_start
xpp_msgs/State6d base
  geometry_msgs/Pose pose
    geometry_msgs/Point position
      float64 x
      float64 y
      float64 z
    geometry_msgs/Quaternion orientation
      float64 x
      float64 y
      float64 z
      float64 w
  geometry_msgs/Twist twist
    geometry_msgs/Vector3 linear
      float64 x
      float64 y
      float64 z
    geometry_msgs/Vector3 angular
      float64 x
      float64 y
      float64 z
  geometry_msgs/Accel accel
    geometry_msgs/Vector3 linear
      float64 x
      float64 y
      float64 z
    geometry_msgs/Vector3 angular
      float64 x
      float64 y
      float64 z
sensor_msgs/JointState joint_state
  std_msgs/Header header
    uint32 seq
    time stamp
    string frame_id
  string[] name
  float64[] position
  float64[] velocity
  float64[] effort
bool[] ee_contact
"""
class JointPub(object):
    def __init__(self):

        rospy.Subscriber("/xpp/joint_mono_des", RobotStateJoint, self.joint_mono_des_callback)
        self.publishers_array = []
        self._haa_joint_pub = rospy.Publisher('/monoped/haa_joint_position_controller/command', Float64, queue_size=1)
        self._hfe_joint_pub = rospy.Publisher('/monoped/hfe_joint_position_controller/command', Float64, queue_size=1)
        self._kfe_joint_pub = rospy.Publisher('/monoped/kfe_joint_position_controller/command', Float64, queue_size=1)
        
        self.publishers_array.append(self._haa_joint_pub)
        self.publishers_array.append(self._hfe_joint_pub)
        self.publishers_array.append(self._kfe_joint_pub)

    def joint_mono_des_callback(self, msg):
        rospy.loginfo(str(msg.joint_state.position))

        self.move_joints(msg.joint_state.position)

    def move_joints(self, joints_array):

        i = 0
        for publisher_object in self.publishers_array:
          joint_value = Float64()
          joint_value.data = joints_array[i]
          rospy.loginfo(str(joint_value))
          publisher_object.publish(joint_value)
          i += 1


    def start_loop(self, rate_value = 2.0):
        rospy.loginfo("Start Loop")
        pos1 = [0.0,1.57,-1.57]
        pos2 = [0.0,0.0,0.0]
        position = "pos1"
        rate = rospy.Rate(rate_value)
        while not rospy.is_shutdown():
          if position == "pos1":
            self.move_joints(pos1)
            position = "pos2"
          else:
            self.move_joints(pos2)
            position = "pos1"
          rate.sleep()


if __name__=="__main__":
    rospy.init_node('joint_publisher_node')
    joint_publisher = JointPub()
    rate_value = 2.0
    joint_publisher.start_loop(rate_value)