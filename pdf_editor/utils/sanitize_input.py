import sys
import os

from pdf_editor.models.pages_replacement_input import PagesReplacementInput
from pdf_editor.models.document_type import DocumentType


REQUIRED_CLI_ARGS_COUNT = 3

def sanitize_input() -> PagesReplacementInput:
    if len(sys.argv) <= REQUIRED_CLI_ARGS_COUNT:
        raise Exception(f"Invalid number of CLI arguments, required 2, instead got {len(sys.argv)}")

    try:
        pages_input = sys.argv[1]
        page_numbers_to_replace = [int(page.strip()) for page in pages_input.split(';')]
    except Exception:
        raise Exception(f'Failed to parse page numbers')
    
    try:
        document_type = sys.argv[3]
    except IndexError:
        document_type = DocumentType.MILITARY_TICKET

    person_with_tin = sys.argv[2]

    assets_path = os.getenv("ASSETS_PATH")

    if not assets_path:
        raise Exception(f'ASSETS_PATH variable is missing in .env')

    return PagesReplacementInput(
        assets_path=assets_path,
        document_type=document_type,
        page_numbers_to_replace=page_numbers_to_replace,
        person_with_tin=person_with_tin,
    )

