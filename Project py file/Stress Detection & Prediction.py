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

