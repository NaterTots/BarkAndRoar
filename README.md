# BarkAndRoar

[Open the toy](https://natertots.github.io/BarkAndRoar/) · [Build status](https://github.com/NaterTots/BarkAndRoar/actions/workflows/pages.yml)

Two friendly animals, two enormous touch targets. Tap the play triangle, then tap
either panel to hear its animal. Drag a face and let go to send it home. Two fingers
can play together. Turn the iPad upright to stack the animals.

No accounts, ads, analytics, music, backend, external asset requests or installation.
Internet is needed to load the game; no offline/PWA caching is installed.

## Open on an iPad

Open **https://natertots.github.io/BarkAndRoar/** in Safari. Set a comfortable device
volume, wait for the play triangle, then tap it. Tap each animal. If you return from
another app or screen lock, tap the triangle again before playing. Normal browser
mode works; fullscreen is unnecessary. Modern WebGL 2 and WebAssembly support are
required. Physical-device acceptance is tracked in [status.md](status.md), with
the exact remaining checks in [the parent checklist](docs/PARENT_TEST.md).

## Run and build

Use **Godot 4.7.2 stable**, standard GDScript editor, and **4.7.2 stable export
templates**, from the [official release](https://github.com/godotengine/godot/releases/tag/4.7.2-stable).
Open `project.godot` and press F6 with `scenes/main.tscn` open, or F5 to run the project.
Install matching export templates through Editor → Manage Export Templates.

From the repository directory, with `godot` and Python on PATH:

```sh
godot --headless --path . --editor --import
godot --headless --path . --script tests/pointers_test.gd
mkdir -p build/web
godot --headless --path . --export-release Web build/web/index.html
python -m http.server 8765 --bind 127.0.0.1 --directory build/web
```

On PowerShell use `New-Item -ItemType Directory -Force build/web` for the directory
step and `& 'C:\path\to\Godot_v4.7.2-stable_win64_console.exe'` in place of `godot`.
Open `http://127.0.0.1:8765/`; `file://` does not work.

The renderer is Compatibility, the Web export is single-threaded, and both audio
players explicitly use Stream. The web canvas renders at one pixel per CSS pixel
to limit GPU work. All assets are packaged in the PCK. Native drawing supplies the
layered artwork; there are no SVG import dependencies.

## Verify

Pointer ownership tests run in CI. For local Chromium browser checks:

```sh
python -m venv .venv
# Activate your virtual environment, then:
python -m pip install -r tests/requirements.txt
python -m playwright install chromium webkit
python tests/browser_check.py http://127.0.0.1:8765/
```

The browser script uses `?qa=1` to expose in-memory diagnostics; it sends nothing
to a server. It saves screenshots and results under ignored `test-results/`.
Emulated touch and desktop WebKit do not establish physical Safari compatibility.

## Deploy changes

Commit and push to `main`. [Deploy BarkAndRoar](https://github.com/NaterTots/BarkAndRoar/actions/workflows/pages.yml)
downloads the exact editor/templates, checks SHA512 hashes against the release
manifest, imports, runs pointer tests, exports `index.html`, uploads the complete
Pages artifact, and deploys it. The repository uses the GitHub Actions Pages source.
The deployed `build-info.json` identifies the exact commit and workflow run.
The workflow also supports manual dispatch. Build output and local tools are ignored.

See [asset credits](ASSET_CREDITS.md) for audio sources and processing, and
[technical notes](docs/TECHNICAL_NOTES.md) for Safari considerations.
