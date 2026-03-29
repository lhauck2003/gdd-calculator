from django.db import connection
from django.db.models import Q

from .models import Crop, PlantedCrop, LifeStage, Field, Farm
def db_health_check() -> bool:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1 AS ok')
        return cursor.fetchone()[0] == 1
    
def search_crops(search: str = None, state: str = None):
    query_set = Crop.objects.select_related('crop', 'crop__state')

def search_planted_crops(search: str = None, 
                         crop: str = None, 
                         state: str = None, 
                         year: int = None,
                         month: int = None,
                         day: int = None,
                         field: str = None):
    query_set = PlantedCrop.objects.select_related('plantedcrop',
                                                   'plantedcrop__crop',
                                                   'plantedcrop__crop__state',
                                                   'plantedcrop__field')
    

def search_lifestages(search: str = None, crop: str = None):
    query_set = LifeStage.objects.select_related('lifestage', 'lifestage__crop')

def search_fields(search: str = None, field: str = None, crop: str = None):
    query_set = Field.objects.select_related('field', 'field__crop')

def search_farms(search: str = None):
    query_set = Farm.objects.select_related('farm')