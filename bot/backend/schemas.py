from pydantic import BaseModel


class CarProducerSchema(BaseModel):
    id: int
    name: str


class CarSchema(BaseModel):
    vin: str
    model: str
    producer_id: int
    producer_name: str
    year_of_production: int
    engine_volume: float
    wheel_drive: str
    fuel: str
    body: str


class CarPartSchema(BaseModel):
    id: int
    name: str
    articul: str
    barcode: str
    sell_price: float
    producer: str
    belongs_to: str
