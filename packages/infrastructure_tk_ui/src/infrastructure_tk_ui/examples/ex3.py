from tkinter import ttk
from infrastructure_tk_ui import widgets
from infrastructure_tk_ui import StyleManager
# стили можно определить и свои (например если планируется несколько слоев виджетов), а можно взять и стандартные как в импортах ниже
from infrastructure_tk_ui import get_standart_styles
from infrastructure_tk_ui import themes_standart
from infrastructure_tk_ui import files_dialog


def ex1():
    """Работа с файловыми диалоговыми окнами"""
    padx, pady = 3, 3
    root = widgets.RootWidget()
    # привязать стили
    style_manager = StyleManager(
        themes=[get_standart_styles(themes_standart.Nord)],
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
        bypass=False,  # если нужно отключить стили полностью то использовать bypass
    )
    # создание размещение элементов (всё стандартными способами tkinter)
    root.form.configure(padx=padx, pady=pady)

    # выбор папки
    ttk.Button(
        text='директория',
        command=lambda: print(files_dialog.select_folder(form=root.form, title='выбор директории'))
    ).pack()
    # выбор файла
    ttk.Button(
        text='файл',
        command=lambda: print(files_dialog.select_file(form=root.form, title='выбор файла'))
    ).pack()

    # применение стилей выбранной темы
    style_manager.apply(container=root.form)
    # отрисовка формы
    root.form.mainloop()


if __name__ == '__main__':
    ex1()
