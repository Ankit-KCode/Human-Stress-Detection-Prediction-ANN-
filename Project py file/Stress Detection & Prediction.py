# Importing Required Libraries.
# For Data Analysis & Visualizations.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# For Model Building
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import joblib

# -------------------------------------------------------------

# Loading Dataset
df = pd.read_csv("D:/Ankit-KCode/Human Stress Detection and Prediction/Human Stress Factors Dataset.csv")
df.head(10)

df.shape

# Data Type info of Colums
df.dtypes

# Statistical Summary of Dataset
df.describe()

df.info()

df.duplicated().sum()

# Checking Distribution of Target Variable
df['Stress Levels'].value_counts()


#---------------------------------------------------------------
#DATA VISUALIZATION

# Bar Plots
# Define the columns for plotting
columns = ['Snoring Rate', 'Respiratory Rate', 'Body Temperature', 'Limb Movement', 'Blood Oxygen', 'Eye Movement', 'Sleep Hours', 'Heart Rate']
stress_levels = df['Stress Levels']

# Set up the figure and subplots (4 rows, 2 columns)
fig, axes = plt.subplots(4, 2, figsize=(10, 15))

# Flatten the axes array for easy iteration
axes = axes.flatten()

# Define a list of colors for each graph
colors = ['blue', 'darkturquoise', 'orange', 'dodgerBlue', 'purple', 'gold', 'green', 'firebrick']

# Plot each column against stress levels
for i, column in enumerate(columns):
    axes[i].bar(stress_levels, df[column], color= colors[i])
    axes[i].set_title('Stress Level vs ' f'{column}')
    axes[i].set_xlabel('Stress Level')
    axes[i].set_ylabel(column)

# Adjusting layout to prevent overlap
plt.tight_layout()
plt.show()

# Plotting Correlation Matrix

# Plot the heatmap
plt.figure(figsize=(8, 6))  # Adjust the figure size for better readability
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

# Add a title
plt.title('Correlation Matrix of Stress Factors')

# Show the plot
plt.show()

# Create a pairplot
sns.pairplot(df, hue='Stress Levels', diag_kind='kde', palette='Set1')

# Show the plot
plt.show()



# Calculate the distribution of stress levels
stress_level_distribution = df['Stress Levels'].value_counts()

# Plot the pie chart
plt.figure(figsize=(5, 5))  # Adjust the figure size if needed
plt.pie(stress_level_distribution, labels=stress_level_distribution.index, autopct='%1.1f%%', startangle=90, colors=['#0096C7', '#48CAE4', '#90E0EF', '#00B4D8', '#023E8A'])

# Add a title
plt.title('Distribution of Stress Levels')

# Display the plot
plt.show()



# Define the columns for which you want to plot boxplots
columns = ['Snoring Rate', 'Respiratory Rate', 'Body Temperature', 'Limb Movement', 'Blood Oxygen', 'Eye Movement', 'Sleep Hours', 'Heart Rate']

# Set up a 2x4 grid for boxplots
fig, axes = plt.subplots(2, 4, figsize=(18, 10))  # 2 rows, 4 columns

# Loop through each column and plot a boxplot in the respective grid position
for i, column in enumerate(columns):
    row = i // 4  # Determine the row index
    col = i % 4   # Determine the column index
    sns.boxplot(x='Stress Levels', y=column, data=df, ax=axes[row, col])
    axes[row, col].set_title(f'{column} vs Stress Levels')

# Adjust layout for better spacing
plt.tight_layout()
plt.show()

#------------------------------------------------------