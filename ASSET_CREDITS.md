# Asset credits

All assets are bundled; the running toy makes no requests to asset providers.

| Asset | Author and source | License | Modifications |
| --- | --- | --- | --- |
| `assets/audio/bark.wav` | Brandon Morris (HaelDB), [Dog barking mono](https://opengameart.org/content/dog-barking-mono); [source WAV](https://opengameart.org/sites/default/files/dog_barking_mono.wav) | CC0 1.0, chosen from the licenses offered on the source page; checked 2026-09-25. Attribution not required. | Short excerpt, mono, gentle band-pass filtering, fades, level adjustment, 32 kHz PCM. |
| `assets/audio/roar.wav` | Podcapocalipsis, [LION ROAR](https://freesound.org/people/Podcapocalipsis/sounds/559600/); [HQ preview source](https://cdn.freesound.org/previews/559/559600_11490791-hq.mp3) | CC0 1.0, verified on the source page 2026-09-25. Attribution not required. | Short excerpt of the author's filtered roar sound effect, mono, gentle band-pass filtering, fades, level adjustment, 32 kHz PCM. |
| Animal art and play icon | Original BarkAndRoar artwork in `scripts/animal.gd` and `scripts/main.gd` | Project MIT license | Native layered vector shapes; no external artwork, fonts or emoji. |

[CC0 legal terms](https://creativecommons.org/publicdomain/zero/1.0/legalcode).
The sound-processing recipe is in `tools/prepare_audio.py`. The two clips peak at
no more than 0.44 before the player's additional -3 dB gain; even simultaneous
full-scale peaks leave mixing headroom. Perceived friendliness and balance still
need a human listening check; numerical measurements cannot establish those.

Godot Engine is MIT licensed; its export includes third-party components. See
[Godot copyright and third-party notices](https://github.com/godotengine/godot/blob/4.7.2-stable/COPYRIGHT.txt)
and [Godot license](https://godotengine.org/license/).
