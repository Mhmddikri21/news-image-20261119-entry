# Thursday 19 November 2026 — one day of world news, one picture

A 1024×1024 broadsheet that sums up Thursday 19 November 2026 in
55 stories: the first-ever Trump–Xi–Putin three-way summit in
Shenzhen, the International Court of Justice ruling that Myanmar
committed genocide against the Rohingya, the third Kerch Bridge
strike in a week, a Houthi missile hitting Riyadh's PIF Tower,
GTA VI going on sale after 13 years, the Dow plunging 1,101 points,
Anthropic's record IPO, the COP31 draft dropping fossil fuels, and
47 more — with a UTC timeline, a numbers strip, a world map, and a
DATE CHECK box for stories that broke before the day.

## Files

- `entry.png` — the image (195,543 bytes, 1024×1024).
- `main.py` — the program. Standard library only: it validates
  `entry.png` as a whole, well-formed PNG (signature, chunk CRCs,
  1024×1024 IHDR, IEND present, under 1 MiB) and copies the exact
  bytes to `/output/entry.png`. No network, no drawing, no
  randomness — run it twice and the output is byte-identical.

## The image

Built with PIL from reporting verified against Reuters, AP, AFP,
the UN/ICJ, the IMD, the ABS and the Federal Reserve on 19 November
2026. Every story happened or was first reported on Thursday
19 November 2026; anything that broke earlier (Kerch's first two
strikes, the Qeshm strikes, Gaza's floods, the Kahana election,
Voyager 1, GPT-6.2, the Jeffries nomination, the Yongbyon
expansion, the dirty-bomb remark) is listed in the DATE CHECK box,
not presented as the day's news. The nine NBA scores are the games
that finished in the early hours of 19 November UTC and were
reported that day.

## Run

```
python3 main.py
# wrote /output/entry.png 195543 bytes sha256=... chunks=...
```
