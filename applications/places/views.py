from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import ListView, DetailView

from .models import Place
from .filters import PlaceFilter
from .serializers import PlaceSerializer


@api_view(['GET'])
def places_list(request):
    place_filter = PlaceFilter(request.GET, queryset=Place.objects.all())
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

class PlaceDetailView(DetailView):
    model = Place
    template_name = 'place-detail.html'