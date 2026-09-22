import tkinter as tk
from infrastructure_tk_ui.parameters_class import PackParameters, GridParameters

__all__ = ['placement_widget_to_parent']


def placement_widget_to_parent(
        widget: tk.Tk | tk.Frame | tk.Toplevel | tk.Misc,
        placement_strategy: PackParameters | GridParameters,  # стратегия размещения
):
    """Размещение виджета, на родительском окне"""
    if isinstance(placement_strategy, PackParameters):
        widget.pack(**placement_strategy.get())
    elif isinstance(placement_strategy, GridParameters):
        widget.grid(**placement_strategy.get())
    else:
        raise RuntimeError(
            f'Не указана стратегия размещения. '
            f'Передай либо pack_parameters, либо grid_parameters.'
        )
