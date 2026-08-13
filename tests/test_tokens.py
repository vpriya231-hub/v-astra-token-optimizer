from v_astra.tokens.counter import estimate_tokens
from v_astra.tokens.savings import savings_ratio


def test_estimate_tokens():
    assert estimate_tokens("") == 0
    assert estimate_tokens("hello") >= 1


def test_savings_ratio():
    assert savings_ratio(100, 40) == 0.6
