from django.urls import path
from .import views

urlpatterns = [
    path('',views.adminhome),
    path('addcategory/', views.addcategory),
    path('managecustomer/', views.managecustomer),
    path('subcategory/', views.subcategory),
    path('customerstatus/', views.customerstatus),
    path('changpass/',views.changpass)
   
]
