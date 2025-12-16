from fastapi import APIRouter, Depends, HTTPException
from shop_app.database.models import ProductImage
from shop_app.database.schema import ProductImageOutSchema, ProductImageInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List



product_images_router = APIRouter(prefix='/product_image', tags=['Product_Images'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_images_router.post('/', response_model=ProductImageOutSchema)
async def create_product_image(image: ProductImageInputSchema, db: Session = Depends(get_db)):
    image_db = ProductImage(**image.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db


@product_images_router.get('/', response_model=List[ProductImageOutSchema])
async def list_product_image(db: Session = Depends(get_db)):
    return db.query(ProductImage).all()


@product_images_router.get('/{image_id}/', response_model=ProductImageOutSchema)
async def detail_product_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id==image_id).first()
    if not image:
        raise HTTPException(status_code=400, detail='Мындай id жок')
    return image



@product_images_router.put("/{image_id}/", response_model=ProductImageOutSchema)
async def update_product_image(image_id: int, image_data: ProductImageInputSchema,db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=400, detail="Image not found")

    for key, value in image_data.dict().items():
        setattr(image, key, value)

    db.commit()
    db.refresh(image)
    return image


@product_images_router.delete("/{image_id}")
async def delete_product_image(image_id: int,db: Session = Depends(get_db)):
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=400, detail="Image not found")

    db.delete(image)
    db.commit()
    return {"detail": "Image deleted successfully"}





