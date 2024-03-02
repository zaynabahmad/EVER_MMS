#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry 
from time import * 


def move_straight():
    rospy.init_node('straight_publisher', anonymous=True)
    

    # Publisher for cmd_vel
    cmd_vel_pub = rospy.Publisher('/cmd_vel', Float64, queue_size=10)
    
    # Publisher for steering angle
    steering_angle_pub = rospy.Publisher('/SteeringAngle', Float64, queue_size=10)
    
    #publisher for the brakes 
    brakes_pub = rospy.Publisher('/brakes',Float64,queue_size = 10)

    rate = rospy.Rate(10)  # 10 Hz

    # Set the linear and angular velocity for circular motion
    velocity = 0.03  # adjust as needed
    brakes = 1.0
   # angular_velocity = 0.5  # adjust as needed

    while not rospy.is_shutdown():
        # Publish Twist message to cmd_vel topic

        cmd_vel_msg = Float64()
        cmd_vel_msg.data= velocity
        cmd_vel_pub.publish(cmd_vel_msg)
        
        sleep(4)

        # Publish Float32 message to steering_angle topic
        steering_angle_msg = Float64()
        brakes_msg = Float64()
        for i in range (30,-5,-5):
            steering_angle_msg.data =i  # set the desired steering angle in degrees
            steering_angle_pub.publish(steering_angle_msg)
            sleep(0.5)
        brakes_msg.data=brakes
        brakes_pub.publish(brakes_msg)
        sleep(2)
        brakes_msg.data=0
        brakes_pub.publish(brakes_msg)        
        for i in range (-30,5,5):
            steering_angle_msg.data =i  # set the desired steering angle in degrees
            steering_angle_pub.publish(steering_angle_msg)
            sleep(0.5)


        rate.sleep()


if __name__ == '__main__':
    try:
        move_straight()
    except rospy.ROSInterruptException:
        pass
