from datetime import datetime

from pydantic import BaseModel, AnyHttpUrl, Field

from common.phonenumber import PhoneNumber


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
    producer_detail_url: AnyHttpUrl
    part_url: AnyHttpUrl
    belongs_to: str


class PartUnitSchema(BaseModel):
    id: int
    quantity: int
    sell_price: float
    total_price: float
    part: CarPartSchema


class CreateAccountSchema(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    username: str | None


class UserSchema(BaseModel):
    id: int
    email: str | None
    username: str
    first_name: str | None
    last_name: str | None
    is_active: bool
    is_superuser: bool


class AccountSchema(CreateAccountSchema):
    user: UserSchema


class CartSchema(BaseModel):
    id: int
    status: str
    sold_at: datetime
    total: float
    total_quantity: int
    products: list[PartUnitSchema]
    customer: UserSchema


class AddPartSchema(BaseModel):
    part_id: int
    quantity: int = 1


class CreateShippingSchema(BaseModel):
    first_name: str = Field(title="Введіть ваше імя")
    last_name: str = Field(title="Введіть ваше прізвище")
    phone_number: PhoneNumber = Field(title="Введіть ваш номер телефону")
    region: str = Field(title="Введіть область")
    city: str = Field(title="Введіть населений пункт")
    office_number: int = Field(gt=0, title="Введіть номер відділення НП")


class ShippingSchema(CreateShippingSchema):
    user_id: int
