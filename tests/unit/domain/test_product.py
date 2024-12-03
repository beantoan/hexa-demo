from src.domain.models.product import Product


def test_product_creation():
    product = Product(
        name="Test Product",
        price=99.99,
        description="Test Description"
    )
    assert product.name == "Test Product"
    assert product.price == 99.99
    assert product.description == "Test Description"
    assert product.id is None
    assert product.created_at is None
    assert product.updated_at is None
