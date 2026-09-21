from infrastructure_tk_ui import PackParameters, FontParameters, AnimationParameters, BorderParameters
from infrastructure_tk_ui import RootWidget, LabelWidget, ButtonWidget
from infrastructure_tk_ui import EntryWidget, TextAreaWidget, FrameWidget
from infrastructure_tk_ui import ComboboxWidget

"""
Применение эффектов (фокусировка, наведение) к виджетам. Пока поддерживаются эффекты для:
EntryWidget, TextAreaWidget, ButtonWidget
"""


def ex1():
    """
    Пример entry виджета, с применением к нему эффектов active и hover ( подсветка при активности и наведении мышью)
    """
    root = RootWidget(
        offset=(1200, 300),
        back_color='gray',  # если в дочерних виджетах не переопределять это поле то цвет возьмется этот по умолчанию
    )
    font_parameters = FontParameters(size=12, family='mono', italic=True)
    frame = FrameWidget(
        frame=root.form,
        pack_parameters=PackParameters(expand=True, fill='x')
    )
    # Установка виджетов на фрейм, и управление их размещением через pack_parameters
    LabelWidget(
        frame=frame.form,
        pack_parameters=PackParameters(side='left', expand=False, fill='y', padx=0, pady=0, ),
        font_parameters=font_parameters,
    )
    EntryWidget(
        frame=frame.form, border_parameters=BorderParameters(th=1, relief='ridge'),
        animation_parameters=AnimationParameters(active_color='green', hover_color='orange'),
        pack_parameters=PackParameters(side='left', expand=False, fill='y', padx=15, pady=0, ),
        font_parameters=font_parameters,
    )
    ButtonWidget(
        frame=frame.form, text='ok',
        pack_parameters=PackParameters(side='right', expand=False, fill='y', padx=0, pady=0, ),
        font_parameters=font_parameters,
        callback=lambda: root.form.destroy(),
    )
    root.form.mainloop()


def ex2():
    root = RootWidget(
        offset=(1200, 300),
        back_color='gray',  # если в дочерних виджетах не переопределять это поле то цвет возьмется этот по умолчанию
    )
    font_parameters = FontParameters(size=12, family='mono', italic=True)
    frame = FrameWidget(
        frame=root.form,
        pack_parameters=PackParameters(expand=True, fill='x')
    )
    TextAreaWidget(
        frame=frame.form, text='row1', size=(40, 5),
        animation_parameters=AnimationParameters(active_color='green', hover_color='orange'),
        font_parameters=font_parameters,
    )
    ButtonWidget(
        frame=frame.form, text='ok',
        back_color='gray', border_parameters=BorderParameters(th=1, relief='ridge'),
        pack_parameters=PackParameters(side='left', expand=False, fill='none', padx=0, pady=0, ),
        font_parameters=font_parameters,
        animation_parameters=AnimationParameters(active_color='green', hover_color='orange'),
        callback=lambda: root.form.destroy(),
    )
    root.form.mainloop()


def ex3():
    root = RootWidget(
        offset=(1200, 300),
        back_color='gray',  # если в дочерних виджетах не переопределять это поле то цвет возьмется этот по умолчанию
    )
    font_parameters = FontParameters(size=12, family='mono', italic=True, color='green')
    frame = FrameWidget(
        frame=root.form,
        pack_parameters=PackParameters(padx=20, pady=20)
    )
    ComboboxWidget(
        frame=frame.form,
        values=['ru', 'en', 'de'],
        default='ru',
        font_parameters=font_parameters,
        animation_parameters=AnimationParameters(hover_color='red', active_color='green'),
        callback=lambda value: print(f'выбран язык: {value}'),
    )
    ButtonWidget(
        frame=frame.form, text='ok',
        back_color='gray', border_parameters=BorderParameters(th=1, relief='ridge'),
        pack_parameters=PackParameters(side='left', expand=False, fill='none', padx=0, pady=0, ),
        font_parameters=font_parameters,
    )
    root.form.mainloop()


if __name__ == '__main__':
    # ex1()
    # ex2()
    ex3()
