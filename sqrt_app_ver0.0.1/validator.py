import re
from errors import ValidationError

_NUMBER_RE = re.compile(r"^-?\d+(\.\d+)?$")

def parse_number(text: str) -> float:
    text = (text or "").strip()
    if not text:
        raise ValidationError("err_empty")


    if not _NUMBER_RE.match(text):
        raise ValidationError("err_format")

    try:
        return float(text)
    except ValueError:
        raise ValidationError("err_format")
