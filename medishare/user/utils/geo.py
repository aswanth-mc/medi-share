from math import radians, cos, sin, asin, sqrt

from unit.models import PalliativeUnit


def calculate_distance(lat1, lon1, lat2, lon2):

    lat1 = float(lat1)
    lon1 = float(lon1)

    lat2 = float(lat2)
    lon2 = float(lon2)

    lon1 = radians(lon1)
    lon2 = radians(lon2)

    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    radius = 6371

    return c * radius


def find_nearest_unit(lat, lon):
    candidates = PalliativeUnit.objects.filter(
        is_verified=True,
        latitude__isnull=False,
        longitude__isnull=False,
    )

    nearest = None
    min_km = None

    for unit in candidates:
        km = calculate_distance(lat, lon, unit.latitude, unit.longitude)
        if min_km is None or km < min_km:
            min_km = km
            nearest = unit

    return nearest, min_km
