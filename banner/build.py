#!/usr/bin/env python3
"""Build the roadside banner artwork.

    python3 banner/build.py            # all designs, all formats
    python3 banner/build.py --svg-only # fast loop while designing

Outputs land in banner/out/:
    <name>.svg      vector master, text already converted to outlines
    <name>.pdf      print-ready vector PDF at true size (8ft x 4ft)
    <name>.png      raster backup, 6000x3000 (~62 dpi at 8ft -- ample for flex)
    logo/           the three logo lockups as svg + vector pdf + alpha png
    index.html      contact sheet for comparing the options

Chrome does the SVG -> PDF/PNG conversion; it keeps everything vector in the
PDF, so the printer can scale to any size without pixelation. See README.md
for what to actually hand the print shop.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import designs as _designs  # noqa: E402
import typeset  # noqa: E402
from designs import DESIGNS, MARGIN, W, H  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Print size of the master artboard. 2:1, so it also covers 6x3 / 10x5 / 12x6.
PRINT_W_IN, PRINT_H_IN = 96, 48
PNG_W = 6000
PNG_H = PNG_W * H // W


def _chrome(args):
    base = [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--disable-lcd-text",
            "--force-device-scale-factor=1",
            "--virtual-time-budget=4000"]
    return subprocess.run(base + args, capture_output=True, text=True, timeout=300)


# The logo lockups already living in public/logo/, re-cut as print files.
LOGO_SRC = os.path.normpath(os.path.join(HERE, "..", "public", "logo"))
LOGOS = [
    # file stem, print width (in), png width (px)
    ("arya-vidya-logo", 12, 3000),
    ("arya-vidya-logo-horizontal", 24, 4000),
    ("arya-vidya-logo-mark", 10, 2400),
]


def _page(svg, width_css, height_css, for_print):
    """Wrap the SVG in a page that is exactly one banner big, no margins."""
    page_rule = (f"@page {{ size: {PRINT_W_IN}in {PRINT_H_IN}in; margin: 0; }}"
                 if for_print else "")
    return f"""<!doctype html><meta charset="utf-8">
<style>
  {page_rule}
  html, body {{ margin: 0; padding: 0; background: #fff; }}
  svg {{ display: block; width: {width_css}; height: {height_css}; }}
</style>
{svg}
"""


def render_pdf(svg, dest, size_in=None):
    w_in, h_in = size_in or (PRINT_W_IN, PRINT_H_IN)
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "page.html")
        with open(src, "w") as fh:
            fh.write(_page(svg, f"{w_in}in", f"{h_in}in", True)
                     .replace(f"size: {PRINT_W_IN}in {PRINT_H_IN}in",
                              f"size: {w_in}in {h_in}in"))
        r = _chrome([f"--print-to-pdf={dest}", "--no-pdf-header-footer",
                     f"file://{src}"])
    if not os.path.exists(dest):
        raise RuntimeError(f"chrome failed to write {dest}\n{r.stderr[-1500:]}")


def render_png(svg, dest, size_px=None, transparent=False):
    w, h = size_px or (PNG_W, PNG_H)
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "page.html")
        page = _page(svg, f"{w}px", f"{h}px", False)
        extra = []
        if transparent:
            page = page.replace("background: #fff;", "background: transparent;")
            extra = ["--default-background-color=00000000"]
        with open(src, "w") as fh:
            fh.write(page)
        r = _chrome([f"--screenshot={dest}", f"--window-size={w},{h}",
                     *extra, f"file://{src}"])
    if not os.path.exists(dest):
        raise RuntimeError(f"chrome failed to write {dest}\n{r.stderr[-1500:]}")


def check_bounds(key):
    """Every text run must sit inside the safe box, not just look like it does.

    typeset records the ink box of each run as it is placed. A line fitted to
    exactly its column width ends up flush against the rail -- technically
    inside, optically about to fall off -- so this also reports the tightest
    margin so a squeeze shows up before the banner is printed.
    """
    runs = typeset.PLACED
    limit_x, limit_y = W - MARGIN, H - MARGIN
    bad = [r for r in runs
           if r[1] < MARGIN or r[2] < MARGIN or r[3] > limit_x or r[4] > limit_y]
    for text, x0, y0, x1, y1 in bad:
        print(f"    ! \"{text[:38]}\" leaves the safe box "
              f"({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
    if bad:
        print(f"  {key}: {len(bad)} RUNS OUTSIDE THE SAFE BOX")
        return False
    # distance from the physical edge of the banner, which is the number that
    # decides whether the hem eats anything
    # a line must be wholly inside a colour band or wholly outside it --
    # never straddling the edge
    for name, rx, ry, rw, rh in _designs.REGIONS:
        for text, x0, y0, x1, y1 in runs:
            overlaps = x0 < rx + rw and x1 > rx and y0 < ry + rh and y1 > ry
            inside = x0 >= rx and x1 <= rx + rw and y0 >= ry and y1 <= ry + rh
            if overlaps and not inside:
                print(f"    ! \"{text[:38]}\" straddles the edge of the {name}")
                bad.append(text)
    if bad:
        print(f"  {key}: {len(bad)} RUNS CROSS A BAND EDGE")
        return False

    edge = min(min(W - r[3], H - r[4], r[1], r[2]) for r in runs)
    print(f"  {key}: {len(runs)} text runs, inside the safe box and their "
          f"colour bands; closest ink to a banner edge {edge / 25:.1f} in")
    return True


def build_logo_pack():
    """Vector PDF + transparent PNG of each logo lockup, for the printer.

    The SVGs in public/logo/ are already outlined, so this is purely a
    format conversion -- nothing about the locked artwork changes.
    """
    dest_dir = os.path.join(OUT, "logo")
    os.makedirs(dest_dir, exist_ok=True)
    print("\n  logo lockups:")
    for stem, w_in, png_w in LOGOS:
        src = os.path.join(LOGO_SRC, f"{stem}.svg")
        if not os.path.exists(src):
            print(f"    ! {stem}.svg missing in public/logo — skipped")
            continue
        svg = open(src).read()
        vb = re.search(r'viewBox="([\d.\-\s]+)"', svg).group(1).split()
        ratio = float(vb[3]) / float(vb[2])
        shutil.copyfile(src, os.path.join(dest_dir, f"{stem}.svg"))
        render_pdf(svg, os.path.join(dest_dir, f"{stem}.pdf"),
                   size_in=(w_in, round(w_in * ratio, 3)))
        render_png(svg, os.path.join(dest_dir, f"{stem}.png"),
                   size_px=(png_w, round(png_w * ratio)), transparent=True)
        print(f"    {stem}: svg + pdf ({w_in}in wide) + png ({png_w}px, alpha)")


CONTACT_SHEET = """<!doctype html><meta charset="utf-8">
<title>Arya Vidya — banner options</title>
<style>
  body {{ margin: 0; padding: 40px; background: #1c1f1d; color: #fff;
         font: 15px/1.5 -apple-system, sans-serif; }}
  h1 {{ font-size: 20px; margin: 0 0 6px; }}
  p.note {{ color: #9aa4a0; margin: 0 0 34px; }}
  figure {{ margin: 0 0 46px; }}
  figcaption {{ margin: 0 0 12px; font-weight: 600; }}
  figcaption span {{ font-weight: 400; color: #9aa4a0; }}
  img {{ width: 100%; display: block; border-radius: 6px;
         box-shadow: 0 10px 34px rgba(0,0,0,.5); }}
</style>
<h1>Arya Vidya Play School — roadside banner options</h1>
<p class="note">Artboard 8ft &times; 4ft (2:1). Same files print at 6&times;3,
10&times;5 or 12&times;6 ft.</p>
{figures}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg-only", action="store_true",
                    help="skip the Chrome conversions")
    ap.add_argument("--only", help="build just this design key")
    args = ap.parse_args()

    if not args.svg_only and not os.path.exists(CHROME):
        sys.exit(f"Google Chrome not found at {CHROME} — needed for PDF/PNG. "
                 f"Re-run with --svg-only for vector masters only.")

    os.makedirs(OUT, exist_ok=True)
    figures = []
    clean = True

    for key, (fn, label) in DESIGNS.items():
        if args.only and args.only != key:
            continue
        typeset.PLACED.clear()
        _designs.REGIONS.clear()
        svg = fn()
        clean &= check_bounds(key)
        svg_path = os.path.join(OUT, f"{key}.svg")
        with open(svg_path, "w") as fh:
            fh.write(svg)
        print(f"  {key}.svg   {os.path.getsize(svg_path) // 1024:>5} KB")

        if not args.svg_only:
            pdf_path = os.path.join(OUT, f"{key}.pdf")
            render_pdf(svg, pdf_path)
            print(f"  {key}.pdf   {os.path.getsize(pdf_path) // 1024:>5} KB  "
                  f"({PRINT_W_IN}in x {PRINT_H_IN}in, vector)")

            png_path = os.path.join(OUT, f"{key}.png")
            render_png(svg, png_path)
            print(f"  {key}.png   {os.path.getsize(png_path) // 1024:>5} KB  "
                  f"({PNG_W}x{PNG_H})")

        figures.append(
            f'<figure><figcaption>{label}<br><span>{key}</span></figcaption>'
            f'<img src="{key}.png" alt="{label}"></figure>')

    if not args.svg_only and not args.only:
        build_logo_pack()

    with open(os.path.join(OUT, "index.html"), "w") as fh:
        fh.write(CONTACT_SHEET.format(figures="\n".join(figures)))
    print(f"\n  out/index.html  — open this to compare the options")
    if not clean:
        sys.exit("\nsafe-box check FAILED — do not send these to the printer")


if __name__ == "__main__":
    main()
