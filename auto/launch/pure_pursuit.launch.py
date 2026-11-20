from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Pure pursuit behind the AEB gate:
    # pure_pursuit_node -> /nav_drive -> drive_node (stops if /aeb) -> /drive -> mux
    # Run from the workspace root: the waypoint path is src/auto/auto/waypoints.csv.
    return LaunchDescription([
        Node(
            package='auto',
            executable='pure_pursuit_node',
            parameters=[{'odom_topic': '/odom', 'drive_topic': '/nav_drive'}]
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
