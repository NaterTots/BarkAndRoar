# BarkAndRoar status

## Milestones
1. Platform and interaction: complete for desktop/emulated validation; early build deployed and browser-tested. Physical iPad acceptance pending.
2. Toddler experience: implemented and Chromium behavior checks pass; human listening and physical-device acceptance pending.
3. Deployment and handoff: complete. GitHub Actions deployment, live-browser validation, asset fetches, README, credits, screenshots and parent checklist delivered. Only physical-device and listening acceptance remain open.

## Implemented / tested
Original native vector faces, two CC0-derived bundled clips, explicit independent pointer ownership, bounded relative dragging, two reusable Stream players, play/resume gate, responsive web shell.

Passed headless import, release Web export, and pointer ownership/cancellation tests. Chromium 153.0.8010.12 on Windows, automated with Playwright 1.63.0: fresh-load gate followed by each animal's first tap produced exactly one activation and nonzero measured audio output; two simultaneous touches/audio streams; extra fingers; clamped cross-divider drag; release and cancellation; rapid tapping with no audio queue; rotation while dragging; simulated focus/visibility loss and resume. All eight panel corner hit targets passed. Injected JavaScript and WASM download failures both displayed readable parent errors. Final full suite passed on the live deployment, with no application errors or missing runtime assets during normal play.

Inspected landscape and portrait screenshots plus simultaneous open-mouth reactions. Fixed initial fixed-aspect letterboxing by expanding the viewport; final portrait correctly stacks the animals. Screenshots captured at 1024×768, 768×1024, 1180×820 and 820×1180 with no page scrolling. Representative images are committed under [docs/screenshots](docs/screenshots).

Desktop WebKit 26.6 was attempted. This Windows automation build exposes neither AudioContext nor webkitAudioContext, so audio validation is unavailable; the earlier run also emitted framebuffer validation errors. It is not counted as a Safari pass. Headless Chromium tab switching did not simulate visibility loss; focus/visibility lifecycle checks are explicitly synthetic. Actual Safari background/lock behavior remains pending. No human listening or physical-device test claimed.

## Versions and deployment
Godot editor/templates: 4.7.2.stable (official ed1daf0bf). Compatibility renderer; no threads/extensions/PWA. Explicit Stream playback. Issue godotengine/godot#116750 remains open as checked 2026-09-25; Stream is a mitigation, not proof of iOS stability.

Authenticated account: NaterTots; public repository https://github.com/NaterTots/BarkAndRoar.

Live URL: https://natertots.github.io/BarkAndRoar/ — deployed and browser-verified.
Validated game-source commit: `5fb8ee7a8d68103881f459c3cc4b6d602ef15de6` (2026-09-25).
Successful build/deploy workflow: https://github.com/NaterTots/BarkAndRoar/actions/runs/36166001357.
The subsequent handoff commit adds only documentation, screenshots and test records; game source is unchanged.
The exact current deployed commit/run is published automatically at https://natertots.github.io/BarkAndRoar/build-info.json.

Evidence: [final live Chromium results](docs/verification/live-chromium.json), [HTTP status, MIME types and content hashes](docs/verification/live-assets.json), [Windows WebKit limitation](docs/verification/windows-webkit-unavailable.json). HTML, JS, WASM, PCK and both audio worklet files returned 200 at the project subdirectory; WASM was served as `application/wasm`. A real browser executed the deployed game in addition to these HTTP checks.
Local Godot editor and template SHA512 hashes verified against the official release manifest. CI independently verifies its downloads.

## Dependencies and next action
The agent has no access to the physical iPad or human listening feedback. Parent supplied target: **iPad (A16), iPadOS 26.5**. No physical-device result has been received. Numerical audio checks passed, but recognizability, friendliness and perceived balance have not been confirmed by listening.

1. On that iPad, open Safari at **https://natertots.github.io/BarkAndRoar/**, set a low audible volume, and tap the play triangle.
2. Tap each animal and both together; confirm correct sound on each first tap, pleasant volume and no distortion.
3. Follow [the exact parent checklist](docs/PARENT_TEST.md), including two fingers, dragging, rotation, Safari toolbar changes, app switching and screen lock/resume, then **15–30 minutes** of repeated interaction.
4. Reply with the test date, iPadOS version, minutes tested, sound-quality result and any failed step. Include the commit from `build-info.json` if it differs from the validated commit above.

No credentials, software installation or repository settings action is required. iPad compatibility and milestone 2's listening acceptance are **pending**, not claimed complete.
