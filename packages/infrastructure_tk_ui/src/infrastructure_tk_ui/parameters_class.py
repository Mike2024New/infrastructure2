from dataclasses import dataclass
from typing import Literal
import tkinter as tk
from tkinter import ttk

__all__ = [
    'FontParameters', 'PackParameters', 'FontResult',
    'AnimationParameters', 'BorderParameters', 'GridParameters',
]


@dataclass
class FontResult:
    color: str
    family: str
    size: int
    style: str
    select_text_back_color: str


@dataclass
class BorderParameters:
    th: int = 0  # толщина бордеров
    relief: Literal['solid', 'ridge', 'flat', 'groove', 'raised', 'sunken'] = 'solid'  # форма бордеров


@dataclass
class FontParameters:
    color: str = 'black'  # цвет шрифта
    family: str = 'Arial'
    size: int = 14
    bold: bool = False
    italic: bool = False
    underline: bool = False
    overstrike: bool = False
    select_text_back_color: str = 'steelblue'  # цвет выделенного текста
    style: str | None = None  # задать стиль на прямую, например "bold italic"

    def get(self) -> FontResult:
        if self.style is not None:
            style = self.style
        else:
            styles = []
            if self.bold:
                styles.append('bold')
            if self.italic:
                styles.append('italic')
            if self.underline:
                styles.append('underline')
            if self.overstrike:
                styles.append('overstrike')
            style = ' '.join(styles) if styles else 'normal'

        return FontResult(
            color=self.color,
            family=self.family,
            size=self.size,
            style=style,
            select_text_back_color=self.select_text_back_color,
        )


@dataclass
class GridParameters:
    row: int
    col: int
    rowspan: int = 1
    columnspan: int = 1
    # прилипание к сторонам: n-верх, s-низ, e-право, w-лево (nsew = растянуть на всю ячейку)
    sticky: str | None = 'nsew'

    def get(self) -> dict:
        return {
            "row": self.row,
            "column": self.col,
            "sticky": self.sticky,
            "rowspan": self.rowspan,
            "columnspan": self.columnspan,
        }


@dataclass
class PackParameters:
    fill: Literal['x', 'y', 'both', 'none'] = 'x'  # растяжение. например заполнить все доступное пространство по x
    padx: int = 0  # отступы снаружи Label, от границ родителя (фрейма)
    pady: int = 0  # отступы снаружи Label, от границ родителя (фрейма)
    expand: bool = False  # растягивать если есть свободное место?
    side: Literal['left', 'right', 'bottom', 'top'] = 'top'  # положение виджета, влияет на размещение дочерних виджетов

    def get(self) -> dict:
        return {
            "fill": self.fill,
            "padx": self.padx,
            "pady": self.pady,
            "expand": self.expand,
            "side": self.side,
        }


@dataclass
class AnimationParameters:
    active_color: str | None = None
    hover_color: str | None = None
    _back_color: str | None = None
    _active: bool = False
    _frame: tk.Tk | tk.Frame | tk.Toplevel | tk.Misc | None = None
    _style_ttk: ttk.Style | None = None
    _style_name_ttk: str | None = None

    def _active_window_in(self, _event) -> None:
        self._active = True
        if self._style_ttk is not None:
            self._style_ttk.map(
                self._style_name_ttk,
                fieldbackground=[('readonly', self.active_color)]
            )
        else:
            self._frame.configure(bg=self.active_color)

    def _active_window_out(self, _event) -> None:
        self._active = False
        if self._style_ttk is not None:
            self._style_ttk.map(
                self._style_name_ttk,
                fieldbackground=[('readonly', self._back_color)]
            )
        else:
            self._frame.configure(bg=self._back_color)

    def _hover_window_in(self, _event) -> None:
        if self._active:
            return
        if self._style_ttk is not None:
            self._style_ttk.map(
                self._style_name_ttk,
                fieldbackground=[('readonly', self.hover_color)]
            )
        else:
            self._frame.configure(bg=self.hover_color)

    def _hover_window_out(self, _event) -> None:
        if self._active:
            return
        if self._style_ttk is not None:
            self._style_ttk.map(
                self._style_name_ttk,
                fieldbackground=[('readonly', self._back_color)]
            )
        else:
            self._frame.configure(bg=self._back_color)

    def bind(
            self,
            back_color: str,
            form: tk.Tk | tk.Frame | tk.Toplevel | tk.Misc,
            style_ttk: tuple[str, ttk.Style] | None = None,
    ) -> None:
        """
        Привязка событий к форме
        :param back_color: фоновый цвет по умолчанию
        :param form: форма к которой применяются стили
        :param style_ttk: ttk более новые стили, у старых tk виджетов их нет. Передается кортеж (название, объект стиля)
        :return:
        """
        self._frame = form
        # если стили ttk виджеты
        if style_ttk:
            self._style_name_ttk, self._style_ttk = style_ttk
        self._back_color = back_color
        self.active_color = self.active_color if self.active_color else self._back_color
        self.hover_color = self.hover_color if self.hover_color else self._back_color

        # оптимизация, подключается только необходимое
        if self.active_color and self.active_color != self._back_color:
            self._frame.bind('<FocusIn>', self._active_window_in)  # событие поле активно
            self._frame.bind('<FocusOut>', self._active_window_out)  # событие поле не активно
        if self.hover_color and self.hover_color != self._back_color:
            self._frame.bind('<Enter>', self._hover_window_in)  # событие мышка навелась на поле
            self._frame.bind('<Leave>', self._hover_window_out)  # событие мышка ушла с поля
