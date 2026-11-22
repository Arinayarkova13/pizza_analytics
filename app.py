
import streamlit as st

from utils.data_loader import get_data
from utils.analytics import filter_data, calculate_metrics
from utils.charts import (
    CATEGORIES,
    monthly_sales_chart,
    hourly_orders_chart,
    weekday_orders_chart,
    popular_pizzas_chart,
    unpopular_pizzas_chart,
    category_sales_chart,
    size_sales_chart,
)


# Настройки страницы
st.set_page_config(
    page_title="Анализ заказов пиццерии",
    page_icon="🍕",
    layout="wide",
)

# Настройка внешнего вида и верхнего отступа основной области
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
        }

        .block-container h1 {
            font-size: 32px;
        }

        .block-container h2 {
            font-size: 26px;
        }

        .block-container h3 {
            font-size: 20px;
        }

        [data-testid="stMetricValue"] {
            font-size: 30px;
        }

        [data-testid="stMetricLabel"] {
            font-size: 15px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_pizza_data():
    """Загружает и кеширует подготовленные данные."""
    return get_data()


# Заголовок приложения
st.title("🍕 Анализ заказов пиццерии")


# Загрузка данных
try:
    df = load_pizza_data()
except Exception as error:
    st.error(f"Ошибка загрузки данных: {error}")
    st.stop()


# Боковая панель с фильтрами
st.sidebar.header("Фильтры")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Период анализа",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)


# Доступные категории и размеры
all_categories = sorted(df["category"].unique())
all_sizes = ["S", "M", "L", "XL", "XXL"]


def select_all_items(key, options):
    """Выбирает все значения фильтра."""
    if "Выбрать все" in st.session_state[key]:
        st.session_state[key] = options


# Фильтр по категориям
categories = st.sidebar.multiselect(
    "Категория пиццы",
    options=["Выбрать все"] + all_categories,
    default=all_categories,
    format_func=lambda category: CATEGORIES.get(category, category),
    key="pizza_categories",
    placeholder="Выберите категории",
    select_all=False,
    on_change=select_all_items,
    args=("pizza_categories", all_categories),
)


# Фильтр по размерам
sizes = st.sidebar.multiselect(
    "Размер пиццы",
    options=["Выбрать все"] + all_sizes,
    default=all_sizes,
    key="pizza_sizes",
    placeholder="Выберите размеры",
    select_all=False,
    on_change=select_all_items,
    args=("pizza_sizes", all_sizes),
)


# Проверка выбранного периода
if len(date_range) != 2:
    st.info("Выберите начальную и конечную даты.")
    st.stop()

start_date, end_date = date_range


# Фильтрация данных
filtered_df = filter_data(
    df,
    start_date,
    end_date,
    categories,
    sizes,
)


# Проверка наличия данных
if filtered_df.empty:
    st.warning("По выбранным фильтрам данные отсутствуют.")
    st.stop()


# Расчет ключевых показателей
metrics = calculate_metrics(filtered_df)

st.header("Ключевые показатели")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Общая выручка",
    f"${metrics['revenue']:,.2f}",
)

col2.metric(
    "Количество заказов",
    f"{metrics['orders']:,}",
)

col3.metric(
    "Продано пицц",
    f"{metrics['pizzas']:,}",
)

col4.metric(
    "Средний чек",
    f"${metrics['average_check']:,.2f}",
)

st.divider()


# Вкладки аналитического дашборда
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Обзор продаж",
        "Анализ загрузки",
        "Анализ ассортимента",
        "Данные",
    ]
)


# Вкладка 1. Обзор продаж
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            category_sales_chart(filtered_df),
            width="stretch",
        )

    with col2:
        st.plotly_chart(
            size_sales_chart(filtered_df),
            width="stretch",
        )

    st.plotly_chart(
        monthly_sales_chart(filtered_df),
        width="stretch",
    )


# Вкладка 2. Анализ загрузки
with tab2:
    st.plotly_chart(
        hourly_orders_chart(filtered_df),
        width="stretch",
    )

    st.plotly_chart(
        weekday_orders_chart(filtered_df),
        width="stretch",
    )


# Вкладка 3. Анализ ассортимента
with tab3:
    st.plotly_chart(
        popular_pizzas_chart(filtered_df),
        width="stretch",
    )

    st.plotly_chart(
        unpopular_pizzas_chart(filtered_df),
        width="stretch",
    )


# Вкладка 4. Просмотр и выгрузка данных
with tab4:
    st.subheader("Детализация заказов")

    display_df = filtered_df[
        [
            "order_id",
            "date",
            "time",
            "name",
            "category",
            "size",
            "quantity",
            "price",
            "revenue",
        ]
    ].copy()

    # Перевод категорий на русский язык
    display_df["category"] = display_df["category"].map(
        CATEGORIES
    )

    # Переименование столбцов
    display_df = display_df.rename(
        columns={
            "order_id": "Номер заказа",
            "date": "Дата",
            "time": "Время",
            "name": "Название пиццы",
            "category": "Категория",
            "size": "Размер",
            "quantity": "Количество",
            "price": "Цена, $",
            "revenue": "Стоимость позиции, $",
        }
    )

    st.write(f"Количество записей: {len(display_df)}")

    st.dataframe(
        display_df,
        hide_index=True,
        width="stretch",
    )

    # Подготовка CSV-файла для скачивания
    csv_data = display_df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="Скачать данные в CSV",
        data=csv_data,
        file_name="pizza_sales_report.csv",
        mime="text/csv",
    )
