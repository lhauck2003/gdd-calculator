from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (CropSerializer, PlantedCropSerializer, LifeStageSerializer, FieldSerializer, FarmSerializer, GDDSerializer,
                          Crop, PlantedCrop, LifeStage, Field, Farm, GDD)


# Create your views here.
class PlantedCropViewSet(viewsets.ModelViewSet):
    queryset = PlantedCrop.objects.all()
    serializer_class = PlantedCropSerializer

    @action(detail=True, methods=["get"])
    def gdd(self, request, pk=None):
        planted_crop = self.get_object()

        gdds = GDD.objects.filter(plantedcrop=planted_crop)

        data = [
            {
                "date": gdd.day,
                "value": gdd.calculate_gdd(),
                "type": gdd.calc_type,
            }
            for gdd in gdds
        ]

        return Response(data)

class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class LifeStageViewSet(viewsets.ModelViewSet):
    queryset = LifeStage.objects.all()
    serializer_class = LifeStageSerializer

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    @action(detail=True, methods=["get"])
    def crops(self, request, pk=None):
        field = self.get_object()
        crops = PlantedCrop.objects.filter(field=field)
        serializer = PlantedCropSerializer(crops, many=True)
        return Response(serializer.data)

class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

    @action(detail=True, methods=["get"])
    def fields(self, request, pk=None):
        farm = self.get_object()
        fields = Field.objects.filter(farm=farm)
        serializer = FieldSerializer(fields, many=True)
        return Response(serializer.data)

class GDDViewSet(viewsets.ModelViewSet):
    queryset = GDD.objects.all()
    serializer_class = GDDSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        plantedcrop = self.request.query_params.get("plantedcrop")
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")

        if plantedcrop:
            queryset = queryset.filter(plantedcrop_id=plantedcrop)

        if start and end:
            queryset = queryset.filter(day__range=[start, end])

        return queryset