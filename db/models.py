from sqlalchemy import Column, Integer, LargeBinary, String
from db.database import Base

class Categories(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    category_name = Column(String(15), index=True)
    description = Column(String)
    picture = Column(LargeBinary, nullable=True)
