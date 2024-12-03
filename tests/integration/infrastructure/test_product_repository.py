import pytest
from sqlalchemy import create_engine
from src.domain.models.product import Product
from src.infrastructure.adapters.persistence.mysql.mysql_product_repository import MySQLProductRepository
from src.infrastructure.adapters.persistence.mysql.models.product_model import metadata


@pytest.fixture
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture
def repository(engine):
    metadata.create_all(engine)
    return MySQLProductRepository('sqlite:///:memory:')


@pytest.fixture
def sample_product():
    return Product(
        name="Test Product",
        price=99.99,
        description="Test Description"
    )


def test_create_and_get_product(repository, sample_product):
    created = repository.create(sample_product)
    assert created.id is not None

    retrieved = repository.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.name == sample_product.name
    assert retrieved.price == sample_product.price


def test_update_product(repository, sample_product):
    created = repository.create(sample_product)
    created.name = "Updated Name"

    updated = repository.update(created)
    assert updated.name == "Updated Name"

    retrieved = repository.get_by_id(created.id)
    assert retrieved.name == "Updated Name"


def test_delete_product(repository, sample_product):
    created = repository.create(sample_product)
    assert repository.delete(created.id) is True
    assert repository.get_by_id(created.id) is None