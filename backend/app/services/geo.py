from math import asin, cos, radians, sin, sqrt


HYDERABAD_CENTER = (17.3850, 78.4867)


def distance_from_hyderabad_km(latitude: float, longitude: float) -> float:
    lat1, lon1 = HYDERABAD_CENTER
    radius_km = 6371.0
    d_lat = radians(latitude - lat1)
    d_lon = radians(longitude - lon1)
    a = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(latitude)) * sin(d_lon / 2) ** 2
    )
    return round(2 * radius_km * asin(sqrt(a)), 1)

