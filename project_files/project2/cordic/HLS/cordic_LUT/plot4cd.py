# %%
import pandas as pd
import matplotlib.pyplot as plt

# The synthetic dataset used for plotting, including your data point for 16 bits
data = {
    'Bits': [4,5,6,7,8],
    'BRAM': [1,2,4,13,60],
    'DSP': [0,0,0,0,0],
    'FF': [5,2,2,2,2],
    'LUT': [54,44,46,48,50],
    'Throughput (MHz)': [95.13,91.79,92.25,95.69,91.24],
    'Latency': [1,1,1,1,1],
    'RMSE (R)': [0.289403885602951,0.163360938429832,0.086298309266567, 0.045045133680105, 0.023094084113836],
    'RMSE (Theta)': [0.595246791839600, 0.317522197961807,0.170881450176239,0.094583898782730,0.051045734435320]
}




# %%
df = pd.DataFrame(data)

def plot_cordic_metrics(df):
    bits = df['Bits']
    
    # # 1. Throughput vs. Bits
    # plt.figure(figsize=(8, 6))
    # plt.plot(bits, df['Throughput (MHz)'], marker='o', linestyle='-', color='blue')
    # plt.title('Throughput vs. Number of Bits')
    # plt.xlabel('Number of Bits')
    # plt.ylabel('Throughput (MHz)')
    # plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # # Label data points
    # for i, txt in enumerate(df['Throughput (MHz)']):
    #     plt.annotate(f'{txt:.2f} MHz', (bits[i], df['Throughput (MHz)'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
    # plt.savefig('throughput_vs_bits.png')
    # plt.close()

    # 2. Resource Usage vs. Bits
    plt.figure(figsize=(10, 6))
    resources = ['BRAM', 'DSP', 'FF', 'LUT']
    colors = ['tab:red', 'tab:green', 'tab:blue', 'tab:orange']
    
    for resource, color in zip(resources, colors):
        plt.plot(bits, df[resource], marker='o', linestyle='-', color=color, label=resource)
        # Label data points for the two largest resources (FF, LUT)
        if resource in ['FF', 'LUT', 'BRAM']:
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
        plt.annotate(f'{df["RMSE (R)"][i]:.1e}', (bits[i], df['RMSE (R)'][i]), textcoords="offset points", xytext=(-15,10), ha='left', fontsize=8)
        plt.annotate(f'{df["RMSE (Theta)"][i]:.1e}', (bits[i], df['RMSE (Theta)'][i]), textcoords="offset points", xytext=(15,-15), ha='right', fontsize=8)

    plt.savefig('rmse_vs_bits.png')
    plt.close()

plot_cordic_metrics(df)


