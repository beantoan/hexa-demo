import pytest
from unittest.mock import Mock
from datetime import datetime
from src.domain.models.product import Product
from src.domain.ports.repositories.product_repository import ProductRepository
from src.application.services.product_service import ProductService
from src.domain.exceptions.domain_exceptions import ProductNotFoundError


@pytest.fixture
def repository():
    return Mock(spec=ProductRepository)


@pytest.fixture
def service(repository):
    return ProductService(repository)


@pytest.fixture
def sample_product():
    return Product(
        id=1,
        name="Test Product",
        price=99.99,
        description="Test Description",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


def test_create_product(service, repository, sample_product):
    repository.create.return_value = sample_product
    result = service.create_product(sample_product)
    repository.create.assert_called_once_with(sample_product)
    assert result == sample_product


def test_get_product_not_found(service, repository):
    repository.get_by_id.return_value = None
    with pytest.raises(ProductNotFoundError):
        service.get_product(999)


def test_get_product_success(service, repository, sample_product):
    repository.get_by_id.return_value = sample_product
    result = service.get_product(1)
    assert result == sample_product


def test_update_product_not_found(service, repository, sample_product):
    repository.get_by_id.return_value = None
    with pytest.raises(ProductNotFoundError):
        service.update_product(sample_product)


def test_delete_product_not_found(service, repository):
    repository.get_by_id.return_value = None
    with pytest.raises(ProductNotFoundError):
        service.delete_product(999)