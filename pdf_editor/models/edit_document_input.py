from dataclasses import dataclass

from pdf_editor.models.document_type import DocumentType
from pdf_editor.models.document_edit_type import DocumentEditType


@dataclass
class EditDocumentInput:
    assets_path: str
    page_numbers_to_edit: list[int]
    person_with_tin: str
    document_type: DocumentType = DocumentType.MILITARY_TICKET
    document_edit_type: DocumentEditType = DocumentEditType.REPLACE
