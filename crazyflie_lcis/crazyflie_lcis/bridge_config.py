import yaml

# Define the data
# Clock data
"""
- ros_topic_name: "/clock"
  gz_topic_name: "/clock"
  ros_type_name: "rosgraph_msgs/msg/Clock"
  gz_type_name: "gz.msgs.Clock"
  direction: GZ_TO_ROS
"""
data_clock = [
    {
        "ros_topic_name": "/clock",
        "gz_topic_name": "/clock",
        "ros_type_name": "rosgraph_msgs/msg/Clock",
        "gz_type_name": "gz.msgs.Clock",
        "direction": "GZ_TO_ROS",
    }
]

# Odometry data
"""
- ros_topic_name: "/crazyflie_1/odom"
  gz_topic_name: "/model/crazyflie_1/odometry"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS
"""
data_odometry = [
    {
        "ros_topic_name": "/crazyflie_1/odom",
        "gz_topic_name": "/model/crazyflie_1/odometry",
        "ros_type_name": "nav_msgs/msg/Odometry",
        "gz_type_name": "gz.msgs.Odometry",
        "direction": "GZ_TO_ROS",
    }
]

# Rotor velocity data
"""
/crazyflie_0/command/motor_speed
- ros_topic_name: "/crazyflie_1/cmd_actuators"
  gz_topic_name: "/crazyflie_1/command/motor_speed"
  ros_type_name: "actuator_msgs/msg/Actuators"
  gz_type_name: "gz.msgs.Actuators"
  direction: ROS_TO_GZ
"""
data_actuators = [
    {
        "ros_topic_name": "/crazyflie_1/cmd_actuators",
        "gz_topic_name": "/crazyflie_1/command/motor_speed",
        "ros_type_name": "actuator_msgs/msg/Actuators",
        "gz_type_name": "gz.msgs.Actuators",
        "direction": "ROS_TO_GZ",
    }
]

# cmd_vel data
"""
- ros_topic_name: "/crazyflie_1/cmd_vel"
  gz_topic_name: "/crazyflie_1/gazebo/command/twist"
  ros_type_name: "geometry_msgs/msg/Twist"
  gz_type_name: "ignition.msgs.Twist"
  direction: ROS_TO_GZ
"""
data_cmd_vel = [
    {
        "ros_topic_name": "/crazyflie_1/cmd_vel",
        "gz_topic_name": "/crazyflie_1/gazebo/command/twist",
        "ros_type_name": "geometry_msgs/msg/Twist",
        "gz_type_name": "ignition.msgs.Twist",
        "direction": "ROS_TO_GZ",
    }
]

def generate_bridge_config_file(file_path, num_drones):
    """
    Generate a YAML configuration file at runtime with topic mappings.
    """

    # Write to YAML file
    with open(file_path, "w") as file:
        file.write("---\n") # add the '---'
        yaml.dump(data_clock, file, default_flow_style=False, sort_keys=False)

        for i in range(num_drones):
            indexed_data_odometry = data_odometry.copy()
            indexed_data_odometry[0]['ros_topic_name'] = f"/crazyflie_{i}/odom"
            indexed_data_odometry[0]['gz_topic_name'] = f"/model/crazyflie_{i}/odom"
            indexed_data_actuators = data_actuators.copy()
            indexed_data_actuators[0]['ros_topic_name'] = f"/crazyflie_{i}/cmd_actuators"
            indexed_data_actuators[0]['gz_topic_name'] = f"/crazyflie_{i}/command/motor_speed"
            indexed_data_cmd_vel = data_cmd_vel.copy()
            indexed_data_cmd_vel[0]['ros_topic_name'] = f"/crazyflie_{i}/cmd_vel"
            indexed_data_cmd_vel[0]['gz_topic_name'] = f"/crazyflie_{i}/gazebo/command/twist"

            yaml.dump(indexed_data_odometry, file, default_flow_style=False, sort_keys=False)
            yaml.dump(indexed_data_actuators, file, default_flow_style=False, sort_keys=False)
            yaml.dump(indexed_data_cmd_vel, file, default_flow_style=False, sort_keys=False)
        
if __name__=="__main__":
    NO_DRONES = 5
    file_path = "bridge_config.yaml"
    generate_bridge_config_file(file_path, NO_DRONES)
    # # Write to YAML file
    # output_file = "bridge_config.yaml"
    # with open(output_file, "w") as file:
    #     file.write("---\n") # add the '---'
    #     yaml.dump(data_clock, file, default_flow_style=False, sort_keys=False)

    #     for i in range(NO_DRONES):
    #         indexed_data_odometry = data_odometry.copy()
    #         indexed_data_odometry[0]['ros_topic_name'] = f"/crazyflie_{i}/odom"
    #         indexed_data_odometry[0]['gz_topic_name'] = f"/model/crazyflie_{i}/odom"
    #         indexed_data_actuators = data_actuators.copy()
    #         indexed_data_actuators[0]['ros_topic_name'] = f"/crazyflie_{i}/cmd_actuators"
    #         indexed_data_actuators[0]['gz_topic_name'] = f"/crazyflie_{i}/command/motor_speed"
    #         indexed_data_cmd_vel = data_cmd_vel.copy()
    #         indexed_data_cmd_vel[0]['ros_topic_name'] = f"/crazyflie_{i}/cmd_vel"
    #         indexed_data_cmd_vel[0]['gz_topic_name'] = f"/crazyflie_{i}/gazebo/command/twist"

    #         yaml.dump(indexed_data_odometry, file, default_flow_style=False, sort_keys=False)
    #         yaml.dump(indexed_data_actuators, file, default_flow_style=False, sort_keys=False)
    #         yaml.dump(indexed_data_cmd_vel, file, default_flow_style=False, sort_keys=False)


    # print(f"YAML file '{output_file}' has been created!")
