from enum import Enum
import math
from decimal import Decimal

class AirCraft(Enum):
    L = 0
    M = 1
    H = 2
    J = 3

def distance(lat_from: Decimal, long_from: Decimal,  lat_to: Decimal, long_to: Decimal) -> Decimal:
    return 0

def emission(distance: Decimal, aircraft: AirCraft) -> Decimal:
    return 0