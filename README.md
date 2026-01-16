# Beluga AMCL Tuning

A ROS 2 package for testing and tuning [Beluga AMCL](https://github.com/Ekumen-OS/beluga) parameters on an omnidirectional (mecanum) robot platform.

## Overview

This package provides a complete launch setup for testing Beluga AMCL localization with:

- Map server for loading pre-built maps
- LIO-SAM for LiDAR-inertial odometry
- Lidar scan pipeline for sensor data processing
- IMU-based odometry transforms

## Dependencies

- `beluga_amcl` - Beluga AMCL localization node
- `lio_sam` - LiDAR-inertial SLAM/odometry
- `mecanum_bot_bringup` - Robot bringup package (IMU odom TF, lidar pipeline)
- `nav2_map_server` - Nav2 map server
- `nav2_lifecycle_manager` - Nav2 lifecycle management

## Usage

### Launch the localization stack

```bash
ros2 launch beluga_amcl_tuning test_beluga_amcl.launch.py map_yaml_file:=/path/to/your/map.yaml
```

### Launch Arguments

| Argument           | Default                           | Description                          |
| ------------------ | --------------------------------- | ------------------------------------ |
| `use_sim_time`     | `false`                           | Use simulation clock                 |
| `amcl_params_file` | `config/beluga_amacl_params.yaml` | Path to Beluga AMCL parameters       |
| `map_params_file`  | `config/map_server_params.yaml`   | Path to map server parameters        |
| `map_yaml_file`    | `""`                              | Path to the map YAML file (required) |

## Configuration

### AMCL Parameters (`config/beluga_amacl_params.yaml`)

Key parameters for tuning:

**Particle Filter:**

- `min_particles`: 500 - Minimum number of particles
- `max_particles`: 2000 - Maximum number of particles
- `pf_err`: 0.05 - Particle filter error threshold
- `pf_z`: 0.99 - Particle filter z-value

**Motion Model (Omnidirectional):**

- `robot_model_type`: "omnidirectional_drive"
- `alpha1-5`: Motion noise parameters

**Laser Model:**

- `laser_model_type`: "likelihood_field"
- `laser_likelihood_max_dist`: 2.0m
- `max_beams`: 60
- `z_hit`, `z_rand`, `sigma_hit`: Sensor model weights

**TF Frames:**

- `global_frame_id`: "map"
- `odom_frame_id`: "odom"
- `base_frame_id`: "base_link"

### Map Server Parameters (`config/map_server_params.yaml`)

- `frame_id`: "map"
- `topic_name`: "map"

## Topics

### Subscribed

- `/scan` - Laser scan data
- `/map` - Occupancy grid map

### Published

- TF: `map` -> `odom` transform

## Maintainer

- Dhagash Desai (dhagash.desai@eternal.ag)
