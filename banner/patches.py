"""Crest patches: A4 sheets of the new crest, to paste over the old logo.

A batch of stationery went out printed with the old tree logo. Rather than
waste it, each sheet here tiles the new crest in a grid of squares; cut along
the dotted lines and paste one square over each old circle.

Nobody measured the old circle before this was needed, so the PDF carries one
page per likely size. Measure the old logo across with a ruler and print the
page whose size is the nearest one not smaller than it.

Each square is the crest plus PAD of white on every side. The white does two
jobs: it hides the old circle's outline, and it keeps a scissor cut that
wanders a millimetre off the line on paper rather than through the ring.

    sheet_svg(d)  one A4 page for an old logo `d` mm across
    SIZES         the pages the PDF carries, in mm
"""

from emblem import place
from paper import A4_H, A4_W, GREY, MM, SEMI, page, text

SIZES = (35, 40, 45, 50)   # old-logo diameters, mm -- one page each
PAD = 2.0 * MM             # white around the crest inside each square
SIDE_M = 6.0 * MM          # minimum page margin, left and right
END_M = 12.0 * MM          # minimum top and bottom: room for the notes
SCALE = 50.0 * MM          # the check bar printed at the foot


def _grid(d):
    """Cell side, columns, rows and the grid's top-left for a `d` mm logo."""
    cell = d * MM + 2 * PAD
    cols = int((A4_W - 2 * SIDE_M) // cell)
    rows = int((A4_H - 2 * END_M) // cell)
    return cell, cols, rows, (A4_W - cols * cell) / 2, (A4_H - rows * cell) / 2


def _cut_guides(cell, cols, rows, x0, y0):
    """Dotted lines on every cut, ticks just outside the grid to start from."""
    line = ('stroke="#C7CCD6" stroke-width="0.5" '
            'stroke-dasharray="3 3" fill="none"')
    tick = 'stroke="#8A91A0" stroke-width="0.7" fill="none"'
    x1, y1, t = x0 + cols * cell, y0 + rows * cell, 3 * MM
    out = []
    for i in range(cols + 1):
        x = x0 + i * cell
        out.append(f'<path d="M {x:.2f} {y0:.2f} V {y1:.2f}" {line}/>')
        out.append(f'<path d="M {x:.2f} {y0 - t:.2f} V {y0:.2f} '
                   f'M {x:.2f} {y1:.2f} V {y1 + t:.2f}" {tick}/>')
    for j in range(rows + 1):
        y = y0 + j * cell
        out.append(f'<path d="M {x0:.2f} {y:.2f} H {x1:.2f}" {line}/>')
        out.append(f'<path d="M {x0 - t:.2f} {y:.2f} H {x0:.2f} '
                   f'M {x1:.2f} {y:.2f} H {x1 + t:.2f}" {tick}/>')
    return "".join(out)


def _notes(d, count, y0, y1):
    """What the page is for above the grid; the scale check below it."""
    size = 7.0
    head = (f"Crest patches for an old logo {d} mm across  ·  "
            f"{count} per sheet  ·  cut on the dotted lines")
    out = [text(head, A4_W / 2, y0 - 4.5 * MM, font=SEMI, size=size,
                fill=GREY, anchor="middle")]
    # A printer set to "Fit to page" shrinks everything by a few percent and
    # the patch no longer covers the old circle. The bar makes that visible.
    bx, by = A4_W / 2 - SCALE / 2, y1 + 4.5 * MM
    out.append(f'<path d="M {bx:.2f} {by - 3:.2f} V {by + 3:.2f} '
               f'M {bx:.2f} {by:.2f} H {bx + SCALE:.2f} '
               f'M {bx + SCALE:.2f} {by - 3:.2f} V {by + 3:.2f}" '
               f'stroke="{GREY}" stroke-width="0.8" fill="none"/>')
    out.append(text("Print at 100% (Actual size). This bar must measure "
                    "exactly 50 mm.", A4_W / 2, by + 4.2 * MM, size=size - 0.5,
                    fill=GREY, anchor="middle"))
    return "".join(out)


def sheet_svg(d):
    """One A4 page of crest squares for an old logo `d` mm across."""
    cell, cols, rows, x0, y0 = _grid(d)
    crests = "".join(place(x0 + i * cell + PAD, y0 + j * cell + PAD,
                           d * MM, full=True)
                     for j in range(rows) for i in range(cols))
    return page(A4_W, A4_H,
                crests + _cut_guides(cell, cols, rows, x0, y0)
                + _notes(d, cols * rows, y0, y0 + rows * cell))


def counts():
    """Patches per sheet, by size -- for the build log."""
    return {d: _grid(d)[1] * _grid(d)[2] for d in SIZES}
