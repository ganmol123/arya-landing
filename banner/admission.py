"""The admission form: one A4 sheet per child, printed both sides.

Side 1 is who the child is and who may be contacted or may collect them.
Side 2 is health, documents, the declarations and the school's own box.

Two things on this form are there for legal reasons rather than
administrative ones, and should not be quietly simplified away:

  * The ID field says "Aadhaar or other government photo ID". UIDAI's
    circulars and Puttaswamy (2018) mean no school may require Aadhaar or
    refuse a child for want of one.
  * Consent is split by purpose and the photography permission is a
    separate opt-in. Under the DPDP Act 2023 a child is anyone under 18 and
    a school holding their data needs verifiable parental consent; a single
    blanket "I agree" on an admission form is specifically not enough.

RETENTION is the school's own policy and the one number here nobody else
can decide. Change it if the school settles on something different.
"""

import typeset
from brand import SCHOOL
from emblem import C
from paper import (A4_H, A4_W, BODY, BOLD, DISPLAY, GREY, HAIR, LABEL, PALE,
                   RULE, SEMI, WARM, WRITE, check, checks, contact_band,
                   crest_band, field, fields, line, page, photo_box, rect,
                   section, stroked, text)

MX, TOP, BOT = 34.0, 30.0, 32.0
INNER = A4_W - 2 * MX
RIGHT = MX + INNER

RETENTION = "while your child is enrolled and for three years after leaving"

# --------------------------------------------------------------- side one
STUDENT_TAIL = (("Blood group", 1), ("Mother tongue", 1.2),
                ("Nationality", 1))
PARENTS = ("Full name", "Occupation", "Mobile number", "Email",
           "Aadhaar or other government photo ID — number")
PARENT_COLS = ("FATHER", "MOTHER", "GUARDIAN (if other)")

# --------------------------------------------------------------- side two
HEALTH = (("Allergies — food, medicine or other", 2),
          ("Ongoing medical conditions (asthma, epilepsy, other)", 2),
          ("Medication taken regularly", 1),
          ("Any support the child needs (speech, hearing, sight, mobility)", 2))
DOCUMENTS = ("Birth certificate (photocopy)",
             "Guardian’s Aadhaar or other government photo ID (photocopy)",
             "2 passport photographs of the child",
             "1 photograph of each person authorised to collect",
             "Immunisation record (photocopy)",
             "Previous school record, if any")
FEE_ACK = ("I have received the school’s fee structure and accept the fees "
           "stated in it. I understand that no payment other than the "
           "notified fees is required.")
DECLARATIONS = (
    "I declare that the information in this form is true and complete to "
    "the best of my knowledge, and I understand that admission may be "
    "withdrawn if any of it is found to be false.",
    "In an emergency, if I cannot be reached, I authorise the school to "
    "give first aid and, if necessary, to take my child to a doctor or "
    "hospital.",
)
DATA_NOTE = (
    "Why we collect this: to admit and teach your child, to reach you, and "
    "to act in an emergency. We keep this form",
    f"{RETENTION}. We do not share it outside the school except where the "
    "law requires. To see, correct or",
    "withdraw your details, write to the school at the address below.",
)
SIGNATURES = ("Signature — Father", "Signature — Mother",
              "Signature — Guardian")
OFFICE = ((("Received by", 1), ("Date", 0.8), ("Admission no. allotted", 1)),
          (("Programme / class", 1), ("Date of joining", 0.8),
           ("Fee receipt no.", 1)))


def _para(lines, x, y, w, size=7.2, lead=10.2, fill=GREY, font=BODY):
    """Pre-broken paragraph lines. Returns (svg, height consumed)."""
    out = [text(s, x, y + i * lead, font=font, size=size, fill=fill)
           for i, s in enumerate(lines)]
    return "".join(out), (len(lines) - 1) * lead


def _break(body, w, size, font=BODY):
    """Greedy line break of `body` to fit `w`."""
    lines, cur = [], ""
    for word in body.split():
        trial = f"{cur} {word}".strip()
        if typeset.measure(trial, font, size) > w and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def _wrap(body, x, y, w, size=7.2, lead=10.2, font=BODY, fill=GREY):
    """Greedy wrap of a single string to `w`, then set it."""
    return _para(_break(body, w, size, font), x, y, w, size, lead, fill, font)


# ------------------------------------------------------------------ page 1
def side_one():
    o, y = [], TOP

    o.append(crest_band(MX, y, INNER, 64, title="ADMISSION FORM",
                        right=SCHOOL["ages"]))
    y += 64 + 18

    # photo block on the right; the admin line and the child's name run
    # alongside it rather than leaving a column of dead paper
    pw, ph = 92.0, 114.0
    px = RIGHT - pw
    o.append(photo_box(px, y, pw, ph, "Photograph", "of the child"))
    col = INNER - pw - 18

    o.append(fields(MX, y + 20, col, [("Admission no.", 1), ("Date", 1)]))
    o.append(section(MX, y + 54, col, 1, "Student"))
    o.append(field(MX, y + 54 + WRITE, col, "Full name of the child, as on the birth certificate"))
    from paper import cells as _cells
    dob, dob_w = _cells(MX, y + 54 + 2 * WRITE, 8, groups=(2, 2, 4),
                        label="Date of birth")
    o.append(dob)
    o.append(fields(MX + dob_w + 16, y + 54 + 2 * WRITE, col - dob_w - 16,
                    [("Gender", 1)]))
    y += ph + 16

    o.append(fields(MX, y, INNER, list(STUDENT_TAIL)))
    o.append(field(MX, y + WRITE, INNER,
                   "Playgroup or school attended before this, if any"))
    y += WRITE + 30

    # ---- parents, as a table: three people, the same five questions
    o.append(section(MX, y, INNER, 2, "Parents and guardian"))
    y += 12
    lab_w = 132.0          # wide enough that no label needs a third line
    cw = (INNER - lab_w) / 3
    for i, head in enumerate(PARENT_COLS):
        o.append(text(head, MX + lab_w + cw * i + cw / 2, y + 9, font=BOLD,
                      size=6.8, fill=C["blue"], anchor="middle", ls=0.8))
    o.append(line(MX, y + 13, INNER, HAIR, 0.9))
    y += 13
    # A label that outgrows its column wraps, and its row grows with it --
    # a fixed row height is what put "Aadhaar or other government photo ID"
    # on top of the father's writing line.
    lead, ry = 8.6, y
    for label in PARENTS:
        lines = _break(label, lab_w - 8, LABEL, SEMI)
        ry += max(28.0, (len(lines) - 1) * lead + 22)
        for i, ln in enumerate(reversed(lines)):
            o.append(text(ln, MX, ry - 4 - i * lead, font=SEMI, size=LABEL,
                          fill=GREY))
        for i in range(3):
            o.append(line(MX + lab_w + cw * i + 4, ry - 1, cw - 8))
    y = ry + 30

    # ---- address
    o.append(section(MX, y, INNER, 3, "Address and contact"))
    o.append(field(MX, y + WRITE, INNER, "Residential address"))
    o.append(field(MX, y + 2 * WRITE, INNER, ""))
    o.append(fields(MX, y + 3 * WRITE, INNER,
                    [("Landmark", 1.5), ("PIN code", 0.7),
                     ("Alternate phone", 1)]))
    y += 3 * WRITE + 32

    # ---- emergency and who may collect the child
    o.append(section(MX, y, INNER, 4,
                     "Emergency contact and who may collect the child"))
    o.append(text("Someone other than the parents, who can reach the school "
                  "quickly", MX, y + 22, font=BOLD, size=6.8,
                  fill=C["blue"]))
    o.append(fields(MX, y + 42, INNER,
                    [("Name", 1.6), ("Relation to the child", 1),
                     ("Phone", 1)]))

    bw, bh = 72.0, 86.0
    bx = RIGHT - (bw * 2 + 10)
    o.append(photo_box(bx, y + 70, bw, bh, "Photo", "father / guardian"))
    o.append(photo_box(bx + bw + 10, y + 70, bw, bh, "Photo",
                       "mother / guardian"))
    col = bx - MX - 20

    o.append(text("Persons authorised to collect the child \u2014 the school will "
                  "not release a child to anyone else",
                  MX, y + 70, font=BOLD, size=6.8, fill=C["magenta"]))
    for i in range(3):
        o.append(fields(MX, y + 92 + i * 27, col,
                        [(f"{i + 1}.  Name", 1.6), ("Relation", 0.9),
                         ("Phone", 1.1)]))
    y += 70 + bh + 6

    o.append(text("Page 1 of 2 — please complete both sides",
                  MX + INNER / 2, A4_H - BOT + 4, font=SEMI, size=6.6,
                  fill="#AEB6C4", anchor="middle"))
    return "".join(o), A4_H - BOT - 14 - y


# ------------------------------------------------------------------ page 2
def _slim_header(y):
    """Side 2 identifies itself without spending another dark band on it."""
    from paper import NAME
    import emblem
    o = [emblem.place(MX, y, 30),
         text(f"{NAME} Play School", MX + 38, y + 14, font=DISPLAY, size=13),
         text("Admission Form · Page 2 of 2", RIGHT, y + 14, font=SEMI,
              size=8, fill=GREY, anchor="end"),
         line(MX, y + 32, INNER, HAIR, 1.0)]
    return "".join(o), 32.0


def side_two():
    o, y = [], TOP
    head, h = _slim_header(y)
    o.append(head)
    y += h + 20

    # ---- health
    o.append(section(MX, y, INNER, 5, "Health"))
    for label, lines in HEALTH:
        o.append(field(MX, y + WRITE, INNER, label))
        for extra in range(1, lines):
            o.append(field(MX, y + WRITE + extra * 24, INNER, ""))
        y += WRITE + (lines - 1) * 24
    o.append(fields(MX, y + WRITE, INNER * 0.62,
                    [("Family doctor", 1.2), ("Doctor’s phone", 1)]))
    imm, iw = check(MX + INNER * 0.66, y + WRITE, "Immunisation up to date")
    o.append(imm)
    o.append(check(MX + INNER * 0.66 + iw + 14, y + WRITE, "Not sure")[0])
    y += WRITE + 26

    # ---- documents
    o.append(section(MX, y, INNER, 6, "Documents attached"))
    docs, dh = checks(MX + 2, y + 20, INNER - 4, DOCUMENTS, cols=2)
    o.append(docs)
    y += 20 + dh + 24

    # ---- fee acknowledgement
    ack, ah = _wrap(FEE_ACK, MX + 14, y + 15, INNER - 120, size=7.2,
                    font=SEMI, fill=C["ink"])
    o.append(rect(MX, y, INNER, ah + 26, WARM, r=7))
    o.append(rect(MX, y + 5, 3.4, ah + 16, C["orange"]))
    o.append(ack)
    o.append(fields(RIGHT - 96, y + ah + 15, 82, [("Date", 1)]))
    y += ah + 26 + 22

    # ---- declarations and consent
    o.append(section(MX, y, INNER, 7, "Declarations and consent"))
    y += 16
    for para in DECLARATIONS:
        svg, ph = _wrap(para, MX + 2, y + 10, INNER - 4)
        o.append(svg)
        y += ph + 20

    o.append(rect(MX, y, INNER, 34, PALE, r=7))
    o.append(text("May the school use photographs or video of your child in "
                  "school displays, printed material and its social media?",
                  MX + 12, y + 13, font=SEMI, size=7.2, fill=C["ink"]))
    yes, yw = check(MX + 12, y + 27, "Yes")
    o.append(yes)
    o.append(check(MX + 12 + yw + 18, y + 27, "No")[0])
    o.append(text("Optional. Admission does not depend on your answer, and "
                  "you may withdraw this permission at any time in writing.",
                  MX + 12 + yw + 70, y + 27, font=BODY, size=6.6, fill=GREY))
    y += 34 + 14

    note, nh = _para(DATA_NOTE, MX + 2, y + 8, INNER - 4, size=6.8, lead=9.6)
    o.append(note)
    y += nh + 30

    sw = (INNER - 2 * 18) / 3
    for i, label in enumerate(SIGNATURES):
        o.append(field(MX + i * (sw + 18), y, sw, ""))
        o.append(text(label, MX + i * (sw + 18), y + 11, font=SEMI, size=6.8,
                      fill=GREY))
    o.append(fields(MX, y + 34, INNER * 0.5, [("Place", 1), ("Date", 1)]))
    y += 34 + 24

    # ---- school use
    o.append(rect(MX, y, INNER, 74, PALE, r=7))
    o.append(text("FOR SCHOOL USE ONLY", MX + 14, y + 17, font=BOLD, size=7,
                  fill=C["blue"], ls=1.1))
    for r, row in enumerate(OFFICE):
        o.append(fields(MX + 14, y + 40 + r * 24, INNER - 28, list(row)))
    y += 74 + 16

    o.append(contact_band(MX, A4_H - BOT - 30, INNER, 30))
    return "".join(o), (A4_H - BOT - 30) - 12 - y


# ----------------------------------------------------------------- output
def page_one_svg():
    return page(A4_W, A4_H, side_one()[0])


def page_two_svg():
    return page(A4_W, A4_H, side_two()[0])


def slack():
    """Points to spare at the foot of each side. Negative means it overran."""
    return (round(side_one()[1], 1), round(side_two()[1], 1))
