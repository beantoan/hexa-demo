from sqlalchemy import create_engine
from typing import List
from src.domain.ports.repositories.product_repository import ProductRepository
from src.domain.models.product import Product
from .models.product_model import metadata, products
from datetime import datetime


class MySQLProductRepository(ProductRepository):
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        metadata.create_all(self.engine)

    def create(self, product: Product) -> Product:
        with self.engine.connect() as conn:
            now = datetime.utcnow()
            result = conn.execute(
                products.insert().values(
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    created_at=now,
                    updated_at=now
                )
            )
            conn.commit()
            product.id = result.inserted_primary_key[0]
            product.created_at = now
            product.updated_at = now
            return product

    def get_by_id(self, id: int) -> Product | None:
        with self.engine.connect() as conn:
            result = conn.execute(
                products.select().where(products.c.id == id)
            ).first()
            if result:
                return Product(
                    id=result.id,
                    name=result.name,
                    price=result.price,
                    description=result.description,
                    created_at=result.created_at,
                    updated_at=result.updated_at
                )
            return None

    def get_all(self) -> List[Product]:
        with self.engine.connect() as conn:
            results = conn.execute(products.select()).fetchall()
            return [
                Product(
                    id=result.id,
                    name=result.name,
                    price=result.price,
                    description=result.description,
                    created_at=result.created_at,
                    updated_at=result.updated_at
                )
                for result in results
            ]

    def update(self, product: Product) -> Product:
        with self.engine.connect() as conn:
            now = datetime.utcnow()
            conn.execute(
                products.update()
                .where(products.c.id == product.id)
                .values(
                    name=product.name,
                    price=product.price,
                    description=product.description,
                    updated_at=now
                )
            )
            conn.commit()
            product.updated_at = now
            return product

    def delete(self, id: int) -> bool:
        with self.engine.connect() as conn:
            result = conn.execute(
                products.delete().where(products.c.id == id)
            )
            conn.commit()
            return result.rowcount > 0