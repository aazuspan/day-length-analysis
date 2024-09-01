import math


def haversine_distance(lat1, lat2, radius=6371):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(0 / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return radius * c


def _solar_declination(doy: int) -> float:
    """Return solar declination in radians, based on the Julian day of year."""
    return -0.409 * math.cos(2 * math.pi/365 * (doy + 10))


def _hour_angle(latitude: float, declination: float) -> float:
    """Return hour angle in radians, based on latitude declination in radians."""
    x = -math.tan(latitude) * math.tan(declination)

    # 24 or 0 hours of daylight
    if x < -1:
        return math.pi
    if x > 1:
        return 0.0

    return math.acos(x)


def get_day_length(latitude: float, doy: int) -> float:
    """Return the day length in hours at a given latitude (in degrees) and Julian day of year."""
    lat_rad = math.radians(latitude)
    declination = _solar_declination(doy)
    ha = _hour_angle(lat_rad, declination=declination)

    return ha * 7.639


def get_latitude(day_length: float, doy: int) -> float:
    """Return the latitude with the given day length on the Julian day of year."""
    declination = _solar_declination(doy)
    lat_rad = -math.atan(math.cos(day_length * 0.130899) / math.tan(declination))

    return math.degrees(lat_rad)