# BarkAndRoar status

## Milestones
1. Platform and interaction: local single-threaded browser build runs; early deployment in progress. Physical iPad acceptance pending.
2. Toddler experience: implemented; browser interaction and layout validation in progress.
3. Deployment and handoff: GitHub Pages configured for Actions; first workflow being prepared.

## Implemented / tested
Original native vector faces, two CC0-derived bundled clips, explicit independent pointer ownership, bounded relative dragging, two reusable Stream players, play/resume gate, responsive web shell.

Passed headless import, release Web export, and pointer ownership/cancellation tests. Chromium fresh-load play then lion tap records one activation and active audio. Landscape screenshot inspected. Initial portrait screenshot exposed fixed-aspect letterboxing; responsive stretch correction is under validation. No human listening or physical-device test claimed.

## Versions and deployment
Godot editor/templates: 4.7.2.stable (official ed1daf0bf). Compatibility renderer; no threads/extensions/PWA. Explicit Stream playback. Issue godotengine/godot#116750 remains open as checked 2026-09-25; Stream is a mitigation, not proof of iOS stability.

Authenticated account: NaterTots; existing public repository https://github.com/NaterTots/BarkAndRoar. Pages URL reserved: https://natertots.github.io/BarkAndRoar/ (not yet deployed/verified).

## Dependencies and next action
Finish browser validation, push and verify Pages workflow/live build. Parent supplied physical target: iPad (A16), iPadOS 26.5. Physical touch/audio, listening quality, Safari toolbar and lock/resume checks plus a 15–30 minute stability session remain pending on that device.
