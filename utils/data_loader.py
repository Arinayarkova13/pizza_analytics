
from pathlib import Path

import pandas as pd


# Путь к папке с исходными данными
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data(data_dir=DATA_DIR):
    """Загружает исходные данные из CSV-файлов"""
    data_dir = Path(data_dir)

    orders = pd.read_csv(data_dir / "orders.csv")
    order_details = pd.read_csv(data_dir / "order_details.csv")
    pizzas = pd.read_csv(data_dir / "pizzas.csv")
    pizza_types = pd.read_csv(
        data_dir / "pizza_types.csv", encoding="latin1"
    )

    return orders, order_details, pizzas, pizza_types


def prepare_data(orders, order_details, pizzas, pizza_types):
    """Объединяет таблицы и подготавливает данные для анализа."""

    # Объединение таблиц по общим идентификаторам
    df = order_details.merge(orders, on="order_id")
    df = df.merge(pizzas, on="pizza_id")
    df = df.merge(pizza_types, on="pizza_type_id")

    # Преобразование даты и времени заказа
    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = pd.to_datetime(
        df["time"], format="%H:%M:%S"
    ).dt.hour

    # Определение месяца и дня недели
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.day_of_week

    # Расчет стоимости каждой позиции заказа
    df["revenue"] = df["quantity"] * df["price"]

    return df


def get_data(data_dir=DATA_DIR):
    """Возвращает подготовленные данные для анализа"""
    return prepare_data(*load_data(data_dir))


# Проверка работы модуля
if __name__ == "__main__":
    df = get_data()

    print("Данные успешно загружены")
    print("Количество строк:", len(df))
    print("Количество столбцов:", len(df.columns))
    print("Количество заказов:", df["order_id"].nunique())
    print("Количество проданных пицц:", df["quantity"].sum())
    print("Общая выручка:", round(df["revenue"].sum(), 2))

    print("\nПервые 5 строк:")
    print(df.head())
