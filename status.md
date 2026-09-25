# BarkAndRoar status

## Milestones
1. Platform and interaction: complete for desktop/emulated validation; early build deployed and browser-tested. Physical iPad acceptance pending.
2. Toddler experience: implemented and Chromium behavior checks pass; human listening and physical-device acceptance pending.
3. Deployment and handoff: first Pages deployment passed and live browser checks passed; final loading-error improvements and validation records being finalized.

## Implemented / tested
Original native vector faces, two CC0-derived bundled clips, explicit independent pointer ownership, bounded relative dragging, two reusable Stream players, play/resume gate, responsive web shell.

Passed headless import, release Web export, and pointer ownership/cancellation tests. Chromium 153.0.8010.12 on Windows, automated with Playwright 1.63.0: fresh-load gate followed by each animal's first tap produced exactly one activation and nonzero measured audio output; two simultaneous touches/audio streams; extra fingers; clamped cross-divider drag; release and cancellation; rapid tapping with no audio queue; rotation while dragging; simulated focus loss and resume. Local and live checks passed. All eight panel corner hit targets also passed locally.

Inspected landscape and portrait screenshots. Fixed initial fixed-aspect letterboxing by expanding the viewport; final portrait correctly stacks the animals. Screenshots captured at 1024×768, 768×1024, 1180×820 and 820×1180 with no page scrolling.

Desktop WebKit 26.6 was attempted. This Windows automation build exposes neither AudioContext nor webkitAudioContext, so audio validation is unavailable; the earlier run also emitted framebuffer validation errors. It is not counted as a Safari pass. Headless Chromium tab switching did not simulate visibility loss; focus/visibility lifecycle checks are explicitly synthetic. Actual Safari background/lock behavior remains pending. No human listening or physical-device test claimed.

## Versions and deployment
Godot editor/templates: 4.7.2.stable (official ed1daf0bf). Compatibility renderer; no threads/extensions/PWA. Explicit Stream playback. Issue godotengine/godot#116750 remains open as checked 2026-09-25; Stream is a mitigation, not proof of iOS stability.

Authenticated account: NaterTots; public repository https://github.com/NaterTots/BarkAndRoar.

Live URL: https://natertots.github.io/BarkAndRoar/ — deployed and browser-verified.
First deployed/tested commit: `1e8672cf086bd11b5c28c41951bc83c8e04fbae4`.
Successful workflow: https://github.com/NaterTots/BarkAndRoar/actions/runs/36165090314.
Local Godot editor and template SHA512 hashes verified against the official release manifest. CI independently verifies its downloads.

## Dependencies and next action
Finish final loading-error validation and publish verification records. Parent supplied physical target: iPad (A16), iPadOS 26.5. Physical touch/audio, listening quality, Safari toolbar and lock/resume checks plus a 15–30 minute stability session remain pending on that device. Exact steps: [docs/PARENT_TEST.md](docs/PARENT_TEST.md). No credentials or repository settings action is required.
