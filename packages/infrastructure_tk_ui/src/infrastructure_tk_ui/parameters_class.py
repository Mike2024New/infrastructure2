from dataclasses import dataclass
from typing import Literal
import tkinter as tk

__all__ = ['FontParameters', 'PackParameters', 'FontResult', 'AnimationParameters']


@dataclass
class FontResult:
    color: str
    family: str
    size: int
    style: str


@dataclass
class FontParameters:
    color: str = 'black'  # цвет шрифта
    family: str = 'Arial'
    size: int = 14
    bold: bool = False
    italic: bool = False
    underline: bool = False
    overstrike: bool = False
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

        return FontResult(color=self.color, family=self.family, size=self.size, style=style)


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

    def _active_window_in(self, _event):
        self._active = True
        self._frame.configure(bg=self.active_color)

    def _active_window_out(self, _event):
        self._active = False
        self._frame.configure(bg=self._back_color)

    def _hover_window_in(self, _event):
        if self._active:
            return
        self._frame.configure(bg=self.hover_color)

    def _hover_window_out(self, _event):
        if self._active:
            return
        self._frame.configure(bg=self._back_color)

    def bind(self, back_color: str, frame: tk.Tk | tk.Frame | tk.Toplevel | tk.Misc):
        """Привязка событий к форме"""
        self._frame = frame
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
