from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship
from database import Base

class Categories(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    category_name = Column(String(15), index=True)
    description = Column(String)
    picture = Column(LargeBinary, nullable=True)


# class Orders(Base):
#     __tablename__ = "orders"
#     order_id = Column(Integer, primary_key=True, index=True)
#     customer_id = Column(Integer, ForeignKey("customer.customer_id"), index=True)
#     employee_id = Column(Integer, ForeignKey("employees.employee_id"), index=True)
#     ship_via = Column(Integer, ForeignKey("shippers.shipper_id"), index=True)
#     order_date = Column(Date)
#     required_date = Column(Date)
#     shipped_date = Column(Date)
#     freight = Column(Integer)
#     ship_name = Column(String)
#     ship_address = Column(String)
#     ship_city = Column(String)
#     ship_region = Column(String)
#     ship_postal_code = Column(String)
#     ship_country = Column(String)
#     order_details = relationship("OrderDetails", back_populates="order")


# class order_details(Base):
#     __tablename__ = "order_details"
#     order_id = Column(Integer, ForeignKey("orders.order_id"), primary_key=True, index=True)
#     product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True, index=True)
#     unit_price = Column(Integer)
#     quantity = Column(Integer)
#     discount = Column(Integer)

#     order = relationship("Orders", back_populates="order_details")

