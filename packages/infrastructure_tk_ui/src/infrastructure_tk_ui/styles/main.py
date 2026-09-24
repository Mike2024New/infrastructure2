import tkinter as tk
from tkinter import ttk
from typing import Any

from infrastructure_tk_ui.styles.style_schemas import StylesTK, StylesTTK

"""
Создание стилей для всего приложения. Централизованно в одном файле.
Этот файл необходимо скопировать в проект, и расписать здесь все конфигурации
"""


class StyleManager:
    def __init__(self, root: tk.Tk | tk.Toplevel):
        self._root = root

    def set_style(
            self, tk_disable: bool = False, ttk_disable: bool = False, options_disable: bool = False
    ) -> tuple[StylesTK, StylesTTK]:
        """Установка и применение стилей"""
        style_tk = self._set_style_tk(disable=tk_disable)
        style_ttk = self._set_style_ttk(disable=ttk_disable)
        self._set_options(disable=options_disable)
        if not tk_disable:
            self._root.configure(**style_tk.root)
        return style_tk, style_ttk

    def _set_style_tk(self, disable: bool = False) -> StylesTK:
        """
        Определение стилей для tk виджетов
        В использующем модуле нужно определить стили
        """
        if disable:
            return StylesTK()

        styles_tk = self._on_style_tk()  # вызов определенных пользователем стилей
        return styles_tk or StylesTK()

    def _set_options(self, disable: bool = False) -> None:
        """
        Применение глобальных опций стилей, например для combobox
        root.form.option_add('*TCombobox*Listbox.font', font)
        """
        if disable:
            return
        options = self._on_options() or ()
        for pattern, value in options:
            self._root.option_add(pattern, value)

    def _on_options(self) -> list[tuple[str, Any]]:
        """Здесь генерируется список кортежей опций для виджетов ttk/tk, например: [('*TCombobox*Listbox.background', 'red' )]"""
        pass

    def _set_style_ttk(self, disable: bool = False) -> StylesTTK:
        """
        Определение стилей для ttk виджетов
        В использующем модуле нужно определить стили и опционально маппинги
        """
        style = ttk.Style()
        style.theme_use('clam')

        styles_ttk = StylesTTK(
            button='TButton',
            label='TLabel',
            checkbutton='TCheckbutton',
            radiobutton='TRadiobutton',
            progressbar='TProgressbar',
            combobox='TCombobox',
        )

        # тема по умолчанию
        if disable:
            return styles_ttk

        self._on_style_ttk(
            style=style,
            styles_ttk=styles_ttk,
        )  # применение стилей для ttk
        return styles_ttk

    def _on_style_tk(self) -> StylesTK | None:
        """В этих методах в дочерних классах реализовываются стили, Здесь генерируется словарь конфигурации для tk виджетов"""
        pass

    def _on_style_ttk(self, style: ttk.Style, styles_ttk) -> None:
        """
        В этих методах в дочерних классах реализовываются стили, здесь применяются конфигурации к стилям ttk
        :param style: объект к которому применяются стили
        :param styles_ttk: названия стилей
        """
        pass
