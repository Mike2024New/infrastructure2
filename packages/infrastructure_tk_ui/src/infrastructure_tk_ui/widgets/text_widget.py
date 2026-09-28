import tkinter as tk


class TextWidget:
    def __init__(self, parent: tk.Tk | tk.Frame | tk.Toplevel, editable: bool = False):
        self._form = tk.Text(parent)
        self.editable = editable
        self._form.configure(
            wrap='word',
            state='normal' if editable else 'disabled',
        )

    @property
    def form(self):
        return self._form

    def insert_text(self, text: str) -> None:
        if self._form and text:
            if not self.editable:
                self._form.configure(state='normal')
            self._form.insert(tk.END, text)
            self._form.see(tk.END)
            if not self.editable:
                self._form.configure(state='disabled')

    def clear_text(self) -> None:
        if not self._form:
            return
        if not self.editable:
            self._form.configure(state='normal')
        self._form.delete('1.0', tk.END)
        if not self.editable:
            self._form.configure(state='disabled')

    def get_text(self) -> str:
        return self._form.get('1.0', tk.END).rstrip('\n')
