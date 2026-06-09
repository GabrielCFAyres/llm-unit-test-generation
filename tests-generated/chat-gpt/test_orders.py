import pytest

from src.orders import validate_order

@pytest.mark.parametrize(
"payment_method",
["credit_card", "debit_card", "pix", "bank_slip"],
)
def test_validate_order_returns_true_for_valid_order_with_accepted_payment_methods(payment_method):
items = [
{
"name": "Notebook",
"quantity": 1,
"unit_price": 3500.00,
"stock": 5,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, payment_method) is True
```

def test_validate_order_returns_true_when_quantity_is_equal_to_stock():
items = [
{
"name": "Mouse",
"quantity": 3,
"unit_price": 80.00,
"stock": 3,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, "pix") is True
```

def test_validate_order_returns_true_for_multiple_valid_items():
items = [
{
"name": "Mouse",
"quantity": 2,
"unit_price": 80.00,
"stock": 10,
},
{
"name": "Teclado",
"quantity": 1,
"unit_price": 150.00,
"stock": 4,
},
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, "credit_card") is True
```

@pytest.mark.parametrize("items", [None, "invalid", 123, {"name": "Produto"}])
def test_validate_order_raises_type_error_when_items_is_not_list(items):
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
with pytest.raises(TypeError, match="items must be a list"):
    validate_order(items, address, "pix")
```

@pytest.mark.parametrize("address", [None, "invalid", 123, ["Rua das Flores"]])
def test_validate_order_raises_type_error_when_address_is_not_dictionary(address):
items = [
{
"name": "Notebook",
"quantity": 1,
"unit_price": 3500.00,
"stock": 5,
}
]

```
with pytest.raises(TypeError, match="address must be a dictionary"):
    validate_order(items, address, "pix")
```

def test_validate_order_returns_false_when_items_list_is_empty():
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order([], address, "pix") is False
```

def test_validate_order_returns_false_when_item_is_not_dictionary():
items = ["invalid_item"]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, "pix") is False
```

@pytest.mark.parametrize(
"item",
[
{"quantity": 1, "unit_price": 10.00, "stock": 5},
{"name": "Produto", "unit_price": 10.00, "stock": 5},
{"name": "Produto", "quantity": 1, "stock": 5},
{"name": "Produto", "quantity": 1, "unit_price": 10.00},
],
)
def test_validate_order_returns_false_when_item_required_field_is_missing(item):
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order([item], address, "pix") is False
```

@pytest.mark.parametrize("name", ["", None])
def test_validate_order_returns_false_when_item_name_is_empty(name):
items = [
{
"name": name,
"quantity": 1,
"unit_price": 10.00,
"stock": 5,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, "pix") is False
```

@pytest.mark.parametrize("quantity", [0, -1])
def test_validate_order_returns_false_when_quantity_is_not_greater_than_zero(quantity):
items = [
{
"name": "Produto",
"quantity": quantity,
"unit_price": 10.00,
"stock": 5,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, "pix") is False
```

@pytest.mark.parametrize("unit_price", [0, -10.00])
def test_validate_order_returns_false_when_unit_price_is_not_greater_than_zero(unit_price):
items = [
{
"name": "Produto",
"quantity": 1,
"unit_price": unit_price,
"stock": 5,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, "pix") is False
```

def test_validate_order_returns_false_when_stock_is_negative():
items = [
{
"name": "Produto",
"quantity": 1,
"unit_price": 10.00,
"stock": -1,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, "pix") is False
```

def test_validate_order_returns_false_when_quantity_is_greater_than_stock():
items = [
{
"name": "Produto",
"quantity": 6,
"unit_price": 10.00,
"stock": 5,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, "pix") is False
```

@pytest.mark.parametrize(
"address",
[
{"number": "123", "city": "Recife", "state": "PE", "zip_code": "50000-000"},
{"street": "Rua das Flores", "city": "Recife", "state": "PE", "zip_code": "50000-000"},
{"street": "Rua das Flores", "number": "123", "state": "PE", "zip_code": "50000-000"},
{"street": "Rua das Flores", "number": "123", "city": "Recife", "zip_code": "50000-000"},
{"street": "Rua das Flores", "number": "123", "city": "Recife", "state": "PE"},
],
)
def test_validate_order_returns_false_when_address_required_field_is_missing(address):
items = [
{
"name": "Produto",
"quantity": 1,
"unit_price": 10.00,
"stock": 5,
}
]

```
assert validate_order(items, address, "pix") is False
```

@pytest.mark.parametrize("invalid_value", [None, ""])
@pytest.mark.parametrize("field", ["street", "number", "city", "state", "zip_code"])
def test_validate_order_returns_false_when_address_required_field_is_empty(field, invalid_value):
items = [
{
"name": "Produto",
"quantity": 1,
"unit_price": 10.00,
"stock": 5,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}
address[field] = invalid_value

```
assert validate_order(items, address, "pix") is False
```

@pytest.mark.parametrize("payment_method", ["cash", "paypal", "", None])
def test_validate_order_returns_false_when_payment_method_is_not_accepted(payment_method):
items = [
{
"name": "Produto",
"quantity": 1,
"unit_price": 10.00,
"stock": 5,
}
]
address = {
"street": "Rua das Flores",
"number": "123",
"city": "Recife",
"state": "PE",
"zip_code": "50000-000",
}

```
assert validate_order(items, address, payment_method) is False
```
