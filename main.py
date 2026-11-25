#!/usr/bin/env python3
"""The World in One Day - 25 November 2026.

Draws a 1024x1024 PNG poster summarising six top world news stories of
25 November 2026. Python standard library only, no network, no file reads,
fully deterministic: two runs produce byte-identical output.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png)
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font 5x7 --
# Each glyph is 7 rows of 5 bits, most significant bit = leftmost pixel.
FONT = {
    "A": (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    ".": (0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C),
    ",": (0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08),
    "'": (0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00),
    ":": (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00),
    ";": (0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x04, 0x08),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04),
    "-": (0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "/": (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    "%": (0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13),
    "+": (0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "$": (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
    "#": (0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A),
    "@": (0x0E, 0x11, 0x17, 0x15, 0x16, 0x10, 0x0E),
    '"': (0x0A, 0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00),
    "=": (0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00),
    "_": (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F),
    "*": (0x00, 0x04, 0x15, 0x0E, 0x15, 0x04, 0x00),
    "<": (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    ">": (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    "|": (0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
}

# --------------------------------------------------------------- stories ---
# Six top world stories of Wednesday 25 November 2026, verified from
# live news reporting (BBC / The Guardian via One Turn; Daily Summary).
STORIES = [
    {
        "tag": "TECH",
        "color": (86, 205, 255),
        "headline": "NVIDIA SLIDES 7%",
        "summary": "Shares fell as lawmakers questioned Trump's role in bringing back CEO Jensen Huang.",
    },
    {
        "tag": "CONFLICT",
        "color": (255, 107, 91),
        "headline": "MINES HIT TANKERS IN HORMUZ",
        "summary": "Iran's Revolutionary Guards said two tankers struck mines in the Strait of Hormuz.",
    },
    {
        "tag": "RESCUE",
        "color": (96, 220, 140),
        "headline": "CARTAGENA HOSTAGES FREED",
        "summary": "Colombian forces stormed a supermarket and rescued all hostages, killing one captor.",
    },
    {
        "tag": "SPACE",
        "color": (196, 141, 255),
        "headline": "CHINA FLIES FIRST FOREIGN ASTRONAUT",
        "summary": "Pakistan's first astronaut reached China's Tiangong space station in orbit.",
    },
    {
        "tag": "ECONOMY",
        "color": (255, 214, 64),
        "headline": "BANGLADESH RAISES GARMENT PAY 36%",
        "summary": "Minimum wage rose to 17,000 taka after weeks of protests by garment workers.",
    },
    {
        "tag": "POLITICS",
        "color": (120, 170, 255),
        "headline": "DEMOCRATS WIN HOUSE MAJORITY",
        "summary": "Democrats clinched at least 259 House seats, their largest majority since 1990.",
    },
]

BG = (16, 30, 51)
CARD = (26, 44, 71)
BORDER = (52, 84, 122)
WHITE = (255, 255, 255)
GOLD = (255, 197, 66)
MUTED = (168, 184, 205)
SUMMARY = (214, 226, 240)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            if yy < 0 or yy >= self.h:
                continue
            base = (yy * self.w + x) * 3
            for xx in range(max(x, 0), min(x + w, self.w)):
                i = base + (xx - x) * 3 if x >= 0 else (yy * self.w + xx) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect_border(self, x, y, w, h, color, t=2):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)


def text_width(text, scale):
    return len(text) * 6 * scale


def draw_text(cv, x, y, text, scale, color):
    """Draw uppercased text with the 5x7 bitmap font."""
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch)
        if glyph is None:
            cx += 6 * scale
            continue
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits & (1 << (4 - col)):
                    for dy in range(scale):
                        for dx in range(scale):
                            cv.set(cx + col * scale + dx, y + row * scale + dy, color)
        cx += 6 * scale


def draw_text_centered(cv, y, text, scale, color, x0=0, x1=W):
    w = text_width(text, scale)
    draw_text(cv, x0 + (x1 - x0 - w) // 2, y, text, scale, color)


def wrap(text, max_chars):
    words = text.split(" ")
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def render():
    cv = Canvas(W, H, BG)

    # Header
    draw_text_centered(cv, 40, "THE WORLD IN ONE DAY", 5, WHITE)
    draw_text_centered(cv, 96, "WEDNESDAY, 25 NOVEMBER 2026", 2, GOLD)
    cv.fill_rect(32, 140, W - 64, 4, GOLD)

    # Story grid: 2 columns x 3 rows
    left, top, gap = 32, 168, 20
    col_w, row_h = 460, 250
    for idx, st in enumerate(STORIES):
        col = idx % 2
        row = idx // 2
        x = left + col * (col_w + gap)
        y = top + row * (row_h + gap)
        cv.fill_rect(x, y, col_w, row_h, CARD)
        cv.rect_border(x, y, col_w, row_h, BORDER, 2)

        # Number badge + tag
        cv.disc(x + 28, y + 30, 16, GOLD)
        num = str(idx + 1)
        draw_text(cv, x + 28 - text_width(num, 2) // 2, y + 23, num, 2, (16, 30, 51))
        draw_text(cv, x + 56, y + 23, st["tag"], 2, st["color"])

        # Headline, scale 3, wrapped to 22 chars per line
        hy = y + 64
        for i, line in enumerate(wrap(st["headline"], 22)):
            draw_text(cv, x + 24, hy + i * 26, line, 3, WHITE)

        # Summary, scale 2, wrapped to 34 chars per line
        sy = hy + len(wrap(st["headline"], 22)) * 26 + 12
        for i, line in enumerate(wrap(st["summary"], 34)):
            draw_text(cv, x + 24, sy + i * 18, line, 2, SUMMARY)

    # Footer
    cv.fill_rect(32, 962, W - 64, 2, BORDER)
    draw_text_centered(cv, 978, "6 STORIES FROM AROUND THE WORLD  |  25 NOVEMBER 2026", 2, MUTED)
    return cv


# -------------------------------------------------------------- PNG write --
def png_chunk(typ, data):
    return (
        struct.pack(">I", len(data))
        + typ
        + data
        + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    )


def write_png(cv, path):
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    row_len = W * 3
    for yy in range(H):
        raw.append(0)
        raw += cv.px[yy * row_len:(yy + 1) * row_len]
    png = (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + png_chunk(b"IEND", b"")
    )
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = render()
    path = os.path.join(out_dir, "entry.png")
    size = write_png(cv, path)
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()
