"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pokemon.views import view_home, view_login, view_logout
from api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    # disponible sur http://127.0.0.1:8000/admin/
    path('api/', api.urls),
    # disponible sur http://127.0.0.1:8000/api/
    # http://127.0.0.1:8000/api/docs → interface Swagger Ninja
    path('', view_home, name='home'),
    path('login/', view_login, name='login'),
    path('logout/', view_logout, name='logout'),
]
