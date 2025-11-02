<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<!-- Short, focused README for Tickrly -->

# Tickrly

A compact macOS stock-and-news ticker built with Tkinter. Tickrly is a lightweight desktop stock-and-news ticker for macOS. It displays a scrolling feed of stock symbols and short news headlines in a compact window. The app is implemented with Tkinter and uses `yfinance` for stock data and `feedparser` for news.

## Key features

- Scrolling stock ticker and news ticker
- Simple in-app Config Editor (add / remove symbols)
- Per-user config stored at `~/Library/Application Support/Tickrly/config.json`
- About and License viewers in the Config Editor
- Packaging support using PyInstaller + dmgbuild


## Summary

- Scrolling stock and news tickers
- Simple in-app Config Editor to add/remove symbols
- Per-user config at `~/Library/Application Support/Tickrly/config.json`

## Quick start (development)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
.venv/bin/python ticker.py
```

## Packaging (macOS)

- Build `.app` with PyInstaller (see `Tickrly.spec`) and create DMG with `dmgbuild`.

Example:

```bash
.venv/bin/python -m PyInstaller --clean --noconfirm Tickrly.spec
.venv/bin/python -m dmgbuild -s dmgbuild_settings.py "Tickrly" "dist/Tickrly.dmg"
```

- Code-sign and notarize the DMG for public distribution.

## Config & license

- On first run the app copies bundled `config.json` (if present) to `~/Library/Application Support/Tickrly/config.json` and uses that file thereafter.
- Add a `LICENSE` file to the repo root to enable the in-app license viewer.

## Troubleshooting

- Run the packaged binary from `dist/Tickrly.app/Contents/MacOS/` to see console output.

