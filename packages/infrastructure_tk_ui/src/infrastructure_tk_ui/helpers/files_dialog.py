from pathlib import Path
from tkinter import filedialog


def select_folder(form, title: str, initialdir: Path = Path.home()) -> Path | None:
    """
    Получение выбранного пути из проводника
    :param form: форма к которой привязан элемент (обычно root - tk.TK)
    :param title: заголовок окна
    :param initialdir: стартовая директория поиска (по умолчанию корень)
    :return: выбранный путь, если отмена то None
    """
    file_path = filedialog.askdirectory(
        parent=form,
        title=title,
        initialdir=initialdir,
    )
    if file_path:
        return Path(file_path)
    return None


def select_file(
        form, title: str, initialdir: Path = Path.home(),
        filetypes: list[tuple[str, ...]] | None = None,
) -> Path | None:
    """
    Получение выбранного пути из проводника
    :param form: форма к которой привязан элемент (обычно root - tk.TK)
    :param title: заголовок окна
    :param initialdir: стартовая директория поиска (по умолчанию корень)
    :param filetypes: выбор типа файлов к загрузке (* шаблон), пример: [("Текстовые файлы", "*.txt"), ("Все файлы", "*")]
    по умолчанию [("Все файлы", "*")]
    :return: выбранный путь, если отмена то None
    """
    filetypes = filetypes if filetypes is not None else [("Все файлы", "*")]

    file_path = filedialog.askopenfilename(
        parent=form,
        title=title,
        initialdir=initialdir,
        filetypes=filetypes,
    )
    if file_path:
        return Path(file_path)
    return None
