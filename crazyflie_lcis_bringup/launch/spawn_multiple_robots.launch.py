import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution

from launch_ros.actions import Node
from string import Template

import numpy as np

from crazyflie.bridge_config import generate_bridge_config_file
from crazyflie.initial_position import generate_random_positions


### Parameters
NO_DRONES = 3

# Initial parameters
p_min = np.array([-1.5, -1.5, 0])
p_max = np.array([1.5, 1.5, 2])
min_distance = 0.3

# initial_position = [[0.0, 0.0, 0.0]]
initial_position = generate_random_positions(NO_DRONES, p_min, p_max, min_distance)





### Define launch description
def generate_launch_description():
    ld = LaunchDescription()

    # Setup project paths
    pkg_ros_gz_sim_path = get_package_share_directory('ros_gz_sim') # use for launching gazebo from ROS
    pkg_crazyflie_lcis_description_path = get_package_share_directory("crazyflie_description") # use for model description
    # Modify the GZ_SIM_RESOURCE_PATH environment variable
    resource_path = os.path.join(pkg_crazyflie_lcis_description_path, 'models')
    if 'GZ_SIM_RESOURCE_PATH' in os.environ:
        os.environ['GZ_SIM_RESOURCE_PATH'] += f":{resource_path}"
    else:
        os.environ['GZ_SIM_RESOURCE_PATH'] = resource_path
    resource_path = os.path.join(pkg_crazyflie_lcis_description_path, 'models')
    set_env_var_action = SetEnvironmentVariable(name='GZ_SIM_RESOURCE_PATH', value=resource_path)


    # action: launch gazebo with empty.sdf world / done by including launch file from ros_gz_sim package
    gz_sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz_sim_path, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r ', 'empty.sdf']}.items(),
    )

    # action: spawn robots
    # - step 1: load sdf as robot description for each robot
    sdf_file = os.path.join(pkg_crazyflie_lcis_description_path,'models','crazyflie','model.sdf')
    with open(sdf_file, 'r') as infp:
        robot_desc = infp.read()        # basically a string
    # - step 2: create a template in order to replace the namespace 
    rd_template = Template(robot_desc) # convert string into template
    # - step 3: spawn each robot
    gz_spawn_nodes = []
    for i in range(NO_DRONES):
        gz_spawn_nodes.append(Node(
            package="ros_gz_sim",
            executable="create",
            output="screen",
            arguments=[
                "-allow_renaming", "true",
                # "-name", f"crazyflie_{i}",
                # "-namespace", f"crazyflie_{i}",
                "-string", rd_template.substitute(namespace=f"crazyflie_{i}"),
                "-x", str(initial_position[i][0]),
                "-y", str(initial_position[i][1]),
                "-z", "0",              # basically the drones start from ground
                "-R", "0",
                "-P", "0",
                "-Y", "0",
            ],
        )
        )

    # action: bridge the topics and services between ROS and Gazebo
    bridge_config_file =  "/tmp/bridge_config.yaml"             # a temporary config file is generated at /tmp/ folder
    generate_bridge_config_file(bridge_config_file, NO_DRONES)   

    bridge_node = Node(                         # use ros_gz_bridge to bridge all the topics and services available
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_config_file,
        }],
        output='screen'
    )




    # add_action
    ld.add_action(gz_sim_launch)

    for i in range(NO_DRONES):
        ld.add_action(gz_spawn_nodes[i])

    ld.add_action(bridge_node)

    return ld
