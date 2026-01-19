import logging
from errors import ValidationError
from validator import parse_number
from core import sqrt_value
from formatter import format_roots

class Controller:
    def __init__(self, loc):
        self.loc = loc

    def calculate(self, input_text: str, precision: int, both_roots: bool) -> str:
        try:
            x = parse_number(input_text)
            root = sqrt_value(x)
            result = format_roots(root, both_roots, precision)
            logging.info("OK input=%s precision=%s both=%s", input_text, precision, both_roots)
            return result
        except ValidationError as e:
            logging.warning("Validation error: %s (input=%s)", e.code, input_text)
            return self.loc.t(e.code)
        except Exception:
            logging.exception("Unexpected error")
            return self.loc.t("err_unknown")
