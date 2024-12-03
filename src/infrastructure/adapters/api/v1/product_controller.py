from typing import Any

from flask import Blueprint, request, jsonify

from src.application.services.product_service import ProductService
from src.domain.exceptions.domain_exceptions import ProductNotFoundError
from src.domain.models.product import Product


class ProductController:
    def __init__(self, service: ProductService):
        self.service = service
        self.blueprint = Blueprint('products', __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.route('/', methods=['POST'])(self.create_product)
        self.blueprint.route('/<int:product_id>', methods=['GET'])(self.get_product)
        self.blueprint.route('/', methods=['GET'])(self.get_all_products)
        self.blueprint.route('/<int:product_id>', methods=['PUT'])(self.update_product)
        self.blueprint.route('/<int:product_id>', methods=['DELETE'])(self.delete_product)

    def create_product(self) -> tuple[dict[str, Any], int]:
        try:
            data = request.get_json()
            product = Product(**data)
            created_product = self.service.create_product(product)
            return jsonify(created_product.__dict__), 201
        except Exception as e:
            return {'error': str(e)}, 400

    def get_product(self, product_id: int) -> tuple[dict[str, Any], int]:
        try:
            product = self.service.get_product(product_id)
            return jsonify(product.__dict__), 200
        except ProductNotFoundError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 500

    def get_all_products(self) -> tuple[dict[str, Any], int]:
        try:
            products = self.service.get_all_products()
            return jsonify([p.__dict__ for p in products]), 200
        except Exception as e:
            return {'error': str(e)}, 500

    def update_product(self, product_id: int) -> tuple[dict[str, Any], int]:
        try:
            data = request.get_json()
            data['id'] = product_id
            product = Product(**data)
            updated_product = self.service.update_product(product)
            return jsonify(updated_product.__dict__), 200
        except ProductNotFoundError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 400

    def delete_product(self, product_id: int) -> tuple[dict[str, Any], int]:
        try:
            self.service.delete_product(product_id)
            return '', 204
        except ProductNotFoundError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': str(e)}, 500