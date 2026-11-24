#!/usr/bin/env python3
"""Render the 24 November 2026 front page of THE WORLD TODAY.

Pure Python 3 stdlib: a tiny 5x7 bitmap font, simple shape drawing,
and a minimal PNG encoder (zlib + struct). No external packages,
no network, no downloaded images -- every pixel is drawn by this file.
"""
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (178, 34, 34)
DARKGREY = (90, 90, 90)
LIGHT = (238, 238, 238)
BLUE = (30, 70, 130)
GOLD = (200, 150, 30)

# ------------------------------------------------------------------ font
# 5x7 bitmap glyphs. '#' = ink, ' ' = blank.
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
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
}

# ----------------------------------------------------------------- canvas
px = bytearray(W * H * 3)
for i in range(0, W * H * 3, 3):
    px[i] = 255
    px[i + 1] = 255
    px[i + 2] = 255


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        o = (y * W + x) * 3
        px[o], px[o + 1], px[o + 2] = color


def rect(x, y, w, h, color):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_px(xx, yy, color)


def hline(x, y, w, color, thick=1):
    rect(x, y, w, thick, color)


def vline(x, y, h, color, thick=1):
    rect(x, y, thick, h, color)


def circle(cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                set_px(xx, yy, color)


def ring(cx, cy, r, color, thick=4):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = (xx - cx) ** 2 + (yy - cy) ** 2
            if (r - thick) ** 2 <= d <= r * r:
                set_px(xx, yy, color)


def triangle(points, color):
    # Fill a triangle by scanline interpolation.
    (x0, y0), (x1, y1), (x2, y2) = points
    ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
    for y in range(ymin, ymax + 1):
        xs = []
        for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                   ((x1, y1), (x2, y2)),
                                   ((x2, y2), (x0, y0))):
            if ay == by:
                continue
            if min(ay, by) <= y < max(ay, by) or (y == ymax and y == max(ay, by)):
                t = (y - ay) / (by - ay)
                xs.append(ax + t * (bx - ax))
        if len(xs) >= 2:
            for x in range(int(min(xs)), int(max(xs)) + 1):
                set_px(x, y, color)


def line(x0, y0, x1, y1, color, thick=2):
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(steps + 1):
        t = i / steps
        x = int(x0 + (x1 - x0) * t)
        y = int(y0 + (y1 - y0) * t)
        rect(x - thick // 2, y - thick // 2, thick, thick, color)


# ------------------------------------------------------------------- text
def text_width(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, color=BLACK):
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[' '])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '1':
                    rect(cx + col * scale, y + row * scale, scale, scale, color)
        cx += 6 * scale
    return cx


def draw_text_centered(cx, y, s, scale, color=BLACK):
    draw_text(cx - text_width(s, scale) // 2, y, s, scale, color)


def wrap_text(s, max_w, scale):
    """Greedy word wrap; returns list of lines fitting max_w pixels."""
    words = s.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(x, y, s, max_w, scale, color=BLACK, line_gap=4):
    lines = wrap_text(s, max_w, scale)
    for i, ln in enumerate(lines):
        draw_text(x, y + i * (7 * scale + line_gap), ln, scale, color)
    return y + len(lines) * (7 * scale + line_gap)


# -------------------------------------------------------------- page frame
M = 28  # margin
# Masthead
draw_text_centered(W // 2, 18, "THE WORLD TODAY", 7, BLACK)
hline(M, 96, W - 2 * M, BLACK, 5)
hline(M, 106, W - 2 * M, BLACK, 2)
# Date line
draw_text(M, 120, "TUESDAY, 24 NOVEMBER 2026", 2, RED)
draw_text(W - M - text_width("WORLD EDITION", 2), 120, "WORLD EDITION", 2, BLACK)
hline(M, 142, W - 2 * M, BLACK, 2)

# ------------------------------------------------------------- illustrations
def draw_jet(x, y, s, color=BLUE):
    # Simple jet silhouette: fuselage, wings, tail, nose.
    rect(x, y + 8 * s, 34 * s, 4 * s, color)          # fuselage
    triangle([(x + 34 * s, y + 8 * s), (x + 44 * s, y + 10 * s),
              (x + 34 * s, y + 12 * s)], color)       # nose
    triangle([(x + 14 * s, y + 8 * s), (x + 20 * s, y + 2 * s),
              (x + 24 * s, y + 8 * s)], color)        # top wing
    triangle([(x + 14 * s, y + 12 * s), (x + 20 * s, y + 18 * s),
              (x + 24 * s, y + 12 * s)], color)       # bottom wing
    triangle([(x + 2 * s, y + 8 * s), (x + 6 * s, y + 2 * s),
              (x + 10 * s, y + 8 * s)], color)        # tail fin
    # speed lines
    for i in range(3):
        hline(x - 14 * s, y + (4 + i * 5) * s, 10 * s, DARKGREY, 2)


def draw_dove(x, y, s, color=BLUE):
    # Stylised dove: body, wing, head, olive branch.
    triangle([(x, y + 8 * s), (x + 20 * s, y + 2 * s),
              (x + 22 * s, y + 10 * s)], color)       # wing up
    rect(x + 4 * s, y + 8 * s, 26 * s, 6 * s, color)  # body
    circle(x + 32 * s, y + 7 * s, 4 * s, color)       # head
    triangle([(x + 36 * s, y + 6 * s), (x + 42 * s, y + 7 * s),
              (x + 36 * s, y + 9 * s)], color)        # beak
    line(x + 38 * s, y + 9 * s, x + 48 * s, y + 14 * s, (40, 140, 60), 2)
    circle(x + 48 * s, y + 15 * s, 2 * s, (40, 140, 60))


def draw_globe(x, y, r, color=BLUE):
    ring(x, y, r, color, 5)
    hline(x - r, y, 2 * r, color, 3)
    vline(x, y - r, 2 * r, color, 3)
    # orbit ring
    for a in range(0, 360, 4):
        import math
        ox = int(x + r * 1.35 * math.cos(math.radians(a)))
        oy = int(y + r * 0.45 * math.sin(math.radians(a)))
        set_px(ox, oy, GOLD)
        set_px(ox + 1, oy, GOLD)
        set_px(ox, oy + 1, GOLD)


def draw_chart(x, y, w, h, color=(40, 140, 60)):
    rect(x, y, w, h, LIGHT)
    hline(x, y + h - 4, w, BLACK, 2)
    vline(x + 4, y, h, BLACK, 2)
    pts = [(x + 8, y + h - 18), (x + w // 3, y + h - 30),
           (x + 2 * w // 3, y + h - 44), (x + w - 10, y + 12)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        line(ax, ay, bx, by, color, 4)
    for (px_, py_) in pts:
        circle(px_, py_, 4, color)
    triangle([(x + w - 16, y + 6), (x + w - 4, y + 6),
              (x + w - 10, y + 16)], color)


def draw_chip(x, y, s, color=BLACK):
    rect(x, y, 30 * s, 30 * s, color)
    rect(x + 6 * s, y + 6 * s, 18 * s, 18 * s, WHITE)
    rect(x + 11 * s, y + 11 * s, 8 * s, 8 * s, RED)
    for i in range(4):
        hline(x + 4 * s + i * 7 * s, y - 5 * s, 3 * s, color, 4 * s)
        hline(x + 4 * s + i * 7 * s, y + 31 * s, 3 * s, color, 4 * s)
        vline(x - 5 * s, y + 4 * s + i * 7 * s, 3 * s, color, 4 * s)
        vline(x + 31 * s, y + 4 * s + i * 7 * s, 3 * s, color, 4 * s)


def draw_flame(x, y, s, color=RED):
    triangle([(x, y + 26 * s), (x + 12 * s, y),
              (x + 16 * s, y + 12 * s)], color)
    triangle([(x + 8 * s, y + 26 * s), (x + 20 * s, y + 6 * s),
              (x + 26 * s, y + 26 * s)], color)
    triangle([(x + 14 * s, y + 26 * s), (x + 24 * s, y + 10 * s),
              (x + 30 * s, y + 26 * s)], color)
    rect(x, y + 26 * s, 30 * s, 3 * s, BLACK)


# ------------------------------------------------------------- lead story
LY = 158
draw_text(M, LY, "LEAD STORY", 2, RED)
draw_text(M, LY + 22, "RUSSIAN JETS ENTER", 3, BLACK)
draw_text(M, LY + 48, "S. KOREA AIR ZONE", 3, BLACK)
draw_wrapped(M, LY + 84,
             "SEOUL SCRAMBLES FIGHTERS AFTER RUSSIAN MILITARY AIRCRAFT ENTER ITS AIR "
             "DEFENCE ZONE NEAR ULLEUNG ISLAND. NO AIRSPACE VIOLATION, AND THE ISLAND "
             "ALERT IS LIFTED WITHIN MINUTES.",
             600, 2, BLACK)
draw_text(M, LY + 176, "SOURCE: AP / YONHAP", 2, DARKGREY)
# Lead illustration: jets over sea
draw_jet(700, LY + 30, 2)
draw_jet(730, LY + 95, 1)
hline(660, LY + 165, 300, BLUE, 3)
hline(660, LY + 178, 300, BLUE, 2)
hline(M, 372, W - 2 * M, BLACK, 2)

# ------------------------------------------------------------ story grid
# Two columns, two rows. Each cell: kicker, headline (scale 3, wrapped),
# body (scale 2, wrapped), small illustration on the right of the kicker.
CELL_W = (W - 2 * M - 24) // 2
CELL_H = 236
GRID_Y = 388


def story_cell(x, y, num, kicker, headline, body, source, art):
    rect(x, y, CELL_W, CELL_H, WHITE)
    hline(x, y, CELL_W, BLACK, 2)
    draw_text(x, y + 12, num + "  " + kicker, 2, RED)
    hy = draw_wrapped(x, y + 38, headline, CELL_W, 3, BLACK)
    by = draw_wrapped(x, hy + 6, body, CELL_W - 110, 2, BLACK)
    draw_text(x, y + CELL_H - 26, "SOURCE: " + source, 2, DARKGREY)
    art(x + CELL_W - 100, y + CELL_H - 110)


story_cell(M, GRID_Y, "2", "UKRAINE",
           "ZELENSKY SEEKS FOUR-WAY PEACE TALKS",
           "KYIV IS READY TO MEET MOSCOW, WASHINGTON AND EUROPE AS SOON AS POSSIBLE, "
           "SAYING IT COULD SIT DOWN AS EARLY AS TUESDAY.",
           "FRANCE 24",
           lambda ax, ay: draw_dove(ax, ay, 2))

story_cell(M + CELL_W + 24, GRID_Y, "3", "UNITED NATIONS",
           "UN CHIEF: AGREE AI SAFETY RULES IN A YEAR",
           "GUTERRES URGES NATIONS TO BUILD A GLOBAL FRAMEWORK FOR AI RISK, WITH "
           "INDEPENDENT OVERSIGHT, WITHIN TWELVE MONTHS.",
           "UNITED NATIONS",
           lambda ax, ay: draw_globe(ax + 45, ay + 45, 34))

story_cell(M, GRID_Y + CELL_H + 16, "4", "MARKETS",
           "ASIAN MARKETS SOAR AS NVIDIA CHIEF RETURNS",
           "NIKKEI JUMPS 5%, SEOUL 7.4% AND TAIWAN 9% AFTER NVIDIA REINSTATES JENSEN "
           "HUANG AS CHIEF EXECUTIVE.",
           "REUTERS",
           lambda ax, ay: draw_chart(ax - 10, ay - 10, 110, 80))

story_cell(M + CELL_W + 24, GRID_Y + CELL_H + 16, "5", "TECH / TRADE",
           "US BLACKLISTS MEGASPEED IN CHIP SCANDAL",
           "WASHINGTON BARS THE SINGAPORE FIRM AT THE CENTRE OF THE NVIDIA SPY ROW "
           "FROM BUYING US AI CHIPS WITHOUT A LICENCE.",
           "AL JAZEERA",
           lambda ax, ay: draw_chip(ax + 8, ay, 2))

# ------------------------------------------------------------ bottom strip
BY = GRID_Y + 2 * CELL_H + 32
hline(M, BY, W - 2 * M, BLACK, 2)
draw_text(M, BY + 12, "6  INDONESIA", 2, RED)
draw_text(M + 170, BY + 12, "24 DEAD IN FACTORY FIRE", 3, BLACK)
draw_wrapped(M, BY + 48,
             "OFFICIALS CONFIRM 24 WORKERS KILLED AND ABOUT 30 MISSING AFTER A BLAZE "
             "GUTS A CANDY FACTORY IN BANTEN. SOURCE: REUTERS",
             760, 2, BLACK)
draw_flame(880, BY + 18, 2)
hline(M, 1000, W - 2 * M, BLACK, 3)
draw_text_centered(W // 2, 1006, "THE WORLD TODAY - TUESDAY, 24 NOVEMBER 2026",
                   1, DARKGREY)

# ---------------------------------------------------------------- PNG out
raw = b"".join(b"\x00" + bytes(px[y * W * 3:(y + 1) * W * 3])
               for y in range(H))


def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)


png = (b"\x89PNG\r\n\x1a\n"
       + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
       + chunk(b"IDAT", zlib.compress(raw, 9))
       + chunk(b"IEND", b""))

with open("entry.png", "wb") as f:
    f.write(png)
print("wrote entry.png", len(png), "bytes,", W, "x", H)
