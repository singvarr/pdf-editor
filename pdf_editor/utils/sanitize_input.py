import sys
import os

from pdf_editor.models.edit_document_input import EditDocumentInput


REQUIRED_CLI_ARGS_COUNT = 5
PAGE_NUMBERS_DELIMITER = ";"

# TODO: improve parsing:
# 1. add ability to pass values from named arguments
# 2. add default values for cli args
def sanitize_input() -> EditDocumentInput:
    if len(sys.argv) != REQUIRED_CLI_ARGS_COUNT:
        raise Exception(
            f"Invalid number of CLI arguments, required {REQUIRED_CLI_ARGS_COUNT - 1}, instead got"
            f" {len(sys.argv)}"
        )

    pages_input = sys.argv[1]
    page_numbers_to_replace = [
        int(page.strip()) for page in pages_input.split(PAGE_NUMBERS_DELIMITER)
    ]

    person_with_tin = sys.argv[2]
    document_type = sys.argv[3]
    document_edit_type = sys.argv[4]

    assets_path = os.getenv("ASSETS_PATH")

    if not assets_path:
        raise Exception(f'ASSETS_PATH variable is missing in .env')

    return EditDocumentInput(
        assets_path=assets_path,
        document_type=document_type,
        page_numbers_to_edit=page_numbers_to_replace,
        person_with_tin=person_with_tin,
        document_edit_type=document_edit_type,
    )

