#!/usr/bin/env python3
# license removed for brevity
import rospy
import time
from std_msgs.msg import Float64

def move_with_brakes():
    velocity = 1.0
    brake = 1
    pub = rospy.Publisher('/cmd_vel', Float64, queue_size=10)
    pub_2 = rospy.Publisher('/brakes', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    for i in range(100):
        rospy.loginfo(velocity)
        pub.publish(velocity)
        rate.sleep()
    #time.sleep(10)
    #rospy.loginfo("braaaaaake")
    #rospy.loginfo(brake)
    #pub_2.publish(brake)
    #velocity = 0
    #pub.publish(velocity)
    rospy.is_shutdown()

def brrr():
    velocity = 0.1
    pub = rospy.Publisher('/cmd_vel', Float64, queue_size=10)
    pub_2 = rospy.Publisher('/brakes', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    rospy.loginfo(velocity)
    pub_2.publish(0)
    pub.publish(velocity)
    rospy.is_shutdown()

if __name__ == '__main__':
    try:
        move_with_brakes()
    except rospy.ROSInterruptException:
        pass