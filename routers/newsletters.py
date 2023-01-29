from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from models.newsletters import Newsletters
from typing import List, Optional
from beanie import PydanticObjectId
from pprint import pprint
from beanie.operators import In
from models.users import UsersPublic
from models.cars import Cars
from auth.security import auth_wrapper

import datetime

newsletter_router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@newsletter_router.get("/", status_code=200, response_description="Get all newsletters")
async def get_all_newsletters() -> List[Newsletters]:
    newsletters = await Newsletters.find_all().to_list()
    pprint(newsletters)
    return newsletters


@newsletter_router.get("/{newsletter_id}", status_code=200, response_description="Get one newsletter", response_model=Newsletters)
async def get_one_newsletter(newsletter_id: PydanticObjectId):
    newsletter = await Newsletters.get(newsletter_id)

    return newsletter


@newsletter_router.post("/", status_code=201, response_description="Get by newsletter id", response_model=Newsletters)
async def create_newsletter(date_filter: datetime.date, user_email=Depends(auth_wrapper)):
    '''date_filter = 2023-01-23'''
    users = await UsersPublic.find(In(UsersPublic.role, ["USER", "Fruits"])).to_list()
    cars = await Cars.find(Cars.date_added <= date_filter).to_list()

    weekly_newsletter = Newsletters(users=users, new_cars=cars)
    await weekly_newsletter.create()
    return weekly_newsletter


@newsletter_router.patch("/{newsletter_id}", response_description="Update content by newsletter id", response_model=Newsletters)
async def update_newsletter(newsletter_id: PydanticObjectId, delete_email: str, user_email=Depends(auth_wrapper)):
    '''Delete user from newsletter'''
    newsletter = await Newsletters.get(newsletter_id)

    users_lst = newsletter.dict().get('users')
    user_to_remove = next(user for user in users_lst if user['email'] == delete_email)
    users_lst.remove(user_to_remove)
    newsletter.users = users_lst
    await newsletter.save()

    return newsletter



@newsletter_router.delete("/{newsletter_id}", response_description="Delete weekly newsletter")
async def delete_newsletter(newsletter_id: PydanticObjectId, user_email=Depends(auth_wrapper)) -> dict:
    newsletter_to_delete = await Newsletters.get(newsletter_id)

    if not newsletter_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource not found'
        )

    await newsletter_to_delete.delete()

    return {
        "message": "Newsletter deleted successfully."
    }


