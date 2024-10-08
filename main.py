from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import db.models as models
from sqlalchemy.orm import Session
from db.database import SessionLocal
from typing import List, Optional

app = FastAPI()

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


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    
    return {
        "message": "Category created successfully", 
        "added_records": 1, 
        "total_records": total_records,
        "data": {
            "category_id": db_category.category_id,
            "category_name": db_category.category_name,
            "description": db_category.description,
            "picture": db_category.picture
        }
    }


# Read a category by ID
@app.get("/category/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Categories).filter(models.Categories.category_id == category_id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

 
# Read all categories with pagination
@app.get("/categories/{page}", response_model=List[Category])
def read_categories(page: int, db: Session = Depends(get_db)):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page should be >=1")
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
    if category.picture:
      db_category.picture = category.picture
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
