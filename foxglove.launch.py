from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
import os

# Used in foxglove_controller as a robot and joint state publisher, also shares the assets folder to the rover can be visualized
# Author: Dena Vafadar Afshar

def generate_launch_description():

    root = os.getcwd()

    urdf = os.path.join(root, "assets", "atom_full.urdf")
    with open(urdf, 'r') as f:
        robot_desc = f.read()

    return LaunchDescription([

        # Robot state publisher (+joint state publisher lives in ros_gz_bridge), needed by foxglove
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            arguments=[urdf],
            parameters=[{
                'robot_description': robot_desc,
            }],
            output='screen',
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            parameters=[{'robot_description': robot_desc}],
            output='screen',
        ),
        # ros->foxglove bridge
        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            output='screen'
        ),

        Node(
            package='joy',
            executable='joy_node',
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
    ])
