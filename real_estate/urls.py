from django.urls import path

from .views import (
    PropertyListView,
    PropertyDetailView,
    PropertyCreateView,
    MainPageView,
    MakeBidView,
    MyLoginView,
    MyRegistrationView
    
    
)

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('create/', PropertyCreateView.as_view(), name='property_create'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', MyRegistrationView.as_view(), name='register'),
    path('properties/', PropertyListView.as_view(), name='property_list'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    path('properties/<int:property_id>/make_bid/', MakeBidView.as_view(), name='make_bid'),
    
]