from django.urls import path

from .views import (
    PlantedCropViewSet,
    CropViewSet,
    LifeStageViewSet,
    FieldViewSet,
    FarmViewSet,
)

urlpatterns = [
    path('plantedcrops/', PlantedCropViewSet.as_view({'get': 'list', 'post': 'create'}), name='plantedcrop-list'),
    path('plantedcrops/<int:pk>/', PlantedCropViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='plantedcrop-detail'),
    path('crops/', CropViewSet.as_view({'get': 'list', 'post': 'create'}), name='crop-list'),
    path('crops/<int:pk>/', CropViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='crop-detail'),
    path('lifestages/', LifeStageViewSet.as_view({'get': 'list', 'post': 'create'}), name='lifestage-list'),
    path('lifestages/<int:pk>/', LifeStageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='lifestage-detail'),
    path('fields/', FieldViewSet.as_view({'get': 'list', 'post': 'create'}), name='field-list'),
    path('fields/<int:pk>/', FieldViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='field-detail'),
    path('farms/', FarmViewSet.as_view({'get': 'list', 'post': 'create'}), name='farm-list'),
    path('farms/<int:pk>/', FarmViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='farm-detail'),
]