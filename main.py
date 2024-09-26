from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from typing import List, Annotated, Optional
from database import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Pydantic models
class CategoryBase(BaseModel):
    category_name: str
    description: str
    picture: Optional[bytes] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int

    class Config:
        orm_mode = True

# Para OrderDetails
# class OrderDetailBase(BaseModel):
#     unit_price: int
#     quantity: int
#     discount: int

# class OrderDetailCreate(OrderDetailBase):
#     pass

# class OrderDetail(OrderDetailBase):
#     order_id: int
#     product_id: int

#     class Config:
#         orm_mode = True


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}

db_dependency = Annotated[Session, Depends(get_db)]
#///////////////////////////////////////////////////////////////////////////////////////////////////////
# Create a new category //hacer excepcion
@app.post("/categories/")
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe una categoría con el mismo nombre
    existing_category = db.query(models.Categories).filter(models.Categories.category_name == category.category_name).first()
    if existing_category:
        raise HTTPException(status_code=409, detail="Category name already exists")
    
    # Encontrar el máximo category_id e incrementarlo en 1
    max_id = db.query(models.Categories.category_id).order_by(models.Categories.category_id.desc()).first()
    new_id = (max_id[0] + 1) if max_id else 1
    
    db_category = models.Categories(
        category_id=new_id,
        category_name=category.category_name,
        description=category.description,
        picture=category.picture
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    # Contar el número total de registros en la base de datos
    total_records = db.query(models.Categories).count()
    
    return {"message": "Category created successfully", "added_records": 1, "total_records": total_records}


# # Create a new order detail
# @app.post("/order_details/", response_model=OrderDetail)
# async def create_order_detail(order_detail: OrderDetailCreate, db: Session = Depends(get_db)):
#     # Find the maximum order_id and product_id and increment them by 1
#     max_order_id = db.query(models.order_details.order_id).order_by(models.order_details.order_id.desc()).first()
#     max_product_id = db.query(models.order_details.product_id).order_by(models.order_details.product_id.desc()).first()
    
#     new_order_id = (max_order_id[0] + 1) if max_order_id else 1
#     new_product_id = (max_product_id[0] + 1) if max_product_id else 1
    
#     db_order_detail = models.order_details(
#         order_id=new_order_id,
#         product_id=new_product_id,
#         unit_price=order_detail.unit_price,
#         quantity=order_detail.quantity,
#         discount=order_detail.discount
#     )
#     db.add(db_order_detail)
#     db.commit()
#     db.refresh(db_order_detail)
    
#     # Count the total number of records in the database
#     total_records = db.query(models.order_details).count()
#     return {"message": "Order detail created successfully", "added_records": 1, "total_records": total_records}


# Read a category by ID //hacer exepcion
@app.get("/category/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# Read all categories with pagination // hacer exepcion .... >=1
@app.get("/categories/{page}", response_model=List[Category])
def read_categories(page: int, db: Session = Depends(get_db)):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page should be >=1")
    limit = 100
    skip = (page - 1) * limit
    categories = db.query(models.Categories).offset(skip).limit(limit).all()
    return categories

# # Read all order details with pagination
# @app.get("/order_details/{page}", response_model=List[OrderDetail])
# def read_order_details(page: int, db: Session = Depends(get_db)):
#     limit = 100
#     skip = (page - 1) * limit
#     order_details = db.query(models.order_details).offset(skip).limit(limit).all()
#     return order_details

# #Read an order detail by order_id and product_id
# @app.get("/order_detail/{order_id}/{product_id}", response_model=OrderDetail)
# def read_order_detail(order_id: int, product_id: int, db: Session = Depends(get_db)):
#     db_order_detail = db.query(models.order_details).filter(models.order_details.order_id == order_id).filter(models.order_details.product_id == product_id).first()
#     if db_order_detail is None:
#         raise HTTPException(status_code=404, detail="Order detail not found")
#     return db_order_detail

# Update a category by ID
@app.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category.category_name = category.category_name
    db_category.description = category.description
    db.commit()
    db.refresh(db_category)
    return db_category

# Delete a category by ID
@app.delete("/categories/{category_id}", response_model=Category)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return db_category


# Function to populate the categories table
@app.post("/populate_categories/")
def populate_categories(db: Session = Depends(get_db)):
    existing_count = db.query(models.Categories).count()
    target_count = 1000
    categories_to_add = target_count - existing_count

    max_id = db.query(models.Categories.category_id).order_by(models.Categories.category_id.desc()).first()
    new_id = (max_id[0] + 1) if max_id else 1

    for i in range(categories_to_add):
        new_category = models.Categories(
            category_id=new_id + i,
            category_name=f"Category {existing_count + i + 1}",
            description=f"Description for category {existing_count + i + 1}",
            picture=None  # or some default picture
        )
        db.add(new_category)
    
    db.commit()
    return {"message": f"Added {categories_to_add} categories to the database."}