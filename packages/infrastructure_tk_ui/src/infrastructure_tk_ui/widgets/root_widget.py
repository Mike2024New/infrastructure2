import tkinter as tk

from infrastructure_tk_ui.helpers import functions


class RootWidget:
    def __init__(
            self,
            size: tuple[int, int] = (0, 0),
            resizable: tuple[bool, bool] = (False, False),
            center_window: bool = True, modal: bool = False,
            parent: tk.Tk | tk.Toplevel | None = None,
    ):
        """
        Создание главного окна (либо модального окна)
        :param size: размеры окна (width, height)
        :param resizable: разрешить растягивать окно? True / False по каждой оси, например (True, True)
        :param center_window: центрировать окно?
        :param modal: сделать окно модальным?
        :param parent: родительское окно к которому привязано модальное окно
        """
        if modal:
            if parent is None:
                raise ValueError('Для модального окна нужен parent')

            self._form = tk.Toplevel(parent)
            self._form.grab_set()
        else:
            self._form = tk.Tk()

        if size[0] > 0 and size[1] > 0:
            self._form.geometry(f'{size[0]}x{size[1]}')
        self._form.resizable(*resizable)
        if center_window:
            functions.center_window(self._form)

    @property
    def form(self):
        """Возвращает объект ttk с доступными свойствами, например configure и другими"""
        return self._form
