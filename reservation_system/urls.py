"""reservation_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('room/new/', AddRoom.as_view()),
    path('room/modify/<int:id>/', EditRoom.as_view()),
    path('room/delete/<int:id>/', DeleteRoom.as_view()),
    path('room/<int:id>/', RoomDetails.as_view(), name="room_details"),
    path('reservation/add/<int:id>/', MakeReservation.as_view()),
    path('reservation/all/', AllReservation.as_view()),
    path('reservation/today/', TodayReservations.as_view()),
    path('reservation/delete/<int:id>/', DeleteReservation.as_view()),
    path('search/', Search.as_view()),
    path('search/result/', Search.as_view())
]
