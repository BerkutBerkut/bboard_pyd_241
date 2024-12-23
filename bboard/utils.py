import re

def has_odd_number(title):
    numbers = re.findall(r"\d+", title)  # Ищем все числа в строке
    for num in numbers:
        if int(num) % 2 != 0:  # Проверяем, является ли число нечетным
            return True
    return False
