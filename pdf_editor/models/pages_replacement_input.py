from dataclasses import dataclass

from pdf_editor.models.document_type import DocumentType


@dataclass
class PagesReplacementInput:
    assets_path: str
    page_numbers_to_replace: list[int]
    person_with_tin: str
    document_type: DocumentType = DocumentType.MILITARY_TICKET
