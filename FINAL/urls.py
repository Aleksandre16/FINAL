from django.contrib import admin
from django.urls import path, include

from library import views
from library.urls import router as library_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('staffusers/', include('staffusers.urls')),
    path('library/', include(library_router.urls)),  #DRF
    path('', views.index, name='index'),

]
