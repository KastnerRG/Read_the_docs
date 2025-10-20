# %%
import pandas as pd
import matplotlib.pyplot as plt

# The synthetic dataset used for plotting, including your data point for 16 bits
data3a = {
    'Bits': [8, 12, 16, 20, 24, 32],
    'BRAM': [0,0,0,0,0,0],
    'DSP': [0,1,1,1,2,4],
    'FF': [125,173,236,284,332,579],
    'LUT': [416,414,528,638,768,820],
    'Throughput (MHz)': [3.74, 4.03, 4.09, 4.08, 4.02, 3.81],
    'Latency': [36, 36, 35, 35, 35, 37],
    'RMSE (R)': [0.143123373389244, 0.006679598707706, 0.000241121990257,0.000011216482562, 0.000000435262308 , 0.000000063990790],
    'RMSE (Theta)': [0.370959520339966, 0.030161513015628, 0.000515445834026, 0.000355231139110,0.000355231139110, 0.000355231139110]
}


data2b = {
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
df = pd.DataFrame(data3a)
df2 = pd.DataFrame(data2b)

def plot_cordic_metrics(df,df2):
    bits = df['Bits']
    bits2b = df2['Bits']
    
    # 1. LUTs vs. Bits
    plt.figure(figsize=(8, 6))
    plt.plot(bits, df['LUT'], marker='o', linestyle='-', color='blue')
    plt.plot(bits2b, df2['LUT'], marker='o', linestyle='-', color='red')
    plt.title('LUTs vs. Number of Bits')
    plt.xlabel('Number of Bits')
    plt.ylabel('LUTs')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(["Question 3a", "Question 2b"])
    
    # Label data points
    for i, txt in enumerate(df['LUT']):
        plt.annotate(f'{txt:.2f}', (bits[i], df['LUT'][i]), textcoords="offset points", xytext=(-5,7), ha='center')
    for i, txt in enumerate(df2['LUT']):
        plt.annotate(f'{txt:.2f}', (bits2b[i], df2['LUT'][i]), textcoords="offset points", xytext=(20,-11), ha='center')
        
    plt.savefig('LUTs_vs_bits.png')
    plt.close()


    # 2. DSPs vs. Bits
    plt.figure(figsize=(8, 6))
    plt.plot(bits, df['DSP'], marker='o', linestyle='-', color='blue')
    plt.plot(bits2b, df2['DSP'], marker='o', linestyle='-', color='red')
    plt.title('DSPs vs. Number of Bits')
    plt.xlabel('Number of Bits')
    plt.ylabel('DSPs')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(["Question 3a", "Question 2b"])
    
    # Label data points
    for i, txt in enumerate(df['DSP']):
        plt.annotate(f'{txt:.2f}', (bits[i], df['DSP'][i]), textcoords="offset points", xytext=(0,10), ha='center')
    for i, txt in enumerate(df2['DSP']):
        plt.annotate(f'{txt:.2f}', (bits2b[i], df2['DSP'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
    plt.savefig('DSPs_vs_bits.png')
    plt.close()


    # 3. FFs vs. Bits
    plt.figure(figsize=(8, 6))
    plt.plot(bits, df['FF'], marker='o', linestyle='-', color='blue')
    plt.plot(bits2b, df2['FF'], marker='o', linestyle='-', color='red')
    plt.title('FFs vs. Number of Bits')
    plt.xlabel('Number of Bits')
    plt.ylabel('FFs')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(["Question 3a", "Question 2b"])

    # Label data points
    for i, txt in enumerate(df['FF']):
        plt.annotate(f'{txt:.2f}', (bits[i], df['FF'][i]), textcoords="offset points", xytext=(0,10), ha='center')
    for i, txt in enumerate(df2['FF']):
        plt.annotate(f'{txt:.2f}', (bits2b[i], df2['FF'][i]), textcoords="offset points", xytext=(15,-13), ha='center')
        
    plt.savefig('FFs_vs_bits.png')
    plt.close()




plot_cordic_metrics(df,df2)


