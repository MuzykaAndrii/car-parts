from components import backend_session
from backend.schemas import CarPartSchema, CarProducerSchema, CarSchema, AccountSchema, CreateAccountSchema, CartSchema, AddPartSchema
from backend.requests import GetManager, CreateManager, DeleteManager, UrlBuilder


async def get_car_producers_endpoint() -> GetManager[CarProducerSchema]:
    return GetManager[CarProducerSchema](
        session=backend_session(),
        url_builder=UrlBuilder("/api/car_producers/"),
        response_schema=CarProducerSchema,
        response_many=True,
        success_statuses=(200,),
    )

async def get_cars_endpoint() -> GetManager[CarSchema]:
    return GetManager[CarSchema](
        session=backend_session(),
        url_builder=UrlBuilder("/api/car_producers/{producer_id}/cars"),
        response_schema=CarSchema,
        response_many=True,
        success_statuses=(200,),
    )

async def get_parts_endpoint() -> GetManager[CarPartSchema]:
    return GetManager[CarPartSchema](
        session=backend_session(),
        url_builder=UrlBuilder("/api/car_producers/{producer_id}/cars/{car_vin}/parts"),
        response_schema=CarPartSchema,
        response_many=True,
        success_statuses=(200,),
    )

async def get_part_endpoint() -> GetManager[CarPartSchema]:
    return GetManager[CarPartSchema](
        session=backend_session(),
        url_builder=UrlBuilder("/api/car_producers/{producer_id}/cars/{car_vin}/parts/{part_id}"),
        response_schema=CarPartSchema,
        response_many=False,
        success_statuses=(200,),
    )

async def get_account_endpoint() -> GetManager[AccountSchema]:
    return GetManager[AccountSchema](
        session=backend_session(),
        url_builder=UrlBuilder("/telegram/api/account/{account_id}"),
        response_schema=AccountSchema,
        response_many=False,
        success_statuses=(200,),
    )

async def create_account_endpoint() -> CreateManager:
    return CreateManager(
        session=backend_session(),
        url_builder=UrlBuilder("/telegram/api/create_account/"),
        create_schema=CreateAccountSchema,
        success_statuses=(201,),
    )

async def get_user_cart_endpoint() -> GetManager[CartSchema]:
    return GetManager[CartSchema](
        session=backend_session(),
        url_builder=UrlBuilder("/store/api/users/{user_id}/cart"),
        response_schema=CartSchema,
        response_many=False,
        success_statuses=(200, 404),
    )

async def add_to_cart_endpoint() -> CreateManager:
    return CreateManager(
        session=backend_session(),
        url_builder=UrlBuilder("/store/api/users/{user_id}/cart/products"),
        create_schema=AddPartSchema,
        success_statuses=(201,),
    )

async def clear_cart_endpoint() -> DeleteManager:
    return DeleteManager(
        session=backend_session(),
        url_builder=UrlBuilder("/store/api/users/{user_id}/cart"),
        success_statuses=(204,),
    )
