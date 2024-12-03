from flask import Flask
import os
from dotenv import load_dotenv

from src.infrastructure.adapters.persistence.csv.csv_product_repository import CSVProductRepository
from src.infrastructure.config.database import DatabaseConfig
from src.infrastructure.adapters.persistence.mysql.mysql_product_repository import MySQLProductRepository
from src.application.services.product_service import ProductService
from src.infrastructure.adapters.api.v1.product_controller import ProductController

load_dotenv()


def create_app():
    app = Flask(__name__)

    # db_config = DatabaseConfig(
    #     host=os.getenv('DB_HOST', 'db'),
    #     port=int(os.getenv('DB_PORT', '3306')),
    #     username=os.getenv('DB_USER', 'user'),
    #     password=os.getenv('DB_PASSWORD', 'password'),
    #     database=os.getenv('DB_NAME', 'products')
    # )

    # repository = MySQLProductRepository(db_config.url)
    repository = CSVProductRepository('products.csv')
    service = ProductService(repository)
    product_controller = ProductController(service)

    app.register_blueprint(product_controller.blueprint, url_prefix='/products')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)