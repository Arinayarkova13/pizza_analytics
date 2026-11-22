
import pandas as pd
import pytest

from utils.data_loader import load_data, get_data


def test_load_data():
    """Проверяет загрузку четырех исходных таблиц."""

    tables = load_data()

    assert len(tables) == 4

    for table in tables:
        assert isinstance(table, pd.DataFrame)
        assert not table.empty


def test_data_row_count():
    """Проверяет количество строк после объединения таблиц."""

    df = get_data()

    assert len(df) == 48620


def test_required_columns():
    """Проверяет наличие необходимых столбцов."""

    df = get_data()

    required_columns = [
        "order_id",
        "date",
        "hour",
        "month",
        "day_of_week",
        "name",
        "category",
        "size",
        "quantity",
        "price",
        "revenue",
    ]

    for column in required_columns:
        assert column in df.columns


def test_date_type():
    """Проверяет формат даты заказа."""

    df = get_data()

    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_revenue_calculation():
    """Проверяет расчет стоимости позиции заказа."""

    df = get_data()

    expected_revenue = df["quantity"] * df["price"]

    pd.testing.assert_series_equal(
        df["revenue"],
        expected_revenue,
        check_names=False,
    )


def test_missing_values():
    """Проверяет отсутствие пропущенных значений."""

    df = get_data()

    assert not df.isna().any().any()


def test_missing_files(tmp_path):
    """Проверяет обработку отсутствующих файлов."""

    with pytest.raises(FileNotFoundError):
        load_data(tmp_path)
