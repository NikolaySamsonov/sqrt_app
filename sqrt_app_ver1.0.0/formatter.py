from typing import Union

Number = Union[float, complex]

def _fmt_real(x: float, precision: int) -> str:

    return f"{x:.{precision}f}"

def _fmt_complex(z: complex, precision: int) -> str:
    a = _fmt_real(z.real, precision)
    b = _fmt_real(abs(z.imag), precision)
    sign = "+" if z.imag >= 0 else "-"
    return f"{a} {sign} {b}i"

def format_number(value: Number, precision: int) -> str:
    if isinstance(value, complex):
        return _fmt_complex(value, precision)
    return _fmt_real(float(value), precision)

def format_roots(root: Number, both: bool, precision: int) -> str:
    r1 = root
    if not both:
        return format_number(r1, precision)

    r2 = -root
    return f"{format_number(r1, precision)}\n{format_number(r2, precision)}"
