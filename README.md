<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<!-- Short, focused README for Tickrly -->

# Tickrly

A compact macOS stock-and-news ticker built with Tkinter.

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

## Contributing

- Add tests for non-UI logic (e.g. `is_market_open`) and CI to run lint/tests and produce builds.

---

If you'd like, I can add a `CONTRIBUTING.md`, an MIT `LICENSE`, and a basic GitHub Actions workflow to build macOS artifacts.

   const API_KEY = 'ENTER YOUR API';
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin Brooks99/TickerApp
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/Brooks99/TickerApp/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/Brooks99/TickerApp/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Brooks99/TickerApp" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the project_license. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact
Project Link: [https://github.com/Brooks99/TickerApp](https://github.com/Brooks99/TickerApp)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
### Tickrly

Tickrly is a lightweight desktop stock-and-news ticker for macOS. It displays a scrolling feed of stock symbols and short news headlines in a compact window. The app is implemented with Tkinter and uses `yfinance` for stock data and `feedparser` for news.

## Key features

- Scrolling stock ticker and news ticker
- Simple in-app Config Editor (add / remove symbols)
- Per-user config stored at `~/Library/Application Support/Tickrly/config.json`
- About and License viewers in the Config Editor
- Packaging support using PyInstaller + dmgbuild

## Quick start (development)

Requirements

- macOS
- Python 3.10+ (development used 3.12)

Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run locally

```bash
.venv/bin/python ticker.py
```

Open the app and click the main window to open the Config Editor. Add or remove symbols and click Save to persist changes.

## Config file behavior

- On first run, the app copies the bundled `config.json` (if present) into `~/Library/Application Support/Tickrly/config.json` and uses that user-local file thereafter.
- All reads/writes happen against the user config to ensure the file is writable and persists across updates.

## Packaging for macOS

We use PyInstaller to build the `.app` bundle and `dmgbuild` to create a DMG installer. Example commands (run from project root with the virtualenv active):

```bash
.venv/bin/python -m PyInstaller --clean --noconfirm Tickrly.spec
.venv/bin/python -m dmgbuild -s dmgbuild_settings.py "Tickrly" "dist/Tickrly.dmg"
```

Notes:

- To include a custom icon, place an `.icns` file in the project and reference it in the `BUNDLE(..., icon='path/to/icon.icns')` call inside `Tickrly.spec`.
- For public distribution, you must code sign the `.app` and notarize the DMG using an Apple Developer account.

## About & License

- The Config Editor contains an About dialog (Version, link) and a License viewer that will display a `LICENSE` file from the repo root if present.
- Add a `LICENSE` file (MIT/Apache/etc.) to enable the in-app license viewer.

## Logging and diagnostics

- The app uses Python's `logging` module. By default logs are INFO-level to stdout. For production, configure a rotating file handler and/or make the log level configurable via environment variable.

## Tests and CI suggestions

- Add unit tests (pytest) for non-UI logic, e.g. config handling and `is_market_open`.
- Use GitHub Actions (macOS runner) to run linting, tests, and produce build artifacts.

## Troubleshooting

- If a packaged app fails to start, run the binary under `dist/Tickrly.app/Contents/MacOS/` in a Terminal to see stderr output.
- If news or feeds fail, check network connectivity and feed URLs. The app attempts a fallback feed when the primary feed fails.

## Production checklist (short)

1. Pin dependencies in `requirements.txt` and test on a clean macOS runner.
2. Add automated linting and testing in CI (GitHub Actions).
3. Code sign the `.app` and notarize the DMG.
4. Provide a proper `.icns` app icon and set it in the PyInstaller spec.
5. Consider a `onedir` PyInstaller mode for macOS bundles.

## Contributing

Contributions welcome. Open issues or PRs and include tests for logic changes.

---

If you'd like, I can also add a `CONTRIBUTING.md`, a sample `LICENSE` (MIT) and a GitHub Actions workflow to build macOS artifacts.
