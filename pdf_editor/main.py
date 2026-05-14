import os

from dotenv import load_dotenv

from pdf_editor.models.document_type import DocumentType
from pdf_editor.models.message_type import MessageType
from pdf_editor.models.pages_replacement import PagesReplacement
from pdf_editor.services.file_backup import FileBackupService
from pdf_editor.services.dialog_manager import DialogManager
from pdf_editor.services.pdf_editor import PDFEditor


if __name__ == "__main__":
    load_dotenv()

    file_backup_service = None

    try:
        assets_path = os.environ["ASSETS_PATH"]
        # dialog_manager = DialogManager()
        # pages_input = sys.argv[1]
        # person_with_tin = sys.argv[2]

        # file_path = dialog_manager.show_replacement_file_selection()

        # if not file_path:
        #     raise Exception('Replacement file is not selected')

        TEST_FOLDER_NAME = 'АНЖИЯК Дмитро Михайлович 2594311199'
        person_with_tin = TEST_FOLDER_NAME
        pages_input = "1,11"
        file_path = os.environ["REPLACEMENT_FILE_PATH"]

        replacement = PagesReplacement(path=file_path, pages=pages_input)

        pdf_editor = PDFEditor(
            assets_path=assets_path,
            person_with_tin=TEST_FOLDER_NAME,
            pages_replacement=replacement,
            document_type=DocumentType.MILITARY_TICKET,
        )
        file_backup_service = FileBackupService(file_path=pdf_editor.document_path)

        file_backup_service.create()
        pdf_editor.run()
        file_backup_service.remove()
    except Exception as exception:
        if file_backup_service:
            file_backup_service.restore()
        # dialog_manager.show_message(
        #     message_type=MessageType.ERROR,
        #     message=f"Сталася помилка при обробці: {exception}",
        # )
