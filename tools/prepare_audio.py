"""Reproduce bundled edits (numpy, soundfile, imageio-ffmpeg).

Download the two CC0 HQ sources in ASSET_CREDITS.md, then run:
python tools/prepare_audio.py <single-dog-bark.mp3> <lion-hq.mp3>
"""
import subprocess
import sys
import tempfile
from pathlib import Path
import imageio_ffmpeg
import numpy as np
import soundfile as sf


def prepare(source, dest, start, end, tempo, rms, tail):
    # Preserve vocal timbre: atempo changes duration without pitch shifting.
    filters = (
        f'atrim=start={start}:end={end},asetpts=PTS-STARTPTS,'
        f'atempo={tempo},highpass=f=65,lowpass=f=7500,'
        'acompressor=threshold=0.30:ratio=2:attack=5:release=55'
    )
    with tempfile.TemporaryDirectory() as temp:
        edited = Path(temp) / 'edited.wav'
        subprocess.run([
            imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error',
            '-i', str(source), '-af', filters, '-ac', '1', '-ar', '32000',
            '-c:a', 'pcm_f32le', str(edited),
        ], check=True)
        samples, rate = sf.read(edited)
    fade_in, fade_out = round(.006 * rate), round(tail * rate)
    samples[:fade_in] *= np.linspace(0, 1, fade_in)
    samples[-fade_out:] *= np.linspace(1, 0, fade_out)
    samples *= min(rms / max(np.sqrt(np.mean(samples**2)), 1e-9), .44 / max(abs(samples)))
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    sf.write(dest, samples, rate, subtype='PCM_16')
    print(dest, f'{len(samples)/rate:.3f}s', 'peak', round(float(max(abs(samples))), 3), 'RMS', round(float(np.sqrt(np.mean(samples**2))), 3))


if __name__ == '__main__':
    prepare(sys.argv[1], 'assets/audio/bark.wav', 0.0, .389, .90, .105, .025)
    # Include the full onset and release, instead of slicing into the vowel.
    prepare(sys.argv[2], 'assets/audio/roar.wav', .18, 1.82, 1.38, .10, .055)
