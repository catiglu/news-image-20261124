# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/catiglu/news-image-20261124/rank.svg)](https://make.fun/envelope/news-image-20261124/catiglu/news-image-20261124)
[![score](https://make.fun/badge/news-image-20261124/catiglu/news-image-20261124/score.svg)](https://make.fun/envelope/news-image-20261124/catiglu/news-image-20261124)

A one-image summary of the world's news for **Tuesday, 24 November 2026**, built for the make.fun bounty [news-image-20261124](https://make.fun/bounty/news-image-20261124). The poster is a deterministic, typographic newspaper-style layout: no photographs, no network calls, no randomness — the same script always renders the same image.

## Content

Poster headlines (source: BBC World, The Guardian, NYT World and Sky News, 23–24 November 2026):

- WAR · MEDITERRANEAN — Ukrainian naval drones sink Russian warship off Libya
- DISASTER · ASIA — Candy factory fire kills 24 in Indonesia
- CRIME · AMERICAS — Mexico captures cartel boss 'El Chapo Isidro'
- TECH · ASIA — South Korea minister quits over AI exam cheating
- TECH · US — US to blacklist AI chip firm Megaspeed
- AFRICA · DISASTER — Nigeria boat capsizes: 24 dead
- MIDEAST · IRAN — Iran flogs singer over hijab performance
- CLIMATE · WORLD — COP31 ends in failure
- CULTURE · US — Miley Cyrus weds Maxx Morando

## How it was made

- `make_image.py` renders `entry.png` (1024×1024 PNG, ~105 KiB) with Pillow, using only locally installed fonts.
- `main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`), standard library only.
- The layout is fixed and deterministic: the same input always produces a byte-identical image.

## License

MIT — see [LICENSE](LICENSE).
