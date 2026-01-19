from typing import Union

Number = Union[float, complex]

def _fmt_real(x: float, precision: int) -> str:
    return f"{x:.{precision}f}"

def _fmt_complex(z: complex, precision: int) -> str:

    eps = 0.5 * (10 ** (-precision)) if precision >= 0 else 0.0

    re = z.real
    im = z.imag


    im_abs = abs(im)
    im_s = _fmt_real(im_abs, precision)


    if abs(re) < eps:
        sign = "-" if im < 0 else ""
        return f"{sign}{im_s}i"


    a = _fmt_real(re, precision)
    sign = "+" if im >= 0 else "-"
    return f"{a} {sign} {im_s}i"

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
