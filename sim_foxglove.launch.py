from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
import os

# This launch file launches a simulation that publishes all its data to ROS and Foxglove
# Used for testing foxglove controls or reading flawless data
# Author: Dena Vafadar Afshar

def generate_launch_description():

    root = os.getcwd()

    world = LaunchConfiguration('world')

    urdf = os.path.join(root, "assets", "atom_full.urdf")
    bridge_config = os.path.join(root, "configs", "ros-gz-bridge.yaml")

    return LaunchDescription([
        
        # Default world selection
        DeclareLaunchArgument(
            'world',
            default_value='flat_world.sdf'
        ),

        # Launches simulation
        ExecuteProcess(
            cmd=['ign', 'gazebo', world],
            cwd=root,
            output='screen'
        ),

        # Robot and joint state publishers, needed by foxglove
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            arguments=[urdf],
            parameters=[{'use_sim_time': True}],
            output='screen'
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            parameters=[
                {'use_sim_time': True},
                {
                    'robot_description': ParameterValue(
                        Command(['cat ', urdf]),
                        value_type=str
                    )
                }
            ],
            output='screen'
        ),

        # ros->foxglove bridge
        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            output='screen'
        ),

        # gz->ros bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{
                'config_file': bridge_config
            }],
            cwd=os.path.join(root, "configs"),
            output='screen'
        ),

        # URDF file host, used by foxglove
        ExecuteProcess(
            cmd=[
                'npx', 'http-server',
                'assets',
                '-p', '8000',
                '--cors'
            ],
            cwd=root,
            output='screen'
        ),

        # Fixes the lidar topic name mismatch between the URDF and SDF files.
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '0','0','0','0','0','0',
                'atom/atom_body/Lidar_Link',
                'atom/atom_body/Lidar_Link/gpu_lidar'
            ],
        ),

        # TF publisher
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '0', '0', '0', #xyz
                '0', '0', '0', #rpy
                'atom',
                'atom/atom_body/Lidar_Link/gpu_lidar'
            ],
            output='screen'
        ),
    ])