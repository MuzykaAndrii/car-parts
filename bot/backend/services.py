from pydantic import TypeAdapter

from backend.schemas import AccountSchema, AddPartSchema, CarPartSchema, CarProducerSchema, CarSchema, CartSchema, CreateAccountSchema
from backend.repository import AiohttpRepository


class BackendService:
    car_producers_path: str = "/api/car_producers/"
    cars_list_path: str = "/api/car_producers/{producer_id}/cars"
    parts_list_path: str = "/api/car_producers/{producer_id}/cars/{car_vin}/parts"
    part_path: str = "/api/car_producers/{producer_id}/cars/{car_vin}/parts/{part_id}"

    create_account_path: str = "/telegram/api/account/"
    get_account_path: str = "/telegram/api/account/{account_id}"

    cart_by_user_path: str = "/store/api/users/{user_id}/cart"
    add_to_cart_path: str = "/store/api/users/{user_id}/cart/products"

    def __init__(self, repo: AiohttpRepository) -> None:
        self.repo = repo

    async def get_car_producers(self) -> list[CarProducerSchema]:
        response = await self.repo.get(self.car_producers_path)
        adapter = TypeAdapter(list[CarProducerSchema])
        return adapter.validate_json(response.body)


    async def get_cars(self, producer_id: int) -> list[CarSchema]:
        response = await self.repo.get(self.cars_list_path.format(producer_id=producer_id))
        adapter = TypeAdapter(list[CarSchema])
        return adapter.validate_json(response.body)


    async def get_parts(self, producer_id: int, car_vin: str) -> list[CarPartSchema]:
        response = await self.repo.get(self.parts_list_path.format(producer_id=producer_id, car_vin=car_vin))
        adapter = TypeAdapter(list[CarPartSchema])
        return adapter.validate_json(response.body)

    async def get_part(self, producer_id: int, car_vin: str, part_id: int) -> CarPartSchema:
        response = await self.repo.get(self.part_path.format(producer_id=producer_id, car_vin=car_vin, part_id=part_id))
        return CarPartSchema.model_validate_json(response.body)

    async def get_account(self, account_id: int) -> AccountSchema:
        response = await self.repo.get(self.get_account_path.format(account_id=account_id))

        return AccountSchema.model_validate_json(response.body)

    async def create_account(self, id: int, first_name: str, username: str | None, last_name: str | None) -> None:
        account = CreateAccountSchema(id=id, first_name=first_name, username=username, last_name=last_name).model_dump_json()
        await self.repo.post(self.create_account_path, data=account)

    async def get_user_cart(self, user_id: int) -> CartSchema | None:
        response = await self.repo.get(self.cart_by_user_path.format(user_id=user_id))
        if response.status_code == 404:
            return None
        
        return CartSchema.model_validate_json(response.body)

    async def add_to_cart(self, user_id: int, part_id: int, quantity: int) -> None:
        product = AddPartSchema(part_id=part_id, quantity=quantity).model_dump_json()
        await self.repo.post(self.add_to_cart_path.format(user_id=user_id), data=product)

    async def clear_cart(self, user_id: int) -> None:
        await self.repo.delete(self.cart_by_user_path.format(user_id=user_id))