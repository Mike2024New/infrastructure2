from enum import Enum
from infrastructure_tk_ui import StyleSchema, StyleSchemaTTK


# ========================================================================
# Стили для tk, ttk, ttk mapping, options, эту часть можно генерить с ИИ
# не перегружая его остальным кодом.
# Элементы для которых задаются стили:
# 'root', 'button', 'entry', 'label', 'checkbox', 'text', 'progressbar', 'combobox', 'checkbutton', 'radiobutton'
# ========================================================================

# ========================================================================
# ЦВЕТА И ШРИФТЫ (менять здесь — применится везде)
# ========================================================================
class Colors(Enum):
    BG = '#0E1B29'  # основной фон (тёмно-синий)
    TEXT = 'white'  # основной текст
    HOVER = '#1A3A5C'  # цвет при наведении
    PRESSED = '#0A1220'  # цвет при нажатии
    DISABLED = 'gray'  # отключённый элемент
    BORDER = 'gray'  # цвет рамки
    BORDER_WIDTH = 1  # бордеры на кнопках и у рамок
    ACCENT = 'white'  # акцент (прогресс бар)


FONT = ('arial', 11, 'normal')

# ========================================================================
# СТИЛИ (по одному слою на каждый виджет)
# ========================================================================
styles = [
    # ---------- ROOT ----------
    StyleSchema(
        widget_name='root',
        tk={'bg': Colors.BG.value},
    ),

    # ---------- BUTTON ----------
    StyleSchema(
        layer=1,
        widget_name='button',
        tk={'bg': Colors.BG.value, 'font': FONT, 'fg': Colors.TEXT.value, 'cursor': 'hand2'},
        ttk=StyleSchemaTTK(
            style_name='Custom.TButton',
            styles_dict={
                'background': Colors.BG.value,
                'foreground': Colors.TEXT.value,
                'bordercolor': Colors.BORDER.value,
                'borderwidth': Colors.BORDER_WIDTH.value,
                'relief': 'solid',
                'font': FONT,
            },
            mapping={
                'background': [
                    ('active', Colors.HOVER.value),
                    ('pressed', Colors.PRESSED.value),
                    ('!disabled', Colors.BG.value),
                ],
                'foreground': [
                    ('disabled', Colors.DISABLED.value),
                    ('!disabled', Colors.TEXT.value),
                ],
            },
        ),
    ),

    # ---------- ENTRY ----------
    StyleSchema(
        layer=1,
        widget_name='entry',
        tk={'bg': Colors.BG.value, 'fg': Colors.TEXT.value, 'font': FONT},
        ttk=StyleSchemaTTK(
            style_name='Custom.TEntry',
            styles_dict={
                'fieldbackground': Colors.BG.value,
                'foreground': Colors.TEXT.value,
                'bordercolor': Colors.BORDER.value,
                'borderwidth': 2,
                'relief': 'solid',
                'padding': 3,
            },
            mapping={
                'fieldbackground': [
                    ('focus', Colors.HOVER.value),
                    ('!disabled', Colors.BG.value),
                ],
                'foreground': [
                    ('disabled', Colors.DISABLED.value),
                    ('!disabled', Colors.TEXT.value),
                ],
            },
        ),
    ),

    # ---------- LABEL ----------
    StyleSchema(
        layer=1,
        widget_name='label',
        tk={'bg': Colors.BG.value, 'fg': Colors.TEXT.value, 'font': FONT},
        ttk=StyleSchemaTTK(
            style_name='Custom.TLabel',
            styles_dict={
                'background': Colors.BG.value,
                'foreground': Colors.TEXT.value,
                'font': FONT,
            },
            mapping={
                'foreground': [
                    ('disabled', Colors.DISABLED.value),
                    ('!disabled', Colors.TEXT.value),
                ],
            },
        ),
    ),

    # ---------- CHECKBOX ----------
    StyleSchema(
        layer=1,
        widget_name='checkbutton',
        tk={'bg': Colors.BG.value, 'fg': Colors.TEXT.value, 'font': FONT},
        ttk=StyleSchemaTTK(
            style_name='Custom.TCheckbutton',
            styles_dict={
                'background': Colors.BG.value,
                'foreground': Colors.TEXT.value,
                'font': FONT,
                'indicatorcolor': Colors.BORDER.value,
            },
            mapping={
                'background': [
                    ('active', 'selected', Colors.BG.value),
                    ('active', '!selected', Colors.BG.value),
                    ('selected', Colors.BG.value),
                    ('disabled', Colors.BG.value),
                    ('!disabled', Colors.BG.value),
                ],
                'indicatorcolor': [
                    ('selected', Colors.ACCENT.value),
                    ('!selected', Colors.BORDER.value),
                    ('disabled', Colors.DISABLED.value),
                ],
                'foreground': [
                    ('disabled', Colors.DISABLED.value),
                    ('!disabled', Colors.TEXT.value),
                ],
            },
        ),
    ),

    # ---------- TEXT (TextArea) ----------
    StyleSchema(
        layer=1,
        widget_name='text',
        tk={
            'bg': Colors.BG.value,
            'fg': Colors.TEXT.value,
            'font': FONT,
            'insertbackground': Colors.TEXT.value,  # цвет курсора
            'selectbackground': Colors.HOVER.value,  # цвет выделения
            'selectforeground': Colors.TEXT.value,
            'relief': 'solid',
            'borderwidth': 2,
        },
    ),

    # ---------- PROGRESS BAR ----------
    StyleSchema(
        layer=1,
        widget_name='progressbar',
        ttk=StyleSchemaTTK(
            style_name='Custom.Horizontal.TProgressbar',
            styles_dict={
                'troughcolor': Colors.PRESSED.value,  # фон пустой части
                'background': Colors.ACCENT.value,  # заполненная часть
                'bordercolor': Colors.BG.value,
                'lightcolor': Colors.ACCENT.value,
                'darkcolor': Colors.ACCENT.value,
            },
            mapping={
                'background': [
                    ('!disabled', Colors.ACCENT.value),
                ],
            },
        ),
    ),

    # ---------- COMBOBOX ----------
    StyleSchema(
        layer=1,
        widget_name='combobox',
        tk={'bg': Colors.BG.value, 'fg': Colors.TEXT.value, 'font': FONT},
        ttk=StyleSchemaTTK(
            style_name='Custom.TCombobox',
            styles_dict={
                'fieldbackground': Colors.BG.value,
                'background': Colors.BG.value,
                'foreground': Colors.TEXT.value,
                'arrowcolor': Colors.TEXT.value,
                'bordercolor': Colors.BORDER.value,
                'borderwidth': 2,
                'relief': 'solid',
                'padding': 3,
            },
            mapping={
                'fieldbackground': [
                    ('readonly', Colors.BG.value),
                    ('!disabled', Colors.BG.value),
                ],
                'background': [
                    ('active', Colors.HOVER.value),
                    ('!disabled', Colors.BG.value),
                ],
                'foreground': [
                    ('readonly', Colors.TEXT.value),
                    ('!disabled', Colors.TEXT.value),
                ],
                'arrowcolor': [
                    ('active', Colors.TEXT.value),
                    ('!disabled', Colors.TEXT.value),
                ],
            },
        ),
        # для внутреннего Listbox (option_add)
        options=[
            ('*TCombobox*Listbox.font', FONT),
            ('*TCombobox*Listbox.background', Colors.BG.value),
            ('*TCombobox*Listbox.foreground', Colors.TEXT.value),
            ('*TCombobox*Listbox.selectBackground', Colors.HOVER.value),
            ('*TCombobox*Listbox.selectForeground', Colors.TEXT.value),
        ],
    ),

    # ---------- RADIOBUTTON ----------
    StyleSchema(
        layer=1,
        widget_name='radiobutton',
        tk={'bg': Colors.BG.value, 'fg': Colors.TEXT.value, 'font': FONT},
        ttk=StyleSchemaTTK(
            style_name='Custom.TRadiobutton',
            styles_dict={
                'background': Colors.BG.value,
                'foreground': Colors.TEXT.value,
                'font': FONT,
                'indicatorcolor': Colors.BORDER.value,
            },
            mapping={
                'background': [
                    ('active', 'selected', Colors.BG.value),
                    ('active', '!selected', Colors.BG.value),
                    ('selected', Colors.BG.value),
                    ('disabled', Colors.BG.value),
                    ('!disabled', Colors.BG.value),
                ],
                'indicatorcolor': [
                    ('selected', Colors.ACCENT.value),
                    ('!selected', Colors.BORDER.value),
                    ('disabled', Colors.DISABLED.value),
                ],
                'foreground': [
                    ('disabled', Colors.DISABLED.value),
                    ('!disabled', Colors.TEXT.value),
                ],
            },
        ),
    ),

]
