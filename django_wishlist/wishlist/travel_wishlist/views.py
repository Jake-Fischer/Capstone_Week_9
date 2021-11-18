from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


# Views
@login_required
def place_list(request):

    """
    If this is a POST request, the user clocked the Add button in the form. 
    Check if the new place is valid, if so, save a new Place to the database, and redirect to this same page. 
    This creates a GET request to this same route.
    
    If not a POST route, or Place is not valid, display a page with a list of places and a form to add a new place.
    """

    if request.method == 'POST':
        # Create new place
        form = NewPlaceForm(request.POST) # Creating a form from data that's in the request
        place = form.save(commit=False) # Creating a model object from form
        place.user = request.user
        if form.is_valid(): # Validation against DB constrains
            place.save() # Save to database
            return redirect('place_list') # Reloads home page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # Used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required
def places_visited(request): # Render list of places visited
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})


@login_required
def about(request): # Information about the program
    author = 'Jake'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})


@login_required
def place_was_visited(request, place_pk): # Change visited to true
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('places_visited')


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # Does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()
    # iF POST request, validate form data and update.
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated.')
        else:
            messages.error(request, form.errors) # Temporary, refine later
        return redirect('place_details', place_pk=place_pk)
    else:
        # if place is visited, show form, if place is not visited, no form.
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place': place, 'review_form': review_form })
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place':place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()