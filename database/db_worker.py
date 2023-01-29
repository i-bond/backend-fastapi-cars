import beanie
from motor.motor_asyncio import AsyncIOMotorClient
from models.cars import Cars
from models.users import UsersPublic
from models.newsletters import Newsletters
from pprint import pprint
from decouple import config

# Load .env variables
DB_URL = config('DB_URL', default='mongodb://localhost:27017', cast=str)
DB_NAME = config('DB_NAME', default='carsDB', cast=str)


async def connect_db():
    client = AsyncIOMotorClient(DB_URL)
    await beanie.init_beanie(database=client[DB_NAME], document_models=[Cars, UsersPublic, Newsletters])


    # Adding Newsletter
    from datetime import date
    # user = await UsersPublic.find_one(UsersPublic.username == 'Jack')
    # # print(user)
    # few_cars = await Cars.find(Cars.brand == 'Citroen').limit(3).to_list()
    # newsletter1 = Newsletters(users=[user], new_cars=few_cars)
    # pprint(newsletter1.dict())
    # await newsletter1.create()

    # newsletters = await Newsletters.find().to_list()
    # print(newsletters)

    # Forming one newsletter
    # from beanie.operators import In
    # import datetime
    # all_users = await UsersPublic.find(In(UsersPublic.role, ["USER", "Fruits"])).to_list()
    # # print(all_users)
    # dt = datetime.datetime.today()
    # # print(dt)
    # all_cars = await Cars.find(Cars.date_added <= datetime.datetime.today()).to_list()
    # print(all_cars)
    # newsletter2 = Newsletters(users=all_users, new_cars=all_cars)
    # print(newsletter2)
    # await newsletter2.create()


    # Updating newsletter
    # newsletter_id = '63b2b6bd0b47f0839166a049'
    # user_email = 'jack@mail.com'
    # newsletter = await Newsletters.get(newsletter_id)
    # # print(newsletter_dict)
    # users_lst = newsletter.dict().get('users')
    # # for user in users_lst:
    # #     if user['email'] == user_email:
    # #         print('user')
    # user_to_remove = next(user for user in users_lst if user['email'] == user_email)
    # users_lst.remove(user_to_remove)
    # print(users_lst)
    # newsletter.users = users_lst
    # pprint(newsletter.dict())


    # for user in newsletter.users:
    #     if user['email'] == user_email:
    #         print('user')

    # newsletter.users.remove()
    # print(users_lst)
    # user_to_delete = [user for user in newsletter.get('users') if user['email'] == user_email]
    # print(user_to_delete)





    from auth.auth_handler import hash_password
    from fastapi.responses import JSONResponse
    from fastapi import HTTPException, status
    from fastapi.encoders import jsonable_encoder
    from auth.auth_handler import verify_hash, create_access_token




    # User Login
    # loginuser = Users(username='jack', email='jack@mail.com', password='justdoit')
    # user_exist = await Users.find_one(Users.email == loginuser.email)
    # print(user_exist)
    # print(user_exist.dict(include={'email', 'role'}))

    # if (user_exist is None) or (not verify_hash(loginuser.password, user_exist.password)):
    #     raise HTTPException(status_code=401, detail="Invalid email and/or password")
    # token = create_access_token(user_exist.email)
    # jsonable = jsonable_encoder(user_exist)
    # print(jsonable); print(type(jsonable))
    # return JSONResponse(
    #     content={"token": token,
    #              "user": jsonable_encoder(user_exist)
    #     }
    # )

    # Register new user
    # new_user = Users(username='jack', email='jack@mail.com', password='justdoit')
    # print(new_user)
    #
    # email_exist = await Users.find_one(Users.email == new_user.email)
    # username_exist = await Users.find_one(Users.username == new_user.username)
    # if email_exist or username_exist:
    #     raise HTTPException(
    #         status_code=409, detail=f"User with specified email/username already exists"
    #     )
    #
    # new_user.password = hash_password(new_user.password)
    # print(new_user)
    # await new_user.insert()
    # created_user = await Users.find_one(Users.username == new_user.username)
    #
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(created_user))


    # Test update car
    # class CarUpdate(BaseModel):
    #     price: Optional[int] = None
    #     year: Optional[int] = 10

    # updated_car = CarUpdate()
    # updated_car.price = 10420
    # updated_car.year = 2021
    # print(updated_car.dict(exclude_unset=True))
    #
    # # Update Car
    # car_id = "63ac6f5a1bd7cc9b907cdffb"
    # car = await Cars.get(car_id)
    # await car.update(Set(updated_car.dict(exclude_unset=True)))
    # new_car = await Cars.get(car_id)
    # print(new_car)








if __name__ == "__main__":
    import asyncio
    asyncio.run(connect_db())



















