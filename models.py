from sqlalchemy import Column, Numeric, Integer, String
from database import Base

from sqlalchemy.orm import relationship


class Data_Table(Base):
    __tablename__ = "table1"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    col1 = Column(Numeric(10, 2))
    col2 = Column(Numeric(10, 2))
    col3 = Column(Numeric(10, 2))
    # col4 = Column(Numeric(10, 2))
