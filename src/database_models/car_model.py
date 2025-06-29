from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from database_models.brand_model import BrandModel
from sqlalchemy.orm import relationship
Base = declarative_base()


class ModelCarModel(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String(70), unique=True, nullable=False)
    average_price = Column(Numeric(10, 2))
    brand_id = Column(Integer, ForeignKey(BrandModel.id), onupdate="CASCADE", nullable=False)
    brand = relationship(BrandModel, backref="models", primaryjoin=brand_id == BrandModel.id)
