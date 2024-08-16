import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
# Set global figure size and DPI
plt.rcParams['figure.figsize'] = (10, 6)  # Adjust the size as needed
plt.rcParams['figure.dpi'] = 300  # Adjust the DPI as needed

# Set global font size
plt.rcParams['font.size'] = 15 # Adjust the font size as needed
current_directory=os.getcwd()
main_directory = os.path.join(current_directory,'run2')
# Read the CSV file into a DataFrame
df = pd.read_csv(os.path.join(main_directory,'run_setup.sigma.csv'), delimiter=',')

# Extract 's' and 'Sx' columns
x_data = df['s']
x_max = np.max(x_data)
print(x_max)
#x_data = x_data - x_max
y_data = df['Sx']
y2_data = df['Sy']
element_names = df['ElementName']
betax_data = df['betaxBeam']  # Multiply by 1e3 to convert from m to mm
betay_data = df['betayBeam'] # Multiply by 1e3 to convert from m to mm

# Create figure and subplots
fig, (ax_betax, ax_main, ax_lattice) = plt.subplots(nrows=3, ncols=1, gridspec_kw={'height_ratios': [4, 4, 2]}, sharex=True)

# Plot betax and betay data
ax_betax.plot(x_data, betax_data,label=r'$\beta_x$')
ax_betax.plot(x_data, betay_data,label=r'$\beta_y$')
ax_betax.set_ylabel('(m)')
ax_betax.legend(loc='upper left')
ax_betax.grid(True)

# Plot the main data
ax_main.plot(x_data, y_data*1e3,label=r'$\sigma_x$')
ax_main.plot(x_data, y2_data*1e3,label=r'$\sigma_y$')
ax_main.set_ylabel(r'(mm)')
ax_main.legend(loc='upper left')
# ax_main.set_title('Plot of s vs Sx')

# Add grid to main plot
ax_main.grid(True)
# Draw a black centerline for the lattice
ax_lattice.axhline(0, color='black', linewidth=1)

# Group DataFrame by 'ElementName'
grouped_df = df.groupby('ElementName')

# Add lattice subplot
for element_name, group_data in grouped_df:
    if element_name.strip().startswith('Q'):  # Stripping to remove any potential whitespace
        print(element_name.strip())
        min_s_value = group_data['s'].min()
        max_s_value = group_data['s'].max()
        print(max_s_value)
        print(min_s_value)
        ax_lattice.add_patch(plt.Rectangle((min_s_value, -0.25), max_s_value - min_s_value, 0.5, edgecolor='black', facecolor='red', linewidth=1))
        element_label_position = (min_s_value + max_s_value) / 2
        print(element_label_position)
        ax_lattice.text(element_label_position, -0.35, element_name.strip(), ha='center', va='center', color='black',size='9')
    if element_name.strip().startswith('_BEG_'):  # Stripping to remove any potential whitespace
        print(element_name.strip())
        min_s_value = group_data['s'].min()
        max_s_value = group_data['s'].max()
        print(max_s_value)
        print(min_s_value)
        ax_lattice.add_patch(
            plt.Rectangle((min_s_value -x_max, -0.25), max_s_value - min_s_value, 0.5, edgecolor='black', facecolor='red',
                          linewidth=1))
        element_label_position = (min_s_value + max_s_value) / 2
        print(element_label_position)
        #ax_lattice.text(element_label_position, -0.35, 'element_name.strip()', ha='center', va='center', color='black',
        #                size='10')
    '''
    elif element_name.strip() in ['D6', 'D7', 'D8', 'D9']:
        print(element_name.strip())
        min_s_value = group_data['s'].min()
        max_s_value = group_data['s'].max()
        print(max_s_value)
        print(min_s_value)
        element_label_position = (min_s_value + max_s_value) / 2
        print(element_label_position)
        new_element_name = 'D' + str(int(element_name.strip()[1:]) - 1)
        ax_lattice.text(element_label_position, 0.35, new_element_name, ha='center', va='center', color='black',size='10')
    elif element_name.strip() in ['D2', 'D3']:
        print(element_name.strip())
        min_s_value = group_data['s'].min()
        max_s_value = group_data['s'].max()
        print(max_s_value)
        print(min_s_value)
        element_label_position = (min_s_value + max_s_value) / 2
        print(element_label_position)
        ax_lattice.text(element_label_position, 0.35, element_name.strip(), ha='center', va='center', color='black',size='10')
    elif element_name.strip() in ['D10']:
        continue
    else:
        if element_name.strip()  not in ['D5','M1','_BEG_']:
            print(element_name.strip())
            min_s_value = group_data['s'].min()
            max_s_value = group_data['s'].max()
            print(max_s_value)
            print(min_s_value)
            element_label_position = (min_s_value + max_s_value) / 2
            print(element_label_position)
            ax_lattice.text(element_label_position, -0.35, element_name.strip(), ha='center', va='center', color='black',size='10')
    '''
# Find the minimum 'Sx' value between s=4 and s=6
min_sx_value_between_4_and_6 = y_data[(x_data >= 1) & (x_data <= 3)].min()
min_sx_index = y_data[(x_data >= 1) & (x_data <= 3)].idxmin()
min_sx_s_value = x_data[min_sx_index]

# Add rectangle patch with text "Plasma chamber"
initial_s_value = x_data.iloc[0]
rectangle_center = initial_s_value # Center point of the rectangle
rect_width = 2 * 0.04  # Total width of the rectangle
ax_lattice.add_patch(plt.Rectangle((rectangle_center - 0.04, -0.25), rect_width, 0.5, edgecolor='black', facecolor='blue', alpha=0.5, linewidth=1))
ax_lattice.text(rectangle_center, 0.35, 'Plasma', ha='center', va='center',color='black',size='10')

# Add rectangle patch with text "Ante chamber"
rectangle_center = min_sx_s_value # Center point of the rectangle
print(f'Ante chamber : {rectangle_center}')
chamber_width = 2*0.106
ax_lattice.add_patch(plt.Rectangle((rectangle_center - (chamber_width/2), -0.25), chamber_width, 0.5, edgecolor='black', facecolor='green', alpha=0.5, linewidth=1))
ax_lattice.text(rectangle_center, 0.35, 'Ante Chamber', ha='center', va='center',color='black',size='10')

# Hide x-axis ticks and labels for the main plot
plt.setp(ax_main.get_xticklabels(), visible=False)

# Customize the lattice subplot
ax_lattice.set_ylim(-0.5, 0.5)
ax_lattice.set_yticks([])
ax_lattice.set_ylabel('Element')

# Show plot
plt.xlabel('s (m)')
plt.tight_layout()
plt.savefig(os.path.join(main_directory,'sigma.png'))
plt.savefig(os.path.join(main_directory,'sigma.pdf'))
