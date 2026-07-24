def parse_value_and_type_from_string(val: str):
    """Парсит аргументы из строки. Пытается извлечь int, float, bool."""
    val = val.strip()

    # пустая строка
    if val == '':
        return val, str

    # Булевы значения
    if val.lower() in ('true', 'false'):
        return val.lower() == 'true', bool

    # None
    if val.lower() in ('none', 'null'):
        return None, None

    # Числа float, int
    try:
        if '.' in val:
            return float(val), float
        return int(val), int
    except ValueError:
        pass

    # Если ничего не подошло — возвращает строку (убирая кавычки)
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1], str
    return val, str


if __name__ == '__main__':
    # пример использования
    print(parse_value_and_type_from_string(val='100'))  # -> (100, <class 'int'>)
