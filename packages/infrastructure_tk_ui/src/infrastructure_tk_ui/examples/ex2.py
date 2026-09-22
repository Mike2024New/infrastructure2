from infrastructure_tk_ui import StyleParameters, PackParameters, PaddingParameters, TextParameters, ButtonWidget, \
    AlignParameters
from infrastructure_tk_ui import RootWidget, FrameWidget, ComboboxWidget

"""
Пример виджета combobox (выпадающий список).
"""


def ex1():
    root = RootWidget(
        offset=(1200, 300),
    )
    frame = FrameWidget(
        parent=root.form,
        placement_strategy=PackParameters(padx=10, pady=10),
    )
    # добавление и стиллизация combobox
    ComboboxWidget(
        parent=frame.form,
        placement_strategy=PackParameters(pady=5, expand=True),
        values=['stt_service', 'tts_service', 'llm_service'],
        default='stt_service',
        style_parameters=StyleParameters(
            back_color='white',
            padding_parameters=PaddingParameters(padx=10, pady=10),
            text_parameters=TextParameters(text_color='black', text_italic=True),
            hover_back_color='gray',
            active_back_color='gray',
        )
    )
    ButtonWidget(
        text='exit',
        parent=frame.form,
        placement_strategy=PackParameters(expand=True),
        style_parameters=StyleParameters(
            back_color='green',
            hover_back_color='gray',
            align_parameters=AlignParameters(justify='center', anchor='center'),
        ),
        callback=lambda: root.form.destroy(),
    )
    root.form.mainloop()


if __name__ == '__main__':
    ex1()
