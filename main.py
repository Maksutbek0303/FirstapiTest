from fastapi import FastAPI
from shop_app.api import (users, categories, subcategory,
                          product, pro_image, reviews, auth)
import uvicorn


shop_app = FastAPI(title='Store Project')
shop_app.include_router(users.users_router)
shop_app.include_router(categories.category_router)
shop_app.include_router(subcategory.subcategory_router)
shop_app.include_router(product.product_router)
shop_app.include_router(pro_image.product_images_router)
shop_app.include_router(reviews.review_router)
shop_app.include_router(auth.auth_router)




if __name__ == '__main__':
    uvicorn.run(shop_app, host='127.0.0.1', port=8001)





