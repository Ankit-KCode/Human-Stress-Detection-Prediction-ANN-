# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.predict_stress, name='predict'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('stress-check/', views.stress_check, name='stress_check'),
    path('stress-result/', views.stress_result, name='stress_result'),
]
