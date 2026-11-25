# The World in One Day — 25 November 2026

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/agielthree/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/agielthree/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

A single 1024x1024 poster summing up the world's top news of Wednesday,
25 November 2026 — six stories, six topics, one image.

## The six stories

1. **TECH — Nvidia slides 7%.** Shares fell as lawmakers questioned Trump's
   role in bringing back CEO Jensen Huang.
2. **CONFLICT — Mines hit tankers in Hormuz.** Iran's Revolutionary Guards
   said two tankers struck mines in the Strait of Hormuz.
3. **RESCUE — Cartagena hostages freed.** Colombian forces stormed a
   supermarket and rescued all hostages, killing one captor.
4. **SPACE — China flies first foreign astronaut.** Pakistan's first
   astronaut reached China's Tiangong space station in orbit.
5. **ECONOMY — Bangladesh raises garment pay 36%.** Minimum wage rose to
   17,000 taka after weeks of protests by garment workers.
6. **POLITICS — Democrats win House majority.** Democrats clinched at
   least 259 House seats, their largest majority since 1990.

## How it is made

`main.py` is pure Python 3 standard library — no dependencies, no network,
no file reads. It draws the poster with a hand-built 5x7 bitmap font and a
from-scratch PNG encoder (zlib + struct), and writes `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`). Output is deterministic: two
runs produce byte-identical PNGs.

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Entry for the [news-image-20261125](https://make.fun/bounty/news-image-20261125)
bounty on [make.fun](https://make.fun).
