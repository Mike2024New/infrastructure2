import tkinter as tk
from tkinter import ttk
from dataclasses import asdict
from typing import Literal

from infrastructure_tk_ui.parameters_class import StyleParameters

__all__ = ['StyleHandler']


class StyleHandler:
    """Контроль за стилями. Разделение стилей на 3 состояния default, hover, active"""

    def __init__(
            self,
            parent: tk.Tk | tk.Frame | tk.Toplevel,
            form: tk.Tk | tk.Frame | tk.Toplevel | tk.Misc | tk.Label,
            parameters: StyleParameters | None = None,
            ttk_style_name: str | None = None,
            ttk_style_map_default: dict | None = None,
            ttk_style_map_hover: dict | None = None,
            ttk_style_map_active: dict | None = None,
    ):
        self._active = False
        self._form = form
        self._parameters = parameters or StyleParameters()
        # карты для ttk стилей
        self._ttk_style_name = ttk_style_name

        # привод стилей для ttk к маппингу (так как лучше работает через маппинг, но через переопределение событий)
        if ttk_style_map_default:
            self._ttk_style_map_default = {key: [('readonly', val)] for key, val in ttk_style_map_default.items()}
        if ttk_style_map_hover:
            self._ttk_style_map_hover = {key: [('readonly', val)] for key, val in ttk_style_map_hover.items()}
        if ttk_style_map_active:
            self._ttk_style_map_active = {key: [('readonly', val)] for key, val in ttk_style_map_active.items()}

        # если цвет не был задан явно, то взять цвет родителя
        if self._parameters.back_color is None:
            self._parameters.back_color = parent.cget('bg')
        if self._parameters.line_color is None:
            self._parameters.line_color = parent.cget('bg')

        # в эти коллекции сохраняются свойства виджетов после ini (чтобы не определять их каждый раз по новой)
        self.tk_default_parameters = {}
        self.tk_hover_parameters = {}
        self.tk_active_parameters = {}

        self.default_ini()  # хеширование параметров по умолчанию
        # подключение обработчиков событий (только те которые указаны явно. О - оптимизация)
        parameters_dict = asdict(self._parameters)
        if any('active_' in key for key in parameters_dict if parameters_dict[key] is not None):
            # обработка активного окна
            self.active_ini()  # хеширование параметров active
            self._form.bind('<FocusIn>', self.set_active)  # событие поле активно
            self._form.bind('<FocusOut>', self.unset_active)  # событие поле не активно
        if any('hover_' in key for key in parameters_dict if parameters_dict[key] is not None):
            self.hover_ini()  # хеширование параметров hover
            # обработка поля когда на него навелась/снялась мышь
            self._form.bind('<Enter>', self.set_hover)
            self._form.bind('<Leave>', self.unset_hover)
        # установить значения по умолчанию
        self.set_default(_event=None)

    def apply_tk_configure(self, prefix: Literal['default', 'active', 'hover'], **kwargs):
        """Кеширование параметров, чтобы не пересчитывать их каждый раз"""
        configure = {}
        # available_configure_fields - отсечь не допустимые для виджета поля, например anchor для entry
        available_configure_fields = self._form.configure()

        for prop, value in kwargs.items():
            if value is not None and prop in available_configure_fields:
                configure[prop] = value
        if prefix == 'default':
            self.tk_default_parameters = configure
        if prefix == 'hover':
            self.tk_hover_parameters = configure
        if prefix == 'active':
            self.tk_active_parameters = configure

    def default_ini(self):
        """Инициализация дефолтных параметров"""
        self.apply_tk_configure(
            prefix='default',
            bg=self._parameters.back_color,
            highlightthickness=self._parameters.line_th,
            highlightbackground=self._parameters.line_color,
            # стилизация отступов
            justify=self._parameters.align_parameters.justify,
            anchor=self._parameters.align_parameters.anchor,
            # стиллизация шрифтов
            fg=self._parameters.text_parameters.text_color,
            font=(
                self._parameters.text_parameters.text_family,
                self._parameters.text_parameters.text_size,
                self._parameters.text_parameters.text_style,
            ),
            # стилизация отступов
            padx=self._parameters.padding_parameters.padx,
            pady=self._parameters.padding_parameters.pady,
        )
        self._form.configure(**self.tk_default_parameters)

    def hover_ini(self):
        """Инициализация параметров для hover эффектов"""
        self.apply_tk_configure(
            prefix='hover',
            bg=self._parameters.hover_back_color,
            highlightthickness=self._parameters.hover_line_th,
            highlightbackground=self._parameters.hover_line_color,
        )
        if self._parameters.hover_text_parameters is not None:
            self.apply_tk_configure(
                prefix='hover',
                fg=self._parameters.hover_text_parameters.text_color,
                font=(
                    self._parameters.hover_text_parameters.text_family,
                    self._parameters.hover_text_parameters.text_size,
                    self._parameters.hover_text_parameters.text_style,
                ),
            )
        if self._parameters.hover_align_parameters is not None:
            self.apply_tk_configure(
                prefix='hover',
                justify=self._parameters.hover_align_parameters.justify,
                anchor=self._parameters.hover_align_parameters.anchor,
            )
        if self._parameters.hover_padding_parameters is not None:
            self.apply_tk_configure(
                prefix='hover',
                padx=self._parameters.hover_padding_parameters.padx,
                pady=self._parameters.hover_padding_parameters.pady,
            )

    def active_ini(self):
        self.apply_tk_configure(
            prefix='active',
            bg=self._parameters.active_back_color,
            highlightthickness=self._parameters.active_line_th,
            highlightbackground=self._parameters.active_line_color,
        )
        if self._parameters.active_text_parameters is not None:
            self.apply_tk_configure(
                prefix='active',
                fg=self._parameters.active_text_parameters.text_color,
                font=(
                    self._parameters.active_text_parameters.text_family,
                    self._parameters.active_text_parameters.text_size,
                    self._parameters.active_text_parameters.text_style,
                ),
            )
        if self._parameters.active_align_parameters is not None:
            self.apply_tk_configure(
                prefix='active',
                justify=self._parameters.active_align_parameters.justify,
                anchor=self._parameters.active_align_parameters.anchor,
            )
        if self._parameters.active_padding_parameters is not None:
            self.apply_tk_configure(
                prefix='active',
                padx=self._parameters.active_padding_parameters.padx,
                pady=self._parameters.active_padding_parameters.pady,
            )

    def set_default(self, _event):
        """Сброс виджета на значения по умолчанию"""
        if self._ttk_style_name is not None and self._ttk_style_map_default:
            style = ttk.Style()
            style.map(self._ttk_style_name, **self._ttk_style_map_default)
        self._form.configure(**self.tk_default_parameters)

    def set_hover(self, _event):
        if self._active:
            return
        if self._ttk_style_name is not None and self._ttk_style_map_hover:
            style = ttk.Style()
            style.map(self._ttk_style_name, **self._ttk_style_map_hover)
        self._form.configure(**self.tk_hover_parameters)

    def unset_hover(self, event):
        """Мышь снялась с элемента"""
        if self._active:
            return
        self.set_default(_event=event)

    def set_active(self, _event):
        self._active = True
        if self._ttk_style_name is not None and self._ttk_style_map_active:
            style = ttk.Style()
            style.map(self._ttk_style_name, **self._ttk_style_map_active)
        self._form.configure(**self.tk_active_parameters)

    def unset_active(self, event):
        """Элемент не активен"""
        self._active = False
        self.set_default(_event=event)

    def stop(self):
        """На будущее если будет необходимость высвобождения ресурса для динамических кнопок"""
        self._form.unbind('<FocusIn>')
        self._form.unbind('<FocusOut>')
        self._form.unbind('<Enter>')
        self._form.unbind('<Leave>')
