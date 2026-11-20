from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Follow the gap behind the AEB gate:
    # planner -> /nav_drive -> drive_node (stops if /aeb) -> /drive -> mux
    planner = LaunchConfiguration('planner')
    return LaunchDescription([
        DeclareLaunchArgument(
            'planner', default_value='gap_follow_v2',
            description='gap_follow (v1 bubble) or gap_follow_v2 (disparity extender)'),
        Node(
            package='auto',
            executable=planner,
            parameters=[{'drive_topic': '/nav_drive'}]
        ),
        Node(
            package='auto',
            executable='aeb_node',
            parameters=[{'odom_topic': '/odom'}]
        ),
        Node(
            package='auto',
            executable='drive_node',
            parameters=[{'input_topic': '/nav_drive'}]
        ),
    ])
