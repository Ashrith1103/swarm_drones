# swarm_drones
In terminal 1 run:

cd ~/fresh_drone_ws
rm -rf build install log
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
ros2 launch drone_swarm_sim drone_swarm_launch.py

in terminal 2 run:

cd ~/fresh_drone_ws
pyenv shell system
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run drone_swarm_sim drone_controller.py
