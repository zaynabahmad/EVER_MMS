#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

class AutonomousCarController:
    def __init__(self):
        rospy.init_node('autonomous_car_controller', anonymous=True)

        # Initialize publishers for cmd_vel and brakes topics
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Float64 , queue_size=10)
        self.brakes_pub = rospy.Publisher('/brakes', Float64, queue_size=10)

        # Set the rate 
        self.rate = rospy.Rate(5)  # 10 Hz

    def move_straight(self, total_distance):
        # Define the linear velocity for moving straight
        linear_velocity = 1  # adjust as needed

        actual_velocity= 28 

        # Calculate the time needed to cover the specified distance

        time_with_constant_vel = total_distance / actual_velocity
        time_to_accerelate = (actual_velocity)/ 4.41 # get the distance to accerelate  and minus it from total distance 
        time_to_move = time_with_constant_vel + time_to_accerelate

        # Create a Twist message to set linear velocity
        move_cmd = Float64()
        move_cmd.data = linear_velocity

        # Publish the command to move straight
        start_time = rospy.get_time()
        while (not rospy.is_shutdown()) and (rospy.get_time() - start_time) < time_to_move:
            throttle_value = Float64()
            throttle_value.data = 0.56
            self.cmd_vel_pub.publish(throttle_value)
            rospy.loginfo(time_to_move)
            rospy.loginfo(rospy.get_time() - start_time)
            
            self.rate.sleep()

        # Stop the car by publishing a brake command
        brake_cmd = Float64()
        brake_cmd.data = 1
        self.cmd_vel_pub.publish(0.0)
        self.brakes_pub.publish(brake_cmd)
        self.cmd_vel_pub.publish(0)
        self.rate.sleep()


if __name__ == '__main__':
    try:
        controller = AutonomousCarController()
        # Move the car straight for 75 meters
        controller.move_straight(75.0) # 1 meter for the dec 
        rospy.spin()

    except rospy.ROSInterruptException:
        pass
