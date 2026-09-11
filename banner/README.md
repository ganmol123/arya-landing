# Roadside banner artwork

Three banner options for Arya Vidya Play School, generated as vector art from
the same brand palette, logo and copy the website uses.

```bash
python3 banner/build.py
```

Everything lands in `banner/out/`. Open `banner/out/index.html` to compare the
three side by side.

## The three options

| File | Look | Use it when |
| --- | --- | --- |
| `a-green-hero` | Solid green field, yellow **ADMISSIONS OPEN** band across the top, white contact footer | Busy road, seen at speed. Highest contrast, holds up in dust and glare. |
| `b-sunshine` | Cream-and-green, full logo lockup, matches the website almost exactly | Slower traffic, foot traffic, school gate. Warmest of the three. |
| `c-split` | Green identity panel on the left, white call-to-action panel on the right | The phone number is the point. Reads well at an angle. |

## What to send the printer

Send the **PDF**. It is a true-size 96 in × 48 in vector file with no embedded
images and no font dependencies — the shop can scale it to any size without it
going soft.

| Format | Notes |
| --- | --- |
| `.pdf` | **Preferred.** Vector, 96 × 48 in, all text already outlined. |
| `.svg` | Same vector art, editable in Illustrator / CorelDRAW. Text is outlined, so it opens correctly on a machine without Baloo 2 / Bubblegum Sans / Poppins installed. |
| `.png` | 6000 × 3000 fallback for shops that only take raster. That is ~62 dpi at 8 × 4 ft, which is normal for flex — large-format is printed at 40–72 dpi because it is viewed from metres away. |

`banner/out/logo/` carries the three logo lockups (square, horizontal, mark
only) as SVG, vector PDF and transparent PNG, for anything else the printer or
a designer needs to make — visiting cards, a gate board, a school diary.

## Sizes

The artboard is 2:1, so one file covers every common flex size:

| Ordered size | Notes |
| --- | --- |
| 6 × 3 ft | Compact, gate or wall |
| **8 × 4 ft** | The size the artwork is drawn at. Good default for roadside. |
| 10 × 5 ft | |
| 12 × 6 ft | |

Tell the shop the size you want and hand them the same PDF — no re-export
needed. For a different **shape** (a tall pole banner, say), the layout needs
redoing rather than stretching; change the canvas in `designs.py` and rebuild.

## Print notes

- Content sits inside a 3.6 in safe margin on all four sides. The hem, the
  fold-over and the eyelets eat the outer strip, so nothing important is near
  an edge.
- Colours are RGB, straight from the website palette. Most Indian flex shops
  print RGB directly; if yours insists on CMYK, ask them to convert, and expect
  the green (`#4DAA57`) to shift very slightly.
- Ask for eyelets every 2 ft on the long edges and one at each corner.

## The safe-box check

`build.py` records the ink box of every line of text as it is placed and fails
the build on two things:

1. **The safe box** — nothing may cross into the hem.
2. **Colour bands** — a line must sit wholly inside a full-bleed band (the
   footer bar, the split panel) or wholly outside it, never straddling the
   edge. Type whose ascenders poke out of its own bar is comfortably inside
   the banner margin and still looks broken, so check 1 alone never sees it.

```
a-green-hero: 8 text runs, inside the safe box and their colour bands; closest ink to a banner edge 3.7 in
```

Two sizing rules keep it honest:

- Long lines are fitted to 93% of their column, not 100% (`AIR`). Fitting to
  exactly the column width leaves a line flush against the rail — technically
  inside the margin, but it reads as about to fall off the banner.
- Icons are sized from the cap height of the line they label, not the font
  size (`ICON_R`). A circular glyph scaled off the em box overhangs its own
  text, which is how the footer ended up straddling its bar.

The footer itself is built from the bar's content box rather than a
hand-picked baseline, and asserts its own extents, so it cannot overflow even
if the copy or the bar height changes.

## Changing the copy

School details live in one place — `SCHOOL` in `banner/brand.py`. Change a
phone number or the age range there and rebuild; every size is fitted at build
time, so nothing overflows even if the new text is longer.

Colours live in `C` in the same file and are lifted from `src/App.jsx`. Keep
the two in step so the banner, the gate and the website stay the same school.

## How the files are built

`typeset.py` shapes text with HarfBuzz and converts every glyph to an SVG
`<path>` via fontTools, so the output has no live text at all. `designs.py`
lays out the three banners on a 2400 × 1200 artboard (25 units per inch).
`build.py` writes the SVG and drives headless Chrome to produce the PDF and
PNG. The fonts in `banner/fonts/` are the same Google Fonts the site loads,
vendored so a rebuild is reproducible offline.
