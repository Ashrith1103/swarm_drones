#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench
from std_msgs.msg import Empty
import time
import numpy as np

class DroneController(Node):
    def __init__(self):
        super().__init__('drone_controller')
        self.pubs = [
            self.create_publisher(Wrench, '/drone_0/apply_force', 10),
            self.create_publisher(Wrench, '/drone_1/apply_force', 10),
            self.create_publisher(Wrench, '/drone_2/apply_force', 10)
        ]
        self.packages = [
            self.create_publisher(Empty, '/gz/sim/set_pose/package_0', 10),
            self.create_publisher(Empty, '/gz/sim/set_pose/package_1', 10),
            self.create_publisher(Empty, '/gz/sim/set_pose/package_2', 10)
        ]
        # Pickup and drop-off positions
        self.pickups = [(-4, 1, 0.5), (-3, 1, 0.5), (-2, 1, 0.5)]
        self.dropoffs = [(1.5, -1, 0.5), (3, 2.5, 0.5), (4, -3, 0.5)]
        self.positions = [(-4, 0, 0.5), (-3, 0, 0.5), (-2, 0, 0.5)]  # Track drone positions
        self.timer = self.create_timer(0.1, self.move_drones)
        self.step = 0
        self.state = ['pickup'] * 3  # Track state per drone

    def move_drones(self):
        if self.step >= 3:
            return  # Stop after all drones complete
        i = self.step
        wrench = Wrench()
        if self.state[i] == 'pickup':
            target = self.pickups[i]
            self.get_logger().info(f'Drone {i} moving to pickup {target}...')
        else:
            target = self.dropoffs[i]
            self.get_logger().info(f'Drone {i} moving to drop-off {target}...')
        
        dx, dy, dz = target[0] - self.positions[i][0], target[1] - self.positions[i][1], target[2] - self.positions[i][2]
        wrench.force.x = dx * 2.0  # Proportional control
        wrench.force.y = dy * 2.0
        wrench.force.z = 5.0 + dz * 2.0  # Base lift + correction
        self.pubs[i].publish(wrench)

        # Update position (simplified, assumes movement)
        self.positions[i] = (
            self.positions[i][0] + dx * 0.01,
            self.positions[i][1] + dy * 0.01,
            self.positions[i][2] + dz * 0.01
        )

        # Check if close to target
        if np.linalg.norm([dx, dy, dz]) < 0.1:
            if self.state[i] == 'pickup':
                self.get_logger().info(f'Drone {i} picking up package...')
                self.move_package(i, *self.pickups[i])
                self.state[i] = 'dropoff'
            else:
                self.get_logger().info(f'Drone {i} dropping off package...')
                self.move_package(i, self.dropoffs[i][0], self.dropoffs[i][1], 0.1)
                self.state[i] = 'done'
                self.step += 1
                # Stop drone
                wrench.force.x = 0.0
                wrench.force.y = 0.0
                wrench.force.z = 5.0  # Hover
                self.pubs[i].publish(wrench)

    def move_package(self, idx, x, y, z):
        msg = Empty()
        self.packages[idx].publish(msg)  # Placeholder: needs pose service

def main():
    rclpy.init()
    node = DroneController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
