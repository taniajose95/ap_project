"""
URL configuration for ap_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from classroom_pro import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.index, name='index'),
    path('view-rooms/', views.room_list, name='room_list'),
    path('manage-booking/', views.manage_booking, name='manage_booking'),
    #path('notification/', views.notification, name='notification'),
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('modify-booking/<int:booking_id>/', views.modify_booking, name='modify_booking'),
] + static(settings.STATIC_URL)


