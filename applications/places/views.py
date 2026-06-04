from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import DeleteView, ListView, DetailView, UpdateView, CreateView
from django.db.models import Avg, Count

from .models import Place
from .filters import PlaceFilter
from .serializers import PlaceSerializer
from .forms import PlaceForm


@api_view(['GET'])
def places_list(request):

    """
        Important Note:
            Changing the queryset 
                from: 
                    Place.objects.all() 
                to:
                    Place.objects.select_related('type').prefetch_related('tags').annotate(
                        avg_rating=Avg("reviews__rating"),
                        review_count=Count("reviews")
                    ).order_by("-avg_rating", "-review_count")

            reduced the database queries from 1009 to 4 queries only when the database had 503 places!!!!!!!!
    """
    #queryset2 = Place.objects.all()
    queryset = Place.objects.select_related('type').prefetch_related('tags').annotate(
        avg_rating=Avg("reviews__rating"),
        review_count=Count("reviews")
    ).order_by("-avg_rating", "-review_count")

    place_filter = PlaceFilter(request.GET, queryset=queryset)
    filtered_qs = place_filter.qs

    serializer = PlaceSerializer(filtered_qs, many=True)
    return Response({
        'places': serializer.data,
        'count': filtered_qs.count(),
        'has_filter': any(field in request.GET for field in place_filter.get_fields())
    })

def map_view(request):
    place_filter = PlaceFilter(request.GET, queryset=Place.objects.all())
    context = {
        'filter': place_filter,
    }
    return render(request, 'places_list.html', context)


class PlacesListView(ListView):
    model = Place
    context_object_name = 'places'
    paginate_by = 10
    template_name = 'places.html'
    queryset = Place.objects.select_related('type').prefetch_related('tags').annotate(
        avg_rating=Avg("reviews__rating"),
        review_count=Count("reviews")
    ).order_by("-avg_rating", "-review_count")


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'place_detail.html'
    queryset = Place.objects.select_related('type').prefetch_related('tags').annotate(
        avg_rating=Avg("reviews__rating"),
        review_count=Count("reviews")
    )


def create_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('places:place-list-view')
    else:
        form = PlaceForm()
    return render(request, 'places/place_form.html', { 'form': form })


def update_place(request, pk):
    place = get_object_or_404(Place, pk = pk)
    if request.method == 'POST':
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            return redirect('places:place-list-view')
    else:
        form = PlaceForm(instance=place)

    """
    We could just add the following line and the function will be ready

    return render(request, 'places/place_form.html', { 'form': form }) 

    But since the Place model has a Many-To-Many tags field we need to pass the correct data to the template
    or we will get a data serialization error like the following
    
    Object of type Tag is not JSON serializable when serializing list item 0 when serializing dict item 'tags' 
    """

    initial_place = {
        'name': form.initial.get('name'),
        'description': form.initial.get('description'),
        'type': form.initial.get('type'),
        'phone': form.initial.get('phone'),
        'website': form.initial.get('website'),
        'latitude': form.initial.get('latitude'),
        'longitude': form.initial.get('longitude'),
    }

    if place.tags.exists():
        initial_place['tags'] = list(place.tags.values_list('id', flat=True))
    else:
        initial_place['tags'] = []

    context = {
        'form': form,
        'initial_place': initial_place,
    }

    return render(request, 'places/place_form.html', context=context)



class PlaceDeleteView(DeleteView):
    model = Place
    template_name = "places/confirm_delete_place.html"
    success_url = reverse_lazy("places:place-list-view")
