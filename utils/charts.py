
import plotly.express as px

from utils.analytics import (
    sales_by_month,
    orders_by_hour,
    orders_by_weekday,
    popular_pizzas,
    unpopular_pizzas,
    sales_by_category,
    sales_by_size,
)


# Названия месяцев
MONTHS = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

# Названия дней недели
WEEKDAYS = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье",
}

# Названия категорий пицц
CATEGORIES = {
    "Classic": "Классические",
    "Chicken": "С курицей",
    "Supreme": "Фирменные",
    "Veggie": "Овощные",
}


def monthly_sales_chart(df):
    """Строит график выручки по месяцам."""

    data = sales_by_month(df)
    data["month"] = data["month"].map(MONTHS)

    fig = px.line(
        data,
        x="month",
        y="revenue",
        markers=True,
        title="Динамика выручки по месяцам",
        labels={
            "month": "Месяц",
            "revenue": "Выручка, $",
        },
    )

    fig.update_traces(line_color="#3B82F6")

    return fig


def hourly_orders_chart(df):
    """Строит график количества заказов по часам."""

    data = orders_by_hour(df)

    fig = px.bar(
        data,
        x="hour",
        y="order_id",
        title="Количество заказов по часам",
        labels={
            "hour": "Час",
            "order_id": "Количество заказов",
        },
    )

    fig.update_traces(marker_color="#8B5CF6")
    fig.update_xaxes(dtick=1)

    return fig


def weekday_orders_chart(df):
    """Строит график количества заказов по дням недели."""

    data = orders_by_weekday(df)
    data["day_of_week"] = data["day_of_week"].map(WEEKDAYS)

    fig = px.bar(
        data,
        x="day_of_week",
        y="order_id",
        title="Количество заказов по дням недели",
        labels={
            "day_of_week": "День недели",
            "order_id": "Количество заказов",
        },
    )

    fig.update_traces(marker_color="#14B8A6")

    return fig


def popular_pizzas_chart(df):
    """Строит график наиболее популярных пицц."""

    data = popular_pizzas(df)

    fig = px.bar(
        data,
        x="quantity",
        y="name",
        orientation="h",
        title="Топ-5 популярных пицц",
        labels={
            "quantity": "Количество проданных пицц",
            "name": "Название пиццы",
        },
    )

    fig.update_traces(marker_color="#27AE60")
    fig.update_yaxes(autorange="reversed")

    return fig


def unpopular_pizzas_chart(df):
    """Строит график наименее популярных пицц."""

    data = unpopular_pizzas(df)

    fig = px.bar(
        data,
        x="quantity",
        y="name",
        orientation="h",
        title="Топ-5 наименее популярных пицц",
        labels={
            "quantity": "Количество проданных пицц",
            "name": "Название пиццы",
        },
    )

    fig.update_traces(marker_color="#C0392B")
    fig.update_yaxes(autorange="reversed")

    return fig


def category_sales_chart(df):
    """Строит диаграмму выручки по категориям пицц."""

    data = sales_by_category(df)
    data["category"] = data["category"].map(CATEGORIES)

    fig = px.pie(
        data,
        names="category",
        values="revenue",
        hole=0.4,
        title="Выручка по категориям пицц",
        labels={
            "category": "Категория",
            "revenue": "Выручка, $",
        },
        color_discrete_sequence=[
            "#3B82F6",
            "#27AE60",
            "#E67E22",
            "#8B5CF6",
        ],
    )

    return fig


def size_sales_chart(df):
    """Строит график продаж по размерам пицц."""

    data = sales_by_size(df)

    fig = px.bar(
        data,
        x="size",
        y="quantity",
        title="Продажи по размерам пицц",
        labels={
            "size": "Размер",
            "quantity": "Количество проданных пицц",
        },
        category_orders={
            "size": ["S", "M", "L", "XL", "XXL"]
        },
    )

    fig.update_traces(marker_color="#E67E22")

    return fig
