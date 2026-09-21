from infrastructure_tk_ui import GridParameters, BorderParameters, PackParameters, FontParameters, AnimationParameters
from infrastructure_tk_ui import RootWidget, FrameWidget, ButtonWidget, LabelWidget

"""
Компоновка (макет) -> деление главного окна и размещение в нем фреймов
"""


def ex1():
    root = RootWidget(
        back_color='white', size=(300, 200), offset=(2000, 300),
        grid_map=((50, 50), (100,)),  # деление сетки 2 строки по 50%, и 1 ячейка 100% (сумма 1 оси не больше 100%)
    )
    main_frame1 = FrameWidget(
        frame=root.form,
        # положение фрейма на сетке, дочерний элемент 'nw' будет прижиматься на северо-запад
        grid_parameters=GridParameters(row=0, col=0, rowspan=1, sticky='nw'),
    )
    ButtonWidget(
        back_color='green',
        frame=main_frame1.form, border_parameters=BorderParameters(th=1),
        pack_parameters=PackParameters(side='left'),
    )
    ButtonWidget(
        back_color='tomato',
        frame=main_frame1.form, border_parameters=BorderParameters(th=1),
        pack_parameters=PackParameters(side='right', padx=10)
    )
    root.form.mainloop()


def ex2():
    """Простой пример компоновки окна, и разбора по цветовым схемам"""
    from dataclasses import dataclass

    # цвета лучше паковать в отдельные классы и централизованно настраивать для всего приложения
    @dataclass
    class ColorScheme:
        text = 'black'
        main_color = '#F5F5F5'  # светло-серый
        button_ok = '#A5D6A7'  # пастельный зелёный
        button_ok_hover = '#81C784'  # средний зелёный
        button_ok_active = '#4CAF50'  # насыщенный зелёный
        button_cancel = '#EF9A9A'  # пастельный красный
        button_cancel_hover = '#E57373'  # средний красный
        button_cancel_active = '#E53935'  # насыщенный красный

    colors = ColorScheme()
    font_parameters = FontParameters(size=12, family='mono', color=colors.text)
    root = RootWidget(
        back_color=colors.main_color, offset=(1200, 300),
        grid_map=((50, 50), (100,)),
        border_parameters=BorderParameters(th=1),
    )
    frame1 = FrameWidget(
        frame=root.form, grid_parameters=GridParameters(row=0, col=0)
    )
    LabelWidget(
        frame=frame1.form, text='Вы точно хотите установить обновление?',
        pack_parameters=PackParameters(expand=True, fill='both', padx=10, pady=10),
        font_parameters=font_parameters,
    )
    frame2 = FrameWidget(
        frame=root.form, grid_parameters=GridParameters(row=1, col=0)
    )
    ButtonWidget(
        back_color=colors.button_ok,
        frame=frame2.form, text='Ок',
        justify='center',
        anchor='center',
        border_parameters=BorderParameters(th=1),
        pack_parameters=PackParameters(expand=True, side='left', fill='both', padx=10, pady=10),
        font_parameters=font_parameters,
        animation_parameters=AnimationParameters(
            active_color=colors.button_ok_active,
            hover_color=colors.button_ok_hover
        ),
    )
    ButtonWidget(
        back_color=colors.button_cancel,
        frame=frame2.form, text='Отмена',
        justify='center',
        anchor='center',
        border_parameters=BorderParameters(th=1),
        pack_parameters=PackParameters(expand=True, side='right', fill='both', padx=10, pady=10),
        font_parameters=font_parameters,
        animation_parameters=AnimationParameters(
            active_color=colors.button_cancel_active,
            hover_color=colors.button_cancel_hover
        ),
    )
    root.form.mainloop()


if __name__ == '__main__':
    # ex1()
    ex2()
