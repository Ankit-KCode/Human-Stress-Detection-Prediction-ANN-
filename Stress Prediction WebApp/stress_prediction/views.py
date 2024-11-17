import numpy as np
from django.shortcuts import redirect, render
from django.http import HttpResponse
from tensorflow.keras.models import load_model
import joblib
#For Sign Up
from django.contrib.auth.models import User
from django.contrib import messages
# from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login, logout

# -------- Loading the model and scaler at the top to avoid reloading every time ----------------
model = load_model('D:\Ankit-KCode\Human Stress Detection and Prediction\Human Stress Predictions.h5')
scaler = joblib.load('D:\Ankit-KCode\Human Stress Detection and Prediction\scaler.pkl')



# ---------------------------Stress Prediction Logic Function --------------------------------------

def stress_prediction(request):
    # prediction = None
    if request.method == 'POST':
        print("entered into post")
        # Getting form data
        snoring_rate = float(request.POST.get('snoring_rate'))
        respiratory_rate = float(request.POST.get('respiratory_rate'))
        body_temperature = float(request.POST.get('body_temperature'))
        limb_movement = float(request.POST.get('limb_movement'))
        blood_oxygen = float(request.POST.get('blood_oxygen'))
        eye_movement = float(request.POST.get('eye_movement'))
        sleep_hours = float(request.POST.get('sleep_hours'))
        heart_rate = float(request.POST.get('heart_rate'))

        
        # Preparing input data for prediction
        input_data = np.array([[snoring_rate, respiratory_rate, body_temperature, limb_movement, blood_oxygen, eye_movement, sleep_hours, heart_rate]])
        print(input_data) 
        
        input_data = scaler.transform(input_data)  # Scalling the input

        # Making prediction
        result = model.predict(input_data)
        prediction = "Stressed" if result[0][0] > 0.5 else "Not Stressed"
        

        request.session['prediction'] = prediction
        return redirect('stress_result')
    else:
        return render(request, 'stress_prediction/stress_check.html')
    


# ---------------------------Rendering Function & Pages --------------------------------------

from django.shortcuts import render, redirect

def home(request):
    username = request.session.get('username', 'N/A')
    return render(request, 'stress_prediction/home.html',{'username': username,})

def about(request):
    return render(request, 'stress_prediction/about.html')

def help(request):
    return render(request, 'stress_prediction/help.html')

def contact(request):
    return render(request, 'stress_prediction/contact.html')

def login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']

        # Store personal information in the session
        request.session['username'] = request.POST.get('username')
        request.session['name'] = request.POST.get('name')
        request.session['age'] = request.POST.get('age')
        request.session['gender'] = request.POST.get('gender')
        request.session['location'] = request.POST.get('location')

        #Authenticating the user
        user = authenticate(request, username=username, password=password)

        #User matches or not
        if user is not None:
            auth_login(request, user)
            fullname = user.first_name
            return render(request, "stress_prediction/home.html", {'fullname' : fullname},)
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request, 'stress_prediction/login.html')  


def stress_check(request):
    return render(request, 'stress_prediction/stress_check.html')


def stress_result(request):
    prediction = request.session.get('prediction', 'No Result Available')
    print("Displaying Prediction:", prediction)
    fullname = request.session.get('fullname', 'N/A')
    username = request.session.get('username', 'N/A')
    name = request.session.get('name', 'N/A')
    age = request.session.get('age', 'N/A')
    gender = request.session.get('gender', 'N/A')
    location = request.session.get('location', 'N/A')

    return render(request, 'stress_prediction/stress_result.html', {
        'prediction': prediction,
        'username': username,
        'name' : name,
        'age': age,
        'gender': gender,
        'location': location
        })



# ------------------------------------- For Sign Up ----------------------------------------
def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fullname = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['password']
        Cpassword = request.POST['Cpassword']

        myuser = User.objects.create_user(username, email, password)
        myuser.fullname = fullname

        myuser.save()

        messages.success(request, "Your Account Has Been Successfully Created.")

        return redirect('login')

    return render(request, 'stress_prediction/signup.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


