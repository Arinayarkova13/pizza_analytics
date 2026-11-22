
import pandas as pd


def filter_data(df, start_date, end_date, categories, sizes):
    """Фильтрует данные по периоду, категориям и размерам пицц."""

    filtered = df[
        (df["date"] >= pd.Timestamp(start_date))
        & (df["date"] <= pd.Timestamp(end_date))
        & (df["category"].isin(categories))
        & (df["size"].isin(sizes))
    ]

    return filtered


def calculate_metrics(df):
    """Рассчитывает основные показатели продаж."""

    # Общая выручка
    revenue = df["revenue"].sum()

    # Количество уникальных заказов
    orders = df["order_id"].nunique()

    # Количество проданных пицц
    pizzas = df["quantity"].sum()

    # Средний чек
    average_check = revenue / orders if orders > 0 else 0

    return {
        "revenue": round(revenue, 2),
        "orders": orders,
        "pizzas": pizzas,
        "average_check": round(average_check, 2),
    }


def sales_by_month(df):
    """Рассчитывает выручку по месяцам."""
    return df.groupby("month")["revenue"].sum().reset_index()


def orders_by_hour(df):
    """Рассчитывает количество заказов по часам."""
    return df.groupby("hour")["order_id"].nunique().reset_index()


def orders_by_weekday(df):
    """Рассчитывает количество заказов по дням недели."""
    return df.groupby("day_of_week")["order_id"].nunique().reset_index()


def popular_pizzas(df, limit=5):
    """Определяет наиболее популярные пиццы."""
    return (
        df.groupby("name")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
        .reset_index()
    )


def unpopular_pizzas(df, limit=5):
    """Определяет наименее популярные пиццы."""
    return (
        df.groupby("name")["quantity"]
        .sum()
        .sort_values()
        .head(limit)
        .reset_index()
    )


def sales_by_category(df):
    """Рассчитывает выручку по категориям пицц."""
    return df.groupby("category")["revenue"].sum().reset_index()


def sales_by_size(df):
    """Рассчитывает количество проданных пицц по размерам."""
    return df.groupby("size")["quantity"].sum().reset_index()
