# Asset credits

All assets are bundled; the running toy makes no requests to asset providers.

| Asset | Author and source | License | Modifications |
| --- | --- | --- | --- |
| `assets/audio/bark.wav` | kwahmah_02, [Single Dog Bark](https://freesound.org/people/kwahmah_02/sounds/277058/); [HQ preview source](https://cdn.freesound.org/previews/277/277058_4486188-hq.mp3) | CC0 1.0, verified on the source page 2026-09-25. Attribution not required. | Complete isolated bark, 0.90× tempo with pitch preserved, mono, light 65–7500 Hz filtering, gentle compression, short fades, level adjustment, 32 kHz PCM. |
| `assets/audio/roar.wav` | Podcapocalipsis, [LION ROAR](https://freesound.org/people/Podcapocalipsis/sounds/559600/); [HQ preview source](https://cdn.freesound.org/previews/559/559600_11490791-hq.mp3) | CC0 1.0, verified on the source page 2026-09-25. Attribution not required. | 0.18–1.82 s excerpt preserving the full onset and release, 1.38× tempo with pitch preserved, mono, light 65–7500 Hz filtering, gentle compression, fades, level adjustment, 32 kHz PCM. |
| Animal art and play icon | Original BarkAndRoar artwork in `scripts/animal.gd` and `scripts/main.gd` | Project MIT license | Native layered vector shapes; no external artwork, fonts or emoji. |

[CC0 legal terms](https://creativecommons.org/publicdomain/zero/1.0/legalcode).
The sound-processing recipe is in `tools/prepare_audio.py`. The two clips peak at
no more than 0.44 before the player's additional -3 dB gain; even simultaneous
full-scale peaks leave mixing headroom. Perceived friendliness and balance still
need a human listening check; numerical measurements cannot establish those.

The early build used Brandon Morris (HaelDB)'s CC0
[Dog barking mono](https://opengameart.org/content/dog-barking-mono). It was replaced
after the parent reported a wooden-sounding bark. Earlier commits retain that
asset and its credit; the current export uses the isolated kwahmah_02 recording.

Godot Engine is MIT licensed; its export includes third-party components. See
[Godot copyright and third-party notices](https://github.com/godotengine/godot/blob/4.7.2-stable/COPYRIGHT.txt)
and [Godot license](https://godotengine.org/license/). Copies are committed under
`licenses/` and included in the exported resource pack.
