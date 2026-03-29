from celery import shared_task
from django.utils import timezone
from .models import PlantedCrop, GDD, GDDCalcType

@shared_task
def calculate_daily_gdd():
    today = timezone.now().date()

    planted_crops = PlantedCrop.objects.select_related(
        "crop", "field"
    ).all()

    created = 0

    for pc in planted_crops:
        # prevent duplicates
        if GDD.objects.filter(plantedcrop=pc, day=today).exists():
            continue

        gdd = GDD(
            plantedcrop=pc,
            day=today,
            calc_type=GDDCalcType.SIMPLE,
        )

        try:
            gdd_value = gdd.calculate_gdd()
        except Exception:
            continue

        gdd.gdd = gdd_value
        gdd.save()

        created += 1

    return f"Created {created} GDD rows"