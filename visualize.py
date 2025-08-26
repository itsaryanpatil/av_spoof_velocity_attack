
import pandas as pd
import matplotlib.pyplot as plt

def visualize_results():
    """Visualizes the simulation results."""
    try:
        df = pd.read_csv("simulation_results.csv")
    except FileNotFoundError:
        print("Error: simulation_results.csv not found.")
        print("Please run simulation.py first.")
        return

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df['x'], df['y'], c=df['smvs'], cmap='jet', s=100)
    plt.colorbar(scatter, label='SMVS')
    plt.xlabel("X position (m)")
    plt.ylabel("Y position (m)")
    plt.title("SLAM Vulnerability Simulation")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    visualize_results()
