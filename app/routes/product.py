from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas, models, database

router = APIRouter()


@router.get("/products",
            response_model=list[schemas.ProductResponse],
            status_code=200,
            summary="List of all product",
            description="Get the list of all products with filter.",
            )
def list_products(db: Session = Depends(database.get_db)):
    products = db.execute(select(models.Product)).scalars().all()
    return products


@router.post("/products",
             response_model=schemas.ProductResponse,
             status_code=201,
             summary="Create new product",
             description="Create new product by providing name and price of the product.",
             )
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    new_products = models.Product(**product.model_dump())
    db.add(new_products)
    db.commit()
    db.refresh(new_products)
    return new_products


@router.get("/product/{product_id}",
            response_model=schemas.ProductResponse,
            status_code=200,
            summary="Get the product",
            description="Get the particular product by ID.",
            )
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    product_obj = db.get(models.Product, product_id)
    if product_obj is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_obj


@router.put("/product/{product_id}",
            response_model=schemas.ProductResponse,
            status_code=200,
            summary="Update the product",
            description="Update the particular product by ID.",
            )
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    product_obj = db.get(models.Product, product_id)
    if product_obj is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.model_dump().items():
        setattr(product_obj, key, value)
    db.commit()
    db.refresh(product_obj)
    return product_obj


@router.delete("/product/{product_id}",
               status_code=200,
               summary="Delete the product",
               description="Delete the particular product by ID.",
               )
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    product_obj = db.get(models.Product, product_id)

    if product_obj is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product_obj)
    db.commit()
    return {"detail": "Product deleted"}
