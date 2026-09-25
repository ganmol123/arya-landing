"""The Arya Vidya crest, rebuilt as vector geometry.

The school supplied the crest as a 334 px JPEG. Everything here was measured
off that scan -- ring radii, the sun's two circles, each figure's silhouette,
the three page layers -- and re-cut as real curves, so the mark stays sharp
from a favicon to an eight-foot banner. Nothing is traced: a trace of a
334 px source carries its own JPEG ringing into every enlargement.

Master space is a 512 x 512 box with the crest centred on (256, 256); the
magenta ring's outer edge lands on r = 254, leaving two units of bleed.
Callers scale that box, they do not edit it.

    crest()       full badge -- rings, ring type, stars, emblem
    mark()        the emblem alone (sun, three children, book), for favicons
    horizontal()  crest beside the wordmark, for wide spaces
"""

import math

import typeset

# ---------------------------------------------------------------- palette
# Sampled off the scan, then cleaned to flat values. The crest carries its
# own colours -- these are the source of truth, src/App.jsx mirrors them.
C = {
    "magenta": "#D6205A",   # outer ring, "Play School", the left child
    "purple": "#452F78",    # "Arya Vidya"
    "ink": "#2D3462",       # inner ring, "Hocher, Ranchi"
    "blue": "#1F4593",      # centre child, the book's bottom leaves
    "midblue": "#1478BC",   # the book's middle leaves
    "green": "#31A04A",     # the right child, the stars
    "orange": "#F5A41D",    # the sun, the book's top leaves
}

CX = CY = 256.0                 # crest centre
RING_R, RING_W = 247.5, 13.0    # outer magenta ring (centreline, stroke)
INNER_R, INNER_W = 155.2, 6.5   # inner ink ring

SUN_CX, SUN_CY = 256.0, 260.9   # the sun's arc is struck from here, not CY
SUN_R = 84.6                    # outer edge of the crescent
CUT_CY, CUT_R = 284.5, 89.9     # the circle bitten out of it, giving the taper
RAY_R0, RAY_R1, RAY_W = 92.5, 134.5, 19.0
# The fan is deliberately not evenly spaced: the gaps narrow towards the
# horizon, which is what stops the outer rays reading as stragglers. Taken
# off the scan and made symmetric about 12 o'clock.
RAY_ANGLES = (28.5, 47.5, 68.25, 90, 111.75, 132.5, 151.5)

TEXT_SIZE = 60.0
TOP_R, TOP_SPAN = 184.6, 181.0      # baseline radius, degrees of arc
BOT_R, BOT_SPAN = 213.2, 108.0
TOP_TEXT = (("Arya Vidya", C["purple"]), ("Play School", C["magenta"]))
BOT_TEXT = "Hocher, Ranchi"

# angle clockwise from 12 o'clock, baseline radius, outer radius of the star
STARS = ((263.5, 201.7, 16.3), (253.0, 198.5, 11.4), (244.0, 193.6, 8.2))

FONT = "baloo-extrabold"


def _f(*vals):
    return " ".join(f"{v:.2f}" for v in vals)


# -------------------------------------------------------------------- sun
def _sun():
    """A crescent plus seven rays.

    The crescent is one circle minus a second, slightly larger one sitting
    lower -- that is what tapers both horns to a point. Drawn as a single
    even-odd path so it stays one shape in Illustrator.
    """
    # where the two circles cross: the horns
    d = CUT_CY - SUN_CY
    a = (SUN_R ** 2 - CUT_R ** 2 + d ** 2) / (2 * d)
    half = math.sqrt(max(SUN_R ** 2 - a ** 2, 0))
    hy = SUN_CY + a
    lx, rx = SUN_CX - half, SUN_CX + half

    crescent = (f'<path d="M {_f(lx, hy)} '
                f'A {_f(SUN_R, SUN_R)} 0 0 1 {_f(rx, hy)} '
                f'A {_f(CUT_R, CUT_R)} 0 0 0 {_f(lx, hy)} Z" '
                f'fill="{C["orange"]}"/>')

    rays = []
    for deg in RAY_ANGLES:
        th = math.radians(deg)
        ux, uy = math.cos(th), -math.sin(th)     # outward, SVG y grows down
        px, py = -uy, ux                         # perpendicular
        tip = (SUN_CX + RAY_R1 * ux, SUN_CY + RAY_R1 * uy)
        base = (SUN_CX + RAY_R0 * ux, SUN_CY + RAY_R0 * uy)
        h = RAY_W / 2

        def on(t, side):
            """Point t of the way from tip to base, `side` half-widths off."""
            return (tip[0] + (base[0] - tip[0]) * t + px * h * side,
                    tip[1] + (base[1] - tip[1]) * t + py * h * side)

        rays.append(
            f'<path d="M {_f(*tip)} '
            f'C {_f(*on(.34, .40))} {_f(*on(.78, .92))} {_f(*on(1, 1))} '
            f'A {_f(3 * h, 3 * h)} 0 0 1 {_f(*on(1, -1))} '
            f'C {_f(*on(.78, -.92))} {_f(*on(.34, -.40))} {_f(*tip)} Z" '
            f'fill="{C["orange"]}"/>')

    return crescent + "".join(rays)


# --------------------------------------------------------------- children
# Silhouettes fitted to the scan edge by edge. Each child is a head disc
# plus one body path; the white gap between them is the crest's own, not a
# stroke, so the mark still reads when it is knocked out in a single colour.
def _centre_child():
    """Arms thrown up, torso tapering to a point between the book's leaves."""
    body = (f'<path d="M {_f(202.1, 230.7)} '
            f'C {_f(207.0, 246.0)} {_f(224.1, 253.6)} {_f(229.9, 269.1)} '
            f'C {_f(241.4, 294.4)} {_f(248.7, 322.1)} {_f(256.0, 349.1)} '
            f'C {_f(263.3, 322.1)} {_f(270.6, 294.4)} {_f(282.1, 269.1)} '
            f'C {_f(287.9, 253.6)} {_f(305.0, 246.0)} {_f(309.9, 230.7)} '
            f'C {_f(294.8, 235.3)} {_f(282.7, 244.9)} {_f(269.9, 253.5)} '
            f'C {_f(265.0, 259.0)} {_f(247.0, 259.0)} {_f(242.1, 253.5)} '
            f'C {_f(229.3, 244.9)} {_f(217.2, 235.3)} {_f(202.1, 230.7)} Z" '
            f'fill="{C["blue"]}"/>')
    return f'<circle cx="256" cy="227.4" r="21.8" fill="{C["blue"]}"/>{body}'


def _side_child(colour, flip):
    """Outer shoulder low, inner hand raised towards the centre child.

    Drawn on the left; `flip` mirrors it about the crest's axis for the
    right-hand child, so the pair cannot drift apart.
    """
    d = (f'M {_f(166.2, 270.7)} '
         f'C {_f(177.8, 271.6)} {_f(186.8, 280.0)} {_f(198.0, 282.1)} '
         f'C {_f(208.3, 282.8)} {_f(212.1, 271.9)} {_f(216.0, 265.0)} '
         f'C {_f(225.7, 279.8)} {_f(225.7, 298.6)} {_f(227.4, 315.6)} '
         f'C {_f(202.2, 306.8)} {_f(184.2, 289.6)} {_f(166.2, 270.7)} Z')
    tr = f' transform="translate({2 * CX:.0f},0) scale(-1,1)"' if flip else ""
    return (f'<g fill="{colour}"{tr}>'
            f'<circle cx="196.0" cy="260.9" r="12.7"/><path d="{d}"/></g>')


# ------------------------------------------------------------------- book
# Three leaves a side, each a band running from its outer corner to the
# spine. Curves are least-squares fits to the scan's edges; the right leaves
# are the left ones mirrored. Only the bottom pair carries `blunt` -- those
# two meet across the spine and make the book's own edge, while the leaves
# above them close to a point and leave the centre child's feet visible.
#     colour, outer top, top controls, spine, bottom controls, outer bottom
LEAVES = (
    ("orange", (178.4, 303.4), ((208.3, 310.8), (233.6, 328.5)),
     (254.4, 350.7), 0.0, ((226.8, 335.0), (197.0, 319.2)), (163.7, 320.5)),
    ("midblue", (151.5, 324.6), ((188.3, 326.8), (231.6, 333.6)),
     (255.2, 365.4), 0.0, ((230.0, 344.5), (191.9, 337.5)), (160.4, 345.8)),
    ("blue", (157.2, 352.4), ((191.0, 351.3), (227.2, 352.8)),
     (257.0, 372.8), 6.5, ((225.9, 363.2), (189.8, 361.7)), (156.4, 366.3)),
)


def _book():
    out = []
    for key, top, tc, spine, blunt, bc, bot in LEAVES:
        d = (f'M {_f(*top)} C {_f(*tc[0])} {_f(*tc[1])} {_f(*spine)} '
             + (f'L {_f(spine[0], spine[1] + blunt)} ' if blunt else "")
             + f'C {_f(*bc[0])} {_f(*bc[1])} {_f(*bot)} Z')
        for flip in (False, True):
            tr = (f' transform="translate({2 * CX:.0f},0) scale(-1,1)"'
                  if flip else "")
            out.append(f'<path d="{d}" fill="{C[key]}"{tr}/>')
    return "".join(out)


# ------------------------------------------------------------------ stars
def _star(cx, cy, r, colour, inner=0.44, rotate=0.0):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * inner
        th = math.radians(-90 + rotate + i * 36)
        pts.append(f"{cx + rr * math.cos(th):.2f},{cy + rr * math.sin(th):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{colour}"/>'


def _stars():
    out = []
    for deg, radius, size in STARS:
        for a in (deg, 360 - deg):
            th = math.radians(a)
            out.append(_star(CX + radius * math.sin(th),
                             CY - radius * math.cos(th), size, C["green"]))
    return "".join(out)


# ------------------------------------------------------------- ring type
def _ring_type():
    out = []
    # the two halves of the top line are coloured differently but set as one
    # run, so the tracking and the join stay right
    (head, head_col), (tail, tail_col) = TOP_TEXT
    whole = f"{head} {tail}"
    ls = typeset.fit_arc(whole, FONT, TOP_SPAN, TOP_R, TEXT_SIZE)
    full = typeset.measure(whole, FONT, TEXT_SIZE, ls)
    # the line is tracked and fitted as one run, then drawn in two colours:
    # the first chunk is flush to the line's start, the second to its end.
    for chunk, colour, flush_end in ((head, head_col, False),
                                     (tail, tail_col, True)):
        w = typeset.measure(chunk, FONT, TEXT_SIZE, ls)
        centre = (full - w) / 2 if flush_end else (w - full) / 2
        out.append(typeset.arc_text(chunk, CX, CY, TOP_R,
                                    mid=math.degrees(centre / TOP_R),
                                    font=FONT, size=TEXT_SIZE,
                                    fill=colour, letter_spacing=ls))

    ls = typeset.fit_arc(BOT_TEXT, FONT, BOT_SPAN, BOT_R, TEXT_SIZE)
    out.append(typeset.arc_text(BOT_TEXT, CX, CY, BOT_R, mid=180, font=FONT,
                                size=TEXT_SIZE, fill=C["ink"],
                                letter_spacing=ls, flip=True))
    return "".join(out)


# ------------------------------------------------------------------ marks
def emblem():
    """Sun, three children, book -- no rings, no type."""
    return (_sun() + _book() + _side_child(C["magenta"], False)
            + _side_child(C["green"], True) + _centre_child())


def rings():
    return (f'<circle cx="{CX:.0f}" cy="{CY:.0f}" r="{RING_R}" fill="none" '
            f'stroke="{C["magenta"]}" stroke-width="{RING_W}"/>'
            f'<circle cx="{CX:.0f}" cy="{CY:.0f}" r="{INNER_R}" fill="none" '
            f'stroke="{C["ink"]}" stroke-width="{INNER_W}"/>')


def crest(size=512, background=None):
    """The full badge as a standalone <svg>."""
    bg = (f'<circle cx="{CX:.0f}" cy="{CY:.0f}" r="{RING_R - RING_W / 2:.1f}" '
          f'fill="{background}"/>') if background else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
            f'width="{size}" height="{size}" role="img" '
            f'aria-label="Arya Vidya Play School, Hocher, Ranchi">'
            f'{bg}{rings()}{_ring_type()}{_stars()}{emblem()}</svg>')


# The emblem's own ink box, squared up and padded a little: the mark has to
# crop tight (the ring's empty margin would eat a 32 px favicon alive) but
# still sit in a square, which is what .ico and apple-touch-icon want.
MARK_BOX = (126, 123, 260, 260)


def mark(size=512):
    x, y, w, h = MARK_BOX
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="{x} {y} {w} {h}" width="{size}" '
            f'height="{size * h / w:.0f}" role="img" '
            f'aria-label="Arya Vidya Play School">{emblem()}</svg>')


def place(x, y, size, full=False):
    """The crest (or the mark) as a <g>, top-left at (x, y), `size` wide.

    For dropping the badge into other artwork -- banners, the fee slip --
    without every caller redoing the box maths.
    """
    if full:
        return (f'<g transform="translate({x:.2f},{y:.2f}) '
                f'scale({size / 512:.5f})">'
                f'{rings()}{_ring_type()}{_stars()}{emblem()}</g>')
    bx, by, _, side = MARK_BOX
    return (f'<g transform="translate({x:.2f},{y:.2f}) '
            f'scale({size / side:.5f}) translate({-bx},{-by})">'
            f'{emblem()}</g>')


# ------------------------------------------------------- horizontal lockup
# The crest already carries the school's name, so the wordmark beside it is
# there for legibility at a distance, not to repeat the badge. Sized off the
# crest's own diameter so the pair scales as one object.
WORDMARK = (("Arya Vidya", FONT, 132.0, 0.0, "purple"),
            ("PLAY SCHOOL", "poppins-semibold", 55.0, 17.0, "magenta"))
LOCKUP_GAP = 56.0


def horizontal(size=1400):
    """The crest on the left, "Arya Vidya / PLAY SCHOOL" on the right."""
    (top, tf, tsize, tls, tcol), (bot, bf, bsize, bls, bcol) = WORDMARK
    x = 512 + LOCKUP_GAP
    widths = [typeset.measure(top, tf, tsize, tls),
              typeset.measure(bot, bf, bsize, bls)]
    top_cap = typeset.cap_height(top, tf, tsize)
    # optical centring: the two lines as one block, centred on the crest
    block = top_cap + 34 + bsize * 0.72
    base = CY - block / 2 + top_cap
    body = (typeset.text_path(top, x, base, font=tf, size=tsize,
                              fill=C[tcol], letter_spacing=tls, track=False)
            + typeset.text_path(bot, x, base + 34 + bsize * 0.72, font=bf,
                                size=bsize, fill=C[bcol],
                                letter_spacing=bls, track=False))
    w = x + max(widths) + 8
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {w:.0f} 512" width="{size}" '
            f'height="{size * 512 / w:.0f}" role="img" '
            f'aria-label="Arya Vidya Play School">'
            f'{rings()}{_ring_type()}{_stars()}{emblem()}{body}</svg>')
