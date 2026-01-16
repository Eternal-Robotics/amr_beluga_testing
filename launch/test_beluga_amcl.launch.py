import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, LifecycleNode


def generate_launch_description():
    pkg_share = get_package_share_directory('beluga_amcl_tuning')

    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    amcl_params_file = LaunchConfiguration('amcl_params_file')
    map_params_file = LaunchConfiguration('map_params_file')
    map_yaml_file = LaunchConfiguration('map_yaml_file')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation clock'
    )

    declare_amcl_params_file = DeclareLaunchArgument(
        'amcl_params_file',
        default_value=os.path.join(pkg_share, 'config', 'beluga_amacl_params.yaml'),
        description='Path to the beluga_amcl parameters file'
    )

    declare_map_params_file = DeclareLaunchArgument(
        'map_params_file',
        default_value=os.path.join(pkg_share, 'config', 'map_server_params.yaml'),
        description='Path to the map_server parameters file'
    )

    declare_map_yaml_file = DeclareLaunchArgument(
        'map_yaml_file',
        default_value='',
        description='Path to the map yaml file'
    )

    # Map server node (lifecycle node)
    map_server_node = LifecycleNode(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        namespace='',
        output='screen',
        parameters=[
            map_params_file,
            {'yaml_filename': map_yaml_file},
            {'use_sim_time': use_sim_time}
        ]
    )

    # Lifecycle manager for map_server
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'autostart': True},
            {'node_names': ['map_server']}
        ]
    )

    # Beluga AMCL node
    beluga_amcl_node = Node(
        package='beluga_amcl',
        executable='amcl_node',
        name='beluga_amcl',
        output='screen',
        parameters=[
            amcl_params_file,
            {'use_sim_time': use_sim_time}
        ],
        remappings=[
            ('scan', 'scan'),
            ('map', 'map'),
        ]
    )

    # IMU Odom TF launch
    imu_odom_tf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('mecanum_bot_bringup'),
            '/launch/imu_odom_tf.launch.py'
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    # Lidar scan pipeline launch
    lidar_scan_pipeline_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('mecanum_bot_bringup'),
            '/launch/lidar_scan_pipeline.launch.py'
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'use_e1r': 'false',
            'use_top': 'false'
        }.items()
    )

    # LIO-SAM launch
    lio_sam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('lio_sam'),
            '/launch/run.launch.py'
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time
        }.items()
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_amcl_params_file,
        declare_map_params_file,
        declare_map_yaml_file,
        imu_odom_tf_launch,
        lidar_scan_pipeline_launch,
        lio_sam_launch,
        map_server_node,
        lifecycle_manager_node,
        beluga_amcl_node,
    ])
