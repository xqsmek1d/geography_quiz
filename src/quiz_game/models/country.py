from pydantic import BaseModel, Field

class Country(BaseModel): 
    id: str
    name: str

    region: str
    subregion: str

    capital_id: str | None = None

    population: int | None = None
    area_sq_km: int | None = None
    gdp: int | None = None
    
    difficulty_score: float | None = None

    flag_image: str | None = None