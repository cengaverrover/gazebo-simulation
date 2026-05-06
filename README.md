# Cengaver Simulation Model
This repository contains the files and instructions on how to run and control the cengaver rover simulation model.

Each version of the rover is designated by its branch codename (e.g Cengaver, Barsoom, etc.). Check to see if you're on the right branch. (current branch: Atom)

# Prerequisites
Make sure you have:

1. ROS Humble
2. Gazebo Ignition Fortress (6.17.0 or 6.X.X)
3. Ubuntu 22.04 (Not required but highly recommended)

Install rest of the required packages via this command

```bash
sudo apt update && sudo apt install git \
npm \
curl \
ros-humble-robot-state-publisher \
ros-humble-joint-state-publisher \
ros-humble-foxglove-bridge \
ros-humble-ros-gz-bridge \
ros-humble-slam-toolbox \
ros-humble-pointcloud-to-laserscan
```

# Installation
Clone this repository and continue with Usage
```bash
git clone https://github.com/cengaverrover/gazebo-simulation.git

cd gazebo-simulation
```
# Usage
Command Description |  Command
--- | --- |
Pure Simulation | `ign gazebo <insert-world-name>.sdf`
Simulation + ROS + Foxglove (Manual Control, No SLAM) | `ros2 launch ./sim_foxglove.launch.py`

# Creating Custom Worlds
It is preferred to use Bullet as the physics engine.

Also, ensure your world uses the plugins below,
```xml
<plugin filename="libignition-gazebo-physics-system.so"
                name="ignition::gazebo::systems::Physics"/>
<plugin filename="libignition-gazebo-user-commands-system.so"
        name="ignition::gazebo::systems::UserCommands"/>
<plugin filename="libignition-gazebo-scene-broadcaster-system.so"
        name="ignition::gazebo::systems::SceneBroadcaster"/>
<plugin filename="libignition-gazebo-sensors-system.so"
    name="ignition::gazebo::systems::Sensors"/>
```

All of the worlds here should have these, they can be good tutorials on how to make simulation worlds.