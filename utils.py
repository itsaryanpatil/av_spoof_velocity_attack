
import numpy as np

def cartesian2polar(x, y):
    """Converts Cartesian coordinates to polar coordinates."""
    r = np.sqrt(x**2 + y**2)
    theta = np.degrees(np.arctan2(y, x)) + 180
    return r, theta

def count_eigen_score(angle_array, eigen_array, step):
    """Counts the sum of eigenvalues in angular bins."""
    list_angle, list_score = [], []
    for i in range(int(360 / step)):
        mask = ((angle_array >= step * i) & (angle_array < step * (i + 1)))
        score_table = np.sum(eigen_array[mask])
        list_score.append(score_table)
        list_angle.append(step * (i + 0.5))
    return list_angle, list_score

def calc_distance_polar(index, index_ref, num_of_indexes):
    """Calculates the shortest distance between two angles in a polar grid."""
    index_diff1 = abs(index - index_ref)
    index_diff2 = num_of_indexes - index_diff1
    return min(index_diff1, index_diff2)

def global_score_polar(score, spoofing_mode="HFR"):
    """Calculates the global SMVS score."""
    sorted_index = np.argsort(-score)
    sorted_score = score[sorted_index]

    largest_index = sorted_index[0]
    localizability = 0

    threshold = 8 if spoofing_mode == "HFR" else 2

    for i, index in enumerate(sorted_index):
        distance = calc_distance_polar(index, largest_index, sorted_index.shape[0])
        score_local = score[index]
        # The original paper uses a reward function. We simplify this to a weighted sum.
        # This captures the essence of penalizing scores far from the most vulnerable direction.
        reward = score_local * (1 / (1 + distance))
        localizability += reward

    return localizability

def height_filter(points, min_height):
    """Filters points based on a minimum height."""
    return points[points[:, 2] > min_height]

def distance_filter(points, min_dist, max_dist):
    """Filters points based on a minimum and maximum distance from the origin."""
    dist = np.sqrt(points[:, 0]**2 + points[:, 1]**2)
    mask = (dist > min_dist) & (dist < max_dist)
    return points[mask]
