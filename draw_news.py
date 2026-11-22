#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Sunday 22 November 2026.

Written from scratch in this session. Python standard library only.
Contains a small PNG encoder (zlib + struct), a pixel canvas, and a
5x7 bitmap font defined below. No external assets, no network.
"""

import os
import struct
import zlib

# ---------------------------------------------------------------- font ----
# Each glyph is 7 rows of 5 characters ('#' = ink, '.' = empty).
FONT = {
    'A': ("..#..",
          ".#.#.",
          "#...#",
          "#####",
          "#...#",
          "#...#",
          "#...#"),
    'B': ("####.",
          "#...#",
          "#...#",
          "####.",
          "#...#",
          "#...#",
          "####."),
    'C': (".####",
          "#....",
          "#....",
          "#....",
          "#....",
          "#....",
          ".####"),
    'D': ("####.",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "####."),
    'E': ("#####",
          "#....",
          "#....",
          "####.",
          "#....",
          "#....",
          "#####"),
    'F': ("#####",
          "#....",
          "#....",
          "####.",
          "#....",
          "#....",
          "#...."),
    'G': (".####",
          "#....",
          "#....",
          "#.###",
          "#...#",
          "#...#",
          ".###."),
    'H': ("#...#",
          "#...#",
          "#...#",
          "#####",
          "#...#",
          "#...#",
          "#...#"),
    'I': ("#####",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "#####"),
    'J': ("..###",
          "...#.",
          "...#.",
          "...#.",
          "...#.",
          "#..#.",
          ".##.."),
    'K': ("#...#",
          "#..#.",
          "#.#..",
          "##...",
          "#.#..",
          "#..#.",
          "#...#"),
    'L': ("#....",
          "#....",
          "#....",
          "#....",
          "#....",
          "#....",
          "#####"),
    'M': ("#...#",
          "##.##",
          "#.#.#",
          "#.#.#",
          "#...#",
          "#...#",
          "#...#"),
    'N': ("#...#",
          "##..#",
          "##..#",
          "#.#.#",
          "#..##",
          "#..##",
          "#...#"),
    'O': (".###.",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".###."),
    'P': ("####.",
          "#...#",
          "#...#",
          "####.",
          "#....",
          "#....",
          "#...."),
    'Q': (".###.",
          "#...#",
          "#...#",
          "#...#",
          "#.#.#",
          "#..#.",
          ".##.#"),
    'R': ("####.",
          "#...#",
          "#...#",
          "####.",
          "#.#..",
          "#..#.",
          "#...#"),
    'S': (".####",
          "#....",
          "#....",
          ".###.",
          "....#",
          "....#",
          "####."),
    'T': ("#####",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    'U': ("#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".###."),
    'V': ("#...#",
          "#...#",
          "#...#",
          "#...#",
          "#...#",
          ".#.#.",
          "..#.."),
    'W': ("#...#",
          "#...#",
          "#...#",
          "#.#.#",
          "#.#.#",
          "##.##",
          "#...#"),
    'X': ("#...#",
          "#...#",
          ".#.#.",
          "..#..",
          ".#.#.",
          "#...#",
          "#...#"),
    'Y': ("#...#",
          "#...#",
          ".#.#.",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    'Z': ("#####",
          "....#",
          "...#.",
          "..#..",
          ".#...",
          "#....",
          "#####"),
    '0': (".###.",
          "#..##",
          "#.#.#",
          "##..#",
          "#...#",
          "#...#",
          ".###."),
    '1': ("..#..",
          ".##..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          ".###."),
    '2': (".###.",
          "#...#",
          "....#",
          "...#.",
          "..#..",
          ".#...",
          "#####"),
    '3': ("####.",
          "....#",
          "....#",
          ".###.",
          "....#",
          "....#",
          "####."),
    '4': ("...#.",
          "..##.",
          ".#.#.",
          "#..#.",
          "#####",
          "...#.",
          "...#."),
    '5': ("#####",
          "#....",
          "####.",
          "....#",
          "....#",
          "#...#",
          ".###."),
    '6': (".###.",
          "#....",
          "#....",
          "####.",
          "#...#",
          "#...#",
          ".###."),
    '7': ("#####",
          "....#",
          "...#.",
          "..#..",
          "..#..",
          "..#..",
          "..#.."),
    '8': (".###.",
          "#...#",
          "#...#",
          ".###.",
          "#...#",
          "#...#",
          ".###."),
    '9': (".###.",
          "#...#",
          "#...#",
          ".####",
          "....#",
          "....#",
          ".###."),
    ' ': (".....",
          ".....",
          ".....",
          ".....",
          ".....",
          ".....",
          "....."),
    '.': (".....",
          ".....",
          ".....",
          ".....",
          ".....",
          ".##..",
          ".##.."),
    ',': (".....",
          ".....",
          ".....",
          ".....",
          "..#..",
          "..#..",
          ".#..."),
    "'": ("..#..",
          "..#..",
          ".#...",
          ".....",
          ".....",
          ".....",
          "....."),
    '!': ("..#..",
          "..#..",
          "..#..",
          "..#..",
          "..#..",
          ".....",
          "..#.."),
    '?': (".###.",
          "#...#",
          "....#",
          "...#.",
          "..#..",
          ".....",
          "..#.."),
    '-': (".....",
          ".....",
          ".....",
          ".###.",
          ".....",
          ".....",
          "....."),
    ':': (".....",
          ".##..",
          ".##..",
          ".....",
          ".##..",
          ".##..",
          "....."),
    ';': (".....",
          ".##..",
          ".##..",
          ".....",
          ".##..",
          ".##..",
          ".#..."),
    '(': ("...#.",
          "..#..",
          ".#...",
          ".#...",
          ".#...",
          "..#..",
          "...#."),
    ')': (".#...",
          "..#..",
          "...#.",
          "...#.",
          "...#.",
          "..#..",
          ".#..."),
    '/': ("....#",
          "...#.",
          "...#.",
          "..#..",
          ".#...",
          ".#...",
          "#...."),
    '%': ("#...#",
          "#..#.",
          "...#.",
          "..#..",
          ".#...",
          ".#..#",
          "#...#"),
    '+': (".....",
          "..#..",
          "..#..",
          ".###.",
          "..#..",
          "..#..",
          "....."),
    '=': (".....",
          ".....",
          ".###.",
          ".....",
          ".###.",
          ".....",
          "....."),
    '&': (".##..",
          "#..#.",
          "#.#..",
          ".#...",
          "#.#.#",
          "#..#.",
          ".##.#"),
    '$': ("..#..",
          ".####",
          "#.#..",
          ".###.",
          "..#.#",
          "####.",
          "..#.."),
    '#': (".#.#.",
          ".#.#.",
          "#####",
          ".#.#.",
          "#####",
          ".#.#.",
          ".#.#."),
}

BLANK = (".....",) * 7


# -------------------------------------------------------------- canvas ----
W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (26, 26, 26)
RED = (150, 30, 30)
GRAY = (112, 108, 98)
LIGHT = (188, 182, 170)
BLUE = (38, 76, 116)
GREEN = (34, 96, 62)
GOLD = (156, 116, 32)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bytes(bg) * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def fill_rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def rect(self, x, y, w, h, color, t=1):
        for k in range(t):
            for xx in range(x, x + w):
                self.set(xx, y + k, color)
                self.set(xx, y + h - 1 - k, color)
            for yy in range(y, y + h):
                self.set(x + k, yy, color)
                self.set(x + w - 1 - k, yy, color)

    def hline(self, x, y, w, color, t=1):
        self.fill_rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.fill_rect(x, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x + a, y + b, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, color, t=1):
        x = 0
        y = r
        d = 3 - 2 * r
        while y >= x:
            for px, py in ((cx + x, cy + y), (cx - x, cy + y),
                           (cx + x, cy - y), (cx - x, cy - y),
                           (cx + y, cy + x), (cx - y, cy + x),
                           (cx + y, cy - x), (cx - y, cy - x)):
                for a in range(t):
                    for b in range(t):
                        self.set(px + a, py + b, color)
            x += 1
            if d > 0:
                y -= 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6

    def filled_circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def filled_triangle(self, p1, p2, p3, color):
        xs = sorted([p1, p2, p3], key=lambda p: p[1])
        (x1, y1), (x2, y2), (x3, y3) = xs
        if y1 == y3:
            return
        def interp(xa, ya, xb, yb, y):
            if yb == ya:
                return xa
            return xa + (xb - xa) * (y - ya) / (yb - ya)
        for y in range(y1, y3 + 1):
            if y < y2:
                xa = interp(x1, y1, x2, y2, y)
                xb = interp(x1, y1, x3, y3, y)
            else:
                xa = interp(x2, y2, x3, y3, y)
                xb = interp(x1, y1, x3, y3, y)
            lo, hi = (xa, xb) if xa <= xb else (xb, xa)
            for xx in range(int(lo), int(hi) + 1):
                self.set(xx, y, color)


# ---------------------------------------------------------------- text ----
def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(cv, x, y, s, color, scale):
    for ci, ch in enumerate(s):
        glyph = FONT.get(ch, BLANK)
        ox = x + ci * 6 * scale
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '#':
                    cv.fill_rect(ox + col * scale, y + row * scale,
                                 scale, scale, color)


def draw_text_centered(cv, cx, y, s, color, scale):
    draw_text(cv, cx - text_width(s, scale) // 2, y, s, color, scale)


def wrap(text, scale, max_w):
    adv = 6 * scale
    max_chars = max(1, max_w // adv)
    lines = []
    for para in text.split('\n'):
        cur = ''
        for word in para.split(' '):
            trial = (cur + ' ' + word).strip()
            if len(trial) <= max_chars:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


# ----------------------------------------------------------- pictograms ----
def pic_radar(cv, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2 + 2, 68
    cv.circle(cx, cy, r, BLUE, 3)
    cv.circle(cx, cy, r - 26, BLUE, 2)
    cv.circle(cx, cy, r - 48, BLUE, 2)
    cv.line(cx - r, cy, cx + r, cy, BLUE, 2)
    cv.line(cx, cy - r, cx, cy + r, BLUE, 2)
    cv.filled_triangle((cx, cy), (cx + 56, cy - 32), (cx + 62, cy - 8), BLUE)
    cv.filled_circle(cx + 32, cy - 28, 4, RED)
    cv.filled_circle(cx - 36, cy + 20, 4, RED)
    cv.filled_circle(cx + 14, cy + 36, 4, RED)
    cv.filled_circle(cx, cy, 5, INK)
    # dish mast below
    cv.line(cx - 18, cy + r, cx - 28, y + h - 2, INK, 3)
    cv.line(cx + 18, cy + r, cx + 28, y + h - 2, INK, 3)
    cv.hline(cx - 32, y + h - 2, 64, INK, 3)


def pic_handcuffs(cv, x, y, w, h):
    cy = y + h // 2
    cv.circle(x + 13, cy, 11, GOLD, 3)
    cv.circle(x + 35, cy, 11, GOLD, 3)
    cv.line(x + 13, cy - 11, x + 35, cy - 11, GOLD, 3)
    cv.line(x + 16, cy + 11, x + 32, cy + 11, GOLD, 3)
    cv.filled_circle(x + 13, cy, 3, INK)
    cv.filled_circle(x + 35, cy, 3, INK)


def pic_globe(cv, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2, 20
    cv.circle(cx, cy, r, GREEN, 3)
    cv.line(cx - r + 3, cy - 9, cx + r - 3, cy - 9, GREEN, 2)
    cv.line(cx - r + 3, cy + 9, cx + r - 3, cy + 9, GREEN, 2)
    cv.line(cx, cy - r, cx, cy + r, GREEN, 2)
    cv.filled_circle(cx + 8, cy - 11, 3, RED)
    cv.filled_circle(cx - 10, cy + 12, 3, RED)


def pic_missile(cv, x, y, w, h):
    # rocket flying up-right
    cv.line(x + 10, y + 36, x + 34, y + 12, INK, 4)
    cv.filled_triangle((x + 34, y + 12), (x + 44, y + 4), (x + 40, y + 18), RED)
    cv.filled_triangle((x + 10, y + 36), (x + 4, y + 40), (x + 14, y + 42), INK)
    cv.filled_triangle((x + 10, y + 36), (x + 16, y + 44), (x + 20, y + 38), INK)
    cv.filled_triangle((x + 6, y + 40), (x + 2, y + 46), (x + 10, y + 44), GOLD)
    cv.filled_circle(x + 30, y + 16, 2, PAPER)


def pic_chart(cv, x, y, w, h):
    cv.line(x + 6, y + 6, x + 6, y + 42, INK, 2)
    cv.line(x + 6, y + 42, x + 44, y + 42, INK, 2)
    cv.line(x + 8, y + 12, x + 18, y + 18, RED, 3)
    cv.line(x + 18, y + 18, x + 26, y + 16, RED, 3)
    cv.line(x + 26, y + 16, x + 34, y + 30, RED, 3)
    cv.line(x + 34, y + 30, x + 42, y + 38, RED, 3)
    cv.filled_triangle((x + 42, y + 38), (x + 42, y + 30), (x + 34, y + 38), RED)


def pic_quake(cv, x, y, w, h):
    cv.filled_triangle((x + 4, y + 26), (x + 16, y + 6), (x + 28, y + 26), BLUE)
    cv.filled_triangle((x + 20, y + 26), (x + 32, y + 10), (x + 44, y + 26), BLUE)
    cv.line(x + 2, y + 32, x + 12, y + 38, RED, 3)
    cv.line(x + 12, y + 38, x + 20, y + 32, RED, 3)
    cv.line(x + 20, y + 32, x + 30, y + 40, RED, 3)
    cv.line(x + 30, y + 40, x + 38, y + 33, RED, 3)
    cv.line(x + 38, y + 33, x + 46, y + 40, RED, 3)


def pic_drone_ship(cv, x, y, w, h):
    # drone above
    cv.line(x + 10, y + 8, x + 26, y + 16, INK, 2)
    cv.line(x + 26, y + 8, x + 10, y + 16, INK, 2)
    for px, py in ((x + 9, y + 7), (x + 27, y + 7), (x + 9, y + 17), (x + 27, y + 17)):
        cv.circle(px, py, 4, INK, 2)
    cv.filled_circle(x + 18, y + 12, 3, RED)
    # ship hull
    cv.filled_triangle((x + 6, y + 30), (x + 42, y + 30), (x + 36, y + 40), BLUE)
    cv.fill_rect(x + 6, y + 30, 36, 4, BLUE)
    cv.fill_rect(x + 20, y + 22, 3, 8, INK)
    # waves
    cv.line(x + 2, y + 44, x + 12, y + 44, BLUE, 2)
    cv.line(x + 16, y + 44, x + 26, y + 44, BLUE, 2)
    cv.line(x + 30, y + 44, x + 44, y + 44, BLUE, 2)


def pic_hospital(cv, x, y, w, h):
    cv.rect(x + 6, y + 4, 36, 36, INK, 2)
    cv.fill_rect(x + 20, y + 10, 8, 24, RED)
    cv.fill_rect(x + 12, y + 18, 24, 8, RED)


def pic_cricket(cv, x, y, w, h):
    # stumps
    for sx in (x + 8, x + 14, x + 20):
        cv.line(sx, y + 18, sx, y + 40, GOLD, 3)
    cv.line(x + 8, y + 16, x + 20, y + 16, GOLD, 2)
    # bat: thick angled blade with handle
    cv.line(x + 28, y + 42, x + 40, y + 14, INK, 5)
    cv.line(x + 40, y + 14, x + 44, y + 4, INK, 3)
    # ball
    cv.filled_circle(x + 32, y + 40, 4, RED)


# -------------------------------------------------------------- layout ----
STORIES = [
    ("MEXICO CAPTURES FBI MOST-WANTED CARTEL BOSS",
     "FBI MOST-WANTED FAUSTO MEZA FLORES SEIZED IN GUASAVE; 11 KILLED IN AFTERMATH.",
     pic_handcuffs),
    ("COP31 DEADLOCK OVER FOSSIL FUELS",
     "ANTALYA TALKS OVERRUN; DRAFT DROPS FOSSIL MENTIONS AND $120BN ADAPTATION PACKAGE.",
     pic_globe),
    ("RUSSIA HITS KRYVYI RIH IN MASS DRONE ATTACK",
     "MISSILES HIT KRYVYI RIH, ZELENSKYY'S HOMETOWN; 2 DEAD, 60 HURT. RUSSIA FIRED 400 DRONES AND 110 MISSILES.",
     pic_missile),
    ("AI SELL-OFF DRAGS MARKETS INTO CORRECTION",
     "S&P 500 FELL 3.7% ON FRIDAY; NIKKEI -5.06%, HANG SENG -3.79%. WALL STREET INDEXES ENTER CORRECTION.",
     pic_chart),
    ("MAGNITUDE 6.9 QUAKE SHAKES PERU ANDES",
     "MAGNITUDE 6.9 QUAKE STRUCK THE ANDES IN PERU; NO CASUALTIES OR DAMAGE REPORTED SO FAR.",
     pic_quake),
    ("DRONE HITS RUSSIAN CARGO SHIP IN BALTIC",
     "DRONE STRUCK A RUSSIAN CARGO SHIP IN THE GULF OF FINLAND; FINLAND TIGHTENS SECURITY.",
     pic_drone_ship),
    ("BOLSONARO IN ICU AFTER ACUTE BOWEL BLOCKAGE",
     "FORMER PRESIDENT JAIR BOLSONARO IN INTENSIVE CARE WITH ACUTE BOWEL OBSTRUCTION.",
     pic_hospital),
    ("NICHOLLS TON LIFTS NZ TO 243/5 IN TEST",
     "NEW ZEALAND 243/5 ON DAY ONE IN WELLINGTON; HENRY NICHOLLS SCORED AN UNBEATEN CENTURY.",
     pic_cricket),
]

LEAD_HEADLINE = "IRAN CLAIMS STRIKES ON US PATRIOT RADARS IN BAHRAIN"
LEAD_SUMMARY = (
    "IRGC SAYS MISSILES AND DRONES HIT TWO US PATRIOT RADARS AT AL-RIFFA AND "
    "AWALI IN BAHRAIN. TRUMP SAYS AN IRAN DEAL COULD LAST 20 YEARS AND SEEKS "
    "'ULTIMATE REGIME CHANGE'; VP VANCE DECLINES TO BACK STRIKES ON IRAN. "
    "US REPORTS RISING ECONOMIC PRESSURE ON IRAN AND A TRILATERAL CONSENSUS "
    "ON THE NUCLEAR ISSUE."
)


def draw_page():
    cv = Canvas(W, H, PAPER)

    # ---- masthead ----
    draw_text_centered(cv, W // 2, 26, "THE WORLD", INK, 12)
    cv.hline(24, 122, W - 48, INK, 3)
    draw_text_centered(cv, W // 2, 134, "SUNDAY, 22 NOVEMBER 2026", RED, 3)
    cv.hline(24, 164, W - 48, INK, 2)

    # ---- lead story ----
    draw_text(cv, 24, 182, "LEAD STORY", RED, 2)
    lead_lines = wrap(LEAD_HEADLINE, 5, W - 48)
    ly = 206
    for ln in lead_lines:
        draw_text(cv, 24, ly, ln, INK, 5)
        ly += 38
    # summary on the left, radar pictogram on the right
    sum_lines = wrap(LEAD_SUMMARY, 2, 700)
    sy = ly + 12
    for ln in sum_lines:
        draw_text(cv, 24, sy, ln, INK, 2)
        sy += 18
    pic_radar(cv, 760, ly + 4, 240, 150)
    cv.hline(24, 452, W - 48, INK, 2)

    # ---- grid: 2 columns x 4 rows ----
    col_w = 476
    row_h = 128
    gx0, gy0 = 24, 468
    for i, (headline, summary, pic) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x0 = gx0 + col * (col_w + 24)
        y0 = gy0 + row * (row_h + 6)
        # pictogram top-right
        pic(cv, x0 + col_w - 50, y0 + 2, 48, 48)
        # headline, width leaves room for pictogram
        hl = wrap(headline, 3, col_w - 62)
        hy = y0 + 2
        for ln in hl[:2]:
            draw_text(cv, x0, hy, ln, INK, 3)
            hy += 24
        # summary below headline
        sl = wrap(summary, 2, col_w)
        sy2 = y0 + 56
        for ln in sl[:3]:
            draw_text(cv, x0, sy2, ln, GRAY, 2)
            sy2 += 17
        # row separator
        if row < 3:
            cv.hline(x0, y0 + row_h - 2, col_w, LIGHT, 1)
    # vertical divider between columns
    cv.vline(512, gy0, 4 * row_h + 3 * 6 - 4, LIGHT, 1)

    # ---- footer ----
    cv.hline(24, 1000, W - 48, INK, 2)
    draw_text_centered(cv, W // 2, 1008,
                       "THE WORLD - SUNDAY, 22 NOVEMBER 2026 - PAGE 1",
                       GRAY, 1)
    return cv


# -------------------------------------------------------------- png out ----
def png_bytes(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]

    def chunk(typ, data):
        out = struct.pack('>I', len(data)) + typ + data
        out += struct.pack('>I', zlib.crc32(typ + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + chunk(b'IEND', b''))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    cv = draw_page()
    data = png_bytes(cv)
    with open(os.path.join(here, 'entry.png'), 'wb') as f:
        f.write(data)
    print('wrote entry.png: %d bytes' % len(data))


if __name__ == '__main__':
    main()
