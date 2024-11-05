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

# MODEL BUILDING

# Feature columns (X) and target column (y)
X = df.drop(columns=['Stress Levels']) # Drop 'Stress Levels' as it's the target
y = df['Stress Levels'] # Target

# Splitting the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


X_train.shape, X_test.shape



# Scalling the features
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train_Scaled = scaler.fit_transform(X_train)
X_test_Scaled = scaler.fit_transform(X_test)

X_train_Scaled = pd.DataFrame(X_train_Scaled, columns=X_train.columns)
X_test_Scaled = pd.DataFrame(X_test_Scaled, columns=X_test.columns)

joblib.dump(scaler, 'scaler.pkl')

X_train_Scaled.head(5)

# Checking Mean value(0) and Standard Deviation(1) after Scaling
np.round(X_train_Scaled.describe(), 1)


#-----------------------Building ANN Model------------------------------

# Convert labels to categorical (one-hot encoding)
# y_train_encoded = to_categorical(y_train)
# y_test_encoded = to_categorical(y_test)

# Initialize the ANN model
model = Sequential()

# Adding input layer and the first hidden layer (neurons=64, activation='relu')
model.add(Dense(units=64, activation= 'relu', input_shape=(X_train.shape[1],)))

# Adding more hidden layers (neurons=32, activation='relu')
model.add(Dense(units=32, activation= 'relu'))

# Adding the output layer (for multi-class classification, use softmax)
model.add(Dense(units=1, activation= 'sigmoid')) # 2 classes for stress levels (0-1)

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# View the model Summary
model.summary()



# Training The Model------------------

history = model.fit(X_train_Scaled, y_train, epochs=50, batch_size=32, validation_data=(X_test_Scaled, y_test))



# Plot training & validation accuracy and loss over epochs
# it helps to check overfitting
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Test Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

#As there is no gap between Train and Test Accuracy Means: There is not much Overfitting.


# Plot training and loss over epochs.
# it helps to check overfitting 
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Test Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

#as there is no gap between Train and Test Loss Means: There is not much Overfitting.



# Evaluate The Model -----------------------------

test_loss, test_accuracy = model.evaluate(X_test_Scaled, y_test)
print(f'Test Accuracy: {test_accuracy*100: .2f}')
print(f'Test Loss: {test_loss*100: .2f}')


# Save The Model ---------------------------------

model.save("Human Stress Predictions.h5")



#---------------------Prediction On Unseen Data (Real Time Predictions)----------------

# Loading the Model and Scaler for Deployment.
from tensorflow.keras.models import load_model
loaded_model = load_model('D:\Ankit-KCode\Human Stress Detection and Prediction\Human Stress Predictions.h5')
loaded_scaler = joblib.load('D:\Ankit-KCode\Human Stress Detection and Prediction\scaler.pkl')


# Make Prediction new Unseen Data
new_data = np.array([[60,18,70,8,97,60,9,75]]) # Replace With actual new Data
new_data_scaled = loaded_scaler.transform(new_data) 
prediction = loaded_model.predict(new_data_scaled)

#Output Prediction in Words.
if prediction > 0.5:
    print("Stressed")

else:
    print("Not Stressed")



#----------------------------MODEL DEPLOYMENT------------------------------------
