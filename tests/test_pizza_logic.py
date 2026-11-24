import pytest
from pizza_logic import calculate_total_price, find_most_profitable_day

#тест 1: проверяем правильность расчета (2 пиццы по 15.5)
def test_calculate_total_price_correct():
    assert calculate_total_price(2, 15.5) == 31.0

#тест 2: проверяем, что программа выдаст ошибку, если количество равно 0
def test_calculate_total_price_error():
    with pytest.raises(ValueError):
        calculate_total_price(0, 15.5)

#тест 3: проверяем поиск лучшего дня
def test_find_most_profitable_day():
    revenue = {'Monday': 107329.55, 'Friday': 136073.90, 'Sunday': 99203.50}
    #ожидаем, что функция найдет пятницу (Friday)
    assert find_most_profitable_day(revenue) == 'Friday'

#тест 4: проверяем работу с пустым словарем
def test_find_most_profitable_day_empty():
    assert find_most_profitable_day({}) is None

#тест 5: проверяем, что программа выдаст ошибку, если цена отрицательная
def test_calculate_total_price_negative_price():
    with pytest.raises(ValueError):
        calculate_total_price(2, -10.0)

#тест 6: проверяем, что программа выдаст ошибку, если количество отрицательное
def test_calculate_total_price_negative_quantity():
    with pytest.raises(ValueError):
        calculate_total_price(-1, 15.5)

#тест 7: проверяем расчет с дробными числами (например, 1.5 пиццы по 10.0)
def test_calculate_total_price_float():
    assert calculate_total_price(1.5, 10.0) == 15.0

#тест 8: проверяем поиск лучшего дня, когда в словаре только один день
def test_find_most_profitable_day_single_item():
    revenue = {'Wednesday': 50000.0}
    assert find_most_profitable_day(revenue) == 'Wednesday'

#тест 9: проверяем поиск лучшего дня с отрицательными значениями (убытки)
def test_find_most_profitable_day_negative_values():
    revenue = {'Monday': -1000.0, 'Tuesday': -500.0, 'Wednesday': -2000.0}
    assert find_most_profitable_day(revenue) == 'Tuesday'
