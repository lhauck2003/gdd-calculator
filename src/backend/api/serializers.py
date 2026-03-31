from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Crop, PlantedCrop, LifeStage, Field, Farm, GDD, Pest

class PestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pest
        fields = ['id', 'name', 'description']

class CropSerializer(serializers.ModelSerializer):
    pests = PestSerializer(many=True, read_only=True)
    class Meta:
        model = Crop
        fields = ['id', 'crop', 'base_temp']

class GDDSerializer(serializers.ModelSerializer):
    class Meta:
        model = GDD
        fields = ['id', 'plantedcrop', 'day', 'calc_type', 'gdd']

class PlantedCropSerializer(serializers.ModelSerializer):
    gdds = GDDSerializer(many=True, read_only=True)
    class Meta:
        model = PlantedCrop
        fields = ['id', 'plant_date', 'field', 'crop', 'gdds']
    
class LifeStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeStage
        fields = ['id', 'name', 'description', 'gdd_C', 'gdd_F', 'stage', 'crop']

class FieldSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Field
        geo_field = "geolocation"
        fields = ['id']

class FarmSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Farm
        geo_field = "location"
        fields = ['id', 'farm_name']