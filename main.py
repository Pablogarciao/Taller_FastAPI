from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from typing import List, Annotated
from database import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Pydantic models
class CategoryBase(BaseModel):
    category_name: str
    description: str
    picture: bytes = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int

    class Config:
        orm_mode = True

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

# Create a new category
@app.post("/categories/")
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    print(db.query(models.Categories).count())
    
    # Find the maximum category_id and increment it by 1
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
    
    # Count the total number of records in the database
    total_records = db.query(models.Categories).count()
    return {"message": "Category created successfully", "added_records": 1, "total_records": total_records}


# Read a category by ID
@app.get("/category/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# # Read all categories
# @app.get("/categories/", response_model=List[Category])
# def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     categories = db.query(models.Categories).offset(skip).limit(limit).all()
#     return categories

# Read all categories with pagination
@app.get("/categories/{page}", response_model=List[Category])
def read_categories(page: int, db: Session = Depends(get_db)):
    limit = 100
    skip = (page - 1) * limit
    categories = db.query(models.Categories).offset(skip).limit(limit).all()
    return categories

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