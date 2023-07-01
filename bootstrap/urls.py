from django.urls import path, include
from .import views
from django . conf import settings
from django . conf. urls. static import static


urlpatterns = [
    path('', views.home),
    path('signup/', views.signup),
    path('login/', views.login),
    path('verifyuser/', views.verifyuser),
    path('viewsubcategory/', views.viewsubcategory),
    path('productfilter/', views.productfilter),
    path('myadmin/', include('myadmin.urls')),
    path('user/', include('user.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
