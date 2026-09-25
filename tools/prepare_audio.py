"""Reproduce the bundled edits. Requires numpy, scipy and soundfile.

Download the two CC0 sources listed in ASSET_CREDITS.md to a temporary folder,
then run: python tools/prepare_audio.py <dog_barking_mono.wav> <lion-hq.mp3>
"""
import sys
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly


def prepare(source, dest, start, duration, rms):
    samples, rate = sf.read(source)
    if samples.ndim == 2:
        samples = samples.mean(axis=1)
    samples = samples[round(start * rate):round((start + duration) * rate)]
    samples = sosfilt(butter(2, [90, 4800], fs=rate, btype='bandpass', output='sos'), samples)
    samples = resample_poly(samples, 320, 441) if rate == 44100 else samples
    out_rate = 32000 if rate == 44100 else rate
    # Gently tame the recording's isolated transient peaks before balancing.
    level = max(np.sqrt(np.mean(samples**2)), 1e-9)
    samples = np.tanh(samples / (level * 3.0))
    fade_in, fade_out = round(.012 * out_rate), round(.09 * out_rate)
    samples[:fade_in] *= np.linspace(0, 1, fade_in)
    samples[-fade_out:] *= np.linspace(1, 0, fade_out)
    samples *= min(rms / max(np.sqrt(np.mean(samples**2)), 1e-9), .44 / max(abs(samples)))
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    sf.write(dest, samples, out_rate, subtype='PCM_16')
    print(dest, f'{len(samples)/out_rate:.2f}s', 'peak', round(float(max(abs(samples))), 3), 'RMS', round(float(np.sqrt(np.mean(samples**2))), 3))


if __name__ == '__main__':
    prepare(sys.argv[1], 'assets/audio/bark.wav', 0.0, .78, .10)
    prepare(sys.argv[2], 'assets/audio/roar.wav', .35, 1.2, .09)
