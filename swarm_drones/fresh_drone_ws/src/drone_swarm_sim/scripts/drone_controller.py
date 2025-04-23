#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
import time

class DroneController(Node):
    def __init__(self):
        super().__init__('drone_controller')
        self.pubs = [
            self.create_publisher(Twist, '/drone_0/cmd_vel', 10),
            self.create_publisher(Twist, '/drone_1/cmd_vel', 10),
            self.create_publisher(Twist, '/drone_2/cmd_vel', 10)
        ]
        # Pickup and drop-off positions
        self.pickups = [(-4, 1, 0.5), (-3, 1, 0.5), (-2, 1, 0.5)]
        self.dropoffs = [(1.5, -1, 0.5), (3, 2.5, 0.5), (4, -3, 0.5)]
        self.packages = [
            self.create_publisher(Empty, '/gz/sim/set_pose/package_0', 10),
            self.create_publisher(Empty, '/gz/sim/set_pose/package_1', 10),
            self.create_publisher(Empty, '/gz/sim/set_pose/package_2', 10)
        ]
        self.timer = self.create_timer(0.1, self.move_drones)

    def move_drones(self):
        for i in range(3):
            # Hover to pickup
            self.get_logger().info(f'Drone {i} moving to pickup...')
            self.move_to(self.pubs[i], *self.pickups[i])
            time.sleep(5)  # Wait to reach pickup
            # "Pick up" package (move it with drone)
            self.move_package(i, *self.pickups[i])
            # Move to drop-off
            self.get_logger().info(f'Drone {i} moving to drop-off...')
            self.move_to(self.pubs[i], *self.dropoffs[i])
            time.sleep(5)  # Wait to reach drop-off
            # "Drop" package
            self.move_package(i, self.dropoffs[i][0], self.dropoffs[i][1], 0.1)
            # Stop drone
            self.move_to(self.pubs[i], 0, 0, 0, stop=True)
            time.sleep(2)  # Wait before next drone

    def move_to(self, pub, x, y, z, stop=False):
        msg = Twist()
        if not stop:
            msg.linear.x = float(x)
            msg.linear.y = float(y)
            msg.linear.z = float(z)
        pub.publish(msg)

    def move_package(self, idx, x, y, z):
        msg = Empty()
        self.packages[idx].publish(msg)  # Placeholder: needs actual pose service

def main():
    rclpy.init()
    node = DroneController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
