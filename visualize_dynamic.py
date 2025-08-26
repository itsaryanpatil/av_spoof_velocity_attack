
import pandas as pd
import matplotlib.pyplot as plt

def visualize_dynamic_results():
    """Visualizes the results of the dynamic velocity spoofing attack."""
    try:
        df = pd.read_csv("dynamic_attack_results.csv")
    except FileNotFoundError:
        print("Error: dynamic_attack_results.csv not found.")
        print("Please run dynamic_simulation.py first.")
        return

    # Create a figure with 3 subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle('Velocity Spoofing Attack Analysis', fontsize=16)

    # --- Plot 1: Position vs. Time ---
    ax1.plot(df['frame'], df['true_pos_x'], 'b-', label='True Position (X)')
    ax1.plot(df['frame'], df['spoofed_pos_x'], 'r--', label='Spoofed Position (X)')
    ax1.set_title('Position Over Time')
    ax1.set_xlabel('Frame')
    ax1.set_ylabel('Position (meters)')
    ax1.legend()
    ax1.grid(True)

    # --- Plot 2: Velocity vs. Time ---
    ax2.plot(df['frame'], df['true_velocity_x'], 'b-', label='True Velocity (X)')
    ax2.plot(df['frame'], df['spoofed_velocity_x'], 'r--', label='Spoofed Velocity (X)')
    ax2.set_title('Perceived Velocity Over Time')
    ax2.set_xlabel('Frame')
    ax2.set_ylabel('Velocity (m/frame)')
    ax2.legend()
    ax2.grid(True)

    # --- Plot 3: Acceleration vs. Time ---
    ax3.plot(df['frame'], df['true_accel_x'], 'b-', label='True Acceleration (X)')
    ax3.plot(df['frame'], df['spoofed_accel_x'], 'r--', label='Spoofed Acceleration (X)')
    ax3.set_title('Perceived Acceleration Over Time')
    ax3.set_xlabel('Frame')
    ax3.set_ylabel('Acceleration (m/frame^2)')
    ax3.legend()
    ax3.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.show()

if __name__ == "__main__":
    visualize_dynamic_results()
