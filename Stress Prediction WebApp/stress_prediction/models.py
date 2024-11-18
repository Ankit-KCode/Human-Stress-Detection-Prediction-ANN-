from django.db import models

# Create your models here.

#Model for Signup User Data for Database ------------
class Signup_Data(models.Model):
    username = models.CharField(max_length=20)
    fullname = models.CharField(max_length=60)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    Cpassword = models.CharField(max_length=20)

    class Meta:
        db_table = "signup_data"


