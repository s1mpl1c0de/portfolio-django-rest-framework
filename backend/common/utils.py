import re
import uuid


def generate_uuid(class_name: str) -> str:
    kebab_case_class_name = re.sub(r'([a-z])([A-Z])', r'\1-\2', class_name)
    return f'{kebab_case_class_name.upper()}-{uuid.uuid4()}'
