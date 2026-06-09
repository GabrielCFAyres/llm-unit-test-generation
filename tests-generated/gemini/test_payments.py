import pytest
from src.payments import validate_payment, calculate_payment_fee

# --- Tests for validate_payment ---

@pytest.mark.parametrize("method, order_value, installments", [
    ("pix", 50.0, 1),
    ("debit_card", 10.5, 1),
    ("bank_slip", 20.0, 1),
    ("bank_slip", 100.0, 1),
    ("credit_card", 10.0, 1),
    ("credit_card", 299.99, 6),
    ("credit_card", 300.0, 7),
    ("credit_card", 500.0, 12),
])
def test_validate_payment_valid_scenarios(method, order_value, installments):
    assert validate_payment(method, order_value, installments) is True

@pytest.mark.parametrize("method, order_value, installments", [
    ("pix", 0, 1),
    ("pix", -10.0, 1),
    ("credit_card", 50.0, 0),
    ("credit_card", 50.0, -1),
    ("invalid_method", 50.0, 1),
    ("pix", 50.0, 2),
    ("debit_card", 50.0, 3),
    ("bank_slip", 50.0, 2),
    ("bank_slip", 19.99, 1),
    ("credit_card", 9.99, 1),
    ("credit_card", 500.0, 13),
    ("credit_card", 299.99, 7),
])
def test_validate_payment_invalid_scenarios(method, order_value, installments):
    assert validate_payment(method, order_value, installments) is False

def test_validate_payment_order_value_type_error():
    with pytest.raises(TypeError, match="order_value must be numeric"):
        validate_payment("pix", "50.0", 1) # type: ignore[arg-type]

def test_validate_payment_installments_type_error():
    with pytest.raises(TypeError, match="installments must be an integer"):
        validate_payment("pix", 50.0, 1.5) # type: ignore[arg-type]

# --- Tests for calculate_payment_fee ---

@pytest.mark.parametrize("method, order_value, installments, expected_fee", [
    ("pix", 100.0, 1, 0.0),
    ("debit_card", 100.0, 1, 1.0),
    ("debit_card", 150.5, 1, 1.51),
    ("bank_slip", 50.0, 1, 2.50),
    ("bank_slip", 20.0, 1, 2.50),
    ("credit_card", 100.0, 1, 2.0),
    ("credit_card", 100.0, 6, 2.0),
    ("credit_card", 300.0, 7, 12.0),
    ("credit_card", 300.0, 12, 12.0),
])
def test_calculate_payment_fee_valid_scenarios(method, order_value, installments, expected_fee):
    assert calculate_payment_fee(method, order_value, installments) == expected_fee

@pytest.mark.parametrize("method, order_value, installments", [
    ("pix", 0, 1),
    ("bank_slip", 10.0, 1),
    ("credit_card", 200.0, 7),
    ("invalid_method", 100.0, 1),
    ("pix", 100.0, 2),
])
def test_calculate_payment_fee_invalid_payment_data(method, order_value, installments):
    with pytest.raises(ValueError, match="invalid payment data"):
        calculate_payment_fee(method, order_value, installments)