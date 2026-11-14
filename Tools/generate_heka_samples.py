#!/usr/bin/env python3
"""
Hieroglyph Phonogram Engine – Formant Sample Generator
Generates individual phoneme WAVs + a cinematic "Oracle" sequence.
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter, butter
import os

SR = 44100
OUT_DIR = "/home/workdir/artifacts/samples"
os.makedirs(OUT_DIR, exist_ok=True)

# Phoneme table from the Cmajor source (26 uniliterals)
# formants[5], qValues[5], voicedMix, durationMs
phonemes = [
    # 0  ꜣ  ʔ
    {"name": "A1_alef", "formants": [300, 1200, 2500, 3500, 4000], "qs": [6.5, 8.0, 9.0, 10.0, 11.0], "voiced": 1.0, "dur": 0.18},
    # 1  r
    {"name": "D21_r", "formants": [450, 1300, 2500, 3400, 4100], "qs": [8.0, 8.5, 9.0, 9.5, 10.0], "voiced": 1.0, "dur": 0.10},
    # 2  w
    {"name": "G43_w", "formants": [300, 2000, 2900, 3600, 4200], "qs": [8.0, 8.5, 9.0, 9.5, 10.0], "voiced": 1.0, "dur": 0.14},
    # 3  f
    {"name": "I9_f", "formants": [400, 1700, 2800, 4500, 6000], "qs": [5.0, 6.0, 7.0, 8.0, 8.0], "voiced": 0.0, "dur": 0.12},
    # 4  m
    {"name": "G17_m", "formants": [280, 900, 2200, 3300, 3900], "qs": [7.0, 7.5, 8.5, 9.5, 10.5], "voiced": 1.0, "dur": 0.16},
    # 5  n
    {"name": "N35_n", "formants": [280, 900, 2200, 3300, 3900], "qs": [7.0, 7.5, 8.5, 9.5, 10.5], "voiced": 1.0, "dur": 0.15},
    # 6  ḥ
    {"name": "O4_h", "formants": [350, 1400, 2400, 3600, 4200], "qs": [4.0, 5.0, 6.0, 7.0, 7.0], "voiced": 0.5, "dur": 0.15},
    # 7  ḫ
    {"name": "V28_x", "formants": [400, 1700, 2800, 4500, 6000], "qs": [5.0, 6.0, 7.0, 8.0, 8.0], "voiced": 0.0, "dur": 0.12},
    # 8  ẖ
    {"name": "Aa1_c", "formants": [400, 1700, 2800, 4500, 6000], "qs": [5.0, 6.0, 7.0, 8.0, 8.0], "voiced": 0.0, "dur": 0.12},
    # 9  s
    {"name": "O34_s", "formants": [400, 1600, 2400, 4200, 5800], "qs": [5.0, 6.0, 7.0, 7.5, 8.0], "voiced": 0.0, "dur": 0.13},
    # 10 š
    {"name": "S29_sh", "formants": [400, 1600, 2400, 4200, 5800], "qs": [5.0, 6.0, 7.0, 7.5, 8.0], "voiced": 0.0, "dur": 0.14},
    # 11 q
    {"name": "N37_q", "formants": [350, 1900, 2700, 3800, 4600], "qs": [4.5, 5.0, 5.5, 6.0, 6.5], "voiced": 0.2, "dur": 0.11},
    # 12 k
    {"name": "V31_k", "formants": [350, 1900, 2700, 3800, 4600], "qs": [4.5, 5.0, 5.5, 6.0, 6.5], "voiced": 0.2, "dur": 0.10},
    # 13 g
    {"name": "W11_g", "formants": [320, 1800, 2600, 3700, 4500], "qs": [5.0, 5.5, 6.0, 6.5, 7.0], "voiced": 0.8, "dur": 0.11},
    # 14 t
    {"name": "X1_t", "formants": [350, 1900, 2700, 3800, 4600], "qs": [4.5, 5.0, 5.5, 6.0, 6.5], "voiced": 0.2, "dur": 0.09},
    # 15 ṯ
    {"name": "D46_tsh", "formants": [380, 1750, 2900, 4300, 5500], "qs": [4.5, 5.0, 5.5, 6.0, 6.0], "voiced": 0.3, "dur": 0.12},
    # 16 d
    {"name": "I10_d", "formants": [320, 1800, 2600, 3700, 4500], "qs": [5.0, 5.5, 6.0, 6.5, 7.0], "voiced": 0.8, "dur": 0.10},
    # 17 ḏ
    {"name": "I11_dzh", "formants": [380, 1750, 2900, 4300, 5500], "qs": [4.5, 5.0, 5.5, 6.0, 6.0], "voiced": 0.3, "dur": 0.12},
    # 18 p
    {"name": "Q3_p", "formants": [350, 1900, 2700, 3800, 4600], "qs": [4.5, 5.0, 5.5, 6.0, 6.5], "voiced": 0.2, "dur": 0.09},
    # 19 b
    {"name": "D58_b", "formants": [320, 1800, 2600, 3700, 4500], "qs": [5.0, 5.5, 6.0, 6.5, 7.0], "voiced": 0.8, "dur": 0.11},
    # 20 h
    {"name": "M12_h", "formants": [400, 1700, 2800, 4500, 6000], "qs": [5.0, 6.0, 7.0, 8.0, 8.0], "voiced": 0.0, "dur": 0.11},
    # 21 h (alt)
    {"name": "O6_h2", "formants": [400, 1700, 2800, 4500, 6000], "qs": [5.0, 6.0, 7.0, 8.0, 8.0], "voiced": 0.0, "dur": 0.11},
    # 22 j
    {"name": "M17_j", "formants": [300, 2000, 2900, 3600, 4200], "qs": [8.0, 8.5, 9.0, 9.5, 10.0], "voiced": 1.0, "dur": 0.13},
    # 23 y
    {"name": "Z4_y", "formants": [300, 2000, 2900, 3600, 4200], "qs": [8.0, 8.5, 9.0, 9.5, 10.0], "voiced": 1.0, "dur": 0.13},
    # 24 ꜥ
    {"name": "G5_ayin", "formants": [350, 1400, 2400, 3600, 4200], "qs": [4.0, 5.0, 6.0, 7.0, 7.0], "voiced": 0.5, "dur": 0.16},
    # 25 ꜥ (alt)
    {"name": "D36_ayin2", "formants": [350, 1400, 2400, 3600, 4200], "qs": [4.0, 5.0, 6.0, 7.0, 7.0], "voiced": 0.5, "dur": 0.16},
]

def lf_glottal(f0, n_samples, open_quotient=0.6, rd=1.0):
    """Simple LF-model style glottal pulse train."""
    t = np.arange(n_samples) / SR
    phase = 2 * np.pi * f0 * t
    # Rough approximation of LF pulse
    pulse = np.sin(phase) * np.exp(-3.0 * (phase % (2 * np.pi)) / (2 * np.pi))
    # Soften
    pulse = pulse / (np.max(np.abs(pulse)) + 1e-9)
    return pulse.astype(np.float32)

def noise_exc(n_samples):
    n = np.random.randn(n_samples).astype(np.float32)
    # Mild high-shelf for fricatives
    b, a = butter(2, 2500 / (SR/2), btype='high')
    return lfilter(b, a, n) * 0.35

def cascade_formant_filter(x, formants, qs):
    """5-pole cascade of bandpass resonators (simplified bilinear)."""
    y = x.copy()
    for f, q in zip(formants, qs):
        # Simple 2-pole resonator approximation
        w0 = 2 * np.pi * f / SR
        alpha = np.sin(w0) / (2 * max(q, 0.5))
        cosw = np.cos(w0)
        a0 = 1 + alpha
        b0 = alpha / a0
        a1 = -2 * cosw / a0
        a2 = (1 - alpha) / a0
        # Direct form II style
        y = lfilter([b0, 0, -b0], [1, a1, a2], y)
    return y.astype(np.float32)

def make_phoneme(p, f0=110.0, duration=None, pitch_glide=0.0):
    dur = duration if duration is not None else p["dur"]
    n = int(dur * SR)
    t = np.arange(n) / SR

    # Glottal + noise mix
    if p["voiced"] > 0.01:
        glot = lf_glottal(f0 + pitch_glide * t, n)
    else:
        glot = np.zeros(n, dtype=np.float32)
    noi = noise_exc(n)
    exc = p["voiced"] * glot + (1.0 - p["voiced"]) * noi

    # Formant filtering
    y = cascade_formant_filter(exc, p["formants"], p["qs"])

    # Soft amplitude envelope (raised-cosine)
    attack = int(0.015 * SR)
    release = int(0.04 * SR)
    env = np.ones(n, dtype=np.float32)
    if attack > 0:
        env[:attack] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, attack))
    if release > 0 and n > release:
        env[-release:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, release))
    y *= env

    # Mild saturation + normalize
    y = np.tanh(y * 1.8) * 0.55
    peak = np.max(np.abs(y)) + 1e-9
    y /= peak
    return y

def add_reverb(x, decay=0.35, mix=0.25):
    """Very simple feedback delay reverb (temple-ish)."""
    delay = int(0.047 * SR)  # ~47 ms
    buf = np.zeros(delay, dtype=np.float32)
    out = np.zeros_like(x)
    idx = 0
    for i in range(len(x)):
        delayed = buf[idx]
        out[i] = x[i] + delayed * decay
        buf[idx] = x[i] + delayed * 0.55
        idx = (idx + 1) % delay
    return (1 - mix) * x + mix * out

def write_wav(path, audio):
    audio = np.clip(audio, -1.0, 1.0)
    wavfile.write(path, SR, (audio * 32767).astype(np.int16))
    print(f"Wrote {path}  ({len(audio)/SR:.2f}s)")

# ------------------------------------------------------------------
# 1. Individual phoneme samples
# ------------------------------------------------------------------
print("Generating individual phonemes…")
for i, p in enumerate(phonemes):
    audio = make_phoneme(p, f0=120.0)
    write_wav(f"{OUT_DIR}/{i:02d}_{p['name']}.wav", audio)

# ------------------------------------------------------------------
# 2. Cinematic "Oracle" preset sequence
#    Slow, mysterious, low fundamental, heavy ritual overtones + reverb
# ------------------------------------------------------------------
print("\nGenerating THE ORACLE sequence…")

# A short mystical phrase using selected phonemes
# Roughly: ꜣ – ḥ – r – ꜥ – m – n   (evocative “oracle-like” vowels/consonants)
oracle_indices = [0, 6, 1, 24, 4, 5, 22, 0]  # ꜣ ḥ r ꜥ m n j ꜣ
oracle_durs   = [0.55, 0.45, 0.35, 0.60, 0.50, 0.45, 0.40, 0.70]
oracle_f0s    = [85, 92, 88, 78, 82, 80, 95, 75]  # low, drifting

segments = []
for idx, dur, f0 in zip(oracle_indices, oracle_durs, oracle_f0s):
    seg = make_phoneme(phonemes[idx], f0=f0, duration=dur, pitch_glide=-8.0)
    # Extra “ritual” shimmer: mild amplitude modulation
    t = np.arange(len(seg)) / SR
    shimmer = 1.0 + 0.12 * np.sin(2 * np.pi * 3.2 * t)
    seg *= shimmer
    segments.append(seg)
    # Small silence between
    segments.append(np.zeros(int(0.08 * SR), dtype=np.float32))

oracle = np.concatenate(segments)
oracle = add_reverb(oracle, decay=0.48, mix=0.38)

# Soft fade-in/out
fade = int(0.15 * SR)
oracle[:fade] *= np.linspace(0, 1, fade)
oracle[-fade:] *= np.linspace(1, 0, fade)

write_wav(f"{OUT_DIR}/THE_ORACLE.wav", oracle)

# ------------------------------------------------------------------
# 3. Short demo phrase (more speech-like)
# ------------------------------------------------------------------
print("\nGenerating short demo phrase…")
demo_idx = [0, 1, 2, 4, 5, 14, 16]  # ꜣ r w m n t d
demo = []
for i in demo_idx:
    demo.append(make_phoneme(phonemes[i], f0=130.0))
    demo.append(np.zeros(int(0.05 * SR), dtype=np.float32))
demo_audio = np.concatenate(demo)
demo_audio = add_reverb(demo_audio, decay=0.3, mix=0.22)
write_wav(f"{OUT_DIR}/demo_phrase.wav", demo_audio)

print("\nDone. Samples written to", OUT_DIR)
