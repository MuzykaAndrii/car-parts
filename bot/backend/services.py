from aiohttp import ClientSession

from backend.schemas import CarProducerSchema


class BackendService:
    car_producers_path: str = "/api/car_producers/"
    cars_list_path: str = "/api/car_producers/{producer_id}/cars"
    car_parts_path: str = "/api/car_producers/{producer_id}/cars/{car_vin}/parts"

    def __init__(self, session: ClientSession) -> None:
        self.session = session
    
    async def get_car_producers(self) -> list[CarProducerSchema]:
        async with self.session.get(self.car_producers_path) as response:
            car_producers = await response.json()
        
        return [CarProducerSchema(**cp) for cp in car_producers]