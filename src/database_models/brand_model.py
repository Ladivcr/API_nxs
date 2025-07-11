from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# MODELOS
class BrandModel(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
