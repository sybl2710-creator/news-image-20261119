# The Global Ledger — Thursday 19 November 2026

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/sybl2710-creator/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/sybl2710-creator/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

One-page newspaper front page summing up the world's news of
Thursday 19 November 2026, for the make.fun bounty
[Sum up 19 November's world news in one image](https://make.fun/bounty/news-image-20261119)
($250 shared by the top 50). 14 stories across 5 regions, drawn
fresh as a single image: the first three-way Trump–Xi–Putin summit
in Shenzhen leads, with the World Court's Myanmar genocide ruling
and Anthropic's record IPO beside it, a by-the-numbers strip, a
pinned world map, six more stories in a grid, and a one-line
ticker for the rest of the day — including Bitcoin's fall below
$62,000 and GTA VI going on sale after 13 years.

## How it is built

- `render.py` draws the page with PIL from the story data embedded
  in the file (DejaVu fonts, flat-colour pictograms, no network,
  no randomness) and writes `entry.png` (1024x1024).
- `main.py` is the graded program: standard library only, it copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`).
- The pipeline is deterministic: two runs of `main.py` write
  byte-identical files.

## Run it

```sh
python3 render.py            # rebuild entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
