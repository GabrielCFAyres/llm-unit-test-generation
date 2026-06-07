def classify_customer_risk(
    score: int,
    overdue_days: int,
    open_amount: float,
) -> str:
    """
    Classifica o risco de um cliente com base em score, dias de atraso
    e valor em aberto.

    Regras:
    - score deve estar entre 0 e 1000.
    - overdue_days não pode ser negativo.
    - open_amount não pode ser negativo.

    Classificação:
    - "high" se:
        - score menor que 400; ou
        - atraso maior que 60 dias; ou
        - valor em aberto maior ou igual a 5000.
    - "medium" se:
        - score entre 400 e 699; ou
        - atraso entre 16 e 60 dias; ou
        - valor em aberto entre 1000 e 4999.99.
    - "low" se:
        - score maior ou igual a 700; e
        - atraso de até 15 dias; e
        - valor em aberto menor que 1000.

    Retorna:
    - "low", "medium" ou "high".

    Exceções:
    - TypeError se score ou overdue_days não forem inteiros.
    - TypeError se open_amount não for número.
    - ValueError se algum valor estiver fora da faixa permitida.
    """

    if not isinstance(score, int):
        raise TypeError("score must be an integer")

    if not isinstance(overdue_days, int):
        raise TypeError("overdue_days must be an integer")

    if not isinstance(open_amount, (int, float)):
        raise TypeError("open_amount must be numeric")

    if score < 0 or score > 1000:
        raise ValueError("score must be between 0 and 1000")

    if overdue_days < 0:
        raise ValueError("overdue_days cannot be negative")

    if open_amount < 0:
        raise ValueError("open_amount cannot be negative")

    if score < 400:
        return "high"

    if overdue_days > 60:
        return "high"

    if open_amount >= 5000:
        return "high"

    if 400 <= score < 700:
        return "medium"

    if 16 <= overdue_days <= 60:
        return "medium"

    if 1000 <= open_amount < 5000:
        return "medium"

    return "low"


def can_customer_place_order(
    score: int,
    overdue_days: int,
    open_amount: float,
    order_value: float,
) -> bool:
    """
    Define se um cliente pode realizar um novo pedido.

    Regras:
    - Clientes de risco alto não podem realizar novos pedidos.
    - Clientes de risco médio podem realizar pedidos de até 1000.
    - Clientes de risco baixo podem realizar pedidos de qualquer valor positivo.
    - O valor do pedido deve ser maior que zero.

    Retorna:
    - True se o cliente puder realizar o pedido.
    - False caso contrário.

    Exceções:
    - TypeError se order_value não for número.
    - ValueError se order_value for menor ou igual a zero.
    """

    if not isinstance(order_value, (int, float)):
        raise TypeError("order_value must be numeric")

    if order_value <= 0:
        raise ValueError("order_value must be greater than zero")

    risk = classify_customer_risk(score, overdue_days, open_amount)

    if risk == "high":
        return False

    if risk == "medium" and order_value > 1000:
        return False

    return True