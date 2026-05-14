from tkinter import filedialog, messagebox, Tk

from pdf_editor.models.message_type import MessageType


class DialogManager:
    def __init__(self):
        root = Tk()
        root.withdraw()

    def show_replacement_file_selection(self):
        file_path = filedialog.askopenfilename(
            title="Оберіть джерело заміни",
            filetypes=[("PDF files", "*.pdf")]
        )

        return file_path

    def show_message(self, message_type: str, message: str):
        match message_type:
            case MessageType.ERROR:
                messagebox.showerror(title="Помилка", message=message)
            case MessageType.SUCCESS:
                messagebox.showinfo(title="Успіх", message=message)

