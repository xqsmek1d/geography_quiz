from pydantic import BaseModel, Field

class Country(BaseModel): 
    id: str
    name: str
    optional_prefix: str | None = None
    optional_suffix: str | None = None
    optional_names: list[str] | None = None

    iso2: str | None = None
    fips: str | None = None

    region: str
    subregion: str

    capital_id: str | None = None

    population: int | None = None
    area_sq_km: int | None = None
    gdp: int | None = None
    
    difficulty_score: float | None = None

    image: str | None = None