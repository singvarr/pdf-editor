from dotenv import load_dotenv

from pdf_editor.models.message_type import MessageType
from pdf_editor.services.file_backup import FileBackupService
from pdf_editor.services.dialog_manager import DialogManager
from pdf_editor.services.pdf_editor import PDFEditor
from pdf_editor.utils.configure_app_paths import configure_app_paths
from pdf_editor.utils.sanitize_input import sanitize_input


if __name__ == "__main__":
    configure_app_paths()
    load_dotenv()

    file_backup_service = None
    dialog_manager = DialogManager()

    try:
        sanitized_input = sanitize_input()

        document_edit_input = dialog_manager.show_replacement_file_selection()

        if not document_edit_input:
            raise Exception('Replacement file is not selected')

        pdf_editor = PDFEditor(
            pages_edit_file_path=document_edit_input,
            edit_document_input=sanitized_input,
            dialog_manager=dialog_manager,
        )
        file_backup_service = FileBackupService(file_path=pdf_editor.document_path)

        file_backup_service.create()
        pdf_editor.run()
        file_backup_service.remove()
        FileBackupService.remove_file(document_edit_input)

        dialog_manager.show_message(message_type=MessageType.SUCCESS, message="Сторінки замінено")
    except Exception as exception:
        dialog_manager.show_message(
            message_type=MessageType.ERROR,
            message=f"Сталася помилка при обробці: {exception}",
        )

        if file_backup_service:
            file_backup_service.restore()
