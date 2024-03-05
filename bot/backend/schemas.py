from pydantic import BaseModel


class CarProducerSchema(BaseModel):
    id: int
    name: str


class CarProducersListSchema(BaseModel):
    producers: list[CarProducerSchema]


class CarSchema(BaseModel):
    vin: str
    model: str
    producer: int
    year_of_production: int
    engine_volume: float
    wheel_drive: str
    fuel: str
    body: str


class CarListSchema(BaseModel):
    cars: list[CarSchema]


class CarPartSchema(BaseModel):
    id: int
    name: str
    articul: str
    barcode: str
    sell_price: float
    producer: str
    belongs_to: str


class CarPartsListSchema(BaseModel):
    parts: list[CarPartSchema]