from django.urls import path
from .import views as v
from django.contrib import admin

urlpatterns=[
    path('', v.home,name='home'),
    path('vendor/',v.vendorpage,name='vendorpage'),

    path('login/', v.auth_view, name='auth'),
    path('logout/', v.logout_view, name='logout'),
     path('explore/<int:package_id>/', v.explore, name='explore'),
     path('details/', v.details, name='details'),

     path('book/<int:package_id>/', v.book_tour, name='book_tour'),


     path('booked/', v.booked_tours, name='booked_tours'),
     path('delete-booking/<int:booking_id>/', v.delete_booking, name='delete_booking'),
     path('my-packages/', v.my_packages, name='my_packages'),
     path('edit-package/<int:pk>/', v.edit_package, name='edit_package'),
     path('delete_package/<int:pk>/', v.delete_package, name='delete_package'),

     path('admin/', admin.site.urls)


   

     



    




   
]