from django.db import models

#from django.contrib.auth.models import User
from django.db import models

from datetime import date

class User(models.Model):
    username = models.CharField(max_length=70)
    email = models.EmailField(blank=True , default="admin@admin.com")
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=(("Dentiste","Dentiste"), ("Prothesiste", "Prothesiste"),("Admin","Admin")), default="Dentiste" )

    def __str__(self) -> str:
        return self.username + " " + self.role


    
class Patient(models.Model):
    data = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateField(default=date.today)


class Cas(models.Model):
    #chnged to user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_avant = models.ImageField(upload_to='images/')
    image_apres = models.ImageField(upload_to='images/')
    # added patient
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    # added shared cases
    shared_with = models.ManyToManyField(User, related_name='shared_cas')
      # added timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SharedCase(models.Model):
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE)
    cas = models.ForeignKey(Cas, on_delete=models.CASCADE)
    end_date = models.DateTimeField(auto_now=True, blank=True)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message