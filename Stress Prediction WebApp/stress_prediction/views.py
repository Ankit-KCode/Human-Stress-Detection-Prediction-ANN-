import numpy as np
from django.shortcuts import render
from tensorflow.keras.models import load_model
import joblib

# Load the model and scaler at the top to avoid reloading every time
model = load_model('path/to/your/Human Stress Predictions.h5')
scaler = joblib.load('path/to/your/scaler.pkl')

def predict_stress(request):
    prediction = None
    if request.method == 'POST':
        # Get form data
        snoring_rate = float(request.POST.get('snoring_rate'))
        respiratory_rate = float(request.POST.get('respiratory_rate'))
        body_temperature = float(request.POST.get('body_temperature'))
        limb_movement = float(request.POST.get('limb_movement'))
        blood_oxygen = float(request.POST.get('blood_oxygen'))
        eye_movement = float(request.POST.get('eye_movement'))
        sleep_hours = float(request.POST.get('sleep_hours'))
        heart_rate = float(request.POST.get('heart_rate'))

        # Prepare input data for prediction
        input_data = np.array([[snoring_rate, respiratory_rate, body_temperature, limb_movement, 
                                blood_oxygen, eye_movement, sleep_hours, heart_rate]])
        input_data = scaler.transform(input_data)  # Scale the input

        # Make prediction
        result = model.predict(input_data)
        prediction = "Stress" if result[0][0] > 0.5 else "Not Stress"

    return render(request, 'stress_detection/predict.html', {'prediction': prediction})

from django.shortcuts import render, redirect

def home(request):
    return render(request, 'stress_prediction/home.html')

def about(request):
    return render(request, 'stress_prediction/about.html')

def help(request):
    return render(request, 'stress_prediction/help.html')

def contact(request):
    return render(request, 'stress_prediction/contact.html')

def login_view(request):
    return render(request, 'stress_prediction/login.html')

def stress_check(request):
    return render(request, 'stress_prediction/stress_check.html')

def stress_result(request):
    # Use your model here for prediction based on inputs.
    return render(request, 'stress_prediction/stress_result.html')
