from dataclasses import dataclass, field


@dataclass
class StylesTK:
    root: dict = field(default_factory=dict)
    textarea: dict = field(default_factory=dict)
    combobox: dict = field(default_factory=dict)


@dataclass
class StylesTTK:
    button: str
    label: str
    checkbutton: str
    radiobutton: str
    progressbar: str
    combobox: str
