from dataclasses import dataclass

__all__ = [
    'Dracula', 'DarkGreen', 'DarkBlue', 'DarkGray', 'DarkPurple', 'DarkRed',
    'LightBlue', 'LightGray', 'LightGreen', 'LightPink', 'LightBeige', 'Nord',
    'HighContrast', 'Solarized', 'Monokai',
]


# ========================================================================
# Цветовые темы для tk, ttk, ttk mapping, options.
# Датаклассы — можно менять поля в рантайме, наследовать, кастомизировать.
# ========================================================================


# ========================================================================
# ТЁМНЫЕ ТЕМЫ
# ========================================================================

@dataclass
class DarkBlue:
    """Тёмно-синяя (текущая)"""
    BG: str = '#0E1B29'
    TEXT: str = 'white'
    HOVER: str = '#1A3A5C'
    PRESSED: str = '#0A1220'
    DISABLED: str = 'gray'
    BORDER: str = 'gray'
    BORDER_WIDTH: int = 1
    ACCENT: str = 'white'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class DarkGray:
    """Тёмно-серая (графит)"""
    BG: str = '#1E1E1E'
    TEXT: str = '#E0E0E0'
    HOVER: str = '#2D2D2D'
    PRESSED: str = '#151515'
    DISABLED: str = '#5A5A5A'
    BORDER: str = '#3A3A3A'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#4A9EFF'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class DarkPurple:
    """Тёмно-фиолетовая (ночь)"""
    BG: str = '#1A0F2E'
    TEXT: str = '#E8D5FF'
    HOVER: str = '#2D1B4E'
    PRESSED: str = '#0F0819'
    DISABLED: str = '#5A4A7A'
    BORDER: str = '#4A2D7A'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#B47AFF'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class DarkGreen:
    """Тёмно-зелёная (терминал)"""
    BG: str = '#0D1F0D'
    TEXT: str = '#B8FFB8'
    HOVER: str = '#1A3A1A'
    PRESSED: str = '#061206'
    DISABLED: str = '#4A6A4A'
    BORDER: str = '#2D5A2D'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#00FF88'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class DarkRed:
    """Тёмно-красная (кровь)"""
    BG: str = '#1F0A0A'
    TEXT: str = '#FFD5D5'
    HOVER: str = '#3A1A1A'
    PRESSED: str = '#120606'
    DISABLED: str = '#6A4A4A'
    BORDER: str = '#5A2D2D'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#FF4A4A'
    FONT: tuple = ('arial', 10, 'normal')


# ========================================================================
# СВЕТЛЫЕ ТЕМЫ
# ========================================================================

@dataclass
class LightGray:
    """Светло-серая (классика)"""
    BG: str = '#F0F0F0'
    TEXT: str = '#1A1A1A'
    HOVER: str = '#E0E0E0'
    PRESSED: str = '#C8C8C8'
    DISABLED: str = '#A0A0A0'
    BORDER: str = '#B0B0B0'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#4A9EFF'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class LightBeige:
    """Светло-бежевая (бумага)"""
    BG: str = '#F5F0E8'
    TEXT: str = '#2D2419'
    HOVER: str = '#E8E0D0'
    PRESSED: str = '#D5C8B0'
    DISABLED: str = '#A89A80'
    BORDER: str = '#C8BAA0'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#8B6F47'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class LightBlue:
    """Светло-голубая (небо)"""
    BG: str = '#E8F4FF'
    TEXT: str = '#0A2540'
    HOVER: str = '#D0E8FF'
    PRESSED: str = '#B0D5F0'
    DISABLED: str = '#8AAAC0'
    BORDER: str = '#A0C8E0'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#0078D4'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class LightGreen:
    """Светло-зелёная (мята)"""
    BG: str = '#E8F8E8'
    TEXT: str = '#0A3A0A'
    HOVER: str = '#D0F0D0'
    PRESSED: str = '#B0E0B0'
    DISABLED: str = '#8AA88A'
    BORDER: str = '#A0D0A0'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#00A650'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class LightPink:
    """Светло-розовая (пастель)"""
    BG: str = '#FFF0F5'
    TEXT: str = '#3A0A1E'
    HOVER: str = '#FFE0EC'
    PRESSED: str = '#F0C8DC'
    DISABLED: str = '#B08AA0'
    BORDER: str = '#E0B8C8'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#E91E63'
    FONT: tuple = ('arial', 10, 'normal')


# ========================================================================
# КОНТРАСТНЫЕ / АКЦЕНТНЫЕ
# ========================================================================

@dataclass
class HighContrast:
    """Высококонтрастная (доступность)"""
    BG: str = 'black'
    TEXT: str = 'white'
    HOVER: str = '#333333'
    PRESSED: str = '#1A1A1A'
    DISABLED: str = '#666666'
    BORDER: str = 'white'
    BORDER_WIDTH: int = 2
    ACCENT: str = 'yellow'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class Solarized:
    """Solarized Dark (классика)"""
    BG: str = '#002B36'
    TEXT: str = '#839496'
    HOVER: str = '#073642'
    PRESSED: str = '#001F27'
    DISABLED: str = '#586E75'
    BORDER: str = '#586E75'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#B58900'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class Monokai:
    """Monokai (для код-редакторов)"""
    BG: str = '#272822'
    TEXT: str = '#F8F8F2'
    HOVER: str = '#3E3D32'
    PRESSED: str = '#1E1F1C'
    DISABLED: str = '#75715E'
    BORDER: str = '#49483E'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#A6E22E'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class Nord:
    """Nord (скандинавская)"""
    BG: str = '#2E3440'
    TEXT: str = '#D8DEE9'
    HOVER: str = '#3B4252'
    PRESSED: str = '#242933'
    DISABLED: str = '#4C566A'
    BORDER: str = '#434C5E'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#88C0D0'
    FONT: tuple = ('arial', 10, 'normal')


@dataclass
class Dracula:
    """Dracula (вампирская)"""
    BG: str = '#282A36'
    TEXT: str = '#F8F8F2'
    HOVER: str = '#44475A'
    PRESSED: str = '#1E1F29'
    DISABLED: str = '#6272A4'
    BORDER: str = '#44475A'
    BORDER_WIDTH: int = 1
    ACCENT: str = '#BD93F9'
    FONT: tuple = ('arial', 10, 'normal')