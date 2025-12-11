from fastapi import APIRouter, Depends, HTTPException
from shop_app.database.models import Product
from shop_app.database.schema import ProductOutSchema, ProductInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


product_router = APIRouter(prefix='/product', tags=['Product'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/', response_model=ProductOutSchema)
async def create_product(product: ProductInputSchema, db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/', response_model=List[ProductOutSchema])
async def list_product(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get('/{product_id}/', response_model=ProductOutSchema)
async def detail_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id==product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail='Мындай id жок')
    return product




