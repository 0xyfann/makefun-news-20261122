#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Sunday 22 November 2026.

Pure standard library: a tiny PNG encoder (zlib + struct), a pixel
canvas, and a hand-defined 5x7 bitmap font. No PIL, no external font
files, no network. Deterministic output: no time or date chunks.
"""

import struct
import zlib

W, H = 1024, 1024

PAPER = (253, 251, 244)
INK = (18, 18, 18)
RED = (165, 28, 28)
BLUE = (24, 64, 120)
GREY = (110, 110, 105)

# ---------------------------------------------------------------- font
# Each glyph is 7 rows of 5 bits, written as strings of '0'/'1'.
# Uppercase, lowercase, digits and common punctuation.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01000", "01110", "01000", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "10001", "11110", "10000"),
    'q': ("00000", "00000", "01111", "10001", "10001", "01111", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("00100", "00100", "01110", "00100", "00100", "00100", "00011"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01010", "00100", "00100"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "01010", "00000", "00000", "00000", "00000"),
    '*': ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
    '#': ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    '@': ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '<': ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    '>': ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
}


def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, w, h, buf):
    """Write an RGB buffer as a PNG. Deterministic: no time chunks."""
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += buf[y * w * 3:(y + 1) * w * 3]
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    data = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + _chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)


class Canvas:
    def __init__(self, w=W, h=H, bg=PAPER):
        self.w, self.h = w, h
        self.buf = bytearray(bg * (w * h))

    def px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.px(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for a in range(thick):
                for b in range(thick):
                    self.px(x0 + a, y0 + b, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, thick=1):
        x, y, d = 0, r, 3 - 2 * r
        while x <= y:
            for px, py in ((cx + x, cy + y), (cx - x, cy + y),
                           (cx + x, cy - y), (cx - x, cy - y),
                           (cx + y, cy + x), (cx - y, cy + x),
                           (cx + y, cy - x), (cx - y, cy - x)):
                for a in range(thick):
                    self.px(px + a, py, color)
            if d < 0:
                d += 4 * x + 6
            else:
                d += 4 * (x - y) + 10
                y -= 1
            x += 1

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.px(xx, yy, color)


# ---------------------------------------------------------------- text

def char_width(scale):
    return 6 * scale


def text_width(text, scale):
    return len(text) * char_width(scale) - scale


def draw_text(cv, x, y, text, scale, color=INK):
    """Draw text with the 5x7 bitmap font. Returns the x after the text."""
    cx = x
    for ch in text:
        glyph = FONT.get(ch)
        if glyph is None:
            glyph = FONT['?']
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '1':
                    cv.rect(cx + col * scale, y + row * scale,
                            scale, scale, color)
        cx += char_width(scale)
    return cx


def draw_text_centered(cv, cx, y, text, scale, color=INK):
    x = cx - text_width(text, scale) // 2
    draw_text(cv, x, y, text, scale, color)
    return x


def wrap_text(text, scale, max_width):
    """Word-wrap text to lines that fit max_width pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(cv, x, y, text, scale, max_width, color=INK, leading=4):
    lines = wrap_text(text, scale, max_width)
    for i, line in enumerate(lines):
        draw_text(cv, x, y + i * (7 * scale + leading), line, scale, color)
    return y + len(lines) * (7 * scale + leading)


# ---------------------------------------------------------------- pictograms
# Each draws inside a size x size box at (x, y). Simple flat shapes.

def pic_radar(cv, x, y, s, color=BLUE):
    cx, cy = x + s // 2, y + s // 2
    for r in (s // 2 - 4, s // 3, s // 5):
        cv.circle(cx, cy, r, color, 2)
    cv.line(cx, cy, cx + s // 3, cy - s // 3, RED, 2)
    cv.disc(cx, cy, 3, RED)
    cv.disc(cx - s // 4, cy - s // 4, 3, color)
    cv.disc(cx + s // 5, cy - s // 2, 3, color)
    cv.disc(cx - s // 6, cy + s // 4, 3, color)


def pic_badge(cv, x, y, s, color=BLUE):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    pts = []
    for i in range(5):
        import math
        a = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
        a2 = a + math.pi / 5
        pts.append((cx + int(r * 0.45 * math.cos(a2)),
                    cy + int(r * 0.45 * math.sin(a2))))
    for i in range(10):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % 10]
        cv.line(x0, y0, x1, y1, color, 2)
    cv.disc(cx, cy, 4, RED)


def pic_globe(cv, x, y, s, color=BLUE):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 4
    cv.circle(cx, cy, r, color, 2)
    cv.hline(cx - r, cy, 2 * r, color, 2)
    cv.circle(cx, cy, r // 2, color, 1)
    cv.line(cx - r + 6, cy - r + 8, cx + r - 10, cy - r + 8, color, 1)
    cv.line(cx - r + 8, cy + r - 10, cx + r - 6, cy + r - 10, color, 1)


def pic_rocket(cv, x, y, s, color=BLUE):
    cx = x + s // 2
    cv.line(cx, y + 4, cx + 12, y + s // 2, color, 3)
    cv.line(cx, y + 4, cx - 12, y + s // 2, color, 3)
    cv.line(cx - 12, y + s // 2, cx + 12, y + s // 2, color, 3)
    cv.line(cx - 8, y + s // 2, cx - 14, y + s - 12, color, 2)
    cv.line(cx + 8, y + s // 2, cx + 14, y + s - 12, color, 2)
    cv.line(cx, y + s // 2 + 4, cx, y + s - 6, RED, 3)
    cv.disc(cx, y + s // 3, 3, RED)


def pic_chart(cv, x, y, s, color=BLUE):
    cv.vline(x + 8, y + 8, s - 16, color, 2)
    cv.hline(x + 8, y + s - 8, s - 16, color, 2)
    pts = [(x + 12, y + 16), (x + s // 3, y + s // 3),
           (x + s // 2, y + s // 2 - 6), (x + 2 * s // 3, y + 2 * s // 3),
           (x + s - 10, y + s - 16)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 3)
    ex, ey = pts[-1]
    cv.line(ex, ey, ex - 10, ey - 2, RED, 3)
    cv.line(ex, ey, ex - 2, ey - 10, RED, 3)


def pic_quake(cv, x, y, s, color=BLUE):
    import math
    pts = []
    n = 7
    for i in range(n + 1):
        px = x + 6 + i * (s - 12) // n
        py = y + s // 2 + (12 if i % 2 else -12)
        pts.append((px, py))
    for i in range(n):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 3)
    cv.disc(x + s // 4, y + s // 4, 3, color)
    cv.disc(x + 3 * s // 4, y + 3 * s // 4, 3, color)


def pic_ship(cv, x, y, s, color=BLUE):
    cy = y + 2 * s // 3
    cv.line(x + 10, cy, x + s - 10, cy, color, 3)
    cv.line(x + 10, cy, x + 18, cy + 12, color, 3)
    cv.line(x + s - 10, cy, x + s - 18, cy + 12, color, 3)
    cv.line(x + 18, cy + 12, x + s - 18, cy + 12, color, 3)
    cv.vline(x + s // 2, y + s // 4, s // 2, color, 3)
    cv.line(x + s // 2, y + s // 4, x + s // 2 + 14, y + s // 3, RED, 2)
    cx, cyy = x + s // 2, y + 14
    cv.line(cx - 10, cyy, cx + 10, cyy, color, 2)
    cv.line(cx, cyy - 6, cx, cyy + 6, color, 2)
    cv.disc(cx - 10, cyy, 2, color)
    cv.disc(cx + 10, cyy, 2, color)


def pic_cross(cv, x, y, s, color=BLUE):
    cx, cy = x + s // 2, y + s // 2
    cv.circle(cx, cy, s // 2 - 4, color, 2)
    cv.rect(cx - 5, cy - 16, 10, 32, RED)
    cv.rect(cx - 16, cy - 5, 32, 10, RED)


def pic_cricket(cv, x, y, s, color=BLUE):
    cv.line(x + 14, y + s - 12, x + s - 20, y + 14, color, 6)
    cv.line(x + s - 20, y + 14, x + s - 10, y + 8, color, 6)
    cv.disc(x + s - 16, y + s - 16, 7, RED)
    cv.disc(x + s - 16, y + s - 16, 7, RED)


# ---------------------------------------------------------------- layout

MARGIN = 32
CONTENT_W = W - 2 * MARGIN  # 960

LEAD_HEADLINE = "IRAN CLAIMS STRIKES ON US PATRIOT RADARS IN BAHRAIN"
LEAD_SUMMARY = (
    "IRGC says missiles and drones hit two US Patriot radar sites "
    "at al-Riffa and Awali in Bahrain. Trump says an Iran deal could "
    "last 20 years, as Vance refuses to back strikes. Washington "
    "reports rising economic pressure on Tehran and a trilateral "
    "consensus on nukes."
)

STORIES = [
    ("MEXICO NABS FBI'S MOST-WANTED CARTEL BOSS",
     "Fausto Isidro Meza Flores, known as El Chapo Isidro, is caught "
     "in Guasave, Sinaloa. Follow-on violence kills 11.",
     pic_badge),
    ("COP31 DEADLOCK AS FOSSIL FUELS VANISH FROM DRAFT",
     "Antalya talks run past deadline. The final draft drops all fossil "
     "mentions and a $120B adaptation package. First COP to admit 1.5C "
     "is passed.",
     pic_globe),
    ("RUSSIA HITS ZELENSKYY'S HOMETOWN",
     "A missile strike on Kryvyi Rih kills 2 and wounds 60. Russia "
     "launches 400 drones and 110 missiles. Debris falls in Poland.",
     pic_rocket),
    ("AI SELL-OFF DRAGS STOCKS INTO CORRECTION",
     "S&P 500 falls 3.7% on Friday. Nikkei drops 5.06%, Hang Seng "
     "3.79%. Wall Street enters correction territory.",
     pic_chart),
    ("6.9 QUAKE SHAKES PERU'S ANDES",
     "A magnitude 6.9 earthquake strikes the Andes in Peru. No "
     "casualties or damage reported yet.",
     pic_quake),
    ("DRONE HITS RUSSIAN CARGO SHIP IN BALTIC",
     "A drone strikes a Russian cargo vessel in the Gulf of Finland. "
     "Finland tightens security. Ukraine is suspected.",
     pic_ship),
    ("BOLSONARO IN ICU WITH BOWEL OBSTRUCTION",
     "Former Brazilian president Jair Bolsonaro is in intensive care "
     "with an acute bowel obstruction.",
     pic_cross),
    ("NICHOLLS TON PUTS NZ 243/5 IN WELLINGTON",
     "New Zealand reach 243 for 5 on day one of the first Test against "
     "India. Henry Nicholls hits an unbeaten century.",
     pic_cricket),
]


def draw_page(cv):
    # Masthead.
    draw_text_centered(cv, W // 2, 26, "THE WORLD", 9, INK)
    cv.hline(MARGIN, 100, CONTENT_W, INK, 3)
    cv.hline(MARGIN, 106, CONTENT_W, INK, 1)
    # Dateline row.
    draw_text(cv, MARGIN, 120, "VOL. I - NO. 326", 1, GREY)
    draw_text_centered(cv, W // 2, 118, "Sunday, 22 November 2026", 2, INK)
    right = "PRICE: FREE"
    draw_text(cv, W - MARGIN - text_width(right, 1), 120, right, 1, GREY)
    cv.hline(MARGIN, 144, CONTENT_W, INK, 1)

    # Lead story.
    draw_text(cv, MARGIN, 162, "LEAD - MIDDLE EAST", 2, RED)
    y = draw_wrapped(cv, MARGIN, 190, LEAD_HEADLINE, 4, 600, INK, 6)
    y = draw_wrapped(cv, MARGIN, y + 10, LEAD_SUMMARY, 2, 600, INK, 5)
    # Radar illustration box, right of the lead text.
    bx, by, bw, bh = 680, 168, 312, 252
    cv.hline(bx, by, bw, INK, 2)
    cv.hline(bx, by + bh, bw, INK, 2)
    cv.vline(bx, by, bh, INK, 2)
    cv.vline(bx + bw, by, bh, INK, 2)
    pic_radar(cv, bx + 66, by + 14, 180)
    draw_text_centered(cv, bx + bw // 2, by + bh - 22,
                       "US PATRIOT RADAR - BAHRAIN", 1, GREY)
    draw_text(cv, MARGIN, 416,
              "MORE INSIDE: MEXICO - COP31 - UKRAINE - MARKETS - AND MORE",
              1, RED)

    cv.hline(MARGIN, 448, CONTENT_W, INK, 2)
    cv.hline(MARGIN, 454, CONTENT_W, INK, 1)

    # Grid: 2 columns x 4 rows of stories.
    grid_top, grid_bottom = 470, 950
    row_h = (grid_bottom - grid_top) // 4
    col_w = (CONTENT_W - 24) // 2
    cv.vline(MARGIN + col_w + 12, grid_top, grid_bottom - grid_top, GREY, 1)
    for r in range(1, 4):
        yy = grid_top + r * row_h
        cv.hline(MARGIN, yy, CONTENT_W, GREY, 1)
    for i, (headline, summary, pic) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 24)
        y = grid_top + row * row_h + 10
        pic(cv, x, y + 2, 64)
        tx = x + 76
        tw = col_w - 76 - 4
        y2 = draw_wrapped(cv, tx, y, headline, 2, tw, INK, 3)
        draw_wrapped(cv, tx, y2 + 4, summary, 1, tw, INK, 3)

    # Footer.
    cv.hline(MARGIN, 962, CONTENT_W, INK, 2)
    draw_text_centered(
        cv, W // 2, 976,
        "THE WORLD - Sunday, 22 November 2026 - All the news that fits "
        "on one page", 1, GREY)


def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    cv = Canvas()
    draw_page(cv)
    out = os.path.join(here, "entry.png")
    write_png(out, W, H, cv.buf)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
