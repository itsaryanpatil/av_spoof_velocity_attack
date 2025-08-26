
import numpy as np

def represent_object(center_x, center_y, num_points=10):
    """Creates a simple square point cloud to represent an object."""
    # Simple square shape
    points = np.random.rand(num_points, 2) - 0.5  # Centered at (0,0)
    points[:, 0] += center_x
    points[:, 1] += center_y
    # Add a z-coordinate (all zeros for this 2D simulation)
    z_coords = np.zeros((num_points, 1))
    return np.hstack([points, z_coords])

def apply_velocity_spoof(true_positions, start_frame, attack_type='accelerate', factor=0.05):
    """
    Modifies a sequence of object positions to simulate acceleration or deceleration.

    Args:
        true_positions (list of dicts): The ground-truth positions of the object.
        start_frame (int): The frame number at which to start the attack.
        attack_type (str): 'accelerate' or 'decelerate'.
        factor (float): The factor for the quadratic term of the spoof.

    Returns:
        list of dicts: The new, spoofed positions of the object.
    """
    spoofed_positions = []
    for i, pos in enumerate(true_positions):
        if i < start_frame:
            spoofed_positions.append(pos.copy())
            continue

        # Time since attack started
        t = i - start_frame

        # The spoofing is based on the equation: delta = 0.5 * a * t^2
        # We apply this delta to the true position.
        spoof_delta_x = 0.5 * factor * (t**2)
        spoof_delta_y = 0.5 * factor * (t**2) # Assuming movement along a diagonal for simplicity

        new_pos = pos.copy()
        if attack_type == 'accelerate':
            new_pos['x'] += spoof_delta_x
            new_pos['y'] += spoof_delta_y
        elif attack_type == 'decelerate':
            # To decelerate, we apply a negative displacement relative to the expected path
            new_pos['x'] -= spoof_delta_x
            new_pos['y'] -= spoof_delta_y
        
        spoofed_positions.append(new_pos)

    return spoofed_positions
