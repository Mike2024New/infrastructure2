from infrastructure_other import parse_value_and_type_from_string


def test_base():
    """Базовый тест приведения типов"""
    assert parse_value_and_type_from_string(val='') == ('', str)
    assert parse_value_and_type_from_string(val='100-001') == ('100-001', str)
    assert parse_value_and_type_from_string(val='100.2') == (100.2, float)
    assert parse_value_and_type_from_string(val='100') == (100, int)
    assert parse_value_and_type_from_string(val='true') == (True, bool)
    assert parse_value_and_type_from_string(val='false') == (False, bool)
