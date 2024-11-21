from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('stress-check/', views.stress_prediction, name='stress_check'),
    path('stress-result/', views.stress_result, name='stress_result'),

#Sign In Page
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('signout', views.signout, name='signout'),
    
]
