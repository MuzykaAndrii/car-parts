from backend import endpoints, schemas


async def get_car_producers() -> list[schemas.CarProducerSchema]:
    endpoint =  endpoints.get_car_producers_endpoint()


async def get_cars(producer_id: int) -> list[schemas.CarSchema]:
    endpoint =  endpoints.get_cars_endpoint(producer_id=producer_id)


async def get_parts(producer_id: int, car_vin: str) -> list[schemas.CarPartSchema]:
    endpoint =  endpoints.get_parts_endpoint(producer_id=producer_id, car_vin=car_vin)


async def get_account(account_id: int) -> schemas.AccountSchema:
    endpoint = await endpoints.get_account_endpoint()
    return await endpoint(account_id=account_id)


async def create_account(id: int, first_name: str, username: str | None, last_name: str | None) -> None:
    await endpoints.create_account_endpoint(
        id=id,
        first_name=first_name,
        username=username,
        last_name=last_name,
    )


async def get_user_cart(user_id: int) -> schemas.CartSchema | None:
    endpoint = await endpoints.get_user_cart_endpoint()
    return await endpoint(user_id=user_id)


async def add_to_cart(user_id: int, part_id: int, quantity: int) -> None:
    await endpoints.add_to_cart_endpoint(user_id=user_id, part_id=part_id, quantity=quantity)


async def clear_cart(user_id: int) -> None:
    await endpoints.clear_cart_endpoint(user_id=user_id)
