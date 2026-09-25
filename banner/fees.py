"""The printed fee slip: one A6 card, four to an A4 sheet.

The card is A6 portrait -- a quarter of A4 -- so one sheet guillotines into
four handouts with two straight cuts. Everything is laid out in PostScript
points, which is what the PDF page is measured in, so a number here is the
number a ruler finds on the paper.

    card_svg()   one A6 card on its own page (the website download)
    sheet_svg()  an A4 with four of them and the cut guides

Fees live in FEES / TOTAL below and are mirrored by the `fees` array in
src/App.jsx. Change them in both places, or the page and the paper disagree.
Everything else on the card -- address, phone, ages, tagline -- comes from
brand.SCHOOL.
"""

import typeset
from brand import SCHOOL
from emblem import C
from paper import (A4_H, A4_W, BODY, BOLD, DISPLAY, GREY, HAIR, PALE, SEMI,
                   WARM, contact_band, crest_band, page)
from paper import rect as _rect
from paper import rupees as _rupees
from paper import text as _t

CARD_W, CARD_H = A4_W / 2, A4_H / 2      # A6, 105 x 148.5 mm

M = 15.0                                 # card margin; also the cut safety
INNER = CARD_W - 2 * M

# name, when it is charged, amount, colour of the "when" tag
FEES = (
    ("Tuition Fee", "monthly", "1,500", "green"),
    ("Development Fee", "one-time", "3,000", "orange"),
    ("Admission Fee", "one-time", "10,500", "midblue"),
)
TOTAL = ("Total Payable at Admission", "15,000")
NOTE = ("One month’s tuition fee is included in the admission fee.",
        "Thereafter ₹1,500/- is payable monthly.")
INCLUDED = (("2 Complimentary Uniform Sets", "magenta"),
            ("Stationery & School Kit", "midblue"),
            ("First Month’s Tuition Fee", "green"))
BRING = ("Please bring:",
         "Guardian’s Aadhaar or other photo ID · Student’s date of birth")


# --------------------------------------------------------------- the card
def _header(y):
    """Crest, school name and age range on the shared dark band."""
    return crest_band(M, y, INNER, 54.0, right=SCHOOL["ages"]), 54.0


def _title(y):
    """"FEE STRUCTURE" in a pill, centred."""
    label, size, ls = "FEE STRUCTURE", 9.5, 2.2
    w = typeset.measure(label, DISPLAY, size, ls) + 30
    h = 19.0
    x = (CARD_W - w) / 2
    return (_rect(x, y, w, h, C["orange"], r=h / 2)
            + _t(label, CARD_W / 2 + ls / 2, y + 13.1, font=DISPLAY,
                 size=size, fill=C["ink"], anchor="middle", ls=ls)), h


def _table(y):
    """Three fee rows, then the total."""
    out, row = [], 24.0
    for i, (name, tag, amount, tag_col) in enumerate(FEES):
        base = y + i * row + 16
        out.append(_t(name, M + 4, base, font=SEMI, size=9.2))
        out.append(_t(tag, M + 4 + typeset.measure(name, SEMI, 9.2) + 6, base,
                      font=BOLD, size=6.2, fill=C[tag_col]))
        out.append(_rupees(amount, CARD_W - M - 4, base, 12, C["ink"]))
        out.append(_rect(M + 4, y + (i + 1) * row - 0.5, INNER - 8, 0.6, HAIR))
    y += len(FEES) * row + 6

    h = 31.0
    out.append(_rect(M, y, INNER, h, PALE, r=7))
    out.append(_rect(M, y + 5, 3.4, h - 10, C["green"]))
    out.append(_t(TOTAL[0], M + 12, y + 20, font=BOLD, size=9))
    out.append(_rupees(TOTAL[1], CARD_W - M - 11, y + 21, 14.5, C["green"]))
    return "".join(out), len(FEES) * row + 6 + h


def _note(y):
    out = [_t(line, CARD_W / 2, y + 6 + i * 9, font=BODY, size=6.4, fill=GREY,
              anchor="middle") for i, line in enumerate(NOTE)]
    return "".join(out), 6 + len(NOTE) * 9


def _included(y):
    h = 15 + len(INCLUDED) * 14 + 8
    out = [_rect(M, y, INNER, h, PALE, r=7)]
    out.append(_t("What’s Included", M + 12, y + 17, font=DISPLAY,
                  size=10, fill=C["blue"]))
    for i, (item, colour) in enumerate(INCLUDED):
        cy = y + 31 + i * 14
        out.append(f'<circle cx="{M + 15.5:.2f}" cy="{cy - 2.6:.2f}" r="3.1" '
                   f'fill="{C[colour]}"/>')
        out.append(_t(item, M + 23, cy, font=SEMI, size=7.6))
    return "".join(out), h


def _required(y):
    """What the parent has to bring.

    Its own strip, and the only warm one on the card: this is the single
    line that asks the reader to do something, so it must not read as more
    small print under the total.
    """
    h, size, gap = 18.0, 6.6, 4.0
    lead, items = BRING
    lw = typeset.measure(lead, BOLD, size)
    x = (CARD_W - (lw + gap + typeset.measure(items, SEMI, size))) / 2
    return (_rect(M, y, INNER, h, WARM, r=6)
            + _t(lead, x, y + 11.8, font=BOLD, size=size, fill=C["magenta"])
            + _t(items, x + lw + gap, y + 11.8, font=SEMI, size=size)), h


def _footer(y):
    h = 30.0
    return contact_band(M, y, INNER, h), h


def card(x=0.0, y=0.0):
    """One A6 card as a <g>, top-left at (x, y)."""
    out, cursor = [_rect(0, 0, CARD_W, CARD_H, "#FFFFFF")], M
    for build, gap in ((_header, 10), (_title, 10), (_table, 6),
                       (_note, 7), (_required, 8), (_included, 8)):
        svg, h = build(cursor)
        out.append(svg)
        cursor += h + gap
    out.append(_t(SCHOOL["tagline"], CARD_W / 2, cursor + 9, font=DISPLAY,
                  size=10, fill=C["green"], anchor="middle"))
    svg, h = _footer(CARD_H - M - 30)
    out.append(svg)
    return (f'<g transform="translate({x:.2f},{y:.2f})">{"".join(out)}</g>',
            CARD_H - M - 30 - (cursor + 12))


# -------------------------------------------------------------- the pages
def _cut_guides():
    """Dotted lines down the two cuts, plus ticks in the sheet's margin.

    Both sit in the cards' own white margin, so a guillotine that wanders a
    point either way still lands on paper rather than through the artwork.
    """
    line = (f'stroke="#C7CCD6" stroke-width="0.5" '
            f'stroke-dasharray="3 3" fill="none"')
    tick = 'stroke="#8A91A0" stroke-width="0.7" fill="none"'
    out = [f'<path d="M {CARD_W:.2f} 0 V {A4_H:.2f}" {line}/>',
           f'<path d="M 0 {CARD_H:.2f} H {A4_W:.2f}" {line}/>']
    for x0, y0, x1, y1 in ((CARD_W, 0, CARD_W, 11),
                           (CARD_W, A4_H - 11, CARD_W, A4_H),
                           (0, CARD_H, 11, CARD_H),
                           (A4_W - 11, CARD_H, A4_W, CARD_H)):
        out.append(f'<path d="M {x0:.2f} {y0:.2f} L {x1:.2f} {y1:.2f}" '
                   f'{tick}/>')
    return "".join(out)


def card_svg():
    """The single card, as its own A6 page -- this is what the site serves."""
    return page(CARD_W, CARD_H, card()[0])


def sheet_svg():
    """A4 portrait, four cards, cut guides."""
    body = "".join(card(cx, cy)[0]
                   for cy in (0, CARD_H) for cx in (0, CARD_W))
    return page(A4_W, A4_H, body + _cut_guides())


def slack():
    """Points left between the tagline and the footer band -- if this goes
    negative the card has overflowed and the layout needs a trim."""
    return card()[1]
