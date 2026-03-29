from __future__ import annotations

import uuid
from decimal import Decimal
from urllib.parse import urlparse

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import MaxLengthValidator
from django.core.validators import MinValueValidator
from django.core.validators import URLValidator
from django.core.validators import validate_email as django_validate_email
#from django.db import models
from django.contrib.gis.db import models
from django.utils import timezone

# GDD calculator
from gddcalc.gdd_calc import GDDCalculator

CROP_NAME_MAX_LENGTH = 25
MAX_NAME_LENGTH = 25

# Create your models here.

class Sample(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(MAX_NAME_LENGTH)]
    )

    location = models.PointField()

class Farm(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(MAX_NAME_LENGTH)]
    )

    location = models.MultiPolygonField()

class Field(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    geolocation = models.PolygonField()

    crop = models.ManyToManyField(
        to="Crop",
        through="PlantedCrop"
    )

    farm = models.ForeignKey(
        to='Farm',
        on_delete=models.CASCADE,
        db_column='farmid'
    )

class PlantedCrop(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    plant_date = models.DateTimeField(default=timezone.now)

    field = models.ForeignKey(
        to='Field',
        on_delete=models.CASCADE,
        db_column='fieldid'
    )

    crop = models.ForeignKey(
        to='Crop',
        on_delete=models.CASCADE,
        db_column='cropid'
    )

class GDDCalcType(models.TextChoices):
    SIMPLE = "simple"
    SINE = "sine"
    OTHER = "other"
    BASKERVILLE_EMIN = "baskerville-emin"

class GDD(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    plantedcrop = models.ForeignKey(
        to='PlantedCrop',
        on_delete=models.DO_NOTHING,
        db_column='plantedcropid',
        related_name='gdds'
    )

    day = models.DateField(default=timezone.now)

    calc_type = models.CharField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(20)],
        choices=GDDCalcType.choices
    )

    gdd = models.FloatField()

    class Meta:
        unique_together = ('plantedcrop', 'day', 'calc_type')


    def calculate_gdd(self) -> float:
        return (GDDCalculator(self.plantedcrop.crop.base_temp)
                .calculate_day(self.calc_type, 
                               self.plantedcrop.field.geolocation, 
                               self.day.timetuple()))


class Crop(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    crop = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(CROP_NAME_MAX_LENGTH)]
    )

    base_temp = models.FloatField(
        null=True, blank=True
    )

    state = models.ManyToManyField(
        to="State"
    )

class LifeStage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(MAX_NAME_LENGTH)]
    )

    description = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(250)]
    )

    gdd_C = models.IntegerField(
        null=True, blank=True
    )

    gdd_F = models.IntegerField(
        null=True, blank=True
    )

    stage = models.FloatField()

    crop = models.ForeignKey(
        to='Crop',
        on_delete=models.CASCADE,
        db_column='cropid'
    )

class State(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.TextField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(MAX_NAME_LENGTH)]
    )

    abbr = models.CharField(
        null=True,
        blank=True,
        validators=[MaxLengthValidator(3)]
    )

class Day:
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    date = models.DateField(default=timezone.now)

class WeatherData:
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    day = models.ForeignKey(
        to="Day",
        on_delete=models.CASCADE,
        db_column="dayid"
    )

    timestamp = models.DateTimeField(default=timezone.now)

    temp = models.FloatField()

