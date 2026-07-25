from pydantic import BaseModel, Field

class Country(BaseModel): 
    id: str
    name: str
    country_id: str
    is_capital: bool
    is_subcapital: bool | None = None
    district_id: str | None = None
    population: int | None = None