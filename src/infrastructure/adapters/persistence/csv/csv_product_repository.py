import csv
from datetime import datetime
from typing import List
from pathlib import Path
from src.domain.ports.repositories.product_repository import ProductRepository
from src.domain.models.product import Product


class CSVProductRepository(ProductRepository):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self._initialize_file()

    def _initialize_file(self):
        if not self.file_path.exists():
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file,
                                        fieldnames=['id', 'name', 'price', 'description', 'created_at', 'updated_at'])
                writer.writeheader()

    def _get_next_id(self) -> int:
        products = self._read_all()
        return max([p.id or 0 for p in products], default=0) + 1

    def _read_all(self) -> List[Product]:
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            return [
                Product(
                    id=int(row['id']),
                    name=row['name'],
                    price=float(row['price']),
                    description=row['description'],
                    created_at=datetime.fromisoformat(row['created_at']),
                    updated_at=datetime.fromisoformat(row['updated_at'])
                )
                for row in reader
            ]

    def _write_all(self, products: List[Product]):
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'price', 'description', 'created_at', 'updated_at'])
            writer.writeheader()
            for product in products:
                writer.writerow({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'description': product.description,
                    'created_at': product.created_at.isoformat(),
                    'updated_at': product.updated_at.isoformat()
                })

    def create(self, product: Product) -> Product:
        product.id = self._get_next_id()
        product.created_at = datetime.utcnow()
        product.updated_at = product.created_at
        products = self._read_all()
        products.append(product)
        self._write_all(products)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        products = self._read_all()
        return next((p for p in products if p.id == product_id), None)

    def get_all(self) -> List[Product]:
        return self._read_all()

    def update(self, product: Product) -> Product:
        products = self._read_all()
        for i, p in enumerate(products):
            if p.id == product.id:
                product.created_at = p.created_at
                product.updated_at = datetime.utcnow()
                products[i] = product
                self._write_all(products)
                return product
        raise ValueError(f"Product with id {product.id} not found")

    def delete(self, product_id: int) -> bool:
        products = self._read_all()
        initial_count = len(products)
        products = [p for p in products if p.id != product_id]
        if len(products) < initial_count:
            self._write_all(products)
            return True
        return False