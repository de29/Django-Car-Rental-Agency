from msilib.schema import File
from django.db import models
from django.db.models import Q
import pymongo


connect_string = "mongodb://localhost:27017/"

from django.conf import settings

my_client = pymongo.MongoClient(connect_string)



# Access your database and collection
db = my_client['locationvoiture1']
clients_collection = db["home_client"]
car_collection = db["home_voiture"]
res_collection = db["home_reservation"]

# Create your models here.
def get_default_picture():
    # Provide the path to the default picture file on your laptop
    default_picture_path = 'C:\\Users\\HP\\Downloads\\images.jpg'


    # Open the file and create a Django File object
    with open(default_picture_path, 'rb') as f:
        django_file = File(f)
        return django_file
    
    
class NonAvailability(models.Model):
    voiture = models.ForeignKey('voiture', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class voiture(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.CharField(max_length=50, default='')
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    FUEL_CHOICES = (
        ('Gasoline', 'Gasoline'),
        ('Diesel', 'Diesel'),
        ('Hybrid', 'Hybrid'),
        ('Electric', 'Electric'),
    )
    seating_capacity = models.PositiveIntegerField(default=5)
    transmission = models.CharField(max_length=50, default='Automatic')
    fuel_type = models.CharField(max_length=50, choices=FUEL_CHOICES, default='Gasoline')
    color = models.CharField(max_length=50, default='Black')
    prix = models.IntegerField(default=2500)
    picture = models.ImageField(upload_to='car_pictures/', default='')
    description = models.TextField(default='Good Car')

    def is_available(self, start_date, end_date):
        reservations = res_collection.find(
            {
                'voiture_id': self.id,
                'status': 'Accepted',
                'start_date': {'$lte': end_date},
                'end_date': {'$gte': start_date}
            }
        )
        return not any(reservations)

    # Add other fields specific to a voiture


class client(models.Model):
    id= models.AutoField(primary_key=True)
    nom= models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    tel = models.CharField(max_length=20)
    address = models.CharField(max_length=100,default='Not Available')
    cin = models.CharField(max_length=50, default='----')
    picture = models.ImageField(upload_to='client_pictures/', default='')
    status = models.CharField(max_length=100, default='actif')
    # Add other fields specific to a client

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    ROLE_CHOICES = (
        ('manager', 'manager'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    registration_date = models.DateField()

    def __str__(self):
        return self.username
    
    
class Reservation(models.Model):
    voiture = models.ForeignKey(voiture, on_delete=models.CASCADE)
    client = models.ForeignKey(client, on_delete=models.CASCADE)
    start_date= models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20,default='En attente')  # Accepted/Refused/Pending
    etat = models.CharField(max_length=20,default='En attente')  # Accepted/Refused/Pending

    prix = models.IntegerField(default=0)
    ...
    # Add other fields related to a reservation



class Manager(models.Model):
    id= models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    nom = models.CharField(max_length=50,default='Not Available')
    prenom = models.CharField(max_length=50,default='Not Available')
    email = models.EmailField(default='Not Available')
    tel = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=100,default='Not Available')
    cin = models.CharField(max_length=50, default='----')
    picture = models.ImageField(upload_to='client_pictures/', default='')
    
    ...
    # Add other fields specific to a manager


class Administrator(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    ...
    # Add other fields specific to an administrator
    
    
class Pricing(models.Model):
    voiture = models.ForeignKey(voiture, on_delete=models.CASCADE)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)


