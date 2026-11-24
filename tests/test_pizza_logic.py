import pytest
from pizza_logic import calculate_total_price, find_most_profitable_day

def test_calculate_total_price_correct():
    assert calculate_total_price(2, 15.5) == 31.0

def test_calculate_total_price_error():
    with pytest.raises(ValueError):
        calculate_total_price(0, 15.5)

def test_find_most_profitable_day():
    revenue = {'Monday': 107329.55, 'Friday': 136073.90, 'Sunday': 99203.50}
    assert find_most_profitable_day(revenue) == 'Friday'

def test_find_most_profitable_day_empty():
    assert find_most_profitable_day({}) is None
