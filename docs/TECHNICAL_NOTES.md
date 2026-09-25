# Technical notes

## Versions and references

- Godot editor and templates: **4.7.2.stable.official.ed1daf0bf**, standard GDScript.
- Compatibility renderer; no threads, C#, GDExtensions or PWA.
- [Godot Web documentation](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html), reviewed 2026-09-25.
- [GitHub Pages custom workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), reviewed 2026-09-25.
- Actions releases verified from their official release APIs on that date: checkout 7.0.1, configure-pages 6.0.0, upload-pages-artifact 5.0.0, deploy-pages 5.0.1.

## Audio and Safari

[Godot issue #116750](https://github.com/godotengine/godot/issues/116750) was open
when checked 2026-09-25. Its report concerns 4.5.1 Sample playback on iOS and reports
Stream avoiding a repeated-playback crash. This project selects Stream explicitly
on each of two preallocated AudioStreamPlayers, as well as in project settings.
This may add latency on the single-threaded export. No universal reliability or
latency claim is made for 4.7.2; physical iPad testing remains necessary.

Godot's web input handler resumes its audio context on a real canvas input gesture.
The initial play triangle consumes the first gesture and does not play a sound;
the following animal tap requests its clip. No async wrapper precedes that gesture.
On focus loss, page hiding or touch cancellation, the web bridge clears ownership,
stops both players and returns to the same play gate. The next real gesture can
resume the audio context. No clips queue: taps animate while an active clip finishes.

Clips are filtered and faded mono PCM, 0.42 seconds (bark) and 1.20 seconds (roar).
Gentle compression and conservative levels leave headroom. Automated
audio-context/PCM checks are separate from human listening and speaker output.

After an initial physical-iPad test confirmed taps/audio but described the bark as
wooden and the roar as insufficiently defined, the bark was replaced with a clean
isolated recording. The roar edit now preserves its whole onset and release,
time-compressed without changing pitch. Lighter filtering and no waveshaping
preserve vocal character. `tools/audio-requirements.txt` pins the optional audio
processing tools; they are not needed to build or run the committed game assets.

## Input and layout

`pointers.gd` owns capture; `main.gd` maps panels and coordinates; `animal.gd`
handles reaction and its one player. Touch and mouse share down/move/up functions.
Both touch/mouse emulation settings are disabled and emulated mouse events are
also filtered. Extra pointers cannot steal a face. Drag is relative to the original
press, starts after nine logical pixels, and is clamped to 10% of the smaller panel
dimension. Tilt is capped at eight degrees. No animation tweens are allocated.

Layout uses the expanded Godot viewport to stack in portrait and divide in landscape.
Resize clears ownership. The shell uses dynamic viewport height, safe-area padding,
canvas-scoped gesture suppression, and manual one-CSS-pixel canvas sizing. Engine
paths remain relative for project Pages hosting. Loading and initialization errors
are parent readable. No service worker is registered.

## Validation limitations

Chromium 153.0.8010.12 / Playwright 1.63.0 on Windows passed the recorded desktop
and emulated-touch checks. Audio analysis observes nonzero samples on the actual
engine output graph; it does not establish perceived sound quality or physical
speaker output. The test probe exists only in the automation script.

Playwright's Windows WebKit 26.6 build exposed no AudioContext or
webkitAudioContext, and an exploratory game run emitted framebuffer errors.
It cannot provide audio acceptance here and is not recorded as a Safari pass.
The final shell displays a readable unsupported-Web-Audio message for that build.
Headless Chromium pages do not reproduce actual tab visibility transitions in
this environment; lifecycle tests dispatch synthetic focus/visibility events.
Actual Safari toolbar changes, backgrounding, screen lock, and sustained playback
must be checked on the target iPad.
