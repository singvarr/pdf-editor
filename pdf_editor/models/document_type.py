from enum import StrEnum


class DocumentType(StrEnum):
    MILITARY_TICKET = "Військовий"
    OFFICER_CARD = "Офіцерське"


document_max_pages = {
    DocumentType.MILITARY_TICKET: 17,
    DocumentType.OFFICER_CARD: 10,
}
