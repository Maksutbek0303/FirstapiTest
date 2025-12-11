from fastapi import APIRouter, Depends, HTTPException
from shop_app.database.models import UserProfile
from shop_app.database.schema import UserProfileOutSchema, UserProfileInputSchema
from shop_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List


users_router = APIRouter(prefix='/users', tags=['UserProfile'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@users_router.post('/', response_model=UserProfileOutSchema)
async def create_user(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@users_router.get('/', response_model=List[UserProfileOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@users_router.get('/{user_id}/', response_model=UserProfileOutSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id==user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Мындай id адам жок')
    return user


@users_router.put("/{user_id}", response_model=UserProfileOutSchema)
async def update_user(user_id: int, user_data: UserProfileInputSchema,db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@users_router.patch("/{user_id}", response_model=UserProfileOutSchema)
async def patch_user(
    user_id: int,
    user_data: UserProfileInputSchema,
    db: Session = Depends(get_db)
):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@users_router.delete("/{user_id}")
async def delete_user(user_id: int,db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}



