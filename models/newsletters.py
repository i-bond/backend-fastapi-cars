from enum import Enum
from typing import Optional, List
from beanie import Document
from pydantic import Field, EmailStr, BaseModel
from models.users import UsersPublic
from models.cars import Cars
import datetime
from beanie import TimeSeriesConfig, Granularity
from pydantic import validator


# _, week_num, _ = date.today().isocalendar()  # Using isocalendar() function
# print(week_num)


class Newsletters(Document):
    date_send: datetime.date = Field(default_factory=datetime.date.today)
    users: List[UsersPublic]
    new_cars: List[Cars]

    class Collection:
        name = 'newsletters'

    class Settings:
        bson_encoders = {
            datetime.date: lambda dt: datetime.datetime(year=dt.year, month=dt.month, day=dt.day),
        }

    class Config:
        '''Payload example'''
        schema_extra = {
            "example": {
                "send_date": "2023-01-01",
                "users": ['List of Users'],
                "new_cars": ['List of new cars']
            }
        }










