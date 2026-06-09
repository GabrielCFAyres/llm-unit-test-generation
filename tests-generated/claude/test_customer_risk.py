import pytest

from src.customer_risk import classify_customer_risk, can_customer_place_order


# ---------------------------------------------------------------------------
# classify_customer_risk
# ---------------------------------------------------------------------------

# --- Classificação "low" ---

def test_low_risk_customer():
    assert classify_customer_risk(800, 5, 500.0) == "low"


def test_low_risk_boundary_values():
    # score >= 700, atraso <= 15, valor em aberto < 1000
    assert classify_customer_risk(700, 15, 999.99) == "low"


# --- Classificação "medium" ---

def test_medium_risk_by_score():
    assert classify_customer_risk(500, 5, 500.0) == "medium"


def test_medium_risk_by_overdue_days():
    assert classify_customer_risk(800, 30, 500.0) == "medium"


def test_medium_risk_by_open_amount():
    assert classify_customer_risk(800, 5, 2000.0) == "medium"


def test_medium_risk_score_lower_boundary():
    assert classify_customer_risk(400, 5, 500.0) == "medium"


def test_medium_risk_score_upper_boundary():
    assert classify_customer_risk(699, 5, 500.0) == "medium"


def test_medium_risk_overdue_lower_boundary():
    assert classify_customer_risk(800, 16, 500.0) == "medium"


def test_medium_risk_open_amount_lower_boundary():
    assert classify_customer_risk(800, 5, 1000.0) == "medium"


# --- Classificação "high" ---

def test_high_risk_by_low_score():
    assert classify_customer_risk(399, 5, 500.0) == "high"


def test_high_risk_by_overdue_days():
    assert classify_customer_risk(800, 61, 500.0) == "high"


def test_high_risk_by_open_amount():
    assert classify_customer_risk(800, 5, 5000.0) == "high"


# --- Valores-limite das faixas válidas ---

def test_score_at_minimum_valid():
    assert classify_customer_risk(0, 0, 0.0) == "high"


def test_score_at_maximum_valid():
    assert classify_customer_risk(1000, 0, 0.0) == "low"


# --- Exceções de tipo ---

def test_score_not_integer_raises_type_error():
    with pytest.raises(TypeError):
        classify_customer_risk("700", 5, 500.0)


def test_overdue_days_not_integer_raises_type_error():
    with pytest.raises(TypeError):
        classify_customer_risk(700, "5", 500.0)


def test_open_amount_not_numeric_raises_type_error():
    with pytest.raises(TypeError):
        classify_customer_risk(700, 5, "500")


# --- Exceções de faixa ---

def test_score_below_range_raises_value_error():
    with pytest.raises(ValueError):
        classify_customer_risk(-1, 5, 500.0)


def test_score_above_range_raises_value_error():
    with pytest.raises(ValueError):
        classify_customer_risk(1001, 5, 500.0)


def test_negative_overdue_days_raises_value_error():
    with pytest.raises(ValueError):
        classify_customer_risk(700, -1, 500.0)


def test_negative_open_amount_raises_value_error():
    with pytest.raises(ValueError):
        classify_customer_risk(700, 5, -1.0)


# ---------------------------------------------------------------------------
# can_customer_place_order
# ---------------------------------------------------------------------------

def test_low_risk_can_place_any_positive_order():
    assert can_customer_place_order(800, 5, 500.0, 10000.0) is True


def test_high_risk_cannot_place_order():
    assert can_customer_place_order(399, 5, 500.0, 100.0) is False


def test_medium_risk_can_place_order_up_to_limit():
    assert can_customer_place_order(500, 5, 500.0, 1000.0) is True


def test_medium_risk_cannot_place_order_above_limit():
    assert can_customer_place_order(500, 5, 500.0, 1000.01) is False


# --- Exceções ---

def test_order_value_not_numeric_raises_type_error():
    with pytest.raises(TypeError):
        can_customer_place_order(800, 5, 500.0, "100")


def test_order_value_zero_raises_value_error():
    with pytest.raises(ValueError):
        can_customer_place_order(800, 5, 500.0, 0)


def test_order_value_negative_raises_value_error():
    with pytest.raises(ValueError):
        can_customer_place_order(800, 5, 500.0, -10.0)
