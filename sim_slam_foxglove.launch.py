from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
import os

def generate_launch_description():

    root = os.getcwd()

    world = LaunchConfiguration('world')

    urdf = os.path.join(root, "assets", "atom_full.urdf")
    bridge_config = os.path.join(root, "configs", "ros-gz-bridge.yaml")
    slam_config = os.path.join(root, "configs", "slam_toolbox_mapper_params_online_async.yaml")

    return LaunchDescription([

        DeclareLaunchArgument(
            'world',
            default_value='flat_world.sdf'
        ),

        ExecuteProcess(
            cmd=['ign', 'gazebo', world],
            cwd=root,
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            arguments=[urdf],
            parameters=[{'use_sim_time': True}],
            remappings=[
                ('/joint_states', '/rover/joint_states'),
                ('/robot_description', '/rover/robot_description')
            ],
            output='screen'
        ),

        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            output='screen'
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            parameters=[{
                'config_file': bridge_config
            }],
            cwd=os.path.join(root, "configs"),
            output='screen'
        ),

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

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '0','0','0','0','0','0',
                'atom/atom_body/Lidar_Link',
                'atom/atom_body/Lidar_Link/gpu_lidar'
            ],
        ),

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

        # For lidar, the simulation creates pointclouds, but slam_toolbox requires laserscan, this is a simple converter
        Node(
            package='pointcloud_to_laserscan',
            executable='pointcloud_to_laserscan_node',
            name='pointcloud_to_laserscan',
            remappings=[
                ('scan', '/rover/lidar/scan'),
            ],
            parameters=[{
                'cloud_in': '/rover/lidar/points',
                'target_frame': 'Lidar_Link',
                'min_height': -0.1,
                'max_height': 0.1,
                'angle_min': -3.14159,
                'angle_max': 3.14159,
                'angle_increment': 0.0058,
                'scan_time': 0.1,
                'range_min': 0.1,
                'range_max': 10.0,
                'use_sim_time': True,
            }]
        ),

        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            remappings=[
                ('scan', '/rover/lidar/scan'),
            ],
            parameters=[{
                'params_file': slam_config,
                'use_sim_time': True,
            }],
            output='screen',
        ),
    ])
