import pytest

from src.payments import validate_payment, calculate_payment_fee


# ---------------------------------------------------------------------------
# validate_payment
# ---------------------------------------------------------------------------

# --- Entradas válidas ---

def test_pix_single_installment_valid():
    assert validate_payment("pix", 100.0) is True


def test_debit_card_single_installment_valid():
    assert validate_payment("debit_card", 100.0) is True


def test_bank_slip_valid_above_minimum():
    assert validate_payment("bank_slip", 50.0) is True


def test_credit_card_single_installment_valid():
    assert validate_payment("credit_card", 100.0) is True


def test_credit_card_six_installments_valid():
    assert validate_payment("credit_card", 100.0, 6) is True


def test_credit_card_twelve_installments_high_value_valid():
    assert validate_payment("credit_card", 300.0, 12) is True


# --- Regras de valor ---

def test_order_value_zero_returns_false():
    assert validate_payment("pix", 0) is False


def test_order_value_negative_returns_false():
    assert validate_payment("pix", -10) is False


# --- Método inválido ---

def test_invalid_method_returns_false():
    assert validate_payment("bitcoin", 100.0) is False


# --- Regras de parcelas ---

def test_installments_zero_returns_false():
    assert validate_payment("credit_card", 100.0, 0) is False


def test_installments_negative_returns_false():
    assert validate_payment("credit_card", 100.0, -1) is False


@pytest.mark.parametrize("method", ["pix", "debit_card", "bank_slip"])
def test_non_credit_methods_reject_multiple_installments(method):
    assert validate_payment(method, 100.0, 2) is False


def test_credit_card_above_twelve_installments_returns_false():
    assert validate_payment("credit_card", 500.0, 13) is False


# --- Valores-limite ---

def test_bank_slip_below_minimum_returns_false():
    assert validate_payment("bank_slip", 19.99) is False


def test_bank_slip_at_minimum_returns_true():
    assert validate_payment("bank_slip", 20) is True


def test_credit_card_below_minimum_returns_false():
    assert validate_payment("credit_card", 9.99) is False


def test_credit_card_at_minimum_returns_true():
    assert validate_payment("credit_card", 10) is True


def test_credit_card_seven_installments_below_300_returns_false():
    assert validate_payment("credit_card", 299.99, 7) is False


def test_credit_card_seven_installments_at_300_returns_true():
    assert validate_payment("credit_card", 300, 7) is True


# --- Exceções ---

def test_order_value_not_numeric_raises_type_error():
    with pytest.raises(TypeError):
        validate_payment("pix", "100")


def test_installments_not_integer_raises_type_error():
    with pytest.raises(TypeError):
        validate_payment("credit_card", 100.0, 1.5)


# ---------------------------------------------------------------------------
# calculate_payment_fee
# ---------------------------------------------------------------------------

def test_pix_fee_is_zero():
    assert calculate_payment_fee("pix", 100.0) == 0.0


def test_debit_card_fee_is_one_percent():
    assert calculate_payment_fee("debit_card", 100.0) == 1.0


def test_bank_slip_fixed_fee():
    assert calculate_payment_fee("bank_slip", 100.0) == 2.50


def test_credit_card_fee_up_to_six_installments():
    assert calculate_payment_fee("credit_card", 100.0, 6) == 2.0


def test_credit_card_fee_above_six_installments():
    assert calculate_payment_fee("credit_card", 400.0, 7) == 16.0


def test_credit_card_fee_single_installment():
    assert calculate_payment_fee("credit_card", 200.0, 1) == 4.0


# --- Exceção de pagamento inválido ---

def test_invalid_payment_raises_value_error():
    with pytest.raises(ValueError):
        calculate_payment_fee("pix", 0)


def test_invalid_method_raises_value_error():
    with pytest.raises(ValueError):
        calculate_payment_fee("bitcoin", 100.0)
