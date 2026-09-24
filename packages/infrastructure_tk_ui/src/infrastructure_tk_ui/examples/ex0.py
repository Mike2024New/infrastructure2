import tkinter as tk
from tkinter import ttk
from typing import Any

from infrastructure_tk_ui import StyleManager as StyleManagerCore
from infrastructure_tk_ui import StylesTK, StylesTTK

"""
Создание стилей для всего приложения. Централизованно в одном файле. Унаследоваться от класса StyleManager и 
реализовать логику присвоения стилей в методах on_style_tk on_style_ttk
"""

background_color = '#0E1B29'
text_color = 'white'
font = ('arial', 12, 'normal')


class StyleManager(StyleManagerCore):
    def __init__(self, root: tk.Tk | tk.Toplevel):
        """
        :param root: проброс главного окна к которому будут применяться опции
        """
        super().__init__(root)

    def _on_options(self) -> list[tuple[str, Any]]:
        """Здесь генерируется список кортежей опций для виджетов ttk/tk, например: [('*TCombobox*Listbox.background', 'red' )]"""
        options = [
            ('*TCombobox*Listbox.font', font),
            ('*TCombobox*Listbox.background', background_color),
        ]
        return options

    def _on_style_tk(self) -> StylesTK | None:
        """В этих методах в дочерних классах реализовываются стили"""
        styles_tk = StylesTK(
            root={'bg': background_color},
            textarea={'bg': background_color, 'fg': text_color, 'font': font},
            combobox={'font': font},
        )
        return styles_tk

    def _on_style_ttk(self, style: ttk.Style, styles_ttk: StylesTTK) -> None:
        """В этих методах в дочерних классах реализовываются стили"""
        # buttons
        style.configure(
            styles_ttk.button, font=font, background=background_color, foreground=text_color,
            bordercolor='gray', borderwidth=2, relief='solid',
        )
        # label
        style.configure(
            styles_ttk.label, font=font, background=background_color, foreground=text_color,
        )
        # checkbox
        style.configure(
            styles_ttk.checkbutton, font=font, background=background_color, foreground=text_color,
        )
        # radiobutton
        style.configure(
            styles_ttk.radiobutton, font=font, background=background_color, foreground=text_color,
        )
        # progress_bar
        style.configure(
            styles_ttk.progressbar,
            troughcolor='black',  # Цвет фона (пустой части)
            background='darkgreen',  # Цвет заполненной части (полосы)
            bordercolor=background_color,  # Цвет границы
        )
        # Combobox -> внимание здесь шрифт игнорируется
        style.configure(
            styles_ttk.combobox,
            fieldbackground=background_color, background=background_color, foreground=text_color,
        )

        # привязка маппинг стилей
        # здесь стили просто отключены (поставлен фоновый цвет)
        # порядок крайне важен
        style.map(
            styles_ttk.checkbutton,
            background=[
                ('active', 'selected', background_color),  # наведена мышь и выбрано значение
                ('active', '!selected', background_color),  # наведена мышь но значение не выбрано
                ('selected', background_color),  # выбран (активно в фокусе)
                ('disabled', background_color),  # не выбран (не активно - не в фокусе)
            ],
        )

        style.map(
            styles_ttk.button, **{
                'background': [
                    ('active', 'selected', 'gray'),  # наведена мышь и выбрано значение
                    ('active', '!selected', 'gray'),  # наведена мышь но значение не выбрано
                    ('selected', background_color),  # выбран (активно в фокусе)
                    ('disabled', background_color),  # не выбран (не активно - не в фокусе)
                ]
            }
        )

        # style.map(
        #     styles_ttk.button,
        #     background=[
        #         ('active', 'selected', 'gray'),  # наведена мышь и выбрано значение
        #         ('active', '!selected', 'gray'),  # наведена мышь но значение не выбрано
        #         ('selected', background_color),  # выбран (активно в фокусе)
        #         ('disabled', background_color),  # не выбран (не активно - не в фокусе)
        #     ],
        # )
