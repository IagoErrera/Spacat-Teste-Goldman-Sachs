from pydantic import BaseModel, Field
from datetime import date, datetime
import uuid

class UserRequest(BaseModel):
    firstName: str
    lastName: str
    addressStreet: str = None
    addressCity: str = None
    addressState: str = None
    addressZip: str = None
    birthDate: date = None

class User(BaseModel):
    userId: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="customer_id")
    firstName: str
    lastName: str
    addressStreet: str = None
    addressCity: str = None
    addressState: str = None
    addressZip: str = None
    birthDate: date = None
    registrationDate: datetime = Field(default_factory=datetime.now)
    lastUpdated: datetime = Field(default_factory=datetime.now)

    def update_fields(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
