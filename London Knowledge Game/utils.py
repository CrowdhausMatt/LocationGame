import json
import math

def read_json(file_path):
    """Load and return JSON data from a file."""
    with open(file_path, "r") as file:
        return json.load(file)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Haversine formula to calculate the distance between two coordinates."""
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in km
