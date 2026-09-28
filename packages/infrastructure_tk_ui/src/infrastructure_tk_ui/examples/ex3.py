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


def ex2():
    """Создание текстового поля (text area)"""
    padx, pady = 10, 10
    # сперва создать root окно (tk.Tk())
    root = widgets.RootWidget()
    # привязать стили
    style_manager = StyleManager(
        themes=[get_standart_styles(themes_standart.LightGreen)],
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
        bypass=False,  # если нужно отключить стили полностью то использовать bypass
    )

    # создание размещение элементов (всё стандартными способами tkinter)
    root.form.configure(padx=padx, pady=pady)

    text = widgets.TextWidget(parent=root.form, editable=False)
    text.form.configure(height=10, width=40)
    text.form.pack(fill='both', expand=True)

    def start_callback():
        text.insert_text('row1: example\nrow2: example')

    style_manager.apply(container=root.form)
    # отрисовка формы
    root.form.after(1000, lambda: start_callback())
    root.form.mainloop()


if __name__ == '__main__':
    # ex1()
    ex2()
