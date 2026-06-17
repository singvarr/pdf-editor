from enum import StrEnum


class DocumentType(StrEnum):
    PASSPORT = "Паспорт"
    LABOURER_TICKET = "Трудова книжка"
    MILITARY_TICKET = "Військовий"
    OFFICER_CARD = "Офіцерське"


document_max_pages = {
    DocumentType.PASSPORT: 9,
    DocumentType.MILITARY_TICKET: 17,
    DocumentType.OFFICER_CARD: 11,
}
