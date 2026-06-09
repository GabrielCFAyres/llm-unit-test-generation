import pytest
import copy
from src.orders import validate_order


@pytest.fixture
def valid_items():
    return [{"name": "Product A", "quantity": 2, "unit_price": 50.0, "stock": 10}]


@pytest.fixture
def valid_address():
    return {
        "street": "Rua Principal",
        "number": "123",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01000-000"
    }


@pytest.mark.parametrize("payment_method", ["credit_card", "debit_card", "pix", "bank_slip"])
def test_validate_order_success(valid_items, valid_address, payment_method):
    assert validate_order(valid_items, valid_address, payment_method) is True


def test_validate_order_items_type_error(valid_address):
    with pytest.raises(TypeError, match="items must be a list"):
        validate_order(items={"name": "Product A"}, address=valid_address, payment_method="pix")  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="items must be a list"):
        validate_order(items=None, address=valid_address, payment_method="pix")  # type: ignore[arg-type]


def test_validate_order_address_type_error(valid_items):
    with pytest.raises(TypeError, match="address must be a dictionary"):
        validate_order(items=valid_items, address="Rua Principal, 123", payment_method="pix")  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="address must be a dictionary"):
        validate_order(items=valid_items, address=None, payment_method="pix")  # type: ignore[arg-type]


def test_validate_order_empty_items(valid_address):
    assert validate_order(items=[], address=valid_address, payment_method="pix") is False


def test_validate_order_item_not_dict(valid_address):
    invalid_items = ["Product A"]
    assert validate_order(items=invalid_items, address=valid_address, payment_method="pix") is False # type: ignore[arg-type]


@pytest.mark.parametrize("missing_field", ["name", "quantity", "unit_price", "stock"])
def test_validate_order_missing_item_fields(valid_items, valid_address, missing_field):
    items = copy.deepcopy(valid_items)
    del items[0][missing_field]
    assert validate_order(items, valid_address, payment_method="pix") is False


@pytest.mark.parametrize("invalid_name", ["", None])
def test_validate_order_invalid_item_name(valid_items, valid_address, invalid_name):
    items = copy.deepcopy(valid_items)
    items[0]["name"] = invalid_name
    assert validate_order(items, valid_address, payment_method="pix") is False


@pytest.mark.parametrize("invalid_quantity", [0, -1])
def test_validate_order_invalid_item_quantity(valid_items, valid_address, invalid_quantity):
    items = copy.deepcopy(valid_items)
    items[0]["quantity"] = invalid_quantity
    assert validate_order(items, valid_address, payment_method="pix") is False


@pytest.mark.parametrize("invalid_price", [0, -10.5])
def test_validate_order_invalid_item_unit_price(valid_items, valid_address, invalid_price):
    items = copy.deepcopy(valid_items)
    items[0]["unit_price"] = invalid_price
    assert validate_order(items, valid_address, payment_method="pix") is False


def test_validate_order_negative_stock(valid_items, valid_address):
    items = copy.deepcopy(valid_items)
    items[0]["stock"] = -1
    assert validate_order(items, valid_address, payment_method="pix") is False


def test_validate_order_quantity_exceeds_stock(valid_items, valid_address):
    items = copy.deepcopy(valid_items)
    items[0]["quantity"] = 11
    items[0]["stock"] = 10
    assert validate_order(items, valid_address, payment_method="pix") is False


def test_validate_order_quantity_equals_stock_success(valid_items, valid_address):
    items = copy.deepcopy(valid_items)
    items[0]["quantity"] = 10
    items[0]["stock"] = 10
    assert validate_order(items, valid_address, payment_method="pix") is True


@pytest.mark.parametrize("missing_field", ["street", "number", "city", "state", "zip_code"])
def test_validate_order_missing_address_fields(valid_items, valid_address, missing_field):
    address = copy.deepcopy(valid_address)
    del address[missing_field]
    assert validate_order(valid_items, address, payment_method="pix") is False


@pytest.mark.parametrize("field", ["street", "number", "city", "state", "zip_code"])
@pytest.mark.parametrize("empty_value", ["", None])
def test_validate_order_empty_address_fields(valid_items, valid_address, field, empty_value):
    address = copy.deepcopy(valid_address)
    address[field] = empty_value
    assert validate_order(valid_items, address, payment_method="pix") is False


@pytest.mark.parametrize("invalid_payment", ["cash", "crypto", "", None])
def test_validate_order_invalid_payment_method(valid_items, valid_address, invalid_payment):
    assert validate_order(valid_items, valid_address, payment_method=invalid_payment) is False  # type: ignore[arg-type]


def test_validate_order_multiple_items_one_invalid(valid_items, valid_address):
    items = copy.deepcopy(valid_items)
    items.append({
        "name": "Product B",
        "quantity": 0,  # Invalid quantity
        "unit_price": 20.0,
        "stock": 5
    })
    assert validate_order(items, valid_address, payment_method="pix") is False