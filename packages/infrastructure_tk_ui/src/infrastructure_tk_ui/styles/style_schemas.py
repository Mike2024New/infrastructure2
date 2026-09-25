from typing import Any, Literal

from pydantic import BaseModel, Field


class StyleSchemaTTK(BaseModel):
    style_name: str
    styles_dict: dict = Field(default_factory=dict)
    mapping: dict[str, list[tuple[str, ...]]] | None = Field(default=None, description='Карта состояний анимации')


class StyleSchema(BaseModel):
    widget_name: Literal[
        'root', 'button', 'entry', 'label', 'checkbox', 'text',
        'progressbar', 'combobox', 'checkbutton', 'radiobutton',
        'frame', 'scrollbar',
    ]
    tk: dict = Field(default_factory=dict)
    ttk: StyleSchemaTTK | None = None
    options: list[tuple[str, Any]] = Field(default_factory=tuple, description='Параметры для составных виджетов')
    layer: int | str | None = None
