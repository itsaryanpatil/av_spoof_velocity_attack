
import numpy as np
import pandas as pd
import utils
import gicp

def run_simulation():
    """Main function to run the LiDAR SMVS simulation."""
    # Load the sample point cloud
    try:
        point_cloud_df = pd.read_csv("data/sample_point_cloud.csv")
        world_points = point_cloud_df[['x', 'y', 'z']].values
    except FileNotFoundError:
        print("Error: data/sample_point_cloud.csv not found.")
        print("Please run this script from the 'my_code' directory.")
        return

    # Define a simple trajectory (e.g., moving along the x-axis)
    trajectory = []
    for x in range(0, 10, 1):
        trajectory.append({'x': x, 'y': 0, 'z': 0})

    results = []

    print("Running simulation...")
    for i, pose in enumerate(trajectory):
        # Transform world points to the robot's local frame
        local_points = world_points - np.array([pose['x'], pose['y'], pose['z']])

        # Filter points (optional, but good practice)
        filtered_points = utils.distance_filter(local_points, 0.1, 50.0)
        filtered_points = utils.height_filter(filtered_points, -2.0)

        if filtered_points.shape[0] == 0:
            continue

        # Simulate GICP to get vulnerability scores
        # These parameters can be tuned.
        coordinates, scores = gicp.execute_gicp(
            array=filtered_points,
            num_iteration=1,
            sample_rate=1.0,
            scale_translation=0.1
        )

        if coordinates.shape[0] == 0:
            continue

        # Convert coordinates to polar to analyze angular distribution
        _, theta = utils.cartesian2polar(coordinates[:, 0], coordinates[:, 1])

        # Calculate SMVS
        list_angle, list_score = utils.count_eigen_score(theta, scores, step=5)
        smvs = utils.global_score_polar(np.array(list_score), spoofing_mode="HFR")

        results.append({
            'timestamp': i,
            'x': pose['x'],
            'y': pose['y'],
            'z': pose['z'],
            'smvs': smvs
        })
        print(f"Step {i+1}/{len(trajectory)}: Pose=({pose['x']}, {pose['y']}), SMVS={smvs:.2f}")

    # Save results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv("simulation_results.csv", index=False)
    print("\nSimulation finished. Results saved to simulation_results.csv")

if __name__ == "__main__":
    run_simulation()
