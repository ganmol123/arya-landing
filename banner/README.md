# Print artwork

Vector artwork for Arya Vidya Play School — the school crest, three roadside
banner options and the printed fee slip — all generated from the same palette,
logo and copy the website uses.

```bash
python3 banner/build.py               # everything
python3 banner/build.py --svg-only    # fast loop while designing a banner
python3 banner/build.py --logos-only  # crest lockups, favicons, og:image
python3 banner/build.py --fees-only   # the two fee slip PDFs
python3 banner/build.py --patches-only  # crest patches for old stationery
```

Banners land in `banner/out/`; open `banner/out/index.html` to compare the
three side by side. The crest, the favicons, the fee slip and the admission
form are written straight into `public/`, because the site serves them.

`paper.py` holds what the printed documents share — the crest band, the
tints, the type scale and the form widgets. The fee slip and the admission
form both draw their header from it, so neither can drift from the other.

## The crest

`emblem.py` is the master. The school supplied the crest as a 334 px JPEG;
every ring radius, the sun's two circles, each child's silhouette and the
three page layers were measured off that scan and re-cut as real curves, so
the badge stays sharp from a 16 px favicon to an eight-foot banner. It is not
a trace — tracing a 334 px source bakes its JPEG ringing into every
enlargement.

Two things are deliberately *not* copies of the scan:

- **The ring type** is set in Baloo 2 ExtraBold, the display face the site and
  the banners already use. The original was set in a slightly narrower face
  that is not in the repo, so the letters are a little rounder and wider.
- **The sun's rays** are made symmetric about 12 o'clock. The scan is within
  a degree of that already; the fan's uneven spacing (wider gaps in the
  middle, narrower at the edges) is kept, because that is what stops the
  outer rays reading as stragglers.

`build.py` cuts it into three lockups in `public/logo/` — `arya-vidya-logo`
(the full badge), `-horizontal` (badge plus wordmark) and `-mark` (the
emblem alone: sun, three children, open book). Everything below about 120 px
uses the mark, because the ring type turns to mush at that size — that
includes both favicons. **Never hand-edit the SVGs in `public/logo/`;** they
are generated, and the next build overwrites them.

## The fee slip

`fees.py` lays the fee structure out as an A6 card — a quarter of A4 — and
`build.py` writes it two ways:

| File | What it is |
| --- | --- |
| `public/Arya-Vidya-Fee-Structure.pdf` | One A6 card on its own page. This is what the website's **Download Fee Structure** button serves, and what reads on a phone. |
| `public/Arya-Vidya-Fee-Structure-A4-4up.pdf` | A4 portrait, four copies, cut guides. Hand this one to the print shop: one sheet guillotines into four handouts with two straight cuts. |

The cut guides are a dotted line down each cut plus ticks in the sheet margin.
Both sit inside the cards' own 15 pt white margin, so a guillotine that
wanders a point either way still lands on paper rather than through artwork.

Fees live in `FEES` / `TOTAL` in `fees.py` and are mirrored by the `fees`
array in `src/App.jsx` — change them in both places, or the page and the paper
disagree. The build fails if the card overflows its page.

## The admission form

`admission.py` lays out `public/Arya-Vidya-Admission-Form.pdf` — **one A4
sheet per child, printed on both sides.** Side 1 is who the child is and who
may collect them; side 2 is health, documents, declarations and the school's
own box.

Two things on it are there for legal reasons and should not be quietly
simplified away:

- **The ID field reads "Aadhaar or other government photo ID."** [UIDAI's
  circulars](https://uidai.gov.in/en/about-uidai/legal-framework/circulars/2049-no-denial-of-admission-in-schools-for-want-of-aadhaar-and-organising-special-aadhaar-enrollment-update-camps-at-schools.html)
  and *Puttaswamy* (2018) mean no school may require Aadhaar or refuse a
  child for want of one.
- **Consent is split by purpose, and the photography permission is a
  separate opt-in.** Under the DPDP Act 2023 a child is anyone under 18, and
  a school holding their data needs verifiable parental consent — a single
  blanket "I agree" on an admission form is [specifically not
  enough](https://ksandk.com/data-protection-and-data-privacy/dpdp-compliance-for-schools-and-edtech/).
  The Act bites once the form is typed into a computer, not while it is
  paper.

`RETENTION` in `admission.py` is how long the school says it keeps the form.
It is the one value on the page nobody outside the school can decide.

The build fails if either side overflows its page, and reports the spare
points at the foot of each.

### Also worth knowing

The [Jharkhand State Play Schools (Recognition and Control) Rules,
2017](https://www.indianemployees.com/acts-rules/details/jharkhand-state-play-schools-recognition-and-control-rules-2017)
cover unaided private play schools teaching ages 3–6 — which is this school.
They require the operator to be a registered society, trust or company, and
they ban **capitation fees**: any payment beyond the notified fee. The
itemised fee slip is on the right side of that. Get the full text from the
District Superintendent of Education, Ranchi. RTE does not apply at this
stage; it covers ages 6–14.

None of this is legal advice — have someone qualified read the declarations
before printing a large batch.

## Crest patches

Some stationery went out printed with the old tree logo.
`banner/out/Arya-Vidya-Crest-Patches.pdf` tiles the new crest in a grid of
squares so each old logo can be covered by one cut-out square rather than the
stationery being thrown away.

The old circle was never measured, so the PDF has **one A4 page per size**:
35, 40, 45 and 50 mm (`SIZES` in `patches.py`). Measure the old logo across
with a ruler and print the nearest page that is not smaller. On that page the
crest prints at that diameter, with 2 mm of white on every side of the square
to hide the old outline and absorb a crooked cut.

Print at **100% / Actual size**. "Fit to page" shrinks the sheet a few
percent and the square stops covering the old circle; the 50 mm bar at the
foot of each page is there to catch that with a ruler. Self-adhesive A4
sticker paper saves the glue.

## The three banner options

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

`banner/out/logo/` carries the three crest lockups (badge, horizontal, mark
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

Colours live in `C` in the same file and are lifted from `src/App.jsx` — that
is the page palette, the light green scheme the banners are built on. The
crest carries its own, denser palette in `emblem.C`; the fee slip uses that
one. Keep each in step with its counterpart so the banner, the gate and the
website stay the same school.

## How the files are built

`typeset.py` shapes text with HarfBuzz and converts every glyph to an SVG
`<path>` via fontTools, so the output has no live text at all; `arc_text`
does the same around a circle, which is how the crest's ring type is set.
`emblem.py` holds the crest and `paper.py` the shared furniture of the
printed documents. `designs.py` lays out the three banners on a 2400 × 1200
artboard (25 units per inch); `fees.py` and `admission.py` lay their pages
out in PostScript points, so a number in those files is the number a ruler
finds on the paper. `build.py` writes the SVG and drives headless Chrome to
produce the PDF and PNG. The fonts in `banner/fonts/` are the same Google Fonts the site loads,
vendored so a rebuild is reproducible offline.
