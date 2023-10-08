import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

from ipywidgets import interact
import ipywidgets as widgets

# Load your dataset
data = pd.read_csv('test_main.csv')
#print(data)

data.fillna(0, inplace=True)

# Now, the NaN values are replaced with 0
print(data)

years = data['Year'].unique()
companies = data['Company'].unique()
ratings = ['-2', '-1', '0', '1', '2']

# Initialize the 3D array with zeros
three_d_array = np.zeros((len(companies), len(years), len(ratings)))

# Fill the 3D array with data
for i, company in enumerate(companies):
    for j, year in enumerate(years):
        for k, rating in enumerate(ratings):
            subset = data[(data['Company'] == company) & (data['Year'] == year)]
            if not subset.empty:
                count = subset[rating].values[0]
                three_d_array[i, j, k] = count

# Create a dictionary to store the data
data_dict = {}

# Fill the dictionary with data
for i, company in enumerate(companies):
    company_data = {}
    for j, year in enumerate(years):
        year_data = {}
        for k, rating in enumerate(ratings):
            count = three_d_array[i, j, k]
            year_data[rating] = count
        company_data[year] = year_data
    data_dict[company.strip()] = company_data

# Now you can access the data for a specific company and year like this:
company_name = "National Association of Manufacturers (NAM)"
year = 2021
try:
    result = data_dict[company_name.strip()][year]
    print(result)
except KeyError:
    print(f"No data found for '{company_name}' in {year}")

# Extract unique years and ratings
years = sorted(set(year for company_data in data_dict.values() for year in company_data.keys()))
ratings = ['-2', '-1', '0', '1', '2']

# Create subplots for each company
num_companies = len(data_dict)
fig, axes = plt.subplots(num_companies, 1, figsize=(10, 6 * num_companies), sharex=True)

# Set bar width
bar_width = 0.15

# Create a list of x positions for bars
x_positions = np.arange(len(years))

# Define custom colors for each rating
rating_colors = {
    '-2': '#e0562f', '-1': '#b3a28b', '0': '#c5c9c7',
    '1': '#14d4de', '2': '#48bd75'
}

# Initialize a set for legend labels to ensure uniqueness
legend_labels = set()

# Iterate through companies and plot data
for i, (company, company_data) in enumerate(data_dict.items()):
    ax = axes[i]
    ax.set_title(company)

    # Iterate through years and ratings and plot bars
    for j, year in enumerate(years):
        for k, rating in enumerate(ratings):
            counts = company_data[year][rating]
            x = x_positions[j] + k * bar_width - (bar_width * len(ratings) / 2)
            bar = ax.bar(x, counts, width=bar_width, label=f'Year {year}, Rating {rating}', color=rating_colors[rating])
            mplcursors.cursor(bar, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"Count: {int(sel.target.get_height())}"))

    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(years)

    # Add each rating label to the set
    for rating in ratings:
        legend_labels.add(f'Rating {rating}')

# Create a common legend outside of the subplots with unique rating labels and custom colors
handles = [plt.Line2D([0], [0], color=rating_colors[rating], lw=4, label=f'Rating {rating}') for rating in ratings]
fig.legend(handles=handles, labels=sorted(legend_labels), title='Ratings', loc='upper right')

plt.tight_layout()
plt.show()