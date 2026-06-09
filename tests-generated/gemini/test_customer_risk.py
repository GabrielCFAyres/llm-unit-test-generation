import pytest
from src.customer_risk import classify_customer_risk, can_customer_place_order


class TestClassifyCustomerRisk:

    @pytest.mark.parametrize("score", ["800", 800.5, None])
    def test_classify_customer_risk_invalid_score_type(self, score):
        with pytest.raises(TypeError, match="score must be an integer"):
            classify_customer_risk(score, 0, 0.0)

    @pytest.mark.parametrize("overdue_days", ["10", 10.5, None])
    def test_classify_customer_risk_invalid_overdue_days_type(self, overdue_days):
        with pytest.raises(TypeError, match="overdue_days must be an integer"):
            classify_customer_risk(800, overdue_days, 0.0)

    @pytest.mark.parametrize("open_amount", ["100.0", None, []])
    def test_classify_customer_risk_invalid_open_amount_type(self, open_amount):
        with pytest.raises(TypeError, match="open_amount must be numeric"):
            classify_customer_risk(800, 0, open_amount)

    @pytest.mark.parametrize("score", [-1, -100, 1001, 2000])
    def test_classify_customer_risk_score_out_of_bounds(self, score):
        with pytest.raises(ValueError, match="score must be between 0 and 1000"):
            classify_customer_risk(score, 0, 0.0)

    @pytest.mark.parametrize("overdue_days", [-1, -50])
    def test_classify_customer_risk_negative_overdue_days(self, overdue_days):
        with pytest.raises(ValueError, match="overdue_days cannot be negative"):
            classify_customer_risk(800, overdue_days, 0.0)

    @pytest.mark.parametrize("open_amount", [-0.01, -100])
    def test_classify_customer_risk_negative_open_amount(self, open_amount):
        with pytest.raises(ValueError, match="open_amount cannot be negative"):
            classify_customer_risk(800, 0, open_amount)

    @pytest.mark.parametrize("score, overdue_days, open_amount", [
        (399, 0, 0.0),       # Score limite inferior "high"
        (0, 0, 0.0),         # Score extremo "high"
        (800, 61, 0.0),      # Atraso limite inferior "high"
        (800, 100, 0.0),     # Atraso extremo "high"
        (800, 0, 5000.0),    # Valor em aberto limite inferior "high"
        (800, 0, 10000.0),   # Valor em aberto extremo "high"
        (100, 100, 10000.0), # Todos os critérios "high"
    ])
    def test_classify_customer_risk_high(self, score, overdue_days, open_amount):
        assert classify_customer_risk(score, overdue_days, open_amount) == "high"

    @pytest.mark.parametrize("score, overdue_days, open_amount", [
        (400, 0, 0.0),       # Score limite inferior "medium"
        (699, 0, 0.0),       # Score limite superior "medium"
        (800, 16, 0.0),      # Atraso limite inferior "medium"
        (800, 60, 0.0),      # Atraso limite superior "medium"
        (800, 0, 1000.0),    # Valor em aberto limite inferior "medium"
        (800, 0, 4999.99),   # Valor em aberto limite superior "medium"
        (500, 30, 2000.0),   # Todos os critérios "medium"
    ])
    def test_classify_customer_risk_medium(self, score, overdue_days, open_amount):
        assert classify_customer_risk(score, overdue_days, open_amount) == "medium"

    @pytest.mark.parametrize("score, overdue_days, open_amount", [
        (700, 15, 999.99),   # Todos os critérios no limite superior "low"
        (1000, 0, 0.0),      # Todos os critérios perfeitos (extremos "low")
        (850, 5, 500.0),     # Valores intermediários "low"
    ])
    def test_classify_customer_risk_low(self, score, overdue_days, open_amount):
        assert classify_customer_risk(score, overdue_days, open_amount) == "low"


class TestCanCustomerPlaceOrder:

    @pytest.mark.parametrize("order_value", ["100", None, []])
    def test_can_customer_place_order_invalid_type(self, order_value):
        with pytest.raises(TypeError, match="order_value must be numeric"):
            can_customer_place_order(800, 0, 0.0, order_value)

    @pytest.mark.parametrize("order_value", [0, 0.0, -0.01, -100])
    def test_can_customer_place_order_invalid_value(self, order_value):
        with pytest.raises(ValueError, match="order_value must be greater than zero"):
            can_customer_place_order(800, 0, 0.0, order_value)

    @pytest.mark.parametrize("score, overdue_days, open_amount, order_value", [
        (399, 0, 0.0, 10.0),     # Cliente High por score
        (800, 61, 0.0, 50.0),    # Cliente High por atraso
        (800, 0, 5000.0, 100.0), # Cliente High por valor em aberto
    ])
    def test_can_customer_place_order_high_risk_denied(self, score, overdue_days, open_amount, order_value):
        assert can_customer_place_order(score, overdue_days, open_amount, order_value) is False

    @pytest.mark.parametrize("order_value", [0.01, 500.0, 1000.0])
    def test_can_customer_place_order_medium_risk_allowed(self, order_value):
        # Cliente Medium por score (500)
        assert can_customer_place_order(500, 0, 0.0, order_value) is True

    @pytest.mark.parametrize("order_value", [1000.01, 2000.0])
    def test_can_customer_place_order_medium_risk_denied(self, order_value):
        # Cliente Medium por atraso (30 dias)
        assert can_customer_place_order(800, 30, 0.0, order_value) is False

    @pytest.mark.parametrize("order_value", [0.01, 1000.0, 5000.0, 999999.99])
    def test_can_customer_place_order_low_risk_allowed(self, order_value):
        # Cliente Low (Score alto, sem atraso, sem valor em aberto)
        assert can_customer_place_order(800, 0, 0.0, order_value) is True