from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'), # Wishlist
    path('about', views.about, name='about'), # About page
    path('visited', views.places_visited, name='places_visited'), # List of places visited
    path('place_in_wishlist/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited') # This is to change an objects visited value with the primary key of /<int:place_pk>/ to 'True'
]