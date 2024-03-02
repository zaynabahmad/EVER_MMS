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
        self.rate = rospy.Rate(10)  # 10 Hz
    def move_straight(self, total_distance):
        max_velocity = 2*33.336/0.68035 # max speed of the car
        throttle_value = 1 # throttle to reach max speed
        max_acceleration = 9.24  # max acceleration

    # Calculate the time needed to reach the max speed
        time_to_max_speed = max_velocity / max_acceleration

    # Calculate the distance covered during acceleration
        distance_during_acceleration = 0.5 * max_acceleration * (time_to_max_speed ** 2)

    # If the distance to accelerate is greater than the total distance, adjust it
        distance_to_accelerate = min(distance_during_acceleration, total_distance)

    # Calculate the time needed to accelerate
        time_to_accelerate = time_to_max_speed

    # Calculate the time needed to cover the remaining distance at max speed
        time_with_constant_vel = (total_distance - distance_to_accelerate) / max_velocity

    # Total time needed for the movement
        total_time = time_to_accelerate + time_with_constant_vel

    # Create a Twist message to set linear velocity
        move_cmd = Float64()

    # Accelerate
        start_time = rospy.get_time()
        while (not rospy.is_shutdown()) and (rospy.get_time() - start_time) < time_to_accelerate:
            move_cmd.data = throttle_value
            self.cmd_vel_pub.publish(move_cmd)
            rospy.loginfo("Accel Time: {} | start time {} ## ".format((rospy.get_time() - start_time) , start_time ))
            self.rate.sleep()

    # Maintain max speed
        start_time = rospy.get_time()
        while (not rospy.is_shutdown()) and (rospy.get_time() - start_time) < time_with_constant_vel:
            move_cmd.data = throttle_value
            self.cmd_vel_pub.publish(move_cmd)
            rospy.loginfo("Constant Vel Time: {} | start time {} ## ".format((rospy.get_time() - start_time) , start_time))
            self.rate.sleep()

    # Decelerate
        start_time = rospy.get_time()
        while (not rospy.is_shutdown()) and (rospy.get_time() - start_time) < time_to_accelerate:
            move_cmd.data = 0.0  # Decelerate by setting throttle to 0
            self.cmd_vel_pub.publish(move_cmd)
            rospy.loginfo("Decel Time: {} | start time {} ## ".format((rospy.get_time() - start_time) , start_time))
            self.rate.sleep()

    # Stop the car by publishing a brake command
            brake_cmd = Float64()
            brake_cmd.data = 1.0  # Adjust as needed
            self.brakes_pub.publish(brake_cmd)
            self.rate.sleep()


if __name__ == '__main__':
    try:
        controller = AutonomousCarController()
        # Move the car straight for 75 meters
        controller.move_straight(75.0)
        rospy.spin()

    except rospy.ROSInterruptException:
        pass