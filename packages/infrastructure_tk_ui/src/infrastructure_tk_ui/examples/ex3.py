from infrastructure_tk_ui import GridParameters, StyleParameters, PackParameters, TextParameters, AlignParameters
from infrastructure_tk_ui import RootWidget, FrameWidget, ButtonWidget
from infrastructure_tk_ui import LabelWidget, ScrollableWidget, RadioGroupWidget


def ex1():
    """Создание scrollable прокручиваемого фрейма, когда элементов много и требуется прокрутка"""
    root = RootWidget(
        offset=(1200, 300),
        resize_width=True, resize_height=True,
    )
    frame = FrameWidget(
        parent=root.form,
        placement_strategy=GridParameters(row=0, col=0, sticky='nsew'),
    )
    scrollable = ScrollableWidget(
        parent=frame.form,
        placement_strategy=GridParameters(row=0, col=0, sticky='nsew'),
        style_parameters=StyleParameters(back_color='gray'),
    )
    [LabelWidget(
        parent=scrollable.form, text=f'label {i}',
        placement_strategy=PackParameters(),
    ) for i in range(20)]
    ButtonWidget(
        text=f'press for exit',
        parent=scrollable.form, callback=lambda: root.form.destroy(),
        placement_strategy=PackParameters(),
        style_parameters=StyleParameters(
            back_color='gray',
            text_parameters=TextParameters(text_color='white'),
        )
    )
    root.form.mainloop()


def ex2():
    root = RootWidget(
        offset=(1200, 300),
    )
    frame = FrameWidget(
        parent=root.form,
        placement_strategy=PackParameters(padx=10, pady=10),
    )
    frame2 = FrameWidget(
        parent=root.form,
        placement_strategy=PackParameters(padx=10, pady=10),
    )
    LabelWidget(
        text='Установить обновление?',
        parent=frame.form,
        placement_strategy=PackParameters(pady=10, expand=True, padx=5),
        style_parameters=StyleParameters(),
    )
    RadioGroupWidget(
        parent=frame.form,
        options=['Русский', 'English', 'Deutsch'],
        default='Русский',
        placement_strategy=PackParameters(side='top'),
        style_parameters=StyleParameters(
            # back_color='gray',
            # hover_back_color='orange',
            # text_parameters=TextParameters(text_size=12),
        ),
        callback=lambda value: print(f'выбран язык: {value}'),
    )
    ButtonWidget(
        text='Да',
        parent=frame2.form,
        placement_strategy=PackParameters(side='left', expand=True, padx=5),
        style_parameters=StyleParameters(
            back_color='green',
            align_parameters=AlignParameters(justify='center', anchor='center')
        ),
    )
    ButtonWidget(
        text='Нет',
        parent=frame2.form,
        placement_strategy=PackParameters(side='right', expand=True, padx=5),
        style_parameters=StyleParameters(
            back_color='red',
            align_parameters=AlignParameters(justify='center', anchor='center')
        ),
    )
    root.form.mainloop()


if __name__ == '__main__':
    # ex1()
    ex2()
