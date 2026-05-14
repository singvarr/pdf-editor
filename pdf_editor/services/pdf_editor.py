import os
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_editor.models.document_type import DocumentType, document_max_pages
from pdf_editor.models.pages_replacement import PagesReplacement


class PDFEditor:
    def __init__(
        self,
        assets_path: str,
        person_with_tin: str,
        pages_replacement: PagesReplacement,
        document_type: DocumentType,
    ):
        self._document_type = document_type
        self._folder_path = Path(assets_path, person_with_tin)
        self._folder_name = person_with_tin

        self._replacement_path = pages_replacement.path
        self._page_numbers_to_replace = [
            int(page.strip()) for page in pages_replacement.pages.split(',')
        ]

    @property
    def document_path(self) -> str:
        document_name = f"{self._document_type} - {self._folder_name}.pdf"

        return self._folder_path / document_name

    def _validate_input(self):
        if not len(self._page_numbers_to_replace):
            raise Exception('No page numbers for replacement specified')
        if not os.path.exists(self._folder_path):
            raise Exception(f'Folder {self._folder_path} doesn\'t exist')
        if not os.path.exists(self.document_path):
            raise Exception(f'{self._document_type} {self.document_path} not found in folder')
        if not os.path.exists(self._replacement_path):
            raise Exception('Replacement file wasn\'t found')

        are_all_page_numbers_valid = any(
            not isinstance(page_number, int) or page_number < 0
            for page_number in self._page_numbers_to_replace
        )

        if are_all_page_numbers_valid:
            raise Exception('All page numbers should be positive integers')

    def _replace_pages(self):
        document_reader = PdfReader(self.document_path)
        replacement_reader = PdfReader(self._replacement_path)

        if len(replacement_reader.pages) != len(self._page_numbers_to_replace):
            raise Exception('Replacement has different number of pages than requested')
        if any(page > len(document_reader.pages) for page in self._page_numbers_to_replace):
            raise Exception('Invalid page number')
        if document_max_pages[self._document_type] != len(document_reader.pages):
            pass

        writer = PdfWriter()
        page_number_in_replacement = 0

        for index, page in enumerate(document_reader.pages):
            if index + 1 in self._page_numbers_to_replace:
                replacement_page = replacement_reader.pages[page_number_in_replacement]
                writer.add_page(replacement_page)

                page_number_in_replacement += 1
            else:
                writer.add_page(page)

        with open("output.pdf", "wb") as file:
            writer.write(file)

    def run(self):
        self._validate_input()
        self._replace_pages()
