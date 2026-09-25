import tkinter as tk
import warnings
from tkinter import ttk
from typing import Any

from infrastructure_tk_ui.styles.style_schemas import StyleSchema


class StyleManager:
    def __init__(
            self, themes: list[list[StyleSchema]], theme_use: str = 'clam',
            disabled_tk: bool = False, disabled_ttk: bool = False, disabled_options: bool = False,
            bypass: bool = False,
    ):
        """
        :param theme_use: используемая тема, например 'clam'
        :param disabled_tk: отключить tk стили
        :param disabled_ttk: отключить ttk стили
        :param disabled_options: отключить общие стили передаваемые через options
        :param bypass: отключить все стили и полностью игнорировать данную обёртку
        """
        self._root: tk.Tk | tk.Toplevel | None = None
        self._styles = ttk.Style()
        self._styles.theme_use(theme_use)  # clam наиболее подходящая под различные OS
        self._current_style: list[StyleSchema] | None = None

        self._disabled_tk = disabled_tk if not bypass else True
        self._disabled_ttk = disabled_ttk if not bypass else True
        self._disabled_options = disabled_options if not bypass else True
        self._bypass = bypass

        # кеширование уже примененных стилей (чтобы не переприменять одни и те же стили
        # на например кучу кнопок которые юзают один и тот же стиль)
        self._applied_ttk_styles: set[str] = set()
        self._applied_options: set[tuple[str, Any]] = set()
        # индекс текущей темы
        self._themes_list = themes
        self._theme_index = 0

    def reset_cache(self) -> None:
        """Сброс стилей (задел на будущее, если стили понадобится менять в рантайме)"""
        self._applied_ttk_styles = set()
        self._applied_options = set()

    def theme_switcher(self):
        """
        Последовательное переключение по списку тем.
        """
        if self._root is None:
            self._bypass = True
            warnings.warn(f'Стили не применены. нужно вызвать метод .apply с передачей корневого окна')
        self._theme_index += 1
        if self._theme_index >= len(self._themes_list):
            self._theme_index = 0
        self.apply(container=self._root)

    def apply(self, container: tk.Misc) -> None:
        """
        :param container: главное окно на котором размещены элементы (к его дочерним элементам применятся стили)
        """
        if self._bypass:
            return

        # определение корневого окна
        self._root = container
        self.reset_cache()
        self._current_style = self._themes_list[self._theme_index]

        self._apply_start(container)
        # применение стилей к root окну (если в styles_in явно прописан root)
        for st in self._current_style:
            if st.widget_name == 'root':
                self._root.configure(st.tk)

    def _apply_start(self, container: tk.Misc | None = None) -> None:
        """
        Рекурсивное применение стилей к дочерним элементам
        :param container: родительское окно в рамках которого стилизуются элементы
        """
        target = container if container is not None else self._root
        if target != self._root:
            self._apply(target)

        for child in target.winfo_children():
            if child.winfo_children():
                self._apply_start(child)
            else:
                self._apply(child)

    def _apply(self, form: tk.Misc | ttk.Widget, layer: int | str | None = None) -> None:
        """
        Применение стилей к конкретным элементам с автораспределением.
        :param layer:
        :param form: форма к которой применяются стили
        """
        if self._bypass:
            return
        name = form.widgetName

        is_ttk = False
        if 'ttk' in name:
            name = name.split(':')[-1]
            is_ttk = True

        current_style = None

        for st in self._current_style:
            if st.widget_name == name:
                if layer is not None and layer != st.layer:
                    continue
                current_style = st

        # если стиль для виджета не найден
        if current_style is None:
            warnings.warn(f'Не найден стиль для элемента `{name}`')
            return

        if is_ttk:
            # если ttk стили переданы
            if current_style.ttk is not None and not self._disabled_ttk:
                # применение ttk стилей
                style_name = current_style.ttk.style_name
                if style_name not in self._applied_ttk_styles:
                    # применение прямых стилей для ttk элементов
                    self._applied_ttk_styles.add(style_name)  # добавить элемент в кеш
                    for key, val in current_style.ttk.styles_dict.items():
                        try:
                            self._styles.configure(style_name, **{key: val})
                        except Exception as err:
                            warnings.warn(
                                f'Не удалось применить конфигурацию ttk,{current_style.ttk.styles_dict}: {err}'
                            )
                    # применение маппинга для ttk стилей (состояния active, pressed, disabled и другие)
                    # если передан disabled, то перезаписывает configure
                    mapping = current_style.ttk.mapping
                    if mapping is not None:
                        for map_schema in mapping:
                            self._styles.map(style_name, **{map_schema: mapping[map_schema]})

                # привязать конфигурацию к элементу
                form.configure(style=style_name)  # noqa

        # применить конфигурацию для tk виджетов
        if not self._disabled_tk:
            allowed_prop = list(form.configure().keys())
            congif = {}
            for key, val in current_style.tk.items():
                if key in allowed_prop:
                    congif[key] = val
            form.configure(**congif)

        if not self._disabled_options:
            # применение общих глобальных опций по шаблону, например стили для выпадающего меню Combobox [('*TCombobox*Listbox.background', 'red' )]
            for pattern, option in current_style.options:
                key = (pattern, option)
                if key not in self._applied_options:
                    self._root.option_add(pattern, option)
                    self._applied_options.add(key)
