import pytest

from src.orders import validate_order


def _valid_item(**overrides):
    item = {"name": "Notebook", "quantity": 1, "unit_price": 100.0, "stock": 10}
    item.update(overrides)
    return item


def _valid_address(**overrides):
    address = {
        "street": "Rua A",
        "number": "100",
        "city": "Recife",
        "state": "PE",
        "zip_code": "50000-000",
    }
    address.update(overrides)
    return address


# --- Entradas válidas ---

def test_valid_order_returns_true():
    assert validate_order([_valid_item()], _valid_address(), "pix") is True


@pytest.mark.parametrize("method", ["credit_card", "debit_card", "pix", "bank_slip"])
def test_valid_order_accepts_all_payment_methods(method):
    assert validate_order([_valid_item()], _valid_address(), method) is True


def test_valid_order_with_multiple_items():
    items = [_valid_item(), _valid_item(name="Mouse", quantity=2, stock=5)]
    assert validate_order(items, _valid_address(), "pix") is True


# --- Regras de itens ---

def test_empty_items_returns_false():
    assert validate_order([], _valid_address(), "pix") is False


def test_item_not_dict_returns_false():
    assert validate_order(["not a dict"], _valid_address(), "pix") is False


def test_item_missing_required_field_returns_false():
    item = {"name": "X", "quantity": 1, "unit_price": 10.0}  # sem stock
    assert validate_order([item], _valid_address(), "pix") is False


def test_item_empty_name_returns_false():
    assert validate_order([_valid_item(name="")], _valid_address(), "pix") is False


def test_item_quantity_zero_returns_false():
    assert validate_order([_valid_item(quantity=0)], _valid_address(), "pix") is False


def test_item_quantity_negative_returns_false():
    assert validate_order([_valid_item(quantity=-1)], _valid_address(), "pix") is False


def test_item_unit_price_zero_returns_false():
    assert validate_order([_valid_item(unit_price=0)], _valid_address(), "pix") is False


def test_item_unit_price_negative_returns_false():
    assert validate_order([_valid_item(unit_price=-5)], _valid_address(), "pix") is False


def test_item_negative_stock_returns_false():
    assert validate_order([_valid_item(stock=-1)], _valid_address(), "pix") is False


def test_quantity_greater_than_stock_returns_false():
    assert validate_order([_valid_item(quantity=5, stock=3)], _valid_address(), "pix") is False


def test_quantity_equals_stock_returns_true():
    assert validate_order([_valid_item(quantity=3, stock=3)], _valid_address(), "pix") is True


# --- Regras de endereço ---

def test_address_missing_field_returns_false():
    address = _valid_address()
    del address["city"]
    assert validate_order([_valid_item()], address, "pix") is False


def test_address_field_none_returns_false():
    assert validate_order([_valid_item()], _valid_address(state=None), "pix") is False


def test_address_field_empty_string_returns_false():
    assert validate_order([_valid_item()], _valid_address(zip_code=""), "pix") is False


# --- Regras de forma de pagamento ---

def test_invalid_payment_method_returns_false():
    assert validate_order([_valid_item()], _valid_address(), "bitcoin") is False


# --- Exceções ---

def test_items_not_list_raises_type_error():
    with pytest.raises(TypeError):
        validate_order("not a list", _valid_address(), "pix")


def test_address_not_dict_raises_type_error():
    with pytest.raises(TypeError):
        validate_order([_valid_item()], "not a dict", "pix")
