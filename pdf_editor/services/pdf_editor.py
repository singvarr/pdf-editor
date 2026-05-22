import os
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_editor.models.document_type import document_max_pages
from pdf_editor.models.pages_replacement_input import PagesReplacementInput
from pdf_editor.services.dialog_manager import DialogManager


class PDFEditor:
    def __init__(
        self,
        pages_replacement_input: PagesReplacementInput,
        pages_replacement_file_path: str,
        dialog_manager: DialogManager,
    ):
        self._document_type = pages_replacement_input.document_type
        self._folder_path = Path(
            pages_replacement_input.assets_path,
            pages_replacement_input.person_with_tin,
        )
        self._folder_name = pages_replacement_input.person_with_tin

        self._pages_replacement_file_path = pages_replacement_file_path
        self._page_numbers_to_replace = pages_replacement_input.page_numbers_to_replace

        self._dialog_manager = dialog_manager

    @property
    def document_path(self) -> Path:
        document_name = f"{self._document_type} - {self._folder_name}.pdf"

        return self._folder_path / document_name

    def _validate_input(self):
        are_all_page_numbers_valid = any(
            not isinstance(page_number, int) or page_number < 0
            for page_number in self._page_numbers_to_replace
        )

        if are_all_page_numbers_valid:
            raise Exception('All page numbers should be positive integers')
        if not len(self._page_numbers_to_replace):
            raise Exception('No page numbers for replacement specified')
        if not os.path.exists(self._folder_path):
            raise Exception(f'Folder {self._folder_path} doesn\'t exist')
        if not os.path.exists(self.document_path):
            raise Exception(f'{self._document_type} {self.document_path} not found in folder')
        if not os.path.exists(self._pages_replacement_file_path):
            raise Exception('Replacement file wasn\'t found')

    def _replace_pages(self):
        document_reader = PdfReader(self.document_path)
        replacement_reader = PdfReader(self._pages_replacement_file_path)

        if len(replacement_reader.pages) != len(self._page_numbers_to_replace):
            raise Exception('Replacement has different number of pages than requested')
        if any(page > len(document_reader.pages) for page in self._page_numbers_to_replace):
            raise Exception('Invalid page number')
        if document_max_pages[self._document_type] != len(document_reader.pages):
            is_edit_confirmed = self._dialog_manager.ask_confirm_document_edit()

            if not is_edit_confirmed:
                raise Exception("Edit of document with different amount of pages is not confirmed")

        writer = PdfWriter()
        page_number_in_replacement = 0

        for index, page in enumerate(document_reader.pages):
            if index + 1 in self._page_numbers_to_replace:
                replacement_page = replacement_reader.pages[page_number_in_replacement]
                writer.add_page(replacement_page)

                page_number_in_replacement += 1
            else:
                writer.add_page(page)

        with open(self.document_path, "wb") as file:
            writer.write(file)

    def run(self):
        self._validate_input()
        self._replace_pages()
