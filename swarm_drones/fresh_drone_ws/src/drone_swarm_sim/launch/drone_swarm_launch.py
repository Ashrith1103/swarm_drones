from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os

def generate_launch_description():
    pkg_share = os.path.join(os.path.expanduser('~/fresh_drone_ws/install/drone_swarm_sim/share/drone_swarm_sim'))
    world_file = os.path.join(pkg_share, 'worlds', 'worlds.sdf')
    drone_file = os.path.join(pkg_share, 'models', 'drone.sdf')
    
    return LaunchDescription([
        ExecuteProcess(
            cmd=['ign', 'gazebo', '-r', world_file],
            output='screen'
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', '/drone_0', '-name', 'drone_0', '-x', '-2', '-y', '0', '-z', '0.5', '-file', drone_file],
            output='screen',
            additional_env={'GZ_SIM_SYSTEM_PLUGIN_PATH': '/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins'},
            parameters=[{'timeout': 20.0}]  # Increase timeout
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', '/drone_1', '-name', 'drone_1', '-x', '-1', '-y', '0', '-z', '0.5', '-file', drone_file],
            output='screen',
            additional_env={'GZ_SIM_SYSTEM_PLUGIN_PATH': '/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins'},
            parameters=[{'timeout': 10.0}]
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', '/drone_2', '-name', 'drone_2', '-x', '0', '-y', '0', '-z', '0.5', '-file', drone_file],
            output='screen',
            additional_env={'GZ_SIM_SYSTEM_PLUGIN_PATH': '/usr/lib/x86_64-linux-gnu/ign-gazebo-6/plugins'},
            parameters=[{'timeout': 10.0}]
        ),
    ])
