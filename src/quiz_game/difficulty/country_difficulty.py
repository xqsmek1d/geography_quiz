import math

from quiz_game.models.country import Country

REGION_DIFFICULTY = {
    "Europe": 0.2,
    "Asia": 0.3,
    "Americas": 0.4,
    "Africa": 0.5,
    "Oceania": 0.6,
}

def calculate_country_difficulty(country: Country, all_countries: list[Country]) -> float:
    population_score = calculate_log_score(
        country.population,
        [c.population for c in all_countries]
    )

    area_score = calculate_log_score(
        country.area_sq_km,
        [c.area_sq_km for c in all_countries]
    )

    gdp_score = calculate_log_score(
        country.gdp,
        [c.gdp for c in all_countries]
    )

    region_score = REGION_DIFFICULTY.get(country.region,0.7)

    return round((0.4*population_score + 0.3*gdp_score + 0.2*area_score + 0.1*region_score),3)

def calculate_log_score(value, values):
    values = [v for v in values if v and v > 0]

    if not value or value <= 0:
        return 1.0

    minimum = min(values)
    maximum = max(values)

    return 1 - ((math.log10(value) - math.log10(minimum))/(math.log10(maximum) - math.log10(minimum)))