from dataclasses import dataclass
from typing import Literal

__all__ = ['FontParameters', 'PackParameters', 'FontResult']


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
