from infrastructure_tk_ui.styles.style_schemas import StyleSchema, StyleSchemaTTK


# ========================================================================
# Стили для tk, ttk, ttk mapping, options, эту часть можно генерить с ИИ
# не перегружая его остальным кодом.
# Элементы для которых задаются стили:
# 'root', 'button', 'entry', 'label', 'checkbox', 'text', 'progressbar', 'combobox', 'checkbutton', 'radiobutton'
# можно полноценно использовать и темы определенные здесь
# ========================================================================
def get_standart_styles(preset) -> list[StyleSchema]:
    """
    Возвращает готовые темы.
    :param preset: описание темы. (см. в presets/themes)
    """
    styles = [
        # ---------- ROOT ----------
        StyleSchema(
            widget_name='root',
            tk={'bg': preset.BG},
        ),

        # ---------- BUTTON ----------
        StyleSchema(
            layer=1,
            widget_name='button',
            tk={'bg': preset.BG, 'font': preset.FONT, 'fg': preset.TEXT, 'cursor': 'hand2'},
            ttk=StyleSchemaTTK(
                style_name='Custom.TButton',
                styles_dict={
                    'background': preset.BG,
                    'foreground': preset.TEXT,
                    'bordercolor': preset.BORDER,
                    'borderwidth': preset.BORDER_WIDTH,
                    'relief': 'solid',
                    'font': preset.FONT,
                },
                mapping={
                    'background': [
                        ('active', preset.HOVER),
                        ('pressed', preset.PRESSED),
                        ('!disabled', preset.BG),
                    ],
                    'foreground': [
                        ('disabled', preset.DISABLED),
                        ('!disabled', preset.TEXT),
                    ],
                },
            ),
        ),

        # ---------- ENTRY ----------
        StyleSchema(
            layer=1,
            widget_name='entry',
            tk={'bg': preset.BG, 'fg': preset.TEXT, 'font': preset.FONT},
            ttk=StyleSchemaTTK(
                style_name='Custom.TEntry',
                styles_dict={
                    'fieldbackground': preset.BG,
                    'foreground': preset.TEXT,
                    'bordercolor': preset.BORDER,
                    'borderwidth': 2,
                    'relief': 'solid',
                    'padding': 3,
                },
                mapping={
                    'fieldbackground': [
                        ('focus', preset.HOVER),
                        ('!disabled', preset.BG),
                    ],
                    'foreground': [
                        ('disabled', preset.DISABLED),
                        ('!disabled', preset.TEXT),
                    ],
                },
            ),
        ),

        # ---------- LABEL ----------
        StyleSchema(
            layer=1,
            widget_name='label',
            tk={'bg': preset.BG, 'fg': preset.TEXT, 'font': preset.FONT},
            ttk=StyleSchemaTTK(
                style_name='Custom.TLabel',
                styles_dict={
                    'background': preset.BG,
                    'foreground': preset.TEXT,
                    'font': preset.FONT,
                },
                mapping={
                    'foreground': [
                        ('disabled', preset.DISABLED),
                        ('!disabled', preset.TEXT),
                    ],
                },
            ),
        ),

        # ---------- CHECKBOX ----------
        StyleSchema(
            layer=1,
            widget_name='checkbutton',
            tk={'bg': preset.BG, 'fg': preset.TEXT, 'font': preset.FONT},
            ttk=StyleSchemaTTK(
                style_name='Custom.TCheckbutton',
                styles_dict={
                    'background': preset.BG,
                    'foreground': preset.TEXT,
                    'font': preset.FONT,
                    'indicatorcolor': preset.BORDER,
                },
                mapping={
                    'background': [
                        ('active', 'selected', preset.BG),
                        ('active', '!selected', preset.BG),
                        ('selected', preset.BG),
                        ('disabled', preset.BG),
                        ('!disabled', preset.BG),
                    ],
                    'indicatorcolor': [
                        ('selected', preset.ACCENT),
                        ('!selected', preset.BORDER),
                        ('disabled', preset.DISABLED),
                    ],
                    'foreground': [
                        ('disabled', preset.DISABLED),
                        ('!disabled', preset.TEXT),
                    ],
                },
            ),
        ),

        # ---------- TEXT (TextArea) ----------
        StyleSchema(
            layer=1,
            widget_name='text',
            tk={
                'bg': preset.BG,
                'fg': preset.TEXT,
                'font': preset.FONT,
                'insertbackground': preset.TEXT,  # цвет курсора
                'selectbackground': preset.HOVER,  # цвет выделения
                'selectforeground': preset.TEXT,
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
                    'troughcolor': preset.PRESSED,  # фон пустой части
                    'background': preset.ACCENT,  # заполненная часть
                    'bordercolor': preset.BG,
                    'lightcolor': preset.ACCENT,
                    'darkcolor': preset.ACCENT,
                },
                mapping={
                    'background': [
                        ('!disabled', preset.ACCENT),
                    ],
                },
            ),
        ),

        # ---------- COMBOBOX ----------
        StyleSchema(
            layer=1,
            widget_name='combobox',
            tk={'bg': preset.BG, 'fg': preset.TEXT, 'font': preset.FONT},
            ttk=StyleSchemaTTK(
                style_name='Custom.TCombobox',
                styles_dict={
                    'fieldbackground': preset.BG,
                    'background': preset.BG,
                    'foreground': preset.TEXT,
                    'arrowcolor': preset.TEXT,
                    'bordercolor': preset.BORDER,
                    'borderwidth': 2,
                    'relief': 'solid',
                    'padding': 3,
                },
                mapping={
                    'fieldbackground': [
                        ('readonly', preset.BG),
                        ('!disabled', preset.BG),
                    ],
                    'background': [
                        ('active', preset.HOVER),
                        ('!disabled', preset.BG),
                    ],
                    'foreground': [
                        ('readonly', preset.TEXT),
                        ('!disabled', preset.TEXT),
                    ],
                    'arrowcolor': [
                        ('active', preset.TEXT),
                        ('!disabled', preset.TEXT),
                    ],
                },
            ),
            # для внутреннего Listbox (option_add)
            options=[
                ('*TCombobox*Listbox.font', preset.FONT),
                ('*TCombobox*Listbox.background', preset.BG),
                ('*TCombobox*Listbox.foreground', preset.TEXT),
                ('*TCombobox*Listbox.selectBackground', preset.HOVER),
                ('*TCombobox*Listbox.selectForeground', preset.TEXT),
            ],
        ),

        # ---------- RADIOBUTTON ----------
        StyleSchema(
            layer=1,
            widget_name='radiobutton',
            tk={'bg': preset.BG, 'fg': preset.TEXT, 'font': preset.FONT},
            ttk=StyleSchemaTTK(
                style_name='Custom.TRadiobutton',
                styles_dict={
                    'background': preset.BG,
                    'foreground': preset.TEXT,
                    'font': preset.FONT,
                    'indicatorcolor': preset.BORDER,
                },
                mapping={
                    'background': [
                        ('active', 'selected', preset.BG),
                        ('active', '!selected', preset.BG),
                        ('selected', preset.BG),
                        ('disabled', preset.BG),
                        ('!disabled', preset.BG),
                    ],
                    'indicatorcolor': [
                        ('selected', preset.ACCENT),
                        ('!selected', preset.BORDER),
                        ('disabled', preset.DISABLED),
                    ],
                    'foreground': [
                        ('disabled', preset.DISABLED),
                        ('!disabled', preset.TEXT),
                    ],
                },
            ),
        ),

        # ---------- FRAME ----------
        StyleSchema(
            layer=1,
            widget_name='frame',
            tk={'bg': preset.BG},
            ttk=StyleSchemaTTK(
                style_name='Custom.TFrame',
                styles_dict={
                    'background': preset.BG,
                    'bordercolor': preset.BORDER,
                    'borderwidth': 0,
                    'relief': 'flat',
                },
                mapping={
                    'background': [
                        ('!disabled', preset.BG),
                    ],
                },
            ),
        ),

        # ---------- SCROLLBAR ----------
        StyleSchema(
            layer=1,
            widget_name='scrollbar',
            tk={'bg': preset.BG, 'troughcolor': preset.PRESSED, 'activebackground': preset.HOVER},
            ttk=StyleSchemaTTK(
                style_name='Custom.Vertical.TScrollbar',
                styles_dict={
                    'background': preset.BORDER,
                    'troughcolor': preset.PRESSED,
                    'bordercolor': preset.BG,
                    'arrowcolor': preset.TEXT,
                    'darkcolor': preset.BORDER,
                    'lightcolor': preset.BORDER,
                },
                mapping={
                    'background': [
                        ('active', preset.HOVER),
                        ('pressed', preset.PRESSED),
                        ('!disabled', preset.BORDER),
                    ],
                    'arrowcolor': [
                        ('disabled', preset.DISABLED),
                        ('!disabled', preset.TEXT),
                    ],
                },
            ),
        ),

    ]
    return styles
