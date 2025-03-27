from dataclasses import dataclass


@dataclass
class BaseResponse:
    status: bool
    http_code: int


@dataclass
class AuthResponse(BaseResponse):
    @dataclass
    class AuthResponseData:
        token: str
        expiration_time: str
        token_type: str

    access_token: AuthResponseData


@dataclass
class ClientInfo:
    id: int
    last_name: str
    name: str
    patronymic: str
    birth_date: str
    registered_city: str
    address: str
    actual_address: str
    place_of_birth: str
    phone: str = None
    email: str = None
    nationality: int = None
    inn: str = None
    snils: str = None
    bonuses: int = None
