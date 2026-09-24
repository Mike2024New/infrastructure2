import tkinter as tk


def center_window(win: tk.Tk | tk.Toplevel):
    """Выравнивание окна по центру"""
    win.withdraw()  # спрятать окно (решение проблемы внезапного появления)
    win.update_idletasks()
    screen_width, screen_height = win.winfo_screenwidth(), win.winfo_screenheight()
    root_width = win.winfo_width()
    root_height = win.winfo_height()
    x = (screen_width // 2) - (root_width // 2)
    y = (screen_height // 2) - (root_height // 2)
    win.geometry(f'+{x}+{y}')
    win.deiconify()  # загрузить окно обратно
