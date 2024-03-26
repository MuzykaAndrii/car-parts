from pydantic_extra_types.phone_numbers import PhoneNumber as PydanticPhoneNumber


class PhoneNumber(PydanticPhoneNumber):
    min_length: str = 10
    max_length: str = 13
    phone_format: str = "NATIONAL"
    default_region_code: str = "UA"