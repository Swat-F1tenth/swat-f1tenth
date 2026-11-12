import rclpy
from rclpy.node import Node
import numpy as np
import math
from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped

class SimpleTest(Node):
    def __init__(self):
        super().__init__('simpletest_node')
        #Making subscriber and publisher same as follow the gap

        self.laser_sub = self.create_subscription(LaserScan, '/scan', self.laserprocess, 10) #Self.XXXX always seems to refer to upcoming function definition
        self.move = self.create_publisher(AckermannDriveStamped, '/drive', 10)

        #Defining parameters -- seems like parameters are all caps by convention if not necessity
        #e.g. self.CAR_WIDTH = 0.33  
        self.MAX_LIDAR_DIST = 5.0 #meters
        self.MIN_LIDAR_DIST = 0.1

    def laserprocess(self, scan_msg): #Simple node to find the angle of the nearest object and steer in that direction
        ranges=np.array(scan_msg.ranges)
        angle_min = scan_msg.angle_min
        angle_max = scan_msg.angle_max
        angle_inc = scan_msg.angle_increment

        num_indices = ((angle_max-angle_min)/angle_inc)

        ranges_clipped = np.clip(ranges, self.MIN_LIDAR_DIST, self.MAX_LIDAR_DIST)
        min_value = np.min()
        target = np.argmin(ranges_clipped)

        angle_steer = math.degrees((target-(num_indices/2))*angle_inc)
        speed_drive = ((min_value**-1)*0.1)
        if speed_drive > 2:
            speed_drive = 2

        drive_msg = AckermannDriveStamped()
        drive_msg.drive.steering_angle = float(angle_steer)
        drive_msg.drive.speed = float(speed_drive)
        self.drive_pub.publish(drive_msg)

    def estop(self):
        stop_msg = AckermannDriveStamped()
        self.drive_pub.publish(stop_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SimpleTest()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.estop()
        node.destroy_node()
        rclpy.shutdown()












        