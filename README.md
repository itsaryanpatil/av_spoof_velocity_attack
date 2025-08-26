
# Simplified SLAM Vulnerability (SMVS) Simulation

This project is a simplified, pure Python implementation of the core concepts from the ICRA 2025 paper "SLAMSpoof: Practical LiDAR Spoofing Attacks on Localization Systems Guided by Scan Matching Vulnerability Analysis". It is designed to be easily runnable on any system, including macOS, without the need for ROS or other complex dependencies.

## Overview

The goal of this project is to simulate the calculation of the Scan Matching Vulnerability Score (SMVS). SMVS is a metric that quantifies how vulnerable a LiDAR-based SLAM system is to spoofing attacks at a given location. The vulnerability is highly dependent on the geometry of the surrounding environment.

This simulation does the following:

1.  **Simulates a Trajectory**: A robot with a LiDAR sensor is moved along a predefined path.
2.  **Simulates LiDAR Scans**: At each point in the trajectory, the robot "sees" a point cloud of the environment.
3.  **Simulates Vulnerability Analysis**: Instead of using the full GICP algorithm, we simulate its output to determine the vulnerability of the scan matching at each point.
4.  **Calculates SMVS**: Based on the simulated vulnerability, the SMVS is calculated for each location in the trajectory.
5.  **Visualizes Results**: The final trajectory is plotted, with each point colored according to its SMVS score.

## Project Structure

- `simulation.py`: The main script to run the simulation.
- `visualize.py`: A script to plot the results of the simulation.
- `utils.py`: Contains helper functions for calculations.
- `gicp.py`: Contains the *simulated* GICP logic.
- `data/`: Contains sample point cloud data.
- `simulation_results.csv`: The output of the simulation.

## Simplified GICP

The original project uses the `small_gicp` library to get the Hessian matrix of the scan registration, which is used to calculate vulnerability. To keep this project simple and dependency-free, `gicp.py` *simulates* this process. It uses a heuristic where the vulnerability of a point is proportional to its distance from the sensor. This captures the essence of the paper's findings: environments with distant, sparse features (like long corridors) are more vulnerable.

## Getting Started

### 1. Prerequisites

- Python 3.6 or higher
- `pip` (Python package installer)

### 2. Installation

1.  **Navigate to the `my_code` directory**:
    ```bash
    cd my_code
    ```

2.  **Install the required Python packages**:
    ```bash
    pip install numpy pandas matplotlib
    ```

### 3. Running the Simulation

1.  **Run the simulation script**:
    ```bash
    python simulation.py
    ```
    This will perform the simulation and create a file named `simulation_results.csv` in the same directory.

2.  **Visualize the results**:
    ```bash
    python visualize.py
    ```
    This will open a plot showing the trajectory colored by SMVS.

## Expected Output

The simulation will print the SMVS at each step. The visualization will show a path. In the beginning, when the robot is far from the "corridor", the SMVS should be low. As the robot enters the corridor, the SMVS should increase, indicating higher vulnerability. This demonstrates how the geometry of the environment affects the security of the SLAM system.

---

## Part 2: Dynamic Velocity Spoofing Attack Simulation

This second simulation demonstrates a different type of attack: spoofing the perceived velocity of a moving object.

### Overview

The simulation creates a scenario where a robot observes another object moving at a constant velocity. The attack starts mid-way through the simulation and manipulates the LiDAR data to make the object appear to accelerate or decelerate.

- `dynamic_simulation.py`: The main script for this attack.
- `spoofing_module.py`: Contains the logic for applying the velocity spoof.
- `visualize_dynamic.py`: The script to visualize the results of this specific attack.
- `dynamic_attack_results.csv`: The output data from the simulation.

### How to Run

1.  **Run the dynamic simulation**:
    ```bash
    python dynamic_simulation.py
    ```
    This will create the `dynamic_attack_results.csv` file.

2.  **Visualize the attack's effect**:
    ```bash
    python visualize_dynamic.py
    ```

### Interpreting the Results

The visualization will show three plots:

1.  **Position vs. Time**: You will see the spoofed path diverge from the true, linear path.
2.  **Velocity vs. Time**: You will see the true velocity as a flat line (constant) and the spoofed velocity as a line that increases or decreases after the attack begins.
3.  **Acceleration vs. Time**: This is the clearest demonstration. The true acceleration will be a flat line at zero, while the spoofed acceleration will show a clear, non-zero value during the attack. This plot proves that the robot *perceives* an acceleration that never actually happened.
