"""Brand constants, plus the crest placed for banner artwork.

The palette is the website's; the crest's own colours are in emblem.C.
Nothing here invents a colour or nudges a coordinate -- the banner has to
match the sign on the gate and the website.
"""

import emblem

# ---------------------------------------------------------------- palette
C = {
    "green": "#4DAA57",
    "greenMid": "#6BCB77",
    "greenLite": "#8FE09A",
    "greenDeep": "#2F7D3C",   # print-safe darker green for large solid fills
    "greenPale": "#F4FBF4",
    "greenSoft": "#DFF3E3",
    "red": "#FF6B6B",
    "yellow": "#FFD93D",
    "blue": "#4D96FF",
    "purple": "#9B59B6",
    "orange": "#FF9F1C",
    "pink": "#FF6B9D",
    "cyan": "#00D9FF",
    "ink": "#2D3436",
    "grey": "#6B7280",
    "cream": "#FFFDF7",
    "white": "#FFFFFF",
}

SCHOOL = {
    "name": "Arya Vidya Play School",
    "tagline": "Where Every Child Shines!",
    "ages": "Ages 3–6 Years",
    "phone": "+91 91287 91292",
    "website": "www.aryavidyaplayschool.com",
    "address": "Near Power Sub Station, Hocher – 834006, Ranchi",
    # split form -- lets the address sit bigger in a narrow column
    "address_l1": "Near Power Sub Station, Hocher",
    "address_l2": "Ranchi, Jharkhand – 834006",
    "headline": "ADMISSIONS OPEN",
}


# ------------------------------------------------------------------ logo
# The crest itself lives in emblem.py -- one master for the website, the
# favicons, the fee slip and these banners. brand.py only places it.
def logo_defs(ns):
    """Kept for the designs' <defs> block. The crest uses flat colour, so
    there is nothing to namespace any more -- the tree logo's gradients
    were the only reason `ns` existed."""
    return ""


def logo(x, y, width, ns="lg", with_text=True):
    """Place the crest with its top-left at (x, y), scaled to `width`.

    Returns (svg, height) so callers can stack things underneath it. The
    crest already carries the school's name, so with_text=False gives the
    emblem alone -- what a design uses when it sets the name itself.
    """
    return emblem.place(x, y, width, full=with_text), width


# ------------------------------------------------------- decorative bits
def star(cx, cy, r, fill, rotate=0, opacity=None):
    """Five-point star -- used sparingly, it reads at 50 m; emoji do not."""
    import math
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.42
        a = math.radians(-90 + i * 36 + rotate)
        pts.append(f"{cx + rad * math.cos(a):.2f},{cy + rad * math.sin(a):.2f}")
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"{op}/>'


def blob(cx, cy, r, fill, opacity=0.16):
    """The website's soft background blob, flattened to a plain circle."""
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" opacity="{opacity}"/>'


def pill(x, y, w, h, fill, extra=""):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{h / 2:.2f}" fill="{fill}" {extra}/>')


def rounded(x, y, w, h, r, fill, extra=""):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
            f'rx="{r:.2f}" fill="{fill}" {extra}/>')


# --------------------------------------------------------------- icons
def icon_phone(cx, cy, size, fill):
    """Solid handset glyph, drawn at 24x24 and scaled."""
    s = size / 24
    d = ("M6.6 10.8c1.4 2.8 3.8 5.2 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4."
         "6 3.7.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1"
         "h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.7.1.3 0 .7-.2 1l-2.3 2.1z")
    return (f'<g transform="translate({cx - size / 2:.2f},{cy - size / 2:.2f}) '
            f'scale({s:.4f})"><path d="{d}" fill="{fill}"/></g>')


def icon_pin(cx, cy, size, fill):
    s = size / 24
    d = ("M12 2c-3.9 0-7 3.1-7 7 0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0"
         " 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z")
    return (f'<g transform="translate({cx - size / 2:.2f},{cy - size / 2:.2f}) '
            f'scale({s:.4f})"><path d="{d}" fill="{fill}"/></g>')


def icon_globe(cx, cy, size, fill):
    s = size / 24
    d = ("M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-2.9a15.6 15.6 0 0 0-1"
         ".4-3.6A8 8 0 0 1 18.9 8zM12 4.1c.7 1 1.3 2.3 1.7 3.9h-3.4c.4-1.6 1-2.9"
         " 1.7-3.9zM4.3 14a8 8 0 0 1 0-4h3.3a17.6 17.6 0 0 0 0 4H4.3zm.8 2h2.9c."
         "3 1.3.8 2.5 1.4 3.6A8 8 0 0 1 5.1 16zm2.9-8H5.1a8 8 0 0 1 4.3-3.6A15.6"
         " 15.6 0 0 0 8 8zM12 19.9c-.7-1-1.3-2.3-1.7-3.9h3.4c-.4 1.6-1 2.9-1.7 3"
         ".9zM14.1 14H9.9a15.7 15.7 0 0 1 0-4h4.2a15.7 15.7 0 0 1 0 4zm.5 5.6c.6"
         "-1.1 1.1-2.3 1.4-3.6h2.9a8 8 0 0 1-4.3 3.6zm1.8-5.6a17.6 17.6 0 0 0 0-"
         "4h3.3a8 8 0 0 1 0 4h-3.3z")
    return (f'<g transform="translate({cx - size / 2:.2f},{cy - size / 2:.2f}) '
            f'scale({s:.4f})"><path d="{d}" fill="{fill}"/></g>')


def icon_whatsapp(cx, cy, size, fill):
    s = size / 24
    d = ("M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67"
         ".15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1."
         "255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.4"
         "58.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.1"
         "98.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-"
         ".669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1"
         ".04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2"
         " 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.57"
         "1-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-."
         "272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-"
         ".214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 "
         "4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 01"
         "2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11."
         "815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5"
         ".945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11"
         ".89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z")
    return (f'<g transform="translate({cx - size / 2:.2f},{cy - size / 2:.2f}) '
            f'scale({s:.4f})"><path d="{d}" fill="{fill}"/></g>')
