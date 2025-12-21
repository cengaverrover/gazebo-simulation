# Cengaver Simulation Model
This repository contains the files and instructions on how to run and control the cengaver rover simulation model.

Each version of the rover is designated by its branch codename (e.g Cengaver, Barsoom, etc.). Check to see if you're on the right branch.

# Prerequisites
Make sure you have:

1. ROS Humble
2. Gazebo Ignition Fortress (6.17.0 or 6.X.X)
3. Ubuntu 22.04 (Not required but recommended)
4. git (authenticated via `gh`, because this repo is private)
# Installation
The cengaver model uses two libraries that need to be downloaded/built: ArmPlugin and BodyPlugin. x86_64 and aarch64(armv8) versions are released by default. But if you have a different architecture, you can build these from their repositories .

[gazebo-arm-plugin](https://github.com/cengaverrover/gazebo-arm-plugin)

[gazebo-body-plugin](https://github.com/cengaverrover/gazebo-body-plugin)

Once done, you can clone this repository and continue with Usage
```bash
git clone https://github.com/cengaverrover/gazebo-simulation.git

cd gazebo-simulation
```
# Usage
You can use
```bash
ign gazebo <test-world>.sdf #Replace with actual world names
```
to display the simulations.


# Using Model for Custom Worlds
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

All of the examples shown here shold these, so they can be good examples