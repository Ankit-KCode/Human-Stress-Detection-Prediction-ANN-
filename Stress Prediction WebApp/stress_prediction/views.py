import numpy as np
from django.shortcuts import redirect, render
from django.http import HttpResponse
from tensorflow.keras.models import load_model
from django.views.decorators.csrf import csrf_protect
import joblib

# For Sign Up-------------------------------
from django.contrib.auth.models import User
from django.contrib import messages

# For SQL Implementation ------------------
import mysql.connector as sql

# from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login, logout




# ------------- Loading the model and scaler at the top to avoid reloading every time -------------
model = load_model('D:\Ankit-KCode\Human Stress Detection and Prediction\Human Stress Predictions.h5')
scaler = joblib.load('D:\Ankit-KCode\Human Stress Detection and Prediction\scaler.pkl')



# ------------------------------Stress Prediction Logic Function ----------------------------------

@csrf_protect
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


        #----SQL Implementation - "stress_input" ----
        conn = sql.connect(
        host = '127.0.0.1',
        user='root',
        password='Ankitsql6060@#',
        database= 'stress_prediction_app_db'
        )

        cursor = conn.cursor()
        
        comm = "INSERT INTO stress_input (Snoring_Rate, Respiratory_Rate, Body_Temperature, Limb_Movement, Blood_Oxygen, Eye_Movement, Sleep_Hours, Heart_Rate, Prediction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(comm, (snoring_rate, respiratory_rate, body_temperature, limb_movement, blood_oxygen, eye_movement, sleep_hours, heart_rate, prediction))
        conn.commit()
         # ------------


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


@csrf_protect
def login(request):
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        location = request.POST['location']

        conn = None
        cursor = None

        # Store personal information in the session
        request.session['username'] = request.POST.get('username')
        request.session['name'] = request.POST.get('name')
        request.session['age'] = request.POST.get('age')
        request.session['gender'] = request.POST.get('gender')
        request.session['location'] = request.POST.get('location')

        #Authenticating the user
        user = authenticate(request, username=username, password=password)
        

        
        #----SQL Implementation - "login_data" --------
        conn = sql.connect(
        host = '127.0.0.1',
        user='root',
        password='Ankitsql6060@#',
        database= 'stress_prediction_app_db'
        )

        cursor = conn.cursor()
        
        comm = "INSERT INTO login_data (name, age, gender, location, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(comm, (name, age, gender, location, username, password))
        conn.commit()
         # -----------


        #User matches or not
        if user is not None:
            auth_login(request, user)
            # fullname = user.first_name
            request.session['username'] = username
            messages.success(request, "Logged in successfully!")
            return redirect('home')
            # return render(request, "stress_prediction/home.html", {'fullname' : fullname},)
        
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

    #----SQL Implementation - "stress_result" ----
    conn = sql.connect(
    host = '127.0.0.1',
    user='root',
    password='Ankitsql6060@#',
    database= 'stress_prediction_app_db'
    )

    cursor = conn.cursor()
    comm = "INSERT INTO stress_result (Full_Name, Age, Gender, Location, Username, Prediction) VALUES (%s, %s, %s, %s, %s, %s)"

    try:
        cursor.execute(comm, (name, age, gender, location, username, prediction))
        conn.commit()
    except sql.Error as e:
        print("SQL Error:", e)
    finally:
        conn.close()
    # ---------------

    return render(request, 'stress_prediction/stress_result.html', {
        'prediction': prediction,
        'username': username,
        'name' : name,
        'age': age,
        'gender': gender,
        'location': location
        })




# ------------------------------------- For Sign Up ----------------------------------------
@csrf_protect
def signup(request):

    if request.method == "POST":
        usr = request.POST['username']
        fname = request.POST['fullname']
        em = request.POST['email']
        ps = request.POST['password']
        cpass = request.POST['Cpassword']

        errors = {}

        if ps != cpass:
            messages.error(request, "Password do not match!")
            return redirect('signup')
        
        if User.objects.filter(username=usr).exists():
            messages.error(request, "Username already taken!")
            return redirect('signup')
        

        myuser = User.objects.create_user(username=usr, email=em, password=ps)
        myuser.first_name = fname

        myuser.save()


        
        try:
            #----SQL Implementation - "signup_data" ------
            conn = sql.connect(
                host = '127.0.0.1',
                user='root',
                password='Ankitsql6060@#',
                database= 'stress_prediction_app_db'
            )

            cursor = conn.cursor()
            
            comm = "INSERT INTO signup_data (username, fullname, email, password, Cpassword) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(comm, (usr, fname, em, ps, cpass))
            conn.commit()

            messages.success(request, "Your Account Has Been Successfully Created.")
            return redirect('login')

        except sql.Error as e:
            messages.error(request, f"Error:{e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            # -------------

    return render(request, 'stress_prediction/signup.html')


#-------------------------------------------------------------


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')


