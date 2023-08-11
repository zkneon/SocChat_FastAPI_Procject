from datetime import datetime

from sqlalchemy import Column, Table, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Operation(Base):
    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[str] = mapped_column(String)
    instrument_type: Mapped[str] = mapped_column(String)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    type: Mapped[str] = mapped_column(String)
