import dateutil
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import datetime
import datetime
import dateutil.parser
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from admin_material.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError,JsonResponse
from .models import *
from .forms import *
from pymongo import MongoClient
from bson import ObjectId
from django.contrib import messages
import pymongo
from django.urls import reverse
from bson import ObjectId
from .forms import ClientForm
from .models import client as Client
from bson import ObjectId
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


connect_string = "mongodb://localhost:27017/"

from django.conf import settings

my_client = pymongo.MongoClient(connect_string)



# Access your database and collection
db = my_client['locationvoiture1']
clients_collection = db["home_client"]
car_collection = db["home_voiture"]
res_collection = db["home_reservation"]
manager_collection = db["home_manager"]
admin_collection = db["home_administrator"]
collection = db['home_client']
clients = collection.find() 


##########LOGIN#########

def loginForm(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        # Check if the user is a Manager
        manager = manager_collection.find_one({"username": username, "password": password})
        if manager:
            print("Helloooo")
            # Perform manager-specific actions or redirect to manager dashboard
            return redirect('manager_dashboard')
        
        # Check if the user is an Administrator
        administrator = admin_collection.find_one({"username": username, "password": password})
        if administrator:
            # Perform administrator-specific actions or redirect to admin dashboard
            return redirect('admin_dashboard')
        
        # If neither Manager nor Administrator, display an error message
        error_message = "Invalid username or password."
        return render(request, 'pages/login.html', {'error_message': error_message})
    
    return render(request, 'pages/login.html')


############LOGOUT############
def logout(request):
    # Perform logout logic
    django_logout(request)
    
    # Redirect the user to the login page or any other desired page after logout
    return redirect('loginForm')





#Access :
def client_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'client':
            return redirect('access_denied')  # Redirect to an access denied page
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'admin':
            return redirect('access_denied')  # Redirect to an access denied page
        return view_func(request, *args, **kwargs)
    return wrapper



def index(request):

    reservations_cursor = res_collection.find({'status': 'En cours'})
    reservations = []
    res_collection.update_many({}, {'$rename': {'start_date ': 'start_date'}})

    today = date.today()
    print(today)

    
    print(reservations_cursor)
    for reservation_doc in reservations_cursor:
        voiture_id = reservation_doc['voiture']
        client_id = reservation_doc['client']
        date_string = reservation_doc['end_date']
        end_date = date.fromisoformat(date_string)
        days_until_end = (end_date - today).days
        print(days_until_end )
        client_data = collection.find_one({'id': int(client_id)})
        voiture_data = car_collection.find_one({'id': int(voiture_id)})
        print(voiture_id)
        print(voiture_data)

        client_obj = Client()
        client_obj.id = client_data['id']
        client_obj.name = client_data['name']
        client_obj.prenom = client_data['prenom']
        client_obj.email = client_data['email']
        client_obj.tel = client_data['tel']
        
        voiture_obj = voiture()
        if voiture_data is not None:
            voiture_obj.id = voiture_data.get('id')
            voiture_obj.make = voiture_data.get('make')
            voiture_obj.model = voiture_data.get('model')


        
        if voiture_obj is None or client_obj is None:
            # Handle the case when voiture or client object is not found
            continue

        # Add the reservation with associated objects to the list
        reservation = {
            'days_until_end':days_until_end ,
            'reservation': reservation_doc,
            'voiture': voiture_obj,
            'client': client_obj,
        }
        reservations.append(reservation)

    
    total_users = clients_collection.count_documents({"status":"actif"})
    total_cars = car_collection.count_documents({})
    total_reservations = res_collection.count_documents({})
    total_reservations_en_cours = res_collection.count_documents({"status": "En cours"})


    context = {
        'reservations': reservations,
        'total_users': total_users,
        'total_cars': total_cars,
        'total_reservations': total_reservations,
        'total_reservations_en_cours': total_reservations_en_cours
    }

    return render(request, 'pages/index.html', context)



def indexAdmin(request):
    
    reservations_cursor = res_collection.find({'status': 'En cours'})
    reservations = []
    res_collection.update_many({}, {'$rename': {'start_date ': 'start_date'}})

    today = date.today()
    print(today)

    
    print(reservations_cursor)
    for reservation_doc in reservations_cursor:
        voiture_id = reservation_doc['voiture']
        client_id = reservation_doc['client']
        date_string = reservation_doc['end_date']
        end_date = date.fromisoformat(date_string)
        days_until_end = (end_date - today).days
        print(days_until_end )
        client_data = collection.find_one({'id': int(client_id)})
        voiture_data = car_collection.find_one({'id': int(voiture_id)})
        print(voiture_id)
        print(voiture_data)

        client_obj = Client()
        client_obj.id = client_data['id']
        client_obj.name = client_data['name']
        client_obj.prenom = client_data['prenom']
        client_obj.email = client_data['email']
        client_obj.tel = client_data['tel']
        
        voiture_obj = voiture()
        if voiture_data is not None:
            voiture_obj.id = voiture_data.get('id')
            voiture_obj.make = voiture_data.get('make')
            voiture_obj.model = voiture_data.get('model')


        
        if voiture_obj is None or client_obj is None:
            # Handle the case when voiture or client object is not found
            continue

        # Add the reservation with associated objects to the list
        reservation = {
            'days_until_end':days_until_end ,
            'reservation': reservation_doc,
            'voiture': voiture_obj,
            'client': client_obj,
        }
        reservations.append(reservation)

    
    total_users = clients_collection.count_documents({})
    total_cars = car_collection.count_documents({})
    total_reservations = res_collection.count_documents({})
    total_reservations_en_cours = res_collection.count_documents({"status": "En cours"})


    context = {
        'reservations': reservations,
        'total_users': total_users,
        'total_cars': total_cars,
        'total_reservations': total_reservations,
        'total_reservations_en_cours': total_reservations_en_cours
    }

    return render(request, 'pages/indexAdmin.html', context)
















def billing(request):
  return render(request, 'pages/billing.html', { 'segment': 'billing' })

def tables(request):
  return render(request, 'pages/tables.html', { 'segment': 'tables' })

def extended(request):
  return render(request, 'examples/tables/extended.html', { 'segment': 'extended' })

def vr(request):
  return render(request, 'pages/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'pages/rtl.html', { 'segment': 'rtl' })

def notification(request):
  return render(request, 'pages/notifications.html', { 'segment': 'notification' })

def profile(request):
  return render(request, 'pages/profile.html', { 'segment': 'profile' })


# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/pages/list_cars.html')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm





# Create your views here.



def index1(request):
    
    # Page from the theme 
    return render(request, 'pages/index1.html')

def profile(request):
    
    # Page from the theme 
    return render(request, 'pages/profile.html')


def extended(request):
  return render(request, 'pages/extended1.html')

def addClient(request):
   return render(request, 'pages/ajouter_client.html')

def addCar(request):
       return render(request, 'pages/add_car.html')

def addManager(request):
       return render(request, 'pages/ajouter_manager.html')

def tables(request):
    users = User.objects.using('your_mongodb_alias').all()  # Retrieve all users from MongoDB
    # return render(request, 'pages/tables.html', {'users': users})
     # Convert users data to a string representation
    users_str = '\n'.join(str(user) for user in users)

    # Create the response content with the users data
    response_content = f"Users:\n{users_str}"

    # Return the response
    return HttpResponse(response_content)
   
   

################MANAGER##################
# add client
def add_manager(request):
    form = ClientForm() 
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        tele = request.POST.get('tele')
        cin = request.POST.get('cin')
        image = request.FILES.get('image')
        # Save the image file
        if image:
            # Assuming you have a specific directory to save the images
            image_path = "{image.name}"
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

       # Retrieve the maximum client ID
        max_id_doc = manager_collection.find_one({}, sort=[("id", -1)])
        max_id = max_id_doc['id'] if (max_id_doc and 'id' in max_id_doc) else 0
        new_id = max_id + 1

        # Save the client data to MongoDB
        manager_data = {
            'id': new_id,
             'username': username,
             'password': password,
            'name': nom,
            'prenom': prenom,
            'email': email,
            'tel': tele,
            'cin': cin,
            'picture': image_path if image else None,
            'status' : 'actif',
        }
        manager_collection.insert_one(manager_data)
        
        return redirect('listManagers')


        return render(request, 'pages/list_clients.html', {'form': form})

    else:
            form = ClientForm()
    
    return render(request, 'pages/list_clients.html', {'form': form})

def listManagers(request):
    managers = manager_collection.find({'status': 'actif'})
    
    # Pass the clients to the template for rendering
    return render(request, 'pages/list_managers.html', {'managers': managers})

#Delete manager 
def delete_manager(request, manager_id):
    # Retrieve the client from the database
    manager = manager_collection.find_one({'id': int(manager_id)})
    
    if manager:
        # Update the client's status to 'deleted'
        manager['status'] = 'deleted'
        manager_collection.update_one({'_id': manager['_id']}, {'$set': manager})

    return redirect('listClients')

##########----EVERYTHING ABOUT CLIENT----###########


    #lister client
def listClients(request):
    # Retrieve 'actif' clients from the collection
    collection = db['home_client']
    clients = collection.find({'status': 'actif'})
    
    # Pass the clients to the template for rendering
    return render(request, 'pages/list_clients.html', {'clients': clients})

# add client
def add_client(request):
    form = ClientForm() 
    if request.method == 'POST':
        # Retrieve form data
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        tele = request.POST.get('tele')
        cin = request.POST.get('cin')

       # Retrieve the maximum client ID
        max_id_doc = clients_collection.find_one({}, sort=[("id", -1)])
        max_id = max_id_doc['id'] if (max_id_doc and 'id' in max_id_doc) else 0
        new_id = max_id + 1

        # Save the client data to MongoDB
        client_data = {
            'id': new_id,
            'name': nom,
            'prenom': prenom,
            'email': email,
            'tel': tele,
            'cin': cin,
            'status' : 'actif',
        }
        clients_collection.insert_one(client_data)
        
        return redirect('listClients')


        return render(request, 'pages/list_clients.html', {'form': form})

    else:
            form = ClientForm()
    
    return render(request, 'pages/list_clients.html', {'form': form})

from django.http import JsonResponse

def edit_client(request, client_id):
    print(request)
    client = clients_collection.find_one({'id': client_id})
   
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Retrieve form data
        nom = request.POST.get('name')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        tele = request.POST.get('tele')
        address = request.POST.get('address')
        cin = request.POST.get('cin')
        print('ASSIIIIIIYAAAAAAA')
        print(nom)
        # Update the client data in MongoDB
        clients_collection.update_one(
            {'id': client_id},
            {'$set': {
                'name': nom,
                'prenom': prenom,
                'email': email,
                'tele': tele,
                'address': address,
                'cin': cin,
            }}
        )

        return redirect('listClients')
    print('invalid')
    return render(request, 'pages/list_clients.html', {'client': client})




#Delete client 
def delete_client(request, client_id):
    # Retrieve the client from the database
    client = clients_collection.find_one({'id': int(client_id)})
    
    if client:
        # Update the client's status to 'deleted'
        client['status'] = 'deleted'
        clients_collection.update_one({'_id': client['_id']}, {'$set': client})

    return redirect('listClients')


#profile client :
def clientProfile(request, client_id):
    # Retrieve the client from the database using the client_id
    collection = db['home_client']
    client = collection.find_one({'id': int(client_id)})
    reservations = res_collection.find({'client': str(client_id)})
    reservations_with_car = []

    for reservation in reservations:
        car_id = reservation['voiture']
        car_collection = db['home_voiture']
        car = car_collection.find_one({'id': int(car_id)})
        print(car)
        if car:
            reservation['car'] = car
            reservations_with_car.append(reservation)

    if client:
        context = {
            'client': client,
            'reservations': reservations_with_car,
        }
        # Pass the client data to the template for rendering
        return render(request, 'pages/profile.html', context)
    else:
        # Handle the case when the client is not found
        return HttpResponse('Client not found')



############---END CLIENT---###############
#lister cars
def listCars(request):
    collection = db['home_voiture']
    cars = collection.find({'available': True})
    
    # Pass the clients to the template for rendering
    return render(request, 'pages/list_cars.html', {'cars': cars})

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def add_car(request):
    if request.method == 'POST':
        make = request.POST.get('make')
        model = request.POST.get('model')
        year = int(request.POST.get('year'))
        prix = int(request.POST.get('prix'))
        transmission = request.POST.get('transmission')
        fuel_type = request.POST.get('fuel_type')
        color = request.POST.get('color')
        available = True 
        picture = request.FILES.get('picture')
        description = request.POST.get('description')
        if picture:
            # Generate a unique file name for the picture
            file_name = picture.name
            
            # Specify the relative path to the desired directory within the media directory
            directory = 'car_pictures'
            
            # Create the directory if it doesn't exist
            os.makedirs(os.path.join(settings.MEDIA_ROOT, directory), exist_ok=True)

            # Save the picture to the specified directory
            file_path = os.path.join(directory, file_name)
            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb') as f:
                for chunk in picture.chunks():
                    f.write(chunk)

            # Get the relative path to the picture
            picture_path = os.path.join(settings.MEDIA_URL, file_path)
        else:
            picture_path = None
    

        # Retrieve the maximum car ID
        max_id_doc = car_collection.find_one({}, sort=[("id", -1)])
        max_id = max_id_doc['id'] if (max_id_doc and 'id' in max_id_doc) else 0
        new_id = max_id + 1

        # Save the car data to MongoDB
        car_data = {
            'id': new_id,
            'make': make,
            'model': model,
            'year': year,
            'transmission': transmission,
            'fuel_type': fuel_type,
            'color': color,
            'prix': prix,
            'available': available,
            'picture': picture_path if picture else None,
            'description': description,
        }
        car_collection.insert_one(car_data)

        return redirect('listCars')
    
    return render(request, 'pages/list_cars.html')


#Delete car
def delete_car(request, car_id):
    # Retrieve the car from the database
    car = car_collection.find_one({'id': int(car_id)})
    
    if car:
        car_collection.delete_one({'_id': car['_id']})
    return redirect('listCars')




####################--RESERVATION LOGIC--#########################

def reservation(request):
    reservations_cursor = res_collection.find({'status': 'En attente'})
    reservations = []
    res_collection.update_many({}, {'$rename': {'start_date ': 'start_date'}})

    print(reservations_cursor)
    for reservation_doc in reservations_cursor:
        voiture_id = reservation_doc['voiture']
        client_id = reservation_doc['client']

        client_data = collection.find_one({'id': int(client_id)})
        voiture_data = car_collection.find_one({'id': int(voiture_id)})
        print(voiture_id)
        print(voiture_data)

        client_obj = Client()
        client_obj.id = client_data['id']
        client_obj.name = client_data['name']
        client_obj.prenom = client_data['prenom']
        client_obj.email = client_data['email']
        client_obj.tel = client_data['tel']
        
        voiture_obj = voiture()
        if voiture_data is not None:
            voiture_obj.id = voiture_data.get('id')
            voiture_obj.make = voiture_data.get('make')
            voiture_obj.model = voiture_data.get('model')


        
        if voiture_obj is None or client_obj is None:
            # Handle the case when voiture or client object is not found
            continue

        # Add the reservation with associated objects to the list
        reservation = {
            'reservation': reservation_doc,
            'voiture': voiture_obj,
            'client': client_obj,
        }
        reservations.append(reservation)

    context = {
        'reservations': reservations
    }
    return render(request, 'pages/reservation.html', context)






  
  

def fetch_client_info(request, client_id):
    try:
        client = clients_collection.find_one({'id': int(client_id)})
        if client:
            # Create a dictionary with the client information
            client_info = {
                'id': client.get('id'),
                'name': client.get('name'),
                'prenom': client.get('prenom'),
                'email': client.get('email'),
                'tele': client.get('tel'),
                'cin': client.get('cin'),
                # Add other fields as needed
            }
            # Return the client information as JSON response
            return JsonResponse(client_info)
        else:
            # Handle case when client is not found
            return HttpResponseNotFound("Client not found")
    except Exception as e:
        # Handle any exceptions that occur during the fetch
        return HttpResponseServerError(str(e))





def search_cars(request):
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    if start_date and end_date:
        start_datetime = dateutil.parser.parse(start_date)
        end_datetime = dateutil.parser.parse(end_date)

        print(end_datetime)
        # Check for date collisions
        collisions = res_collection.find({
            "$and": [
                {
                    "$or": [
                        {
                            "start_date": {
                                "$lte": end_datetime
                            }
                        },
                        {
                            "end_date": {
                                "$gte": start_datetime
                            }
                        }
                    ]
                },
                {
                    "status": {
                        "$ne": "Annulée"
                    }
                }
            ]
        })

        print(collisions)
        if collisions:
            available_cars = []
        else:
            available_cars = db.home_voiture.find({
                "$and": [
                    {
                        "$or": [
                            {
                                "$lte": {
                                    "start_date": end_datetime
                                }
                            },
                            {
                                "$gte": {
                                    "end_date": start_datetime
                                }
                            }
                        ]
                    },
                    {
                        "$not": {
                            "$in": [
                                {
                                    "$oid": collision.voiture_id
                                } for collision in collisions
                            ]
                        }
                    }
                ]
            })
            print(available_cars)
    else:
        available_cars = db.home_voiture.find({"available": True})

    context = {
        'cars': available_cars
    }

    return render(request, 'pages/list_cars.html', context)



#Afficher res terminer : 

def res_termine(request):
    reservations_cursor = res_collection.find({'status': 'En cours'})
    reservations_ended = []  # Separate list for ended reservations
    res_collection.update_many({}, {'$rename': {'start_date ': 'start_date'}})

    today = date.today()

    for reservation_doc in reservations_cursor:
        voiture_id = reservation_doc['voiture']
        client_id = reservation_doc['client']
        date_string = reservation_doc['end_date']
        end_date = date.fromisoformat(date_string)
        days_until_end = (end_date - today).days

        client_data = collection.find_one({'id': int(client_id)})
        voiture_data = car_collection.find_one({'id': int(voiture_id)})

        client_obj = Client()
        client_obj.id = client_data['id']
        client_obj.name = client_data['name']
        client_obj.prenom = client_data['prenom']
        client_obj.email = client_data['email']
        client_obj.tel = client_data['tel']
        
        voiture_obj = voiture()
        if voiture_data is not None:
            voiture_obj.id = voiture_data.get('id')
            voiture_obj.make = voiture_data.get('make')
            voiture_obj.model = voiture_data.get('model')

        if voiture_obj is None or client_obj is None:
            # Handle the case when voiture or client object is not found
            continue

        # Add the reservation with associated objects to the appropriate list
        reservation = {
            'days_until_end': days_until_end,
            'reservation': reservation_doc,
            'voiture': voiture_obj,
            'client': client_obj,
        }

        if end_date <= today:
            reservations_ended.append(reservation)

    context = {
        'reservations_ended': reservations_ended,  # Include the ended reservations in the context
    }

    return render(request, 'pages/list_reservations-terminée.html', context)



#Creer Réservation
def add_res(request):
    if request.method == 'POST':
        voiture = request.POST.get('id')
        idClient = request.POST.get('id-client')
        fromDate= request.POST.get('fromDate')
        toDate= request.POST.get('toDate')
        prix = request.POST.get('prix')
        
        
        # Retrieve the maximum car ID
        max_id_doc = res_collection.find_one({}, sort=[("id", -1)])
        max_id = max_id_doc['id'] if (max_id_doc and 'id' in max_id_doc) else 0
        new_id = max_id + 1

        # Save the car data to MongoDB
        car_data = {
            'id':new_id,
            'voiture': voiture,
            'client': idClient,
            'start_date ': fromDate,
            'end_date': toDate,
            'status': 'En attente',
            'prix': prix,
        }
        res_collection.insert_one(car_data)
        
        
        """ # Check if the car is available
        voiture = car_collection.find_one({'id': voiture_id})
        if voiture:
            is_available = voiture.is_available(fromDate, toDate)
            if is_available:
                # Retrieve the maximum reservation ID
                max_id_doc = res_collection.find_one({}, sort=[("id", -1)])
                max_id = max_id_doc['id'] if (max_id_doc and 'id' in max_id_doc) else 0
                new_id = max_id + 1
                
                # Save the reservation data to MongoDB
                res_data = {
                    'id': new_id,
                    'voiture_id': voiture_id,
                    'client': idClient,
                    'start_date': fromDate,
                    'end_date': toDate,
                    'status': 'En attente',
                    'prix': prix,
                }
                res_collection.insert_one(res_data)"""

        return redirect('listCars')
    
    return render(request, 'pages/list_cars.html')




#Accepter et refuser reservation : 
def accept_reservation(request, reservation_id):
    res_collection.update_one(
        {'id': int(reservation_id)},
        {'$set': {'status': 'En cours', 'etat': 'Acceptée'}}
    )
    return redirect('reservation')
    # Redirect to a success page or return a JSON response indicating success

def refuse_reservation(request, reservation_id):
    res_collection.update_one(
        {'id': int(reservation_id)},
        {'$set': {'status': 'refus', 'etat': 'Refusée'}}
    )
    return redirect('reservation')
    # Redirect to a success page or return a JSON response indicating success


#Marquer la fin de la reservation : 
def mark_reservation_complete(request, reservation_id):
    
            # Update the reservation status in the database
            res_collection.update_one({'id': int(reservation_id)}, {'$set': {'status': 'Réservation complète, voiture rendue'}})
            return redirect('listCars')
    


###############################################################""

def car_list(request):
    cars = voiture.objects.all()
    context = {'cars': cars}
    return render(request, 'pages/list_cars.html', context)

def client_list(request):
    clients = client.objects.all()
    context = {'clients': clients}
    return render(request, 'pages/add-client.html', context)

def client_list(request):
    clients = client.objects.all()
    context = {'clients': clients}
    return render(request, 'pages/add-client-1.html', context)



    

    