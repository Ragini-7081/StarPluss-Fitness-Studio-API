
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserSignup(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class FitnessClassCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    date_time: datetime = Field(alias="dateTime")
    instructor: str = Field(min_length=2, max_length=100)
    available_slots: int = Field(
        alias="availableSlots",
        ge=0,
        le=10000,
    )

    @field_validator("date_time")
    @classmethod
    def validate_class_datetime(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError(
                "dateTime must include a timezone, such as +05:30 or Z"
            )
        return value

    model_config = ConfigDict(populate_by_name=True)


class FitnessClassResponse(BaseModel):
    id: int
    name: str
    date_time: datetime = Field(serialization_alias="dateTime")
    instructor: str
    available_slots: int = Field(serialization_alias="availableSlots")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class BookingCreate(BaseModel):
    class_id: int = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=100)
    client_email: EmailStr


class BookingResponse(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookedClassResponse(BaseModel):
    id: int
    name: str
    date_time: datetime = Field(serialization_alias="dateTime")
    instructor: str
    available_slots: int = Field(serialization_alias="availableSlots")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class MyBookingResponse(BaseModel):
    id: int
    client_name: str
    client_email: EmailStr
    created_at: datetime
    fitness_class: BookedClassResponse

    model_config = ConfigDict(from_attributes=True)
