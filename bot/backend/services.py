from aiohttp import ClientSession

from backend.schemas import CarPartSchema, CarProducerSchema, CarSchema


class BackendService:
    car_producers_path: str = "/api/car_producers/"
    cars_list_path: str = "/api/car_producers/{producer_id}/cars"
    parts_list_path: str = "/api/car_producers/{producer_id}/cars/{car_vin}/parts"
    part_path: str = "/api/car_producers/{producer_id}/cars/{car_vin}/parts/{part_id}"

    def __init__(self, session: ClientSession) -> None:
        self.session = session
    
    async def get_car_producers(self) -> list[CarProducerSchema]:
        async with self.session.get(self.car_producers_path) as resp:
            car_producers = await resp.json()
        
        return [CarProducerSchema(**cp) for cp in car_producers]
    
    async def get_cars(self, producer_id: int) -> list[CarSchema]:
        async with self.session.get(self.cars_list_path.format(producer_id=producer_id)) as resp:
            cars = await resp.json()
        
        return [CarSchema(**car) for car in cars]
    
    async def get_parts(self, producer_id: int, car_vin: str) -> list[CarPartSchema]:
        async with self.session.get(self.parts_list_path.format(producer_id=producer_id, car_vin=car_vin)) as resp:
            parts = await resp.json()
        
        return [CarPartSchema(**part) for part in parts]
    
    async def get_part(self, producer_id: int, car_vin: str, part_id: int) -> CarPartSchema:
        async with self.session.get(self.part_path.format(producer_id=producer_id, car_vin=car_vin, part_id=part_id)) as resp:
            part = await resp.json()
        
        return CarPartSchema(**part)