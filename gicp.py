
import numpy as np

def simulate_gicp(point_cloud):
    """
    Simulates the output of the GICP process for vulnerability analysis.
    In the original paper, the eigenvalues of the Hessian matrix from GICP are used.
    Here, we simulate this by assigning a "vulnerability score" to each point.
    The score is a heuristic based on the point's distance and local density.
    """
    # A simple heuristic: vulnerability is proportional to distance.
    # This simulates the idea that points further away have more uncertainty.
    distances = np.sqrt(point_cloud[:, 0]**2 + point_cloud[:, 1]**2)
    
    # Normalize distances to get a base vulnerability score.
    if np.max(distances) > 0:
        normalized_distances = distances / np.max(distances)
    else:
        normalized_distances = distances

    # Another heuristic: points in sparse angular regions are more vulnerable.
    # We can simulate this by assigning a random factor, or by a more complex
    # analysis of the point distribution. For simplicity, we'll primarily use distance.
    vulnerability_scores = normalized_distances

    return point_cloud, vulnerability_scores

def execute_gicp(array, num_iteration, sample_rate, scale_translation):
    """
    This function mimics the structure of the original registration_separated.py.
    It uses the simulated GICP.
    """
    # In this simplified version, we don't need to iterate or add noise,
    # as the GICP is simulated. We'll just run the simulation once.
    
    # We can still do random sampling to simulate using a subset of the point cloud.
    num_sample = int(array.shape[0] * sample_rate)
    if num_sample > 0:
        indices = np.random.choice(array.shape[0], num_sample, replace=False)
        sampled_array = array[indices]
    else:
        sampled_array = array

    if sampled_array.shape[0] == 0:
        return np.array([]), np.array([])

    # Get the simulated vulnerability scores.
    coordinates, scores = simulate_gicp(sampled_array)
    
    return coordinates, scores
