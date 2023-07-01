from django.urls import path
from .import views

urlpatterns = [
    path('', views.userhome),
    path('changepassworduser/', views.changepassworduser),
    path('addproduct/', views.addproduct),
    path('fetchSubcategoryAJAX/', views.fetchSubcategoryAJAX),
    path('viewproduct/', views.viewproduct),
    path("cancel/", views.cancel),
    path('success/', views.success),
    path('payment/', views.payment),
    path('bidproduct/', views.bidproduct),
    path('bidproductview/', views.bidproductview),
    path('bidhistory/', views.bidhistory),
    path('mybid/', views.mybid)

]
