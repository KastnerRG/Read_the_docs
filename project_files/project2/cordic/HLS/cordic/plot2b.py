# %%
import pandas as pd
import matplotlib.pyplot as plt

# The synthetic dataset used for plotting, including your data point for 16 bits
data = {
    'Bits': [8, 12, 16, 20, 24, 32],
    'BRAM': [0,0,0,0,0,0],
    'DSP': [2, 3, 3, 3, 6, 8],
    'FF': [111, 157, 215, 399, 479, 973],
    'LUT': [333, 324, 395, 569, 718, 873],
    'Throughput (MHz)': [2.74, 2.54, 2.60, 4.01, 3.64, 2.07],
    'Latency': [68, 53, 68, 37, 37, 69],
    'RMSE (R)': [0.056847866624594, 0.005622595082968, 0.000378676515538, 0.000029942908441,0.000002250143098,0.000000070739446],
    'RMSE (Theta)': [0.165135517716408, 0.019701045006514, 0.000614974473137, 0.000178924950887, 0.000015287263523, 0.000015017188161]
}

# %%
df = pd.DataFrame(data)

def plot_cordic_metrics(df):
    bits = df['Bits']
    
    # 1. Throughput vs. Bits
    plt.figure(figsize=(8, 6))
    plt.plot(bits, df['Throughput (MHz)'], marker='o', linestyle='-', color='blue')
    plt.title('Throughput vs. Number of Bits')
    plt.xlabel('Number of Bits')
    plt.ylabel('Throughput (MHz)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Label data points
    for i, txt in enumerate(df['Throughput (MHz)']):
        plt.annotate(f'{txt:.2f} MHz', (bits[i], df['Throughput (MHz)'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
    plt.savefig('throughput_vs_bits.png')
    plt.close()

    # 2. Resource Usage vs. Bits
    plt.figure(figsize=(10, 6))
    resources = ['BRAM', 'DSP', 'FF', 'LUT']
    colors = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange']
    
    for resource, color in zip(resources, colors):
        plt.plot(bits, df[resource], marker='o', linestyle='-', color=color, label=resource)
        # Label data points for the two largest resources (FF, LUT)
        if resource in ['FF', 'LUT']:
            for i, txt in enumerate(df[resource]):
                plt.annotate(f'{txt}', (bits[i], df[resource][i]), textcoords="offset points", xytext=(0,5), ha='center')

    plt.title('Resource Usage vs. Number of Bits')
    plt.xlabel('Number of Bits')
    plt.ylabel('Resource Count')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.savefig('resources_vs_bits.png')
    plt.close()

    # 3. RMSE (Theta and R) vs. Bits (Logarithmic Y-axis)
    plt.figure(figsize=(8, 6))
    
    # Plot RMSE (R)
    plt.plot(bits, df['RMSE (R)'], marker='s', linestyle='-', color='purple', label='RMSE (R)')
    # Plot RMSE (Theta)
    plt.plot(bits, df['RMSE (Theta)'], marker='^', linestyle='-', color='darkgreen', label='RMSE (Theta)')
    
    plt.yscale('log') # Use log scale for clarity due to exponential drop
    plt.title('RMSE (Precision) vs. Number of Bits')
    plt.xlabel('Number of Bits')
    plt.ylabel('RMSE (Log Scale)')
    plt.legend()
    plt.grid(True, which='major', linestyle='-', linewidth=0.7)
    plt.grid(True, which='minor', linestyle='--', linewidth=0.4)
    
    # Label data points
    for i in range(len(bits)):
        plt.annotate(f'{df["RMSE (R)"][i]:.1e}', (bits[i], df['RMSE (R)'][i]), textcoords="offset points", xytext=(5,10), ha='left', fontsize=8)
        plt.annotate(f'{df["RMSE (Theta)"][i]:.1e}', (bits[i], df['RMSE (Theta)'][i]), textcoords="offset points", xytext=(-5,-15), ha='right', fontsize=8)

    plt.savefig('rmse_vs_bits.png')
    plt.close()

plot_cordic_metrics(df)


