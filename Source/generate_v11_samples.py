#!/usr/bin/env python3
"""
Hieroglyph Phonogram Engine v1.1 – Biliteral & Triliteral Samples
Generates co-articulated sequences for the new glyphs listed in the roadmap.
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter, butter
import os

SR = 44100
OUT = "/home/workdir/artifacts/samples_v11"
os.makedirs(OUT, exist_ok=True)

# Re-use core uniliteral data (subset)
uni = {
    "ꜣ": {"f": [300,1200,2500,3500,4000], "q": [6.5,8,9,10,11], "v": 1.0},
    "r": {"f": [450,1300,2500,3400,4100], "q": [8,8.5,9,9.5,10], "v": 1.0},
    "w": {"f": [300,2000,2900,3600,4200], "q": [8,8.5,9,9.5,10], "v": 1.0},
    "f": {"f": [400,1700,2800,4500,6000], "q": [5,6,7,8,8], "v": 0.0},
    "m": {"f": [280,900,2200,3300,3900], "q": [7,7.5,8.5,9.5,10.5], "v": 1.0},
    "n": {"f": [280,900,2200,3300,3900], "q": [7,7.5,8.5,9.5,10.5], "v": 1.0},
    "ḥ": {"f": [350,1400,2400,3600,4200], "q": [4,5,6,7,7], "v": 0.5},
    "ḫ": {"f": [400,1700,2800,4500,6000], "q": [5,6,7,8,8], "v": 0.0},
    "s": {"f": [400,1600,2400,4200,5800], "q": [5,6,7,7.5,8], "v": 0.0},
    "š": {"f": [400,1600,2400,4200,5800], "q": [5,6,7,7.5,8], "v": 0.0},
    "q": {"f": [350,1900,2700,3800,4600], "q": [4.5,5,5.5,6,6.5], "v": 0.2},
    "k": {"f": [350,1900,2700,3800,4600], "q": [4.5,5,5.5,6,6.5], "v": 0.2},
    "g": {"f": [320,1800,2600,3700,4500], "q": [5,5.5,6,6.5,7], "v": 0.8},
    "t": {"f": [350,1900,2700,3800,4600], "q": [4.5,5,5.5,6,6.5], "v": 0.2},
    "ṯ": {"f": [380,1750,2900,4300,5500], "q": [4.5,5,5.5,6,6], "v": 0.3},
    "d": {"f": [320,1800,2600,3700,4500], "q": [5,5.5,6,6.5,7], "v": 0.8},
    "ḏ": {"f": [380,1750,2900,4300,5500], "q": [4.5,5,5.5,6,6], "v": 0.3},
    "p": {"f": [350,1900,2700,3800,4600], "q": [4.5,5,5.5,6,6.5], "v": 0.2},
    "b": {"f": [320,1800,2600,3700,4500], "q": [5,5.5,6,6.5,7], "v": 0.8},
    "h": {"f": [400,1700,2800,4500,6000], "q": [5,6,7,8,8], "v": 0.0},
    "j": {"f": [300,2000,2900,3600,4200], "q": [8,8.5,9,9.5,10], "v": 1.0},
    "ꜥ": {"f": [350,1400,2400,3600,4200], "q": [4,5,6,7,7], "v": 0.5},
}

def lf_glottal(f0, n):
    t = np.arange(n) / SR
    phase = 2 * np.pi * f0 * t
    pulse = np.sin(phase) * np.exp(-2.8 * (phase % (2*np.pi)) / (2*np.pi))
    return (pulse / (np.max(np.abs(pulse))+1e-9)).astype(np.float32)

def noise_exc(n):
    nse = np.random.randn(n).astype(np.float32)
    b, a = butter(2, 2200/(SR/2), btype='high')
    return lfilter(b, a, nse) * 0.32

def formant_filter(x, formants, qs):
    y = x.copy()
    for f, q in zip(formants, qs):
        w0 = 2*np.pi*f/SR
        alpha = np.sin(w0)/(2*max(q,0.6))
        cosw = np.cos(w0)
        a0 = 1+alpha
        b0 = alpha/a0
        a1 = -2*cosw/a0
        a2 = (1-alpha)/a0
        y = lfilter([b0,0,-b0],[1,a1,a2], y)
    return y.astype(np.float32)

def make_segment(key, f0=115.0, dur=0.18, glide=0.0):
    p = uni[key]
    n = int(dur*SR)
    t = np.arange(n)/SR
    if p["v"] > 0.05:
        glot = lf_glottal(f0 + glide*t, n)
    else:
        glot = np.zeros(n, dtype=np.float32)
    noi = noise_exc(n)
    exc = p["v"]*glot + (1-p["v"])*noi
    y = formant_filter(exc, p["f"], p["q"])
    # envelope
    att = int(0.012*SR)
    rel = int(0.035*SR)
    env = np.ones(n, dtype=np.float32)
    if att>0: env[:att] = 0.5-0.5*np.cos(np.linspace(0,np.pi,att))
    if rel>0 and n>rel: env[-rel:] = 0.5+0.5*np.cos(np.linspace(0,np.pi,rel))
    y *= env
    y = np.tanh(y*1.7)*0.5
    return y / (np.max(np.abs(y))+1e-9)

def coarticulate(keys, durs, f0s, transition_ms=25):
    """Concatenate segments with linear formant cross-fade style amplitude blend."""
    segs = []
    for k, d, f0 in zip(keys, durs, f0s):
        segs.append(make_segment(k, f0=f0, dur=d))
    # simple overlap-add with short cross-fade
    cross = int(transition_ms/1000 * SR)
    out = segs[0]
    for s in segs[1:]:
        if cross > 0 and len(out) > cross and len(s) > cross:
            fade_out = np.linspace(1,0,cross)
            fade_in  = np.linspace(0,1,cross)
            out[-cross:] = out[-cross:]*fade_out + s[:cross]*fade_in
            out = np.concatenate([out, s[cross:]])
        else:
            out = np.concatenate([out, s])
    return out.astype(np.float32)

def add_reverb(x, decay=0.42, mix=0.30):
    delay = int(0.053*SR)
    buf = np.zeros(delay, dtype=np.float32)
    out = np.zeros_like(x)
    idx = 0
    for i in range(len(x)):
        d = buf[idx]
        out[i] = x[i] + d*decay
        buf[idx] = x[i] + d*0.52
        idx = (idx+1)%delay
    return (1-mix)*x + mix*out

def write(path, audio):
    audio = np.clip(audio, -1, 1)
    wavfile.write(path, SR, (audio*32767).astype(np.int16))
    print(f"  {path}  ({len(audio)/SR:.2f}s)")

print("=== Biliterals ===")
# mn  𓏠  m→n
audio = coarticulate(["m","n"], [0.22,0.28], [105,98], 28)
audio = add_reverb(audio)
write(f"{OUT}/biliteral_mn_memory.wav", audio)

# ḥr  𓄋  ḥ→r
audio = coarticulate(["ḥ","r"], [0.20,0.25], [110,102], 22)
audio = add_reverb(audio, mix=0.28)
write(f"{OUT}/biliteral_hr_face.wav", audio)

# sḏ  𓊿  s→ḏ
audio = coarticulate(["s","ḏ"], [0.16,0.22], [125,118], 18)
audio = add_reverb(audio, mix=0.22)
write(f"{OUT}/biliteral_sd_hear.wav", audio)

# ṯꜣ  𓎢  ṯ→ꜣ
audio = coarticulate(["ṯ","ꜣ"], [0.18,0.30], [115,95], 25)
audio = add_reverb(audio)
write(f"{OUT}/biliteral_ta_raise.wav", audio)

# ꜥnḫ  (actually listed as biliteral example but is trilit – treat as sequence)
audio = coarticulate(["ꜥ","n","ḫ"], [0.22,0.18,0.20], [100,95,105], 20)
audio = add_reverb(audio, decay=0.45, mix=0.35)
write(f"{OUT}/triliteral_anx_live.wav", audio)

print("\n=== Triliterals ===")
# nfr  𓄤  n→f→r
audio = coarticulate(["n","f","r"], [0.20,0.16,0.28], [108,120,100], 22)
audio = add_reverb(audio, mix=0.32)
write(f"{OUT}/triliteral_nfr_beauty.wav", audio)

# wbn  𓅱𓃀𓈖  w→b→n
audio = coarticulate(["w","b","n"], [0.22,0.18,0.26], [95,100,90], 25)
audio = add_reverb(audio, decay=0.48, mix=0.38)
write(f"{OUT}/triliteral_wbn_rise.wav", audio)

# ḫpr  𓆣  ḫ→p→r
audio = coarticulate(["ḫ","p","r"], [0.18,0.14,0.30], [115,125,105], 20)
audio = add_reverb(audio)
write(f"{OUT}/triliteral_xpr_become.wav", audio)

# snb  𓋴𓈖𓃀  s→n→b
audio = coarticulate(["s","n","b"], [0.15,0.20,0.28], [120,110,100], 22)
audio = add_reverb(audio, mix=0.30)
write(f"{OUT}/triliteral_snb_healthy.wav", audio)

# Bonus cinematic Oracle-style triliteral phrase
print("\n=== Bonus cinematic phrase ===")
audio = coarticulate(
    ["ḫ","p","r", "n","f","r", "ꜥ","n","ḫ"],
    [0.25,0.18,0.35, 0.22,0.16,0.30, 0.25,0.18,0.40],
    [88,95,82, 90,105,85, 80,78,75],
    28
)
audio = add_reverb(audio, decay=0.55, mix=0.42)
# gentle fade
fade = int(0.2*SR)
audio[:fade] *= np.linspace(0,1,fade)
audio[-fade:] *= np.linspace(1,0,fade)
write(f"{OUT}/cinematic_xpr_nfr_anx.wav", audio)

print("\nDone.")
