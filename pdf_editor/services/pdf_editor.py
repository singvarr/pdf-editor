import os
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_editor.models.document_type import document_max_pages
from pdf_editor.models.edit_document_input import EditDocumentInput
from pdf_editor.models.document_edit_type import DocumentEditType
from pdf_editor.services.dialog_manager import DialogManager


class PDFEditor:
    def __init__(
        self,
        edit_document_input: EditDocumentInput,
        pages_edit_file_path: str,
        dialog_manager: DialogManager,
    ):
        self._document_type = edit_document_input.document_type
        self._folder_path = Path(
            edit_document_input.assets_path,
            edit_document_input.person_with_tin,
        )
        self._folder_name = edit_document_input.person_with_tin

        self._pages_edit_file_path = pages_edit_file_path
        self._page_numbers_to_edit = edit_document_input.page_numbers_to_edit

        self._mode = edit_document_input.document_edit_type

        self._dialog_manager = dialog_manager

    @property
    def document_path(self) -> Path:
        document_name = f"{self._document_type} - {self._folder_name}.pdf"

        return self._folder_path / document_name

    def _validate_input(self):
        has_invalid_page_number = any(
            not isinstance(page_number, int) or page_number < 0
            for page_number in self._page_numbers_to_edit
        )

        if has_invalid_page_number:
            raise Exception('All page numbers should be positive integers')
        if not len(self._page_numbers_to_edit):
            raise Exception('No page numbers for update specified')
        if not os.path.exists(self._folder_path):
            raise Exception(f'Folder {self._folder_path} doesn\'t exist')
        if not os.path.exists(self.document_path):
            raise Exception(f'{self._document_type} {self.document_path} not found in folder')
        if not os.path.exists(self._pages_edit_file_path):
            raise Exception('File with update wasn\'t found')

    def _edit_document(self):
        document_reader = PdfReader(self.document_path)
        update_reader = PdfReader(self._pages_edit_file_path)

        if len(update_reader.pages) != len(self._page_numbers_to_edit):
            raise Exception('Update has different number of pages than requested')
        if any(page > len(document_reader.pages) for page in self._page_numbers_to_edit):
            raise Exception('Invalid page number')
        if document_max_pages[self._document_type] != len(document_reader.pages):
            is_edit_confirmed = self._dialog_manager.ask_confirm_document_edit()

            if not is_edit_confirmed:
                raise Exception("Edit of document with different amount of pages is not confirmed")

        writer = PdfWriter()
        page_number_in_edit = 0

        for index, page in enumerate(document_reader.pages):
            if self._mode == DocumentEditType.REPLACE and index + 1 in self._page_numbers_to_edit:
                replacement_page = update_reader.pages[page_number_in_edit]
                writer.add_page(replacement_page)

                page_number_in_edit += 1
            elif (
                self._mode == DocumentEditType.INSERT_AFTER and 
                index + 1 in self._page_numbers_to_edit
            ):
                writer.add_page(page)

                replacement_page = update_reader.pages[page_number_in_edit]
                writer.add_page(replacement_page)
                page_number_in_edit += 1
            else:
                writer.add_page(page)

        with open(self.document_path, "wb") as file:
            writer.write(file)

    def run(self):
        self._validate_input()
        self._edit_document()
