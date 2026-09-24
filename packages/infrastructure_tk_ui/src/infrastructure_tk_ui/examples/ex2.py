from time import sleep
from infrastructure_tk_ui import RootWidget, ProgressBarWidgetTTK, ComboBoxTTK
import threading
from tkinter import ttk
from infrastructure_tk_ui import StyleManager
# стили можно определить и свои (например если планируется несколько слоев виджетов), а можно взять и стандартные как в импортах ниже
from infrastructure_tk_ui import get_standart_styles
from infrastructure_tk_ui import themes_standart as themes

"""
Примеры построения основных виджетов, встроенными tkinter методами, и классами расширителями, а также применение стилей
Стили определены в ex0
"""


def ex1():
    """Создание простого прогресс бара"""
    padx, pady = 10, 10
    root = RootWidget()
    # ВАЖНО! Активацию стилей делать только после создания root окна (иначе будет появляться второе окно)
    # активация стилей, их можно отключить при необходимости (флаги disable)
    style_manager = StyleManager(
        root=root.form, styles_in=get_standart_styles(themes.Nord),
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
        bypass=False,
    )
    root.form.configure(padx=padx, pady=pady)
    label = ttk.Label(root.form, text='stt_vosk: Загрузка компонента')
    label.configure(justify='left', anchor='nw', width=50)
    label.pack(fill='x', padx=padx, pady=pady, expand=True)
    style_manager.apply(label)
    # label.configure(foreground='green')  # style_manager не конфликтует с баз. настройками, можно здесь переопределять
    progress = ProgressBarWidgetTTK(root.form)
    progress.form.pack(expand=True, fill='both', padx=padx, pady=pady)
    style_manager.apply(progress.form)

    # callback функция которая изменяет значение прогресс бара, (её в отдельный поток)
    def callback():
        for i in range(100):
            if i == 30:
                label.configure(text='stt_vosk: сборка приложения')
            if i == 60:
                label.configure(text='stt_vosk: удаление остаточных файлов')
            sleep(0.1)
            progress.set_value(i)
        progress.form.destroy()
        root.form.destroy()

    button = ttk.Button(root.form, text='отмена', command=lambda: root.form.destroy())
    style_manager.apply(button)
    button.pack(side='right', padx=padx, pady=pady)

    # просто пример вызова прогресс бара. Спустя 10 ms, после отрисовки окна запустится прогресс бар
    root.form.after(10, threading.Thread(target=callback, daemon=True).start())
    root.form.mainloop()


def ex2():
    """Создание выпадающего списка combobox"""
    padx, pady = 10, 10
    root = RootWidget(size=(300, 60))
    root.form.configure(padx=padx, pady=pady)
    style_manager = StyleManager(
        root=root.form, styles_in=get_standart_styles(themes.LightGray),
        disabled_tk=False, disabled_ttk=False, disabled_options=False,
    )
    root.form.configure(padx=padx, pady=pady)

    combobox = ComboBoxTTK(
        parent=root.form,
        values=['python', 'algol', 'cobol', 'vba'],
        default='python'
    )
    style_manager.apply(form=combobox.form)
    combobox.form.pack()
    root.form.mainloop()


def ex3():
    """Создание выпадающего списка combobox"""
    padx, pady = 10, 10
    root = RootWidget(center_window=True)
    root.form.configure(padx=padx, pady=pady)
    style_manager = StyleManager(
        root=root.form, styles_in=get_standart_styles(themes.HighContrast),
        disabled_tk=False, disabled_ttk=False, disabled_options=False, bypass=False,
    )

    btn = ttk.Button(text='yes')
    btn.pack(side='left', fill='both', expand=True)
    style_manager.apply(form=btn, layer=1)
    btn2 = ttk.Button(text='no')
    btn2.configure(style='Custom.TButton')
    btn2.pack(side='left', fill='both', expand=True)
    style_manager.apply(form=btn2, layer=1)
    root.form.mainloop()


if __name__ == '__main__':
    # ex1()
    # ex2()
    ex3()
