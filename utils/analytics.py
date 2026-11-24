
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


def calculate_metrics(df, start_date=None, end_date=None):
    """Рассчитывает основные показатели продаж."""

    # Общая выручка
    revenue = df["revenue"].sum()

    # Количество уникальных заказов
    orders = df["order_id"].nunique()

    # Количество проданных пицц
    pizzas = df["quantity"].sum()

    # Средний чек
    average_check = revenue / orders if orders > 0 else 0

    # Средняя выручка за календарный день выбранного периода
    daily_sales = sales_by_day(df, start_date, end_date)
    average_daily_revenue = (
        daily_sales["revenue"].mean() if not daily_sales.empty else 0
    )

    # Среднее количество пицц в заказе
    average_pizzas_per_order = pizzas / orders if orders > 0 else 0

    return {
        "revenue": round(revenue, 2),
        "orders": orders,
        "pizzas": pizzas,
        "average_check": round(average_check, 2),
        "average_daily_revenue": round(average_daily_revenue, 2),
        "average_pizzas_per_order": round(average_pizzas_per_order, 2),
    }


def sales_by_day(df, start_date=None, end_date=None):
    """Рассчитывает выручку за каждый день, включая дни без продаж."""
    sales = df.groupby("date")["revenue"].sum()
    start_date = sales.index.min() if start_date is None else start_date
    end_date = sales.index.max() if end_date is None else end_date

    if pd.isna(start_date) or pd.isna(end_date):
        return sales.reset_index()

    dates = pd.date_range(start_date, end_date, name="date")
    return sales.reindex(dates, fill_value=0).reset_index()


def sales_by_month(df):
    """Рассчитывает выручку по месяцам."""
    return df.groupby("month")["revenue"].sum().reset_index()


def orders_by_hour(df):
    """Рассчитывает количество заказов по часам."""
    return df.groupby("hour")["order_id"].nunique().reset_index()


def orders_by_weekday(df):
    """Рассчитывает количество заказов по дням недели."""
    return df.groupby("day_of_week")["order_id"].nunique().reset_index()


def orders_by_weekday_and_hour(df):
    """Рассчитывает количество заказов по дням недели и часам."""
    return (
        df.groupby(["day_of_week", "hour"])["order_id"]
        .nunique()
        .reset_index()
    )


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


def pizzas_by_category(df):
    """Рассчитывает количество проданных пицц по категориям."""
    return df.groupby("category")["quantity"].sum().reset_index()


def sales_by_size(df):
    """Рассчитывает количество проданных пицц по размерам."""
    return df.groupby("size")["quantity"].sum().reset_index()
