from django.contrib import admin
from django.urls import path, include
from stress_prediction import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stress_prediction.urls')),
    path('stress_prediction/', views.stress_prediction, name='stress_prediction'),
    # path('login/', views.login, name='login'),
]
