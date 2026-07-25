def slugify(text: str) -> str:
    # Convert a text to be suitable for a filename.
    return (text.lower().replace(" ", "_").replace("-", "_").replace("'", ""))

def parse_population(population: str) -> int | None:
    if not population:
        return None

    return int(population)

def parse_area(area_sq_km: str) -> int | None:
    if not area_sq_km:
        return None

    return int(area_sq_km)

def parse_gdp(gdp: str) -> int | None:
    if not gdp:
        return None

    return int(gdp)