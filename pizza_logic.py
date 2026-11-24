#этот файл содержит функции, которые будем тестировать
def calculate_total_price(quantity, price):
    """Считает общую стоимость позиции (количество * цену)"""
    if quantity <= 0 or price < 0:
        raise ValueError("Количество должно быть больше 0, а цена не может быть отрицательной")
    return quantity * price

def find_most_profitable_day(revenue_dict):
    """Находит день недели с самой большой выручкой из словаря"""
    if not revenue_dict:
        return None
    #max() с key находит ключ-день, у которого самое большое значение-выручка
    return max(revenue_dict, key=revenue_dict.get)
