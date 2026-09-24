from time import sleep
from infrastructure_tk_ui import RootWidget, ProgressBarWidgetTTK, ComboBoxTTK
from infrastructure_tk_ui.examples.ex0 import StyleManager
import threading

"""
Примеры построения основных виджетов, встроенными tkinter методами, и классами расширителями, а также применение стилей
Стили определены в ex0
"""


def ex1():
    """Создание простого прогресс бара"""
    padx, pady = 10, 10
    root = RootWidget(size=(400, 40))
    # ВАЖНО! Активацию стилей делать только после создания root окна (иначе будет появляться второе окно)
    # активация стилей, их можно отключить при необходимости (флаги disable)
    style_manager = StyleManager(root=root.form)
    styles, styles_ttk = style_manager.set_style(tk_disable=False, ttk_disable=False, options_disable=False)
    root.form.configure(padx=padx, pady=pady, **styles.root)

    progress = ProgressBarWidgetTTK(root.form)
    progress.form.pack(expand=True, fill='both')

    # callback функция которая изменяет значение прогресс бара, (её в отдельный поток)
    def callback():
        for i in range(100):
            sleep(0.05)
            progress.set_value(i)
        progress.form.destroy()
        root.form.destroy()

    # просто пример вызова прогресс бара. Спустя 10 ms, после отрисовки окна запустится прогресс бар
    root.form.after(10, threading.Thread(target=callback, daemon=True).start())
    root.form.mainloop()


def ex2():
    """Создание выпадающего списка combobox"""
    padx, pady = 20, 20
    root = RootWidget(size=(300, 80))
    # ВАЖНО! Активацию стилей делать только после создания root окна (иначе будет появляться второе окно)
    # активация стилей, их можно отключить при необходимости (флаги disable)
    style_manager = StyleManager(root=root.form)
    styles, styles_ttk = style_manager.set_style(tk_disable=False, ttk_disable=False, options_disable=False)
    root.form.configure(padx=padx, pady=pady, **styles.root)

    combobox = ComboBoxTTK(
        parent=root.form,
        values=['python', 'algol', 'cobol', 'vba'],
        default='python'
    )
    # внимание! Combobox имеет гибридный стиль, то есть и ttk и обычный configure
    combobox.form.configure(style=styles_ttk.combobox, cursor='hand2', **styles.combobox)
    combobox.form.pack()
    root.form.mainloop()


def ex3():
    """Создание выпадающего списка combobox"""
    from tkinter import ttk
    root = RootWidget(size=(300, 50))

    # инициализация стилей
    style_manager = StyleManager(root=root.form)  # к root применяются стили автоматически (если tk_disable)
    styles, styles_ttk = style_manager.set_style(tk_disable=False, ttk_disable=False, options_disable=False)
    ttk.Button(text='yes', style=styles_ttk.button).pack(side='left', fill='both', expand=True)
    ttk.Button(text='no', style=styles_ttk.button).pack(side='left', fill='both', expand=True)
    root.form.mainloop()


if __name__ == '__main__':
    # ex1()
    # ex2()
    ex3()
