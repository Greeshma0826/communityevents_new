"""
URL configuration for communityevents_new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from events import views  # Import your views here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),  # Include your events app URLs
    path('my_events/', views.my_events_view, name='my_events'),  # Example view for my_events
    path('create_event/', views.create_event_view, name='create_event'),
   path('logout/', views.CustomLogoutView.as_view(), name='custom_logout'),
    path('', views.home, name='home'),  # Add this line for the root path
    path('', include('events.urls')),
]

