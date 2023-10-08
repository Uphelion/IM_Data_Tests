import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# Load your dataset
data = pd.read_csv('data.csv')

# Extract the relevant columns
years = data['Year of Evidence']
evidence_counts = data['Number of Evidence (for given Evidence Quality Rating)']
quality_ratings = data['Evidence Quality Rating']

# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
scatter = ax.scatter(years, evidence_counts, quality_ratings, c=quality_ratings, cmap='coolwarm', s=50)

# Set axis labels and title
ax.set_xlabel('Year of Evidence')
ax.set_ylabel('Number of Evidence')
ax.set_zlabel('Evidence Quality Rating')
ax.set_title('3D Scatter Plot of Company Data')

# Add color bar for evidence quality ratings
cbar = plt.colorbar(scatter)
cbar.set_label('Evidence Quality Rating')

# Show the plot
plt.show()