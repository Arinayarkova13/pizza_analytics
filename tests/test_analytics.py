
import pandas as pd
import pytest

from utils.analytics import (
    filter_data,
    calculate_metrics,
    sales_by_month,
    orders_by_hour,
    orders_by_weekday,
    popular_pizzas,
    unpopular_pizzas,
    sales_by_category,
    sales_by_size,
     find_most_profitable_day,
)


@pytest.fixture
def sample_data():
    """Создает тестовый набор данных."""

    return pd.DataFrame(
        {
            "order_id": [1, 1, 2, 3],
            "date": pd.to_datetime(
                [
                    "2015-01-01",
                    "2015-01-01",
                    "2015-01-02",
                    "2015-02-01",
                ]
            ),
            "hour": [12, 12, 15, 18],
            "month": [1, 1, 1, 2],
            "day_of_week": [3, 3, 4, 6],
            "name": ["Pizza A", "Pizza B", "Pizza A", "Pizza C"],
            "category": ["Classic", "Chicken", "Classic", "Veggie"],
            "size": ["M", "L", "M", "S"],
            "quantity": [2, 1, 3, 1],
            "price": [10, 20, 10, 15],
            "revenue": [20, 20, 30, 15],
        }
    )


def test_calculate_metrics(sample_data):
    """Проверяет расчет основных показателей."""

    result = calculate_metrics(sample_data)

    assert result["revenue"] == 85
    assert result["orders"] == 3
    assert result["pizzas"] == 7
    assert result["average_check"] == 28.33


def test_empty_data(sample_data):
    """Проверяет расчет показателей при отсутствии данных."""

    empty_data = sample_data.iloc[0:0]
    result = calculate_metrics(empty_data)

    assert result["revenue"] == 0
    assert result["orders"] == 0
    assert result["pizzas"] == 0
    assert result["average_check"] == 0


def test_filter_data(sample_data):
    """Проверяет фильтрацию данных."""

    result = filter_data(
        sample_data,
        "2015-01-01",
        "2015-01-01",
        ["Classic"],
        ["M"],
    )

    assert len(result) == 1
    assert result.iloc[0]["name"] == "Pizza A"


def test_filter_no_results(sample_data):
    """Проверяет фильтрацию при отсутствии подходящих записей."""

    result = filter_data(
        sample_data,
        "2015-03-01",
        "2015-03-31",
        ["Classic"],
        ["M"],
    )

    assert result.empty


def test_sales_by_month(sample_data):
    """Проверяет расчет выручки по месяцам."""

    result = sales_by_month(sample_data)

    assert result["month"].tolist() == [1, 2]
    assert result["revenue"].tolist() == [70, 15]


def test_orders_by_hour(sample_data):
    """Проверяет количество уникальных заказов по часам."""

    result = orders_by_hour(sample_data)

    assert result["hour"].tolist() == [12, 15, 18]
    assert result["order_id"].tolist() == [1, 1, 1]


def test_orders_by_weekday(sample_data):
    """Проверяет количество заказов по дням недели."""

    result = orders_by_weekday(sample_data)

    assert result["day_of_week"].tolist() == [3, 4, 6]
    assert result["order_id"].tolist() == [1, 1, 1]


def test_popular_pizzas(sample_data):
    """Проверяет определение наиболее популярной пиццы."""

    result = popular_pizzas(sample_data, limit=1)

    assert result.iloc[0]["name"] == "Pizza A"
    assert result.iloc[0]["quantity"] == 5


def test_unpopular_pizzas(sample_data):
    """Проверяет определение наименее популярных пицц."""

    result = unpopular_pizzas(sample_data, limit=2)

    assert set(result["name"]) == {"Pizza B", "Pizza C"}
    assert result["quantity"].tolist() == [1, 1]


def test_sales_by_category(sample_data):
    """Проверяет расчет выручки по категориям."""

    result = sales_by_category(sample_data)

    revenue = dict(zip(result["category"], result["revenue"]))

    assert revenue == {
        "Chicken": 20,
        "Classic": 50,
        "Veggie": 15,
    }


def test_sales_by_size(sample_data):
    """Проверяет количество проданных пицц по размерам."""

    result = sales_by_size(sample_data)

    quantity = dict(zip(result["size"], result["quantity"]))

    assert quantity == {
        "L": 1,
        "M": 5,
        "S": 1,
    }

def test_find_most_profitable_day_correct(sample_data):
    """Проверяет, что функция находит день с максимальной выручкой."""
    # В sample_data: день 3 (сумма 40), день 4 (сумма 30), день 6 (сумма 15). 
    # Максимум у дня 3.
    assert find_most_profitable_day(sample_data) == 3

def test_find_most_profitable_day_empty():
    """Проверяет работу с пустым DataFrame."""
    empty_df = pd.DataFrame(columns=["day_of_week", "revenue"])
    assert find_most_profitable_day(empty_df) is None

def test_find_most_profitable_day_tie():
    """Проверяет сценарий с одинаковой максимальной выручкой."""
    df = pd.DataFrame({
        "day_of_week": [1, 2], 
        "revenue": [10000, 10000]
    })
    result = find_most_profitable_day(df)
    assert result in [1, 2]
