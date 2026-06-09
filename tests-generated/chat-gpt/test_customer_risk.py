import pytest

from src.customer_risk import classify_customer_risk, can_customer_place_order


@pytest.mark.parametrize(
    "score, overdue_days, open_amount",
    [
        (0, 0, 0),
        (399, 0, 0),
        (350, 20, 2000),
        (350, 61, 5000),
    ],
)
def test_classify_customer_risk_returns_high_when_score_is_below_400(
    score, overdue_days, open_amount
):
    assert classify_customer_risk(score, overdue_days, open_amount) == "high"


@pytest.mark.parametrize(
    "score, overdue_days, open_amount",
    [
        (700, 61, 0),
        (700, 100, 999.99),
        (400, 61, 1000),
    ],
)
def test_classify_customer_risk_returns_high_when_overdue_days_is_greater_than_60(
    score, overdue_days, open_amount
):
    assert classify_customer_risk(score, overdue_days, open_amount) == "high"


@pytest.mark.parametrize(
    "score, overdue_days, open_amount",
    [
        (700, 0, 5000),
        (700, 15, 5000.0),
        (500, 30, 6000),
    ],
)
def test_classify_customer_risk_returns_high_when_open_amount_is_at_least_5000(
    score, overdue_days, open_amount
):
    assert classify_customer_risk(score, overdue_days, open_amount) == "high"


@pytest.mark.parametrize(
    "score, overdue_days, open_amount",
    [
        (400, 0, 0),
        (699, 15, 999.99),
        (500, 0, 500),
    ],
)
def test_classify_customer_risk_returns_medium_when_score_is_between_400_and_699(
    score, overdue_days, open_amount
):
    assert classify_customer_risk(score, overdue_days, open_amount) == "medium"


@pytest.mark.parametrize(
    "score, overdue_days, open_amount",
    [
        (700, 16, 0),
        (1000, 60, 999.99),
        (800, 30, 500),
    ],
)
def test_classify_customer_risk_returns_medium_when_overdue_days_is_between_16_and_60(
    score, overdue_days, open_amount
):
    assert classify_customer_risk(score, overdue_days, open_amount) == "medium"


@pytest.mark.parametrize(
    "score, overdue_days, open_amount",
    [
        (700, 0, 1000),
        (1000, 15, 4999.99),
        (800, 10, 2500),
    ],
)
def test_classify_customer_risk_returns_medium_when_open_amount_is_between_1000_and_4999_99(
    score, overdue_days, open_amount
):
    assert classify_customer_risk(score, overdue_days, open_amount) == "medium"


@pytest.mark.parametrize(
    "score, overdue_days, open_amount",
    [
        (700, 0, 0),
        (700, 15, 999.99),
        (1000, 15, 999),
    ],
)
def test_classify_customer_risk_returns_low_when_all_values_are_low_risk(
    score, overdue_days, open_amount
):
    assert classify_customer_risk(score, overdue_days, open_amount) == "low"


@pytest.mark.parametrize("score", [-1, 1001])
def test_classify_customer_risk_raises_value_error_when_score_is_out_of_range(score):
    with pytest.raises(ValueError, match="score must be between 0 and 1000"):
        classify_customer_risk(score, 0, 0)


def test_classify_customer_risk_raises_value_error_when_overdue_days_is_negative():
    with pytest.raises(ValueError, match="overdue_days cannot be negative"):
        classify_customer_risk(700, -1, 0)


def test_classify_customer_risk_raises_value_error_when_open_amount_is_negative():
    with pytest.raises(ValueError, match="open_amount cannot be negative"):
        classify_customer_risk(700, 0, -0.01)


@pytest.mark.parametrize("score", ["700", 700.5, None])
def test_classify_customer_risk_raises_type_error_when_score_is_not_integer(score):
    with pytest.raises(TypeError, match="score must be an integer"):
        classify_customer_risk(score, 0, 0)


@pytest.mark.parametrize("overdue_days", ["15", 15.5, None])
def test_classify_customer_risk_raises_type_error_when_overdue_days_is_not_integer(
    overdue_days,
):
    with pytest.raises(TypeError, match="overdue_days must be an integer"):
        classify_customer_risk(700, overdue_days, 0)


@pytest.mark.parametrize("open_amount", ["1000", None, []])
def test_classify_customer_risk_raises_type_error_when_open_amount_is_not_numeric(
    open_amount,
):
    with pytest.raises(TypeError, match="open_amount must be numeric"):
        classify_customer_risk(700, 0, open_amount)


@pytest.mark.parametrize(
    "score, overdue_days, open_amount, order_value",
    [
        (700, 0, 0, 1),
        (700, 15, 999.99, 1000),
        (1000, 0, 0, 10000),
    ],
)
def test_can_customer_place_order_returns_true_for_low_risk_customer_with_positive_order_value(
    score, overdue_days, open_amount, order_value
):
    assert can_customer_place_order(score, overdue_days, open_amount, order_value) is True


@pytest.mark.parametrize(
    "score, overdue_days, open_amount, order_value",
    [
        (400, 0, 0, 1000),
        (700, 16, 0, 999.99),
        (700, 0, 1000, 1),
    ],
)
def test_can_customer_place_order_returns_true_for_medium_risk_customer_when_order_value_is_at_most_1000(
    score, overdue_days, open_amount, order_value
):
    assert can_customer_place_order(score, overdue_days, open_amount, order_value) is True


@pytest.mark.parametrize(
    "score, overdue_days, open_amount, order_value",
    [
        (400, 0, 0, 1000.01),
        (700, 16, 0, 1500),
        (700, 0, 4999.99, 2000),
    ],
)
def test_can_customer_place_order_returns_false_for_medium_risk_customer_when_order_value_is_greater_than_1000(
    score, overdue_days, open_amount, order_value
):
    assert can_customer_place_order(score, overdue_days, open_amount, order_value) is False


@pytest.mark.parametrize(
    "score, overdue_days, open_amount, order_value",
    [
        (399, 0, 0, 1),
        (700, 61, 0, 1000),
        (700, 0, 5000, 10000),
    ],
)
def test_can_customer_place_order_returns_false_for_high_risk_customer(
    score, overdue_days, open_amount, order_value
):
    assert can_customer_place_order(score, overdue_days, open_amount, order_value) is False


@pytest.mark.parametrize("order_value", [0, -1, -0.01])
def test_can_customer_place_order_raises_value_error_when_order_value_is_not_positive(
    order_value,
):
    with pytest.raises(ValueError, match="order_value must be greater than zero"):
        can_customer_place_order(700, 0, 0, order_value)


@pytest.mark.parametrize("order_value", ["1000", None, []])
def test_can_customer_place_order_raises_type_error_when_order_value_is_not_numeric(
    order_value,
):
    with pytest.raises(TypeError, match="order_value must be numeric"):
        can_customer_place_order(700, 0, 0, order_value)


def test_can_customer_place_order_propagates_customer_risk_validation_errors():
    with pytest.raises(ValueError, match="score must be between 0 and 1000"):
        can_customer_place_order(1001, 0, 0, 100)