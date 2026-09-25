"""Shared furniture for the school's printed paperwork.

The fee slip and the admission form are different documents that have to
look like the same school: identical crest band, identical tints, identical
type. That band lives here rather than in either document, so neither can
drift from the other.

Everything is laid out in PostScript points, which is what a PDF page is
measured in, so a number in these files is the number a ruler finds on the
paper.
"""

import emblem
import typeset
from brand import SCHOOL
from emblem import C

MM = 72 / 25.4
A4_W, A4_H = 210 * MM, 297 * MM          # 595.28 x 841.89 pt
A6_W, A6_H = A4_W / 2, A4_H / 2          # a quarter of A4, 105 x 148.5 mm

NAME, KIND = "Arya Vidya", "PLAY SCHOOL"

PALE = "#F4F6FB"        # panel tint, a wash of the crest's ink
WARM = "#FDF3E4"        # reserved for anything asking the reader to act
HAIR = "#E4E8F0"        # rules between rows
GREY = "#6B7280"
RULE = "#9AA3B2"        # the lines people actually write on: darker than HAIR
BAND_SUB = "#C9D0E6"    # secondary type on the dark band

BOLD, SEMI, BODY = "poppins-bold", "poppins-semibold", "poppins"
DISPLAY = "baloo-extrabold"


# ------------------------------------------------------------- primitives
def text(s, x, y, font=BODY, size=8, fill=C["ink"], anchor="start", ls=0):
    return typeset.text_path(s, x, y, font=font, size=size, fill=fill,
                             anchor=anchor, letter_spacing=ls, track=False)


def rect(x, y, w, h, fill, r=0):
    rx = f' rx="{r:.2f}"' if r else ""
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" '
            f'height="{h:.2f}"{rx} fill="{fill}"/>')


def line(x, y, w, colour=RULE, width=0.7, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M {x:.2f} {y:.2f} H {x + w:.2f}" stroke="{colour}" '
            f'stroke-width="{width}" fill="none"{d}/>')


def stroked(x, y, w, h, colour=RULE, width=0.7, r=0, fill="none", dash=None):
    rx = f' rx="{r:.2f}"' if r else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" '
            f'height="{h:.2f}"{rx} fill="{fill}" stroke="{colour}" '
            f'stroke-width="{width}"{d}/>')


def page(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {w:.2f} {h:.2f}" width="{w:.2f}" '
            f'height="{h:.2f}">'
            f'<rect width="{w:.2f}" height="{h:.2f}" fill="#FFFFFF"/>'
            f'{body}</svg>')


def rupees(amount, x, y, size, fill, tail="/-"):
    """Right-aligned "₹1,500/-" — the /- set smaller, as on an Indian bill."""
    tw = typeset.measure(tail, BODY, size * 0.62)
    return (text(tail, x, y, font=BODY, size=size * 0.62, fill=fill,
                 anchor="end")
            + text(f"₹{amount}", x - tw - 1, y, font=DISPLAY, size=size,
                   fill=fill, anchor="end"))


# ------------------------------------------------------------- crest band
# Proportions of the band's own height. They are what they are because the
# fee slip was drawn first and signed off at h=54; the band was lifted out
# of it unchanged, so anything else that uses it matches the slip exactly.
# written as /54 so they stay exactly the slip's own point sizes
_RAD, _PAD, _MARK, _MARK_GAP = 9 / 54, 8 / 54, 40 / 54, 10 / 54
_NAME_SIZE, _NAME_BASE = 23 / 54, 28 / 54
_KIND_SIZE, _KIND_LS, _KIND_BASE = 6.6 / 54, 2.6 / 54, 41 / 54
_SUB_BASE = 34 / 54


def crest_band(x, y, w, h, title=None, right=None):
    """The dark band every document opens with.

    Crest and school name on the left. `title` sets a pill on the right --
    the document's own name -- and `right` a small line, under the pill if
    there is one and on the band's centre line if there is not.
    """
    pad, mark_w = h * _PAD, h * _MARK
    out = [rect(x, y, w, h, C["ink"], r=h * _RAD),
           emblem.place(x + pad, y + (h - mark_w) / 2, mark_w)]

    tx = x + pad + mark_w + h * _MARK_GAP
    out.append(text(NAME, tx, y + h * _NAME_BASE, font=DISPLAY,
                    size=h * _NAME_SIZE, fill="#FFFFFF"))
    out.append(text(KIND, tx + 1.5, y + h * _KIND_BASE, font=SEMI,
                    size=h * _KIND_SIZE, fill=BAND_SUB, ls=h * _KIND_LS))

    if title:
        size, ls = h * 0.175, h * 0.040
        pill_w = typeset.measure(title, DISPLAY, size, ls) + h * 0.52
        pill_h = h * 0.36
        px = x + w - pad - pill_w
        py = y + (h - pill_h) / 2 - (h * 0.11 if right else 0)
        out.append(rect(px, py, pill_w, pill_h, C["orange"], r=pill_h / 2))
        out.append(text(title, px + pill_w / 2 + ls / 2, py + pill_h * 0.70,
                        font=DISPLAY, size=size, fill=C["ink"],
                        anchor="middle", ls=ls))
        if right:
            out.append(text(right, px + pill_w / 2, py + pill_h + h * 0.20,
                            font=SEMI, size=h * _KIND_SIZE, fill=BAND_SUB,
                            anchor="middle"))
    elif right:
        out.append(text(right, x + w - pad - 1, y + h * _SUB_BASE, font=SEMI,
                        size=h * _KIND_SIZE, fill=BAND_SUB, anchor="end"))
    return "".join(out)


def contact_band(x, y, w, h, r=7):
    """Address and phone, closing a document."""
    return (rect(x, y, w, h, C["ink"], r=r)
            + text(SCHOOL["address"], x + w / 2, y + h * (13 / 30), font=SEMI,
                   size=h * 0.22, fill="#FFFFFF", anchor="middle")
            + text(SCHOOL["phone"], x + w / 2, y + h * (23.5 / 30), font=SEMI,
                   size=h * 0.24, fill=C["orange"], anchor="middle"))


# ----------------------------------------------------------- form widgets
# A form is mostly four things: a numbered section head, a labelled line to
# write on, a tick box and a box to paste a photo into. They live here
# rather than in admission.py so a second form inherits them.
LABEL = 7.4          # the printed label beside a writing line
WRITE = 27.0         # baseline to baseline: room for adult handwriting


def section(x, y, w, n, title, colour=None):
    """Numbered chip, title, and a hairline across what is left of `w`."""
    chip, size = 13.0, 10.0
    out = [rect(x, y - chip + 2.5, chip, chip, colour or C["magenta"], r=3.2),
           text(str(n), x + chip / 2, y - 1.6, font=DISPLAY, size=8.4,
                fill="#FFFFFF", anchor="middle"),
           text(title, x + chip + 7, y, font=DISPLAY, size=size,
                fill=C["ink"])]
    used = chip + 7 + typeset.measure(title, DISPLAY, size) + 9
    if w - used > 12:
        out.append(line(x + used, y - 3.2, w - used, HAIR, 1.0))
    return "".join(out)


def field(x, y, w, label, size=LABEL):
    """A label, then a rule running to `x + w`. `y` is the writing line."""
    if not label:
        return line(x, y, w)
    lw = typeset.measure(label, SEMI, size)
    return (text(label, x, y - 3, font=SEMI, size=size, fill=GREY)
            + line(x + lw + 5, y, max(w - lw - 5, 0)))


def fields(x, y, w, cells, gap=14):
    """A row of fields. `cells` are (label, weight); weights split the row."""
    total = sum(c[1] for c in cells) or 1
    avail = w - gap * (len(cells) - 1)
    out, cx = [], x
    for label, weight in cells:
        cw = avail * weight / total
        out.append(field(cx, y, cw, label))
        cx += cw + gap
    return "".join(out)


def check(x, y, label, size=7.4, box=8.2):
    """A tick box with its label. Returns (svg, width consumed)."""
    svg = (stroked(x, y - box + 1.4, box, box, RULE, 0.8, r=1.6)
           + text(label, x + box + 5, y, font=SEMI, size=size))
    return svg, box + 5 + typeset.measure(label, SEMI, size)


def checks(x, y, w, labels, cols=2, lead=17.0):
    """A checklist laid out in columns. Returns (svg, height consumed)."""
    out, col_w = [], w / cols
    for i, label in enumerate(labels):
        out.append(check(x + (i % cols) * col_w, y + (i // cols) * lead,
                         label)[0])
    rows = -(-len(labels) // cols)
    return "".join(out), (rows - 1) * lead


def photo_box(x, y, w, h, caption=None, sub=None):
    """A dashed box to paste a photograph into."""
    out = [stroked(x, y, w, h, "#B4BCCB", 0.9, r=4, dash="3.5 3")]
    if caption:
        out.append(text(caption, x + w / 2, y + h / 2 - (2 if sub else -2.6),
                        font=SEMI, size=7, fill="#9AA3B2", anchor="middle"))
    if sub:
        out.append(text(sub, x + w / 2, y + h / 2 + 9, font=BODY, size=6.2,
                        fill="#AEB6C4", anchor="middle"))
    return "".join(out)


def cells(x, y, n, groups=None, cell=12.0, h=15.0, gap=5.0, label=None,
          size=LABEL):
    """Character boxes, e.g. DD / MM / YYYY. Returns (svg, width consumed)."""
    out, cx = [], x
    if label:
        out.append(text(label, x, y - 3, font=SEMI, size=size, fill=GREY))
        cx += typeset.measure(label, SEMI, size) + 6
    start = cx
    for gi, size_of in enumerate(groups or [n]):
        for _ in range(size_of):
            out.append(stroked(cx, y - h + 2, cell, h, RULE, 0.7, r=1.6))
            cx += cell + 1.5
        if gi < len(groups or [n]) - 1:
            out.append(text("/", cx + gap / 2 - 1, y - 2, font=SEMI, size=8,
                            fill=GREY))
            cx += gap + 2
    return "".join(out), cx - start + (start - x)
