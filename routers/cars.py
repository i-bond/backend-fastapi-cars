from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.cars import Cars, CarUpdateBody
from typing import Optional, List
from pprint import pprint
from beanie import PydanticObjectId
from beanie.odm.operators.update.general import Set
from auth.security import auth_wrapper
from fastapi import Form, UploadFile, File
from PIL import Image
import random
import string

cars_router = APIRouter(prefix="/cars", tags=["cars"])



@cars_router.get("/", status_code=200, response_description="Get all cars")
async def get_all_cars(
    min_price: int = 0,
    max_price: int = 100000,
    brand: Optional[str] = None,
    page: int = 1
)-> List[Cars]:
    '''Returns a set of objects, 5 page = skip 80 from start,81...100'''

    RESULTS_PER_PAGE = 20
    skip_n = (page - 1) * RESULTS_PER_PAGE

    cars = await Cars.find(limit=20) \
                     .sort("-_id") \
                     .skip(skip_n) \
                     .limit(RESULTS_PER_PAGE) \
                     .to_list()

    return cars


@cars_router.get("/{car_id}",  status_code=200, response_description="Get one car", response_model=Cars)
async def get_one_car(car_id: PydanticObjectId):
    car = await Cars.get(car_id)

    return car


@cars_router.post("/", status_code=201, response_description="Add new car", response_model=Cars)
async def post_car(
                   brand: str = Form(..., min_length=1),
                   make: str = Form(..., min_length=1),
                   year: int = Form(..., gt=1975, lt=2023),
                   price: int = Form(...),
                   km: int = Form(...),
                   cm3: int = Form(...),
                   picture: UploadFile = File(...),
                   user_email = Depends(auth_wrapper)
):

    image = Image.open(picture.file)
    random_name = ''.join(random.choices(string.ascii_lowercase, k=10))
    image_url = f"./static/images/{random_name}.png"
    image.save(image_url, "PNG")

    car = Cars(
        brand=brand,
        make=make,
        year=year,
        price=price,
        km=km,
        cm3=cm3,
        picture=image_url.strip('.'), #/static/images/{random_name}.png
        added_by=user_email
    )

    created_car = await car.create()
    return created_car


@cars_router.patch("/{car_id}", status_code=200, response_description="Update car properties", response_model=Cars)
async def update_car(car_id: PydanticObjectId, updated_car: CarUpdateBody, user_email=Depends(auth_wrapper)):
    car = await Cars.get(car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource not found'
        )

    await car.update(Set(updated_car.dict(exclude_unset=True)))

    new_car = await Cars.get(car_id)
    return new_car


@cars_router.delete("/{car_id}", response_description="Delete car")
async def delete_car(car_id: PydanticObjectId, user_email=Depends(auth_wrapper)) -> dict:
    car_to_delete = await Cars.get(car_id)

    if not car_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource not found'
        )

    await car_to_delete.delete()

    return {
        "message": "Car deleted successfully."
    }



