# %%
import pandas as pd
import matplotlib.pyplot as plt

# The synthetic dataset used for plotting, including your data point for 16 rotations
data = {
    'Rotations': [10, 12, 14, 16, 18, 20],
    'BRAM': [0, 0, 0, 0, 0, 0],
    'DSP': [21, 21, 21, 21, 21, 21],
    'FF': [1864, 1864, 1864, 1864, 1865, 1865],
    'LUT': [2796, 2798, 2800, 2802, 2804, 2806],
    'Throughput (MHz)': [0.77, 0.66, 0.57, 0.51, 0.46, 0.42],
    'Latency': [179, 209, 239, 269, 299, 329],
    'RMSE (R)': [0.000602988351602, 0.000602198531851, 0.000602195214015, 0.000602195214015, 0.000602195214015, 0.000602195214015],
    'RMSE (Theta)': [0.001035753288306, 0.000253744772635, 0.000141665732372, 0.000114684880828, 0.000117761483125, 0.000116337556392]
}

# %%
df = pd.DataFrame(data)

def plot_cordic_metrics(df):
    rotations = df['Rotations']
    
    # 1. Throughput vs. Rotations
    plt.figure(figsize=(8, 6))
    plt.plot(rotations, df['Throughput (MHz)'], marker='o', linestyle='-', color='blue')
    plt.title('Throughput vs. Number of Rotations')
    plt.xlabel('Number of Rotations')
    plt.ylabel('Throughput (MHz)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Label data points
    for i, txt in enumerate(df['Throughput (MHz)']):
        plt.annotate(f'{txt:.2f} MHz', (rotations[i], df['Throughput (MHz)'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
    plt.savefig('throughput_vs_rotations.png')
    plt.close()

    # 2. Resource Usage vs. Rotations
    plt.figure(figsize=(10, 6))
    resources = ['BRAM', 'DSP', 'FF', 'LUT']
    colors = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange']
    
    for resource, color in zip(resources, colors):
        plt.plot(rotations, df[resource], marker='o', linestyle='-', color=color, label=resource)
        # Label data points for the two largest resources (FF, LUT)
        if resource in ['FF', 'LUT']:
            for i, txt in enumerate(df[resource]):
                plt.annotate(f'{txt}', (rotations[i], df[resource][i]), textcoords="offset points", xytext=(0,5), ha='center')

    plt.title('Resource Usage vs. Number of Rotations')
    plt.xlabel('Number of Rotations')
    plt.ylabel('Resource Count')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.savefig('resources_vs_rotations.png')
    plt.close()

    # 3. RMSE (Theta and R) vs. Rotations (Logarithmic Y-axis)
    plt.figure(figsize=(8, 6))
    
    # Plot RMSE (R)
    plt.plot(rotations, df['RMSE (R)'], marker='s', linestyle='-', color='purple', label='RMSE (R)')
    # Plot RMSE (Theta)
    plt.plot(rotations, df['RMSE (Theta)'], marker='^', linestyle='-', color='darkgreen', label='RMSE (Theta)')
    
    plt.yscale('log') # Use log scale for clarity due to exponential drop
    plt.title('RMSE (Precision) vs. Number of Rotations')
    plt.xlabel('Number of Rotations')
    plt.ylabel('RMSE (Log Scale)')
    plt.legend()
    plt.grid(True, which='major', linestyle='-', linewidth=0.7)
    plt.grid(True, which='minor', linestyle='--', linewidth=0.4)
    
    # Label data points
    for i in range(len(rotations)):
        plt.annotate(f'{df["RMSE (R)"][i]:.1e}', (rotations[i], df['RMSE (R)'][i]), textcoords="offset points", xytext=(5,10), ha='left', fontsize=8)
        plt.annotate(f'{df["RMSE (Theta)"][i]:.1e}', (rotations[i], df['RMSE (Theta)'][i]), textcoords="offset points", xytext=(-5,-15), ha='right', fontsize=8)

    plt.savefig('rmse_vs_rotations.png')
    plt.close()

plot_cordic_metrics(df)


