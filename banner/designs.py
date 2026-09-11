"""The banner designs.

Canvas is 2400 x 1200 user units = 25 units per inch at 8ft x 4ft. Because
it is pure vector the same file prints at 6x3, 8x4, 10x5 or 12x6 ft -- any
2:1 flex -- with no loss.

Roadside legibility rules these layouts obey:
  * ~1 inch of cap height reads from ~10 ft, so on an 8 ft banner the
    headline clears 5 in of cap height and the phone number clears 3.5 in.
  * Nothing lands outside MARGIN..SAFE_B -- the hem and the eyelets eat that
    strip, and a phone number folded into a hem is a reprint.
  * Four blocks maximum, in the order a driver needs them: the offer, whose
    it is, who to call. A driver gets about three seconds.
  * Every size runs through typeset.fit(), so the copy can change without
    anything silently overflowing.
"""

from brand import (C, SCHOOL, logo, logo_defs, blob, pill, rounded,
                   icon_pin, icon_globe, icon_whatsapp)
from typeset import text_path, measure, fit, cap_height, bbox

W, H = 2400, 1200
MARGIN = 90
SAFE_B = H - 66          # last safe baseline

# fit() shrinks text to exactly the width it is handed, so a long line ends up
# pinned flush to the rail it was measured against -- optically it reads as
# about to fall off the banner even when it is technically inside the margin.
# Long lines are fitted to this fraction of their column instead.
AIR = 0.93

# Icon size as a multiple of the cap height of the line it sits against.
# Sizing icons off the font size instead lets a circular glyph poke above the
# text it labels -- which is how the footer ended up straddling its own bar.
ICON_R = 1.08

# Full-bleed colour bands each design lays down, as (name, x, y, w, h).
# build.py asserts no line of text straddles one of these edges: a footer
# whose ascenders poke out of its own bar is well inside the banner margin
# and still looks broken, so the safe-box check alone never catches it.
REGIONS = []


def _region(name, x, y, w, h):
    REGIONS.append((name, x, y, w, h))


def _svg(ns, defs, body, bg):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- Arya Vidya Play School - roadside banner. Pure vector, all text already
     converted to outlines: no fonts needed to open or print this file.
     Artboard 2400x1200 = 8ft x 4ft at 25 units/inch; prints at any 2:1 size. -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"
     width="96in" height="48in"
     role="img" aria-label="{SCHOOL['name']} - Admissions Open">
  <title>{SCHOOL['name']} — Admissions Open</title>
  <defs>{logo_defs(ns)}{defs}</defs>
  <rect width="{W}" height="{H}" fill="{bg}"/>
{body}
</svg>
'''


# ------------------------------------------------------- shared blocks
def _headline_slab(x, y, w, h, radius, fill_slab, fill_text, track=0.028):
    """ADMISSIONS OPEN set as large as the slab allows, optically centred."""
    pad = w * 0.040
    size, ls = fit(SCHOOL["headline"], "baloo-extrabold", w - pad * 2,
                   600, letter_spacing=600 * track)
    cap = cap_height(SCHOOL["headline"], "baloo-extrabold", size, ls)
    if cap > h - 56:                       # slab too short for that width
        size *= (h - 56) / cap
        ls = size * track
        cap = cap_height(SCHOOL["headline"], "baloo-extrabold", size, ls)
    return (rounded(x, y, w, h, radius, fill_slab)
            + text_path(SCHOOL["headline"], x + w / 2, y + h / 2 + cap / 2,
                        font="baloo-extrabold", size=size, fill=fill_text,
                        letter_spacing=ls, anchor="middle")), size


def _ages_metrics(max_w, start=96, track=0.03):
    """Size the ages chip without drawing it, for callers stacking blocks."""
    size, ls = fit(SCHOOL["ages"], "poppins-bold", max_w * 0.74, start,
                   letter_spacing=start * track)
    tw = measure(SCHOOL["ages"], "poppins-bold", size, ls)
    return size, ls, tw + size * 1.30, size * 1.62


def _ages_pill(x, y, max_w, fill, text_fill, start=96, track=0.03,
               anchor="start", extra=""):
    size, ls, pw, ph = _ages_metrics(max_w, start, track)
    px = x - pw / 2 if anchor == "middle" else x
    cap = cap_height(SCHOOL["ages"], "poppins-bold", size, ls)
    return (pill(px, y, pw, ph, fill, extra)
            + text_path(SCHOOL["ages"], px + pw / 2, y + ph / 2 + cap / 2,
                        font="poppins-bold", size=size, fill=text_fill,
                        letter_spacing=ls, anchor="middle")), ph


def _centre_baseline(box, text, font, max_w):
    """Baseline that centres `text` inside a box, by ink rather than metrics."""
    size, _ = fit(text, font, max_w * 0.815, 600)
    cap = cap_height(text, font, size)
    return (box[0] + box[1]) / 2 + cap / 2


def _phone_block(x, baseline, max_w, colour, icon_colour=None, anchor="start"):
    """WhatsApp mark + the number, sized to fill max_w exactly."""
    size, _ = fit(SCHOOL["phone"], "poppins-extrabold", max_w * 0.815, 600)
    ph_w = measure(SCHOOL["phone"], "poppins-extrabold", size)
    ic, gap = size * 0.92, size * 0.26
    total = ic + gap + ph_w
    x0 = x - total / 2 if anchor == "middle" else x
    cap = cap_height(SCHOOL["phone"], "poppins-extrabold", size)
    return (icon_whatsapp(x0 + ic / 2, baseline - cap / 2, ic,
                          icon_colour or colour)
            + text_path(SCHOOL["phone"], x0 + ic + gap, baseline,
                        font="poppins-extrabold", size=size, fill=colour)), total


def _footer_stack(x, box, max_w, web_colour, addr_colour, leading=1.22):
    """Website + a two-line address, fitted inside a bar's content box.

    Driven by the box, not by a hand-picked baseline. The footer bars are
    full-bleed colour, so type whose ascenders start a few units above the
    bar reads as broken even though it is comfortably inside the banner
    margin -- the safe-box check never sees it. Sizing from the box makes
    that impossible rather than merely unlikely.
    """
    top, bot = box
    avail = bot - top

    # width limit: icon + gap scale with the type, so solve for the size
    # directly instead of fitting against a width that depends on it
    k = measure(SCHOOL["website"], "poppins-semibold", 100) / 100
    s = max_w * AIR / (k + 1.30 * AIR)

    # height limit: the first row's ink, two leadings, then the descender of
    # the last line. Icons are sized off the text's cap rather than the em
    # box, so a round glyph cannot overhang the line it labels.
    for _ in range(4):
        cap = cap_height(SCHOOL["website"], "poppins-semibold", s)
        head = max(cap, cap / 2 + cap * ICON_R / 2)
        desc = bbox(SCHOOL["address_l2"], "poppins-medium", s * 0.94)[3]
        need = head + 2 * leading * s + desc
        if need <= avail:
            break
        s *= avail / need

    cap = cap_height(SCHOOL["website"], "poppins-semibold", s)
    icon, gap = cap * ICON_R, s * 0.36
    body_w = max_w - icon - gap
    lead = leading * s
    b1 = top + max(cap, cap / 2 + icon / 2)

    o = [icon_globe(x + icon / 2, b1 - cap / 2, icon, web_colour),
         text_path(SCHOOL["website"], x + icon + gap, b1,
                   font="poppins-semibold", size=s, fill=web_colour)]

    a = min(s * 0.94,
            fit(SCHOOL["address_l1"], "poppins-medium", body_w, s)[0],
            fit(SCHOOL["address_l2"], "poppins-medium", body_w, s)[0])
    a_cap = cap_height(SCHOOL["address_l1"], "poppins-medium", a)
    o.append(icon_pin(x + icon / 2, b1 + lead - a_cap / 2, icon * 0.92,
                      addr_colour))
    o.append(text_path(SCHOOL["address_l1"], x + icon + gap, b1 + lead,
                       font="poppins-medium", size=a, fill=addr_colour))
    o.append(text_path(SCHOOL["address_l2"], x + icon + gap, b1 + lead * 2,
                       font="poppins-medium", size=a, fill=addr_colour))

    ink_top = min(b1 - cap, b1 - cap / 2 - icon / 2)
    ink_bot = b1 + lead * 2 + bbox(SCHOOL["address_l2"], "poppins-medium", a)[3]
    assert top - 1 <= ink_top and ink_bot <= bot + 1, (
        f"footer stack {ink_top:.0f}..{ink_bot:.0f} escapes its box {box}")
    return "".join(o), s


# ------------------------------------------------------------------ A
def design_a():
    """GREEN HERO — solid green field, yellow headline band, white footer.

    The highest-contrast option: it holds up in dust, glare and at speed.
    Pick this one if the banner faces a busy road.
    """
    ns = "a"
    defs = f'''
    <linearGradient id="{ns}Bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{C['green']}"/>
      <stop offset="100%" stop-color="{C['greenDeep']}"/>
    </linearGradient>'''
    o = [f'<rect width="{W}" height="{H}" fill="url(#{ns}Bg)"/>']
    o += [blob(180, 470, 380, C["greenLite"], 0.13),
          blob(2280, 640, 300, C["greenLite"], 0.10)]

    # ---- 1. the offer, full width
    slab, _ = _headline_slab(MARGIN, 62, W - MARGIN * 2, 244, 40,
                             C["yellow"], C["ink"])
    o.append(slab)

    # ---- 2. identity band
    band_top, band_bot = 350, 842
    card_w, card_h = 480, band_bot - band_top
    o.append(rounded(MARGIN, band_top, card_w, card_h, 46, C["white"]))
    mark_w = 372
    o.append(logo(MARGIN + (card_w - mark_w) / 2,
                  band_top + (card_h - mark_w * 208 / 184) / 2,
                  mark_w, ns=ns, with_text=False)[0])

    x = MARGIN + card_w + 88
    col_w = W - MARGIN - x
    n_size, _ = fit(SCHOOL["name"], "baloo-extrabold", col_w * AIR, 400)
    n_cap = cap_height(SCHOOL["name"], "baloo-extrabold", n_size)
    t_size, _ = fit(SCHOOL["tagline"], "bubblegum", col_w * 0.90, 120)
    ages_h = _ages_metrics(col_w, start=94)[3]

    block_h = n_cap + t_size * 1.04 + 40 + ages_h
    top = band_top + (card_h - block_h) / 2
    name_y = top + n_cap
    o.append(text_path(SCHOOL["name"], x, name_y, font="baloo-extrabold",
                       size=n_size, fill=C["white"]))
    tag_y = name_y + t_size * 1.04
    o.append(text_path(SCHOOL["tagline"], x, tag_y, font="bubblegum",
                       size=t_size, fill=C["yellow"]))
    # translucent chip so the green field shows through, like the site's hero
    o.append(_ages_pill(x, tag_y + 40, col_w, "#FFFFFF", C["white"], start=94,
                        extra='fill-opacity="0.20" stroke="#FFFFFF" '
                              'stroke-width="5"')[0])

    # ---- 3. contact footer
    BAR_Y, STRIP = 876, 12
    o.append(f'<rect x="0" y="{BAR_Y}" width="{W}" height="{H - BAR_Y}" fill="{C["white"]}"/>')
    o.append(f'<rect x="0" y="{BAR_Y}" width="{W}" height="{STRIP}" fill="{C["yellow"]}"/>')
    _region("white footer bar", 0, BAR_Y + STRIP, W, H - BAR_Y - STRIP)
    box = (BAR_Y + STRIP + 8, H - MARGIN)
    o.append(_footer_stack(1150, box, W - MARGIN - 1150, C["green"], C["grey"])[0])
    o.append(_phone_block(MARGIN, _centre_baseline(box, SCHOOL["phone"],
                                                   "poppins-extrabold", 1000),
                          1000, C["ink"], C["green"])[0])
    return _svg(ns, defs, "\n".join(o), C["green"])


# ------------------------------------------------------------------ B
def design_b():
    """SUNSHINE — the website's cream-and-green look, blown up.

    Warmer and more premium than A, and the closest match to the site a
    parent lands on after they scan or search. Best where traffic is slow
    or people are on foot.
    """
    ns = "b"
    defs = f'''
    <linearGradient id="{ns}Bg" x1="0%" y1="0%" x2="24%" y2="100%">
      <stop offset="0%" stop-color="{C['cream']}"/>
      <stop offset="100%" stop-color="{C['greenPale']}"/>
    </linearGradient>
    <linearGradient id="{ns}Bar" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{C['greenMid']}"/>
      <stop offset="100%" stop-color="{C['green']}"/>
    </linearGradient>'''
    o = [f'<rect width="{W}" height="{H}" fill="url(#{ns}Bg)"/>']
    o += [blob(110, 150, 330, C["greenMid"], 0.15),
          blob(2330, 560, 290, C["greenMid"], 0.11)]
    # confetti from the logo's own fruit colours, kept clear of the type
    for cx, cy, r, col in [(2180, 690, 24, C["red"]), (2258, 792, 16, C["yellow"]),
                           (2028, 846, 18, C["blue"]), (1868, 730, 13, C["orange"]),
                           (130, 212, 19, C["purple"]), (212, 146, 13, C["pink"])]:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity="0.8"/>')

    BAR_Y = 882
    band_top, band_bot = 92, BAR_Y - 44

    # ---- full logo lockup, left
    logo_w = 540
    o.append(logo(MARGIN + 26,
                  band_top + (band_bot - band_top - logo_w * 260 / 184) / 2,
                  logo_w, ns=ns)[0])

    x = MARGIN + 26 + logo_w + 104
    col_w = W - MARGIN - x

    slab_y, slab_h = band_top + 10, 210
    o.append(_headline_slab(x, slab_y, col_w, slab_h, slab_h / 2,
                            C["yellow"], C["ink"], track=0.024)[0])

    n_size, _ = fit(SCHOOL["name"], "baloo-extrabold", col_w * AIR, 400)
    n_cap = cap_height(SCHOOL["name"], "baloo-extrabold", n_size)
    name_y = slab_y + slab_h + 92 + n_cap
    o.append(text_path("Arya Vidya", x, name_y, font="baloo-extrabold",
                       size=n_size, fill=C["green"]))
    o.append(text_path(" Play School",
                       x + measure("Arya Vidya", "baloo-extrabold", n_size),
                       name_y, font="baloo-extrabold", size=n_size, fill=C["ink"]))

    t_size, _ = fit(SCHOOL["tagline"], "bubblegum", col_w * 0.88, 114)
    tag_y = name_y + t_size * 1.02
    o.append(text_path(SCHOOL["tagline"], x, tag_y, font="bubblegum",
                       size=t_size, fill=C["grey"]))
    o.append(_ages_pill(x, tag_y + 42, col_w, C["greenSoft"], C["green"],
                        start=92)[0])

    # ---- green contact bar
    o.append(f'<rect x="0" y="{BAR_Y}" width="{W}" height="{H - BAR_Y}" fill="url(#{ns}Bar)"/>')
    _region("green footer bar", 0, BAR_Y, W, H - BAR_Y)
    box = (BAR_Y + 14, H - MARGIN)
    o.append(_footer_stack(1150, box, W - MARGIN - 1150, C["white"], "#E4F5E8")[0])
    o.append(_phone_block(MARGIN, _centre_baseline(box, SCHOOL["phone"],
                                                   "poppins-extrabold", 1000),
                          1000, C["white"])[0])
    return _svg(ns, defs, "\n".join(o), C["cream"])


# ------------------------------------------------------------------ C
def design_c():
    """SPLIT — green identity panel, white call-to-action panel.

    The most structured of the three and the one that pushes the phone
    number hardest: the number is the single biggest thing on the right.
    Good where the banner is read at an angle or from far off.
    """
    ns = "c"
    SPLIT = 840
    defs = f'''
    <linearGradient id="{ns}Panel" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{C['greenMid']}"/>
      <stop offset="100%" stop-color="{C['green']}"/>
    </linearGradient>'''
    o = [f'<rect width="{W}" height="{H}" fill="{C["white"]}"/>',
         f'<rect width="{SPLIT}" height="{H}" fill="url(#{ns}Panel)"/>',
         f'<rect x="{SPLIT}" y="0" width="14" height="{H}" fill="{C["yellow"]}"/>']
    _region("green identity panel", 0, 0, SPLIT, H)
    o += [blob(80, 1150, 300, C["white"], 0.13),
          blob(800, 60, 250, C["white"], 0.11)]

    # ---- left: identity, optically centred in the panel
    lcx, lw = SPLIT / 2, SPLIT - MARGIN * 2
    mark_w, mark_y = 462, 172
    o.append(logo(lcx - mark_w / 2, mark_y, mark_w, ns=ns, with_text=False)[0])
    mark_bot = mark_y + mark_w * 208 / 184

    nm, _ = fit("Arya Vidya", "bubblegum", lw, 190)
    o.append(text_path("Arya Vidya", lcx, mark_bot + 132, font="bubblegum",
                       size=nm, fill=C["white"], anchor="middle"))
    sub, sub_ls = fit("PLAY SCHOOL", "poppins-semibold", lw, 80,
                      letter_spacing=80 * 0.17)
    o.append(text_path("PLAY SCHOOL", lcx, mark_bot + 224,
                       font="poppins-semibold", size=sub, fill="#E4F5E8",
                       anchor="middle", letter_spacing=sub_ls))
    tg, _ = fit(SCHOOL["tagline"], "bubblegum", lw, 94)
    o.append(text_path(SCHOOL["tagline"], lcx, mark_bot + 344, font="bubblegum",
                       size=tg, fill=C["yellow"], anchor="middle"))

    # ---- right: the call to action
    x = SPLIT + 14 + 100
    col_w = W - MARGIN - x
    cx = x + col_w / 2

    slab_y, slab_h = 96, 230
    o.append(_headline_slab(x, slab_y, col_w, slab_h, 38,
                            C["yellow"], C["ink"])[0])

    ages, ages_h = _ages_pill(cx, slab_y + slab_h + 70, col_w, C["green"],
                              C["white"], start=98, anchor="middle")
    o.append(ages)

    lab, lab_ls = fit("CALL / WHATSAPP", "poppins-bold", col_w * 0.66, 64,
                      letter_spacing=64 * 0.18)
    lab_y = slab_y + slab_h + 70 + ages_h + 118
    o.append(text_path("CALL / WHATSAPP", cx, lab_y, font="poppins-bold",
                       size=lab, fill=C["grey"], anchor="middle",
                       letter_spacing=lab_ls))

    o.append(_phone_block(cx, lab_y + 172, col_w, C["ink"], C["green"],
                          anchor="middle")[0])

    rule_y = lab_y + 240
    o.append(f'<rect x="{x + col_w * 0.07}" y="{rule_y}" width="{col_w * 0.86}" '
             f'height="5" rx="2.5" fill="{C["greenSoft"]}"/>')

    w_size, _ = fit(SCHOOL["website"], "poppins-semibold", col_w * 0.84, 72)
    w_w = measure(SCHOOL["website"], "poppins-semibold", w_size)
    o.append(icon_globe(cx - w_w / 2 - w_size * 0.78, rule_y + 74,
                        w_size * 0.96, C["green"]))
    o.append(text_path(SCHOOL["website"], cx + w_size * 0.52, rule_y + 96,
                       font="poppins-semibold", size=w_size, fill=C["green"],
                       anchor="middle"))

    a_size, _ = fit(SCHOOL["address"], "poppins-medium", col_w * 0.82, 58)
    a_w = measure(SCHOOL["address"], "poppins-medium", a_size)
    o.append(icon_pin(cx - a_w / 2 - a_size * 0.72, rule_y + 158,
                      a_size * 0.98, C["grey"]))
    o.append(text_path(SCHOOL["address"], cx + a_size * 0.44, rule_y + 178,
                       font="poppins-medium", size=a_size, fill=C["grey"],
                       anchor="middle"))
    return _svg(ns, defs, "\n".join(o), C["white"])


DESIGNS = {
    "a-green-hero": (design_a, "Green Hero — solid green, maximum contrast"),
    "b-sunshine": (design_b, "Sunshine — the website's cream-and-green look"),
    "c-split": (design_c, "Split — identity panel + big call-to-action"),
}
