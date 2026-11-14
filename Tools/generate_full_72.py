#!/usr/bin/env python3
"""Generate remaining biliteral + triliteral samples for full 72-set."""
import numpy as np
from scipy.io import wavfile
from scipy.signal import lfilter, butter
import os

SR = 44100
OUT = "/home/workdir/artifacts/samples_v11_full"
os.makedirs(OUT, exist_ok=True)

uni = {
    "ꜣ": {"f":[300,1200,2500,3500,4000],"q":[6.5,8,9,10,11],"v":1.0},
    "r": {"f":[450,1300,2500,3400,4100],"q":[8,8.5,9,9.5,10],"v":1.0},
    "w": {"f":[300,2000,2900,3600,4200],"q":[8,8.5,9,9.5,10],"v":1.0},
    "f": {"f":[400,1700,2800,4500,6000],"q":[5,6,7,8,8],"v":0.0},
    "m": {"f":[280,900,2200,3300,3900],"q":[7,7.5,8.5,9.5,10.5],"v":1.0},
    "n": {"f":[280,900,2200,3300,3900],"q":[7,7.5,8.5,9.5,10.5],"v":1.0},
    "ḥ": {"f":[350,1400,2400,3600,4200],"q":[4,5,6,7,7],"v":0.5},
    "ḫ": {"f":[400,1700,2800,4500,6000],"q":[5,6,7,8,8],"v":0.0},
    "ẖ": {"f":[400,1700,2800,4500,6000],"q":[5,6,7,8,8],"v":0.0},
    "s": {"f":[400,1600,2400,4200,5800],"q":[5,6,7,7.5,8],"v":0.0},
    "š": {"f":[400,1600,2400,4200,5800],"q":[5,6,7,7.5,8],"v":0.0},
    "q": {"f":[350,1900,2700,3800,4600],"q":[4.5,5,5.5,6,6.5],"v":0.2},
    "k": {"f":[350,1900,2700,3800,4600],"q":[4.5,5,5.5,6,6.5],"v":0.2},
    "g": {"f":[320,1800,2600,3700,4500],"q":[5,5.5,6,6.5,7],"v":0.8},
    "t": {"f":[350,1900,2700,3800,4600],"q":[4.5,5,5.5,6,6.5],"v":0.2},
    "ṯ": {"f":[380,1750,2900,4300,5500],"q":[4.5,5,5.5,6,6],"v":0.3},
    "d": {"f":[320,1800,2600,3700,4500],"q":[5,5.5,6,6.5,7],"v":0.8},
    "ḏ": {"f":[380,1750,2900,4300,5500],"q":[4.5,5,5.5,6,6],"v":0.3},
    "p": {"f":[350,1900,2700,3800,4600],"q":[4.5,5,5.5,6,6.5],"v":0.2},
    "b": {"f":[320,1800,2600,3700,4500],"q":[5,5.5,6,6.5,7],"v":0.8},
    "h": {"f":[400,1700,2800,4500,6000],"q":[5,6,7,8,8],"v":0.0},
    "j": {"f":[300,2000,2900,3600,4200],"q":[8,8.5,9,9.5,10],"v":1.0},
    "y": {"f":[300,2000,2900,3600,4200],"q":[8,8.5,9,9.5,10],"v":1.0},
    "ꜥ": {"f":[350,1400,2400,3600,4200],"q":[4,5,6,7,7],"v":0.5},
}

def lf(f0,n):
    t=np.arange(n)/SR; phase=2*np.pi*f0*t
    p=np.sin(phase)*np.exp(-2.8*(phase%(2*np.pi))/(2*np.pi))
    return (p/(np.max(np.abs(p))+1e-9)).astype(np.float32)

def noise(n):
    nse=np.random.randn(n).astype(np.float32)
    b,a=butter(2,2200/(SR/2),btype='high')
    return lfilter(b,a,nse)*0.32

def ff(x,fs,qs):
    y=x.copy()
    for f,q in zip(fs,qs):
        w0=2*np.pi*f/SR; alpha=np.sin(w0)/(2*max(q,0.6)); cosw=np.cos(w0)
        a0=1+alpha; b0=alpha/a0; a1=-2*cosw/a0; a2=(1-alpha)/a0
        y=lfilter([b0,0,-b0],[1,a1,a2],y)
    return y.astype(np.float32)

def seg(key,f0=115.,dur=0.18):
    p=uni[key]; n=int(dur*SR)
    glot=lf(f0,n) if p["v"]>0.05 else np.zeros(n,np.float32)
    exc=p["v"]*glot+(1-p["v"])*noise(n)
    y=ff(exc,p["f"],p["q"])
    att=int(0.012*SR); rel=int(0.035*SR)
    env=np.ones(n,np.float32)
    if att>0: env[:att]=0.5-0.5*np.cos(np.linspace(0,np.pi,att))
    if rel>0 and n>rel: env[-rel:]=0.5+0.5*np.cos(np.linspace(0,np.pi,rel))
    y*=env; y=np.tanh(y*1.7)*0.5
    return y/(np.max(np.abs(y))+1e-9)

def coart(keys,durs,f0s,tm=24):
    segs=[seg(k,f0,d) for k,d,f0 in zip(keys,durs,f0s)]
    cross=int(tm/1000*SR); out=segs[0]
    for s in segs[1:]:
        if cross>0 and len(out)>cross and len(s)>cross:
            out[-cross:]=out[-cross:]*np.linspace(1,0,cross)+s[:cross]*np.linspace(0,1,cross)
            out=np.concatenate([out,s[cross:]])
        else: out=np.concatenate([out,s])
    return out.astype(np.float32)

def rev(x,dec=0.4,mix=0.28):
    dly=int(0.05*SR); buf=np.zeros(dly,np.float32); out=np.zeros_like(x); i=0
    for j in range(len(x)):
        dd=buf[i]; out[j]=x[j]+dd*dec; buf[i]=x[j]+dd*0.5; i=(i+1)%dly
    return (1-mix)*x+mix*out

def write(path,a):
    a=np.clip(a,-1,1); wavfile.write(path,SR,(a*32767).astype(np.int16))
    print(path, f"{len(a)/SR:.2f}s")

# --- Remaining common biliterals (28 more to reach ~32) ---
bilits = [
    ("pr","p","r",[0.14,0.22],[130,110],"go/house"),
    ("nw","n","w",[0.18,0.22],[105,95],"see/water"),
    ("jm","j","m",[0.16,0.24],[115,100],"in/sea"),
    ("jr","j","r",[0.15,0.25],[120,105],"eye/do"),
    ("wr","w","r",[0.18,0.24],[100,95],"great"),
    ("nb","n","b",[0.16,0.22],[110,100],"lord/all"),
    ("kꜣ","k","ꜣ",[0.14,0.28],[125,90],"ka/spirit"),
    ("tꜣ","t","ꜣ",[0.12,0.28],[130,95],"land"),
    ("ḥw","ḥ","w",[0.18,0.22],[110,100],"announce"),
    ("sꜣ","s","ꜣ",[0.14,0.28],[125,95],"son/protect"),
    ("mꜣ","m","ꜣ",[0.16,0.26],[105,90],"see/truth"),
    ("rꜥ","r","ꜥ",[0.18,0.26],[100,85],"Ra/sun"),
    ("pt","p","t",[0.12,0.14],[130,125],"sky"),
    ("tp","t","p",[0.12,0.14],[125,120],"head"),
    ("ḥr","ḥ","r",[0.18,0.22],[110,100],"face"),  # already had one, variation
    ("ḏd","ḏ","d",[0.16,0.18],[115,105],"speak"),
    ("gm","g","m",[0.14,0.22],[120,105],"find"),
    ("šm","š","m",[0.15,0.22],[120,105],"go"),
    ("ḫt","ḫ","t",[0.14,0.14],[125,120],"thing/wood"),
    ("st","s","t",[0.13,0.13],[125,120],"place"),
    ("wn","w","n",[0.18,0.20],[100,95],"be/open"),
    ("jꜣ","j","ꜣ",[0.15,0.28],[115,90],"oh"),
    ("ꜥꜣ","ꜥ","ꜣ",[0.20,0.26],[95,85],"great"),
    ("bꜣ","b","ꜣ",[0.16,0.28],[110,90],"ba/soul"),
    ("pꜣ","p","ꜣ",[0.12,0.26],[130,95],"the"),
    ("nṯ","n","ṯ",[0.16,0.18],[110,115],"god"),
    ("ḫw","ḫ","w",[0.14,0.20],[120,100],"protect"),
    ("sn","s","n",[0.13,0.20],[125,110],"brother/smell"),
]

print("=== Remaining Biliterals ===")
for name,a,b,durs,f0s,meaning in bilits:
    audio=coart([a,b],durs,f0s,22)
    audio=rev(audio)
    write(f"{OUT}/biliteral_{name}_{meaning.replace('/','_')}.wav",audio)

# --- Remaining triliterals (9 more) ---
trils = [
    ("ꜥnḫ","ꜥ","n","ḫ",[0.20,0.16,0.18],[100,95,110],"live"),  # already had, variation
    ("nfr","n","f","r",[0.18,0.14,0.24],[108,120,100],"good"),
    ("wbn","w","b","n",[0.20,0.16,0.22],[95,100,90],"rise"),
    ("ḫpr","ḫ","p","r",[0.16,0.12,0.26],[115,125,105],"become"),
    ("snb","s","n","b",[0.13,0.18,0.24],[120,110,100],"healthy"),
    ("stp","s","t","p",[0.13,0.12,0.14],[125,120,125],"choose"),
    ("ḥtp","ḥ","t","p",[0.18,0.12,0.14],[110,120,125],"peace/offer"),
    ("ḏsr","ḏ","s","r",[0.16,0.13,0.22],[115,125,105],"holy"),
    ("mꜣꜥ","m","ꜣ","ꜥ",[0.16,0.24,0.22],[105,90,85],"truth"),
]

print("\n=== Remaining Triliterals ===")
for name,a,b,c,durs,f0s,meaning in trils:
    audio=coart([a,b,c],durs,f0s,24)
    audio=rev(audio,0.42,0.30)
    write(f"{OUT}/triliteral_{name}_{meaning}.wav",audio)

print("\nDone – full set samples generated.")
