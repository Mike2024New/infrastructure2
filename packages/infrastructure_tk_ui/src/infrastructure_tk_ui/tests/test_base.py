import pytest
from infrastructure_tk_ui import RootWidget
from infrastructure_tk_ui import StyleManager, get_standart_styles, themes_standart

"""
Набор smoke тестов для проверки формы (что форма запускается и не вылетают ошибки)
"""


@pytest.fixture(scope='function')
def root():
    root = RootWidget(center_window=False)  # центрирование окна здесь не нужно
    root.form.withdraw()  # отключение окна для теста
    yield root
    root.form.destroy()  # завершение работы окна


def test_smoke_root_window(root):
    """Проверка что виджет запускается"""
    assert root.form.winfo_exists(), 'окно не запустилось'


def test_smoke_root_window_theme(root):
    """Проверка что стили применяются"""
    theme = get_standart_styles(preset=themes_standart.Nord())
    style_manager = StyleManager(themes=[theme])
    style_manager.apply(container=root.form)
    # тема применяется
    assert root.form.cget('bg') == themes_standart.Nord().BG, 'не применилась стандартная тема'
