from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from dependencies import Base
import uuid

class Unit(Base):
    __tablename__ = "units"
    unit_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)