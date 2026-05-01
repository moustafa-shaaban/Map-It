from django.urls import reverse
from rest_framework import serializers

from .models import Place, Type, Tag

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class PlaceSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField()
    type = TypeSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = "__all__"

    def get_detail_url(self, obj):
        return reverse('places:place-detail-view', args=[obj.pk])
    

# class PlaceSerializer(serializers.ModelSerializer):
#     detail_url = serializers.SerializerMethodField()
#     type_name = serializers.CharField(source='type.name', read_only=True)
#     tag_names = serializers.SerializerMethodField()

#     class Meta:
#         model = Place
#         fields = "__all__"

#     def get_detail_url(self, obj):
#         return reverse('places:place-detail-view', args=[obj.pk])
    
#     def get_tag_names(self, obj):
#         return [tag.name for tag in obj.tags.all()]