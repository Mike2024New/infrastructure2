from dataclasses import dataclass, field
from typing import Literal

__all__ = [
    'TextParameters', 'PackParameters',
    'StyleParameters', 'BorderParameters', 'GridParameters',
    'AlignParameters', 'PaddingParameters',
]


@dataclass
class AlignParameters:
    justify: Literal['left', 'right', 'center'] = 'left'  # выравнивание текста слева, важно учитывать
    anchor: Literal['center', 'e', 'n', 'nw', 's', 'se', 'sw', 'w'] = 'nw'  # стартовая точка виджета (например север)


@dataclass
class PaddingParameters:
    padx: int = 0
    pady: int = 0


@dataclass
class BorderParameters:
    th: int = 0  # толщина бордеров
    color: str = 'black'
    relief: Literal['solid', 'ridge', 'flat', 'groove', 'raised', 'sunken'] = 'solid'  # форма бордеров


@dataclass
class TextParameters:
    text_color: str = 'black'  # цвет шрифта
    text_family: str = 'Arial'
    text_size: int = 14
    text_bold: bool = False
    text_italic: bool = False
    text_underline: bool = False
    text_overstrike: bool = False
    text_select_back_color: str = 'steelblue'  # цвет выделенного текста

    @property
    def text_style(self) -> str:
        styles = []
        if self.text_bold:
            styles.append('bold')
        if self.text_italic:
            styles.append('italic')
        if self.text_underline:
            styles.append('underline')
        if self.text_overstrike:
            styles.append('overstrike')
        return ' '.join(styles) if styles else 'normal'


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
    # у fill -> both заполнить по обоим осям
    fill: Literal['x', 'y', 'both', 'none'] = 'x'  # растяжение. например заполнить все доступное пространство по x
    padx: int = 0  # отступы снаружи Label, от границ родителя (фрейма)
    pady: int = 0  # отступы снаружи Label, от границ родителя (фрейма)
    expand: bool = False  # растягивать если есть свободное место? (экспансия на всё свободное место)
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
class StyleParameters:
    back_color: str | None = None
    line_color: str | None = None
    line_th: int = 0
    text_parameters: TextParameters = field(default_factory=TextParameters)
    align_parameters: AlignParameters = field(default_factory=AlignParameters)
    padding_parameters: PaddingParameters = field(default_factory=PaddingParameters)
    # стили при активности (например input в котором печатается текст)
    active_back_color: str | None = None
    active_line_color: str | None = None
    active_line_th: int | None = None
    active_text_parameters: TextParameters | None = None
    active_align_parameters: AlignParameters | None = None
    active_padding_parameters: PaddingParameters | None = None
    # стили при наведении
    hover_back_color: str | None = None
    hover_line_color: str | None = None
    hover_line_th: int | None = None
    hover_text_parameters: TextParameters | None = None
    hover_align_parameters: AlignParameters | None = None
    hover_padding_parameters: PaddingParameters | None = None
