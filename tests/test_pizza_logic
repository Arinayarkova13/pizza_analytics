import pytest
import pandas as pd
from utils.analytics import find_most_profitable_day

#создаем тестовые данные (мини-таблицу), чтобы не брать реальную базу
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "day_of_week": [1, 1, 5, 5, 7], # 1-Пн, 5-Пт, 7-Вс
        "revenue": [10000, 5000, 20000, 15000, 8000]
    })

#тест 1: проверяем, что функция находит день с максимальной выручкой
def test_find_most_profitable_day_correct(sample_data):
    # Пятница (5) имеет 20000 + 15000 = 35000 (максимум)
    assert find_most_profitable_day(sample_data) == 5

#тест 2: проверяем работу с пустым DataFrame
def test_find_most_profitable_day_empty():
    empty_df = pd.DataFrame(columns=["day_of_week", "revenue"])
    assert find_most_profitable_day(empty_df) is None

#тест 3: заменяем тест с отрицательной выручкой на сценарий с одинаковой выручкой
def test_find_most_profitable_day_tie():
    #два дня с одинаковой максимальной выручкой (10000)
    df = pd.DataFrame({
        "day_of_week": [1, 2], 
        "revenue": [10000, 10000]
    })
    #функция вернет либо 1, либо 2. Нам главное, чтобы она не упала с ошибкой.
    result = find_most_profitable_day(df)
    assert result in [1, 2]
