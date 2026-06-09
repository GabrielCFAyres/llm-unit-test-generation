import pytest

from src.payments import calculate_payment_fee, validate_payment


@pytest.mark.parametrize(
    "method, order_value, installments",
    [
        ("pix", 1, 1),
        ("debit_card", 1, 1),
        ("bank_slip", 20, 1),
        ("credit_card", 10, 1),
        ("credit_card", 10, 6),
        ("credit_card", 300, 7),
        ("credit_card", 300, 12),
    ],
)
def test_validate_payment_returns_true_for_valid_payment_data(
    method, order_value, installments
):
    assert validate_payment(method, order_value, installments) is True


@pytest.mark.parametrize(
    "method, order_value, installments",
    [
        ("cash", 100, 1),
        ("pix", 0, 1),
        ("pix", -1, 1),
        ("pix", 100, 2),
        ("debit_card", 100, 2),
        ("bank_slip", 100, 2),
        ("bank_slip", 19.99, 1),
        ("credit_card", 9.99, 1),
        ("credit_card", 100, 0),
        ("credit_card", 100, -1),
        ("credit_card", 300, 13),
        ("credit_card", 299.99, 7),
    ],
)
def test_validate_payment_returns_false_for_invalid_payment_data(
    method, order_value, installments
):
    assert validate_payment(method, order_value, installments) is False


@pytest.mark.parametrize("order_value", ["100", None, [100], {"value": 100}])
def test_validate_payment_raises_type_error_when_order_value_is_not_numeric(
    order_value,
):
    with pytest.raises(TypeError, match="order_value must be numeric"):
        validate_payment("pix", order_value, 1)


@pytest.mark.parametrize("installments", ["1", 1.5, None, [1]])
def test_validate_payment_raises_type_error_when_installments_is_not_integer(
    installments,
):
    with pytest.raises(TypeError, match="installments must be an integer"):
        validate_payment("credit_card", 100, installments)


@pytest.mark.parametrize(
    "method, order_value, installments, expected_fee",
    [
        ("pix", 100, 1, 0.0),
        ("debit_card", 100, 1, 1.0),
        ("debit_card", 123.45, 1, 1.23),
        ("bank_slip", 100, 1, 2.50),
        ("credit_card", 100, 1, 2.0),
        ("credit_card", 100, 6, 2.0),
        ("credit_card", 300, 7, 12.0),
        ("credit_card", 300, 12, 12.0),
    ],
)
def test_calculate_payment_fee_returns_expected_fee(
    method, order_value, installments, expected_fee
):
    assert calculate_payment_fee(method, order_value, installments) == expected_fee


@pytest.mark.parametrize(
    "method, order_value, installments",
    [
        ("cash", 100, 1),
        ("pix", 0, 1),
        ("pix", 100, 2),
        ("debit_card", 100, 2),
        ("bank_slip", 19.99, 1),
        ("credit_card", 9.99, 1),
        ("credit_card", 300, 13),
        ("credit_card", 299.99, 7),
    ],
)
def test_calculate_payment_fee_raises_value_error_for_invalid_payment_data(
    method, order_value, installments
):
    with pytest.raises(ValueError, match="invalid payment data"):
        calculate_payment_fee(method, order_value, installments)