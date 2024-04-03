from pydantic import TypeAdapter

from .schemas import (
    AccountSchema,
    AddPartSchema,
    CarPartSchema,
    CarProducerSchema,
    CarSchema,
    CartSchema,
    CreateAccountSchema,
    CreateShippingSchema,
    PartUnitSchema,
    ShippingSchema
)
from modules.http_requests.repositories.interface import IAsyncRequestRepository


class BackendService:
    car_producers_path: str = "/api/car_producers/"
    cars_list_path: str = "/api/car_producers/{producer_id}/cars"
    parts_list_path: str = "/api/car_producers/{producer_id}/cars/{car_vin}/parts"
    part_path: str = "/api/car_producers/{producer_id}/cars/{car_vin}/parts/{part_id}"

    create_account_path: str = "/telegram/api/account/"
    get_account_path: str = "/telegram/api/account/{account_id}"

    cart_by_user_path: str = "/store/api/users/{user_id}/cart"
    add_to_cart_path: str = "/store/api/users/{user_id}/cart/products"
    cart_product_path: str = "/store/api/users/{user_id}/cart/products/{product_id}"

    shipping_path: str = "/user/api/{user_id}/shipping/"

    submit_order_path: str = "/store/api/users/{user_id}/order/submit"

    search_path: str = "/api/search"

    def __init__(self, repo: IAsyncRequestRepository) -> None:
        self.repo = repo

    async def get_car_producers(self) -> list[CarProducerSchema]:
        _, data = await self.repo.get(self.car_producers_path)
        adapter = TypeAdapter(list[CarProducerSchema])
        return adapter.validate_json(data)


    async def get_cars(self, producer_id: int) -> list[CarSchema]:
        _, data = await self.repo.get(self.cars_list_path.format(producer_id=producer_id))
        adapter = TypeAdapter(list[CarSchema])
        return adapter.validate_json(data)


    async def get_parts(self, producer_id: int, car_vin: str) -> list[CarPartSchema]:
        _, data = await self.repo.get(self.parts_list_path.format(producer_id=producer_id, car_vin=car_vin))
        adapter = TypeAdapter(list[CarPartSchema])
        return adapter.validate_json(data)

    async def get_part(self, producer_id: int, car_vin: str, part_id: int) -> CarPartSchema:
        status, data = await self.repo.get(self.part_path.format(producer_id=producer_id, car_vin=car_vin, part_id=part_id))
        return CarPartSchema.model_validate_json(data)

    async def get_account(self, account_id: int) -> AccountSchema:
        _, data = await self.repo.get(self.get_account_path.format(account_id=account_id))

        return AccountSchema.model_validate_json(data)

    async def create_account(self, id: int, first_name: str, username: str | None, last_name: str | None) -> None:
        account = CreateAccountSchema(id=id, first_name=first_name, username=username, last_name=last_name).model_dump_json()
        await self.repo.post(self.create_account_path, data=account)

    async def get_user_cart(self, user_id: int) -> CartSchema | None:
        status, data = await self.repo.get(self.cart_by_user_path.format(user_id=user_id))
        if status == 404:
            return None
        
        return CartSchema.model_validate_json(data)

    async def add_to_cart(self, user_id: int, part_id: int, quantity: int) -> None:
        product = AddPartSchema(part_id=part_id, quantity=quantity).model_dump_json()
        await self.repo.post(self.add_to_cart_path.format(user_id=user_id), data=product)
    
    async def get_cart_product(self, user_id: int, product_id: int) -> PartUnitSchema | None:
        url = self.cart_product_path.format(user_id=user_id, product_id=product_id)
        status, data = await self.repo.get(url)

        if status == 404:
            return None
        
        return PartUnitSchema.model_validate_json(data)
    

    async def delete_cart_product(self, user_id: int, product_id: int) -> bool:
        url = self.cart_product_path.format(user_id=user_id, product_id=product_id)
        status, _ = await self.repo.delete(url)

        if status == 204:
            return True
        return False

    async def clear_cart(self, user_id: int) -> None:
        await self.repo.delete(self.cart_by_user_path.format(user_id=user_id))
    

    async def get_user_shipping(self, user_id: int) -> ShippingSchema | None:
        url = self.shipping_path.format(user_id=user_id)
        status, data = await self.repo.get(url)

        if status == 404:
            return None
        
        if status == 200:
            return ShippingSchema.model_validate_json(data)
    

    async def create_user_shipping(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        phone_number: int,
        region: str,
        city: str,
        office_number: int,
    ) -> ShippingSchema:
        url = self.shipping_path.format(user_id=user_id)
        data = CreateShippingSchema(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            region=region,
            city=city,
            office_number=office_number
        ).model_dump_json()

        status, data = await self.repo.post(url, data)

        if status in [409, 400]:
            raise

        return ShippingSchema.model_validate_json(data)
    
    
    async def submit_user_order(self, user_id: int) -> None:
        url = self.submit_order_path.format(user_id=user_id)
        status, _ = await self.repo.patch(url, None)

        if status in [404, 500]:
            raise
    

    async def search_products(self, query: str) -> list[CarPartSchema] | None:
        url = self.search_path
        status, data = await self.repo.get(url, params={"keywords": query})

        match status:
            case 404:
                return None
            case 200:
                return TypeAdapter(list[CarPartSchema]).validate_json(data)
            case _:
                raise