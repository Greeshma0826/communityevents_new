from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from django.contrib.auth import views as auth_views # type: ignore
from . import views
from .views import SignupView, create_event_view, event_create, event_dashboard_view, update_profile
from .views import EventDashboardView, CustomLogoutView
from django.contrib.auth.views import LoginView # type: ignore
from .views import event_list  # Ensure event_list is imported
from .views import CustomLogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', SignupView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('create_event/', create_event_view, name='create_event'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('my_events/', views.my_events_view, name='my_events'),
    path('my_registrations/', views.my_registrations, name='my_registrations'),
    path('event-recommendations/', views.event_recommendations, name='event_recommendations'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback/thank_you/', views.feedback_thank_you, name='feedback_thank_you'),
    path('admin/manage/', views.admin_manage, name='admin_manage'),
    path('event_dashboard/', event_dashboard_view, name='event_dashboard'),
    path('update_profile/', update_profile, name='update_profile'),
    path('event/create/', views.event_create, name='event_create'),
    path('dashboard/', EventDashboardView.as_view(), name='event_dashboard'),
    path('logout/', views.CustomLogoutView.as_view(), name='custom_logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('event_list', event_list, name='event_list'),  # This is for the event list
    path('event/create/', views.event_create, name='event_create'),
    path('search/', views.search_events, name='search_results'),
    path('register_event/<int:event_id>/', views.register_event, name='register_event'),

]
