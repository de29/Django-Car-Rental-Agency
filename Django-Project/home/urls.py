from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dashboard-manager/', views.index, name='manager_dashboard'),
    path('dashboard-admin/', views.indexAdmin, name='admin_dashboard'),

    path('profile/', views.profile, name='profile'),
    path('car-list/', views.car_list, name='car_list'),
    path('add-car/', views.add_car, name='add_car'),
    path('addClient/', views.addClient, name='addClient'),
    path('clientList/', views.client_list, name='clientList'),
    path('clientList1/', views.client_list, name='clientList1'),
    path('delete_client', views.delete_client, name='delete_client'),
    #LOGIN
    path('', views.loginForm, name='loginForm'),
    #LOGOUT
    path('logout/', views.logout, name='logout'),
   # path('voirVoiture/',views.,name='voirVoiture'),
   
   #add my pages(Assiya)
   ###########CLIENTS
   path('listClients/', views.listClients, name='listClients'),
   #Creating client
   path('create-client-page/',views.addClient, name='create_client_page'),
   path('create-client/',views.add_client, name='create_client'),
   #Deleting client
   path('delete-client/<int:client_id>/', views.delete_client, name='delete_client'),
   #client profile
   path('client-profile/<int:client_id>/',views.clientProfile, name='client-profile'),
   #Editing client
   path('edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
   
   ###########CARS
   path('listCars/', views.listCars, name='listCars'),
   #Creating car 
   path('create-car-page/',views.addCar, name='create_car_page'),
    #Deleting client
   path('delete-car/<int:car_id>/', views.delete_car, name='delete_car'),
   path('api/clients/<int:client_id>/', views.fetch_client_info, name='fetch_client_info'),
   
   #Searchbar
   path('search/', views.search_cars, name='search_cars'),
   #Creating reservation
   path('create-res/',views.add_res, name='create_reservation'),
   #reservation
   path('reservation/', views.reservation, name='reservation'),
   #accepter et refuser reservation
   path('reservation/accept/<int:reservation_id>/', views.accept_reservation, name='accept_reservation'),
   path('reservation/refuse/<int:reservation_id>/', views.refuse_reservation, name='refuse_reservation'),
   path('delete-manager/<int:manager_id>/', views.delete_manager, name='delete_manager'),
   #Afficher reservations terminées : 
   path('res_termine/',views.res_termine, name='res_termine'),
   #Marque la fin de la reservation : 
   path('mark_reservation_complete/<str:reservation_id>/', views.mark_reservation_complete, name='mark_reservation_complete'),

  #Add Manager
  path('create-manager/',views.add_manager, name='create_manager'),
  path('create-manager-page/',views.addManager, name='create_manager_page'),
  #lister manager 
  path('listManagers/', views.listManagers, name='listManagers'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
