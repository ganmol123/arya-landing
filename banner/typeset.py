"""Text -> SVG path outlines.

Print shops open our SVGs in Illustrator / CorelDRAW where 'Baloo 2' and
'Bubblegum Sans' are not installed. Live <text> would silently reflow into
Arial and wreck the layout, so every glyph in the banner artwork is baked
into a <path>. HarfBuzz does the shaping (real kerning), fontTools pulls the
outlines.
"""

import functools
import math
import os

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.misc.transform import Transform

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

# Friendly name -> file. Keep these in step with the @import in src/App.jsx.
# Only the weights the banners use are vendored -- Baloo 2 carries a full
# Devanagari set and each TTF is ~400 KB. Add a weight back to fonts/ and to
# this map together if a design needs one.
FONTS = {
    "baloo-extrabold": "Baloo2-ExtraBold.ttf",
    "bubblegum": "BubblegumSans.ttf",
    "poppins": "Poppins-Regular.ttf",
    "poppins-medium": "Poppins-Medium.ttf",
    "poppins-semibold": "Poppins-SemiBold.ttf",
    "poppins-bold": "Poppins-Bold.ttf",
    "poppins-extrabold": "Poppins-ExtraBold.ttf",
}


@functools.lru_cache(maxsize=None)
def _load(name):
    path = os.path.join(FONT_DIR, FONTS[name])
    with open(path, "rb") as fh:
        data = fh.read()
    face = hb.Face(data)
    hb_font = hb.Font(face)
    tt = TTFont(path)
    return hb_font, tt, tt.getGlyphSet(), face.upem


def _shape(name, text, size, letter_spacing):
    """Return (glyph runs, total advance) in final user units."""
    hb_font, tt, glyphset, upem = _load(name)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hb_font, buf)

    scale = size / upem
    order = tt.getGlyphOrder()
    runs, pen_x = [], 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        runs.append((order[info.codepoint],
                     pen_x + pos.x_offset * scale,
                     pos.y_offset * scale))
        pen_x += pos.x_advance * scale + letter_spacing
    if runs and letter_spacing:
        pen_x -= letter_spacing  # no trailing gap
    return runs, pen_x, glyphset, scale


def measure(text, font="poppins", size=100, letter_spacing=0):
    """Advance width of `text` in user units."""
    _, width, _, _ = _shape(font, text, size, letter_spacing)
    return width


def metrics(font="poppins", size=100):
    """(ascender, descender, cap_height) in user units."""
    _, tt, _, upem = _load(font)
    scale = size / upem
    hhea, os2 = tt["hhea"], tt.get("OS/2")
    cap = getattr(os2, "sCapHeight", None) or hhea.ascender * 0.72
    return hhea.ascender * scale, hhea.descender * scale, cap * scale


# Every text_path drawn straight onto the artboard records its ink box here,
# so build.py can prove nothing crossed into the hem instead of us squinting
# at a PNG. Text drawn inside a transformed <g> (the logo wordmark) passes
# track=False -- its coordinates are in the group's space, not the banner's.
PLACED = []


def text_path(text, x=0, y=0, font="poppins", size=100, fill="#000",
              anchor="start", letter_spacing=0, opacity=None, extra="",
              track=True):
    """One <path> holding every glyph of `text`.

    `y` is the baseline. `anchor` is start | middle | end, matching
    SVG's text-anchor so callers can centre without measuring first.
    """
    runs, width, glyphset, scale = _shape(font, text, size, letter_spacing)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width

    chunks = []
    for glyph_name, gx, gy in runs:
        pen = SVGPathPen(glyphset, ntos=lambda v: f"{v:.2f}")
        # y flips: font units go up, SVG user units go down.
        tpen = TransformPen(pen, Transform(scale, 0, 0, -scale, x + gx, y - gy))
        glyphset[glyph_name].draw(tpen)
        d = pen.getCommands()
        if d:
            chunks.append(d)

    if not chunks:
        return ""
    if track:
        bx0, by0, bx1, by1 = bbox(text, font, size, letter_spacing)
        PLACED.append((text, x + bx0, y + by0, x + bx1, y + by1))
    attrs = f' fill="{fill}"'
    if opacity is not None:
        attrs += f' opacity="{opacity}"'
    if extra:
        attrs += f" {extra}"
    return f'<path d="{" ".join(chunks)}"{attrs}/>'


def bbox(text, font="poppins", size=100, letter_spacing=0):
    """Tight ink bounds of `text` drawn at baseline y=0, x=0.

    Returns (xmin, ymin, xmax, ymax) in SVG user units (y grows downward),
    so ymin is negative for anything above the baseline. Display type is
    optically centred off this, not off font metrics -- Baloo 2 carries a
    huge Devanagari ascender that would throw the maths out.
    """
    from fontTools.pens.boundsPen import BoundsPen

    runs, _, glyphset, scale = _shape(font, text, size, letter_spacing)
    xs, ys = [], []
    for glyph_name, gx, gy in runs:
        pen = BoundsPen(glyphset)
        glyphset[glyph_name].draw(pen)
        if pen.bounds is None:
            continue
        x0, y0, x1, y1 = pen.bounds
        xs += [x0 * scale + gx, x1 * scale + gx]
        ys += [-(y1 * scale) - gy, -(y0 * scale) - gy]
    if not xs:
        return (0.0, 0.0, 0.0, 0.0)
    return (min(xs), min(ys), max(xs), max(ys))


def fit(text, font, max_width, size, letter_spacing=0, min_size=8):
    """Largest (size, letter_spacing) <= the given ones that fits max_width.

    Layout on a banner is width-driven: the phone number and the school name
    have to span a column exactly, and a two-point overflow past the hem is
    a reprint. Everything downstream sizes through here rather than trusting
    a hand-tuned constant.
    """
    track = letter_spacing / size if size else 0
    w = measure(text, font, size, letter_spacing)
    if w <= max_width:
        return size, letter_spacing
    # advance width is linear in size, so one step lands it; refine once for
    # the rounding in hinted advances.
    for _ in range(3):
        size = max(min_size, size * max_width / w)
        letter_spacing = size * track
        w = measure(text, font, size, letter_spacing)
        if w <= max_width:
            break
    return size, letter_spacing


def cap_height(text, font, size, letter_spacing=0):
    """Ink height above the baseline -- what a driver actually perceives."""
    return -bbox(text, font, size, letter_spacing)[1]


def arc_text(text, cx, cy, radius, mid=0.0, font="baloo-extrabold", size=100,
             fill="#000", letter_spacing=0, flip=False, extra=""):
    """One <path> holding `text` set around a circle.

    `mid` is where the middle of the string sits, in degrees clockwise from
    12 o'clock. `radius` is the baseline circle. flip=False puts the glyphs
    outside that circle (top-of-badge text, tops pointing out); flip=True
    puts them inside it (bottom-of-badge text, tops pointing at the centre)
    and still reads left to right.

    Each glyph is rotated about its own advance centre rather than its
    origin -- at badge sizes one glyph spans several degrees, and hanging
    them off their left edge visibly fans the wide ones apart.
    """
    runs, width, glyphset, scale = _shape(font, text, size, letter_spacing)
    if not runs:
        return ""

    # per-glyph advance, recovered from the gaps between pen positions
    pens = [r[1] for r in runs] + [width]
    chunks = []
    for i, (glyph_name, gx, gy) in enumerate(runs):
        pen = SVGPathPen(glyphset, ntos=lambda v: f"{v:.2f}")
        glyphset[glyph_name].draw(TransformPen(pen, Transform(scale, 0, 0,
                                                              -scale, 0, -gy)))
        d = pen.getCommands()
        if not d:
            continue
        advance = pens[i + 1] - pens[i]
        offset = gx + advance / 2 - width / 2       # along the arc, from centre
        sweep = math.degrees(offset / radius)
        a = mid - sweep if flip else mid + sweep
        rad = math.radians(a)
        px = cx + radius * math.sin(rad)
        py = cy - radius * math.cos(rad)
        rot = a + 180 if flip else a
        chunks.append(
            f'<g transform="translate({px:.2f},{py:.2f}) rotate({rot:.2f}) '
            f'translate({-advance / 2:.2f},0)"><path d="{d}"/></g>')

    return f'<g fill="{fill}"{" " + extra if extra else ""}>{"".join(chunks)}</g>'


def arc_span(text, font="baloo-extrabold", size=100, letter_spacing=0,
             radius=100):
    """Degrees of arc `text` occupies at `radius` -- for fitting to a band."""
    return math.degrees(measure(text, font, size, letter_spacing) / radius)


def fit_arc(text, font, degrees, radius, size, letter_spacing=0):
    """Letter-spacing that makes `text` span exactly `degrees` at `radius`.

    Badge type is set to fill its band edge to edge, so the tracking is
    derived from the gap rather than dialled in by hand.
    """
    target = math.radians(degrees) * radius
    base = measure(text, font, size, 0)
    n = max(1, len(text) - 1)
    return (target - base) / n
