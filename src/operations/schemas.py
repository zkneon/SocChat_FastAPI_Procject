from datetime import datetime

from pydantic import BaseModel


class OperationCreate(BaseModel):
    id: int
    quantity: str
    instrument_type: str
    date: datetime
    type: str

    class Config:
        from_attribute = True



