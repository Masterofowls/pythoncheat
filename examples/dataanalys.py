import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# Create sample data
data = {
    'date': pd.date_range(start='2023-01-01', periods=100),
    'sales': np.random.normal(100, 20, 100),
    'customers': np.random.randint(50, 150, 100)
}

# Create DataFrame
df = pd.DataFrame(data)

# Basic statistical analysis
print("\nBasic Statistics:")
print(df.describe())

# Calculate correlations
print("\nCorrelations:")
print(df.corr())

# Create visualizations
plt.figure(figsize=(12, 6))

# Plot 1: Sales over time
plt.subplot(1, 2, 1)
plt.plot(df['date'], df['sales'])
plt.title('Sales Over Time')
plt.xticks(rotation=45)

# Plot 2: Scatter plot of sales vs customers
plt.subplot(1, 2, 2)
plt.scatter(df['customers'], df['sales'])
plt.title('Sales vs Customers')
plt.xlabel('Number of Customers')
plt.ylabel('Sales')

plt.tight_layout()
plt.show()