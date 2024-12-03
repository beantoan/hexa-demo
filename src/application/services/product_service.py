from typing import List

from src.domain.exceptions.domain_exceptions import ProductNotFoundError
from src.domain.models.product import Product
from src.domain.ports.repositories.product_repository import ProductRepository
from src.domain.ports.services.product_service import ProductService as ProductServicePort


class ProductService(ProductServicePort):
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(self, product: Product) -> Product:
        return self.repository.create(product)

    def get_product(self, id: int) -> Product:
        product = self.repository.get_by_id(id)
        if not product:
            raise ProductNotFoundError(f"Product with id {id} not found")
        return product

    def get_all_products(self) -> List[Product]:
        return self.repository.get_all()

    def update_product(self, product: Product) -> Product:
        if not self.repository.get_by_id(product.id):
            raise ProductNotFoundError(f"Product with id {product.id} not found")
        return self.repository.update(product)

    def delete_product(self, id: int) -> bool:
        if not self.repository.get_by_id(id):
            raise ProductNotFoundError(f"Product with id {id} not found")
        return self.repository.delete(id)
