import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Set global figure size and DPI
plt.rcParams['figure.figsize'] = (10, 6)  # Adjust the size as needed
plt.rcParams['figure.dpi'] = 300  # Adjust the DPI as needed

# Set global font size
plt.rcParams['font.size'] = 15  # Adjust the font size as needed
current_directory = os.getcwd()
main_directory = os.path.join(current_directory, 'run11')

# Read the CSV file into a DataFrame
df = pd.read_csv(os.path.join(main_directory, 'run_setup.sigma.csv'), delimiter=',')

# Extract 's', 'emitx', and 'emity' columns
x_data = df['s']
x_max = np.max(x_data)
emitx_data = df['enx'] * 1e6  # Convert to um rad
emity_data = df['eny'] * 1e6  # Convert to um rad
sigma_x = df['Sx']  # Sigma values
sigma_y = df['Sy']

# Extract element names and beta functions
element_names = df['ElementName']
betax_data = df['betaxBeam']
betay_data = df['betayBeam']

# Create figure and subplots
fig, (ax_main, ax_lattice) = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [4, 2]}, sharex=True)

# Plot emittances
ax_main.plot(x_data, emitx_data, label=r'$\epsilon_x \ (\mu m \cdot rad)$')
ax_main.plot(x_data, emity_data, label=r'$\epsilon_y \ (\mu m \cdot rad)$')
ax_main.set_ylabel(r'$(\mu m \cdot rad)$')
ax_main.legend(loc='upper left')
ax_main.set_yscale('log')  # Use logarithmic scale
ax_main.grid(True)

# Draw a black centerline for the lattice
ax_lattice.axhline(0, color='black', linewidth=1)

# Group DataFrame by 'ElementName'
grouped_df = df.groupby('ElementName')

# Add lattice subplot
for element_name, group_data in grouped_df:
    if element_name.strip().startswith('Q'):
        min_s_value = group_data['s'].min()
        max_s_value = group_data['s'].max()
        ax_lattice.add_patch(plt.Rectangle((min_s_value, -0.25), max_s_value - min_s_value, 0.5, edgecolor='black', facecolor='red', linewidth=1))
        element_label_position = (min_s_value + max_s_value) / 2
        ax_lattice.text(element_label_position, -0.35, element_name.strip(), ha='center', va='center', color='black', size='9')
    if element_name.strip().startswith('_BEG_'):
        min_s_value = group_data['s'].min()
        max_s_value = group_data['s'].max()
        ax_lattice.add_patch(
            plt.Rectangle((min_s_value - x_max, -0.25), max_s_value - min_s_value, 0.5, edgecolor='black', facecolor='red', linewidth=1))

# Find the minimum 'sigma_x' value between s=5 and s=7
min_sx_value_between_5_and_7 = sigma_x[(x_data >= 5) & (x_data <= 7)].min()
min_sx_index = sigma_x[(x_data >= 5) & (x_data <= 7)].idxmin()
min_sx_s_value = x_data[min_sx_index]

# Find the minimum 'sigma_x' value between s=4 and s=6
min_sx_value_between_4_and_6 = sigma_x[(x_data >= 4) & (x_data <= 6)].min()
min_sx_index_2 = sigma_x[(x_data >= 4) & (x_data <= 6)].idxmin()
min_sx_s_value_2 = x_data[min_sx_index_2]


# Add rectangle patches for chambers
rectangle_center = min_sx_s_value
rect_width = 2 * 0.04  # Total width of the rectangle
ax_lattice.add_patch(plt.Rectangle((rectangle_center - 0.04, -0.25), rect_width, 0.5, edgecolor='black', facecolor='blue', alpha=0.5, linewidth=1))
ax_lattice.text(rectangle_center, 0.35, 'Plasma', ha='center', va='center', color='black', size='10')

rectangle_center = min_sx_s_value_2
chamber_width = 2 * 0.106
ax_lattice.add_patch(plt.Rectangle((rectangle_center - (chamber_width / 2), -0.25), chamber_width, 0.5, edgecolor='black', facecolor='green', alpha=0.5, linewidth=1))
ax_lattice.text(rectangle_center, 0.35, 'Ante Chamber', ha='center', va='center', color='black', size='10')

# Annotate emittance values at the plasma chamber position on the top plot
plasma_emitx = emitx_data[min_sx_index]
plasma_emity = emity_data[min_sx_index]

ax_main.annotate(
    f'{plasma_emitx:.2f} μm·rad\n{plasma_emity:.2f} μm·rad',
    xy=(min_sx_s_value, plasma_emitx),
    xytext=(min_sx_s_value + 0.5, plasma_emitx * 2),
    arrowprops=dict(facecolor='black', arrowstyle='->'),
    fontsize=10,
    ha='center'
)

# Find the emittance values at s = 0
s_zero_index = x_data.idxmin()
s_zero_emitx = emitx_data[s_zero_index]
s_zero_emity = emity_data[s_zero_index]

# Annotating the emittance values at s = 0
ax_main.annotate(
    f'{s_zero_emitx:.2f} μm·rad\n{s_zero_emity:.2f} μm·rad',
    xy=(0, s_zero_emitx),
    xytext=(0 + 0.5, s_zero_emitx * 2),
    arrowprops=dict(facecolor='black', arrowstyle='->'),
    fontsize=10,
    ha='center'
)

# Customize lattice subplot
ax_lattice.set_ylim(-0.5, 0.5)
ax_lattice.set_yticks([])
ax_lattice.set_ylabel('Element')

# Hide x-axis ticks and labels for the main plot
plt.setp(ax_main.get_xticklabels(), visible=False)

# Show plot
plt.xlabel('s (m)')
plt.tight_layout()
plt.savefig(os.path.join(main_directory, 'emit.png'))
plt.savefig(os.path.join(main_directory, 'emit.pdf'))
