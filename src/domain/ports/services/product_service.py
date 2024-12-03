from abc import ABC, abstractmethod
from typing import List
from src.domain.models.product import Product


class ProductService(ABC):
    @abstractmethod
    def create_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_product(self, id: int) -> Product:
        pass

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def update_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def delete_product(self, id: int) -> bool:
        pass