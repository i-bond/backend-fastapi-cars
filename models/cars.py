from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, Field
from fastapi import Form, UploadFile, File
import datetime

class Cars(Document):
    brand: str = Field(..., min_length=1)
    make: str = Field(..., min_length=1)
    year: int = Field(..., gt=1975, lt=2023)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(...)
    picture: Optional[str] = None
    added_by: Optional[str] = None
    date_added: Optional[datetime.date] = Field(default_factory=datetime.date.today)

    class Settings:
        '''Set DB collection name'''
        name = "filteredCars"
        bson_encoders = {
            datetime.date: lambda dt: datetime.datetime(year=dt.year, month=dt.month, day=dt.day),
        }

    class Config:
        '''Payload example'''
        schema_extra = {
            "example": {
                "brand": "Kia",
                "make": "Niro",
                "year": 2021,
                "price": 25033,
                "km": 100,
                "cm3": 2500,
            }
        }


class CarUpdateBody(BaseModel):
    brand: Optional[str]
    make: Optional[str]
    year: Optional[int]
    price: Optional[int]
    km: Optional[int]
    cm3: Optional[int]



# if __name__ == '__main__':
#     print( datetime.datetime(year=2021, month=12, day=21))


