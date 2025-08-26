
import numpy as np
import pandas as pd
import spoofing_module

def perceive_kinematics(positions):
    """Calculates velocity and acceleration from a sequence of positions."""
    velocities = []
    accelerations = []
    
    # First position has zero velocity and acceleration
    velocities.append({'vx': 0, 'vy': 0})
    accelerations.append({'ax': 0, 'ay': 0})

    # Calculate velocity (change in position)
    for i in range(1, len(positions)):
        vx = positions[i]['x'] - positions[i-1]['x']
        vy = positions[i]['y'] - positions[i-1]['y']
        velocities.append({'vx': vx, 'vy': vy})

    # First velocity has zero acceleration
    accelerations.append({'ax': 0, 'ay': 0})

    # Calculate acceleration (change in velocity)
    for i in range(1, len(velocities)):
        ax = velocities[i]['vx'] - velocities[i-1]['vx']
        ay = velocities[i]['vy'] - velocities[i-1]['vy']
        accelerations.append({'ax': ax, 'ay': ay})
        
    # Ensure accelerations list is the same size as positions
    while len(accelerations) < len(positions):
        accelerations.append({'ax': 0, 'ay': 0})

    return velocities, accelerations

def run_dynamic_simulation():
    """Main function to simulate the velocity spoofing attack."""
    # --- 1. Define the Scenario ---
    num_frames = 50
    initial_pos = {'x': 5, 'y': 5}
    constant_velocity = {'vx': 0.5, 'vy': 0.5} # Object moves diagonally

    # --- 2. Generate Ground Truth Data ---
    true_positions = []
    for t in range(num_frames):
        pos = {
            'x': initial_pos['x'] + constant_velocity['vx'] * t,
            'y': initial_pos['y'] + constant_velocity['vy'] * t
        }
        true_positions.append(pos)

    # --- 3. Apply Spoofing Attack ---
    attack_start_frame = 20
    # Change attack_type to 'decelerate' to see the other effect
    spoofed_positions = spoofing_module.apply_velocity_spoof(
        true_positions,
        start_frame=attack_start_frame,
        attack_type='accelerate',
        factor=0.1
    )

    # --- 4. Perceive and Calculate Kinematics ---
    true_velocities, true_accelerations = perceive_kinematics(true_positions)
    spoofed_velocities, spoofed_accelerations = perceive_kinematics(spoofed_positions)

    # --- 5. Save Results ---
    results = []
    for i in range(num_frames):
        results.append({
            'frame': i,
            'true_pos_x': true_positions[i]['x'],
            'true_pos_y': true_positions[i]['y'],
            'spoofed_pos_x': spoofed_positions[i]['x'],
            'spoofed_pos_y': spoofed_positions[i]['y'],
            'true_velocity_x': true_velocities[i]['vx'],
            'spoofed_velocity_x': spoofed_velocities[i]['vx'],
            'true_accel_x': true_accelerations[i]['ax'],
            'spoofed_accel_x': spoofed_accelerations[i]['ax'],
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv("dynamic_attack_results.csv", index=False)
    print("Dynamic simulation finished. Results saved to dynamic_attack_results.csv")
    print(f"Attack started at frame {attack_start_frame}. Check the CSV and run visualize_dynamic.py.")

if __name__ == "__main__":
    run_dynamic_simulation()
