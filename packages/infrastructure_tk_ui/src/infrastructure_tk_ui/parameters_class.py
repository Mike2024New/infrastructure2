from dataclasses import dataclass
from typing import Literal

__all__ = ['FontParameters', 'PackParameters']


@dataclass
class FontParameters:
    font_color: str = 'black'  # цвет шрифта
    font_family: str = 'Arial'
    font_size: int = 14
    font_style: Literal['normal', 'italic', 'bold'] = 'normal'


@dataclass
class PackParameters:
    fill: Literal['x', 'y', 'both', 'none'] = 'x'  # растяжение. например заполнить все доступное пространство по x
    padx: int = 5  # отступы снаружи Label, от границ родителя (фрейма)
    pady: int = 5  # отступы снаружи Label, от границ родителя (фрейма)
    expand: bool = True  # растягивать если есть свободное место?
    side: Literal['left', 'right', 'bottom', 'top'] = 'top'  # положение виджета, влияет на размещение дочерних виджетов

    def get(self) -> dict:
        return {
            "fill": self.fill,
            "padx": self.padx,
            "pady": self.pady,
            "expand": self.expand,
            "side": self.side,
        }
