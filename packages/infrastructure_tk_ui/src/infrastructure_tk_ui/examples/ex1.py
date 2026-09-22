from infrastructure_tk_ui import StyleParameters, PackParameters, PaddingParameters, TextParameters
from infrastructure_tk_ui import RootWidget, FrameWidget, ButtonWidget
from infrastructure_tk_ui import LabelWidget, CheckBoxWidget


def ex1():
    """Создание scrollable прокручиваемого фрейма, когда элементов много и требуется прокрутка"""
    text_size = 12
    root = RootWidget(
        offset=(1200, 300),
        resize_width=True, resize_height=True,
    )
    frame = FrameWidget(
        parent=root.form,
        placement_strategy=PackParameters(padx=10, pady=10),
    )
    LabelWidget(
        parent=frame.form,
        placement_strategy=PackParameters(pady=10),
        style_parameters=StyleParameters(
            text_parameters=TextParameters(text_size=text_size),
            back_color='white',
            line_th=1,
            line_color='green',
            padding_parameters=PaddingParameters(padx=5, pady=5),
        )
    )
    check_box = CheckBoxWidget(
        text='выборы',
        parent=frame.form,
        placement_strategy=PackParameters(),
        style_parameters=StyleParameters(
            back_color='red',
            text_parameters=TextParameters(text_size=text_size),
        )
    )
    ButtonWidget(
        text=f'press for exit',
        parent=frame.form, callback=lambda: print(check_box.get_value()),
        placement_strategy=PackParameters(pady=10),
        style_parameters=StyleParameters(
            hover_back_color='gray',
            padding_parameters=PaddingParameters(padx=5, pady=5),
            text_parameters=TextParameters(text_size=text_size),
        )
    )
    root.form.mainloop()


if __name__ == '__main__':
    ex1()
