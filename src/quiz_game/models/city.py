from pydantic import BaseModel, Field
from shapely import Point

class City(BaseModel): 
    id: str
    name: str
    country_id: str

    is_capital: bool
    is_subcapital: bool | None = None

    admin_id: str | None = None
    admin_name: str | None = None

    population: int | None = None
    
    image: str | None = None

    latitude: float | None = None
    longitude: float | None = None
