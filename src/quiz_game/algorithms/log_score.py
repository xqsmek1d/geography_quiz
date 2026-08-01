import math

def calculate_log_score(value, values):
    values = [v for v in values if v and v > 0]

    if not value or value <= 0:
        return 1.0

    minimum = min(values)
    maximum = max(values)

    return 1 - ((math.log10(value) - math.log10(minimum))/(math.log10(maximum) - math.log10(minimum)))