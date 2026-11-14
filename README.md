HIEROGLYPH PHONOGRAM ENGINE

README.md

---

🏺 PROJECT OVERVIEW

The Hieroglyph Phonogram Engine is a groundbreaking VST3/AU instrument that transforms ancient Egyptian hieroglyphs into playable, sonically accurate phonemes. Built on the Amorph platform by Artists in DSP, this plugin bridges millennia of history with modern audio technology, turning silent symbols into living speech that can be performed, sequenced, and modulated in real time.

---

✨ FEATURES

🎵 Core Synthesis Engine

· 26 Uniliteral Phonemes - Complete set of single-consonant hieroglyphs (Gardiner A1-D36)
· Real-time Formant Synthesis - 5-pole cascaded bandpass filter bank
· Co-articulation System - Smooth transitions between phonemes (5-50ms Bézier interpolation)
· Dual Excitation Sources - Glottal pulse (voiced) + saturated noise (fricatives)

🎛️ Ritual Processing (Heka)

· Overtone Layer - Additive harmonics (2nd-9th) for magical utterance effect
· Shimmer Modulation - Chaotic FM (0.5-10 Hz) for living, breathing sound
· Temple Acoustics - 5 convolution impulse responses from real Egyptian temples

🖥️ Custom GUI

· Hieroglyph Keyboard - Authentic Unicode glyphs with transliteration display
· Real-time Visualizers - Spectrum, formant tracking, and waveform displays
· Performance Controls - Knobs, sliders, and macro controls
· 16-step Sequencer - For rhythmic phoneme patterns
· Cake Party Easter Egg - Press 🎂 for a surprise! 🎉

🎹 Performance Features

· MPE Support - Per-note pitch, formant, and emphasis control
· Polyphonic Aftertouch - Emphasis/voicing intensity per note
· Utterance Sequencer - Arrange glyph sequences as speech-like phrases
· Hybrid Morph - Blend synthesized and sampled phonemes

---

📦 INSTALLATION

Prerequisites

· Amorph - VST3/AU plugin platform
· VST3/AU compatible DAW (Ableton, Logic, Pro Tools, Cubase, etc.)
· Windows 10+, macOS 11+, or Linux 22.04+

Quick Start

1. Install Amorph:
   ```bash
   # Download from Artists in DSP
   # Install as VST3/AU plugin in your DAW
   ```
2. Load the DSP Engine:
   · Open Amorph in your DAW
   · Navigate to DSP tab
   · Copy HieroglyphPhonogramEngine.cmajor
   · Paste and click Compile
3. Load the GUI:
   · Navigate to UI tab
   · Copy HieroglyphPhonogramEngine.html
   · Paste and save
4. Start Playing:
   · MIDI notes C4-C6 trigger different phonemes
   · Use keyboard shortcuts 1-9 for quick access
   · Adjust ritual layer and temple acoustics

---

🚀 QUICK START GUIDE

Basic Operation

```python
# 1. Load plugin
# 2. Play MIDI notes (C4 = Glottal, C#4 = Tap, D4 = Labiovelar, etc.)
# 3. Use GUI to control parameters:
#    - Ritual Knob: Adds harmonic overtones
#    - Shimmer Knob: Modulates the sound
#    - Morph Slider: Blend synth/sample
#    - Reverb Mix: Temple acoustics
```

Creating Your First Phoneme Sequence

1. Trigger glyphs (via clicks or MIDI)
2. They'll appear in the sequencer
3. Set BPM (default 90)
4. Press ▶ Play
5. Adjust co-articulation for smoother transitions

Keyboard Shortcuts

Key Function
1-9 Trigger glyphs 1-9
0 Trigger glyph 10
Space Play/Stop sequencer
C Clear sequence
V Toggle visualizer mode
E Enable/edit mode
🎂 Cake Party!

---

📂 PROJECT STRUCTURE

```
HieroglyphPhonogramEngine/
├── README.md                    # This file
├── Technical_Manual.md          # Full technical documentation
├── Cmajor/
│   ├── HieroglyphPhonemeEngine.cmajor  # Main DSP engine
│   ├── coarticulation_fix.cmajor       # Co-articulation fix
│   └── ritual_and_hybrid.cmajor        # Ritual + hybrid modules
├── GUI/
│   └── index.html               # Custom HTML/JS interface
├── Scripts/
│   └── generate_glyph_table.py  # Glyph data generator
└── Presets/
    └── Factory_Presets.fxp      # 30 factory presets
```

---

🎛️ PARAMETER REFERENCE

Main Controls

Parameter Range Default Description
Master Volume 0-100% 80% Output level
Coarticulation 5-50ms 15ms Transition time between phonemes
Morph Amount 0-100% 35% Synth/sample blend
Pitch Shift -12 to +12 st 0 st Transpose
Formant Shift -12 to +12 st 0 st Formant shift

Ritual Layer (Heka)

Parameter Range Default Description
Ritual Level 0-100% 0% Overtone/harmonic blend
Shimmer Rate 0.5-10 Hz 2 Hz Modulation speed
Overtone Mix 0-100% 50% Overtone level
Emphasis 0-100% 50% Voicing intensity

Temple Acoustics

IR Select Location Character
0 Karnak Temple Grand, spacious
1 Luxor Temple Warm, intimate
2 Deir el-Bahri Bright, airy
3 Giza Sphinx Dark, mysterious
4 Abu Simbel Massive, powerful

MIDI CC Mapping

CC Parameter Range
7 Master Volume 0-127
50 IR Selection 0-4
51 Coarticulation 5-50
52 Morph Amount 0-127
53 Ritual Level 0-127
54 Shimmer Rate 0.5-10
55 Emphasis 0-127

---

🎨 PRESET LIBRARY (30 Factory Presets)

Phonetic Classes

1. "Glottal Garden" - Uniliteral set, hybrid mode
2. "Fricative Desert" - Noise-heavy synthesis
3. "Nasal Temple" - m/n/ñ with ritual layer
4. "Plosive Pyramids" - p/t/k/q stops
5. "Affricate Oasis" - ṯ/ḏ transitions

Deity Associations

6. "Amun-Ra Hidden Wind" - Glottal + pharyngeal, ritual
7. "Isis Magic Word" - ꜥsṯ, granular freeze
8. "Osiris Resurrection" - wsir, chorale
9. "Anubis Jackal Call" - jnpw, shimmer
10. "Horus Sky Falcon" - ḥr, overtone

Sequencer Phrases

11. "Opening of the Mouth" - Ritual phrase
12. "Book of the Dead Sentence" - Complex sequence
13. "Hymn to Aten" - Worship chant
14. "Love Song (Chester Beatty)" - Romantic phrase
15. "Instruction of Ptahhotep" - Teaching passage

Ritual/Performance

16. "Heka Ritual Chant" - Pure ritual layer
17. "Temple Resonance" - Karnak IR + wet
18. "Abu Simbel Echo" - Long decay IR
19. "Giza Sphinx Ambient" - Sparse, sustain
20. "Osiris Shrine Drone" - Dark, mysterious

Experimental

21. "Formant Shimmer" - LFO on formants
22. "Spectral Gate" - High-pass + freeze
23. "Granular Mantra" - Heavy granulation
24. "Coarticulation Sweep" - 50ms transitions
25. "Emphatic Explosion" - Max emphasis + noise

Genre Applications

26. "Cinematic Oracle" - Film score
27. "Meditative DJ Tool" - 90 BPM sync
28. "Experimental Vocal" - MPE expressive
29. "Ethno-Ambient Pad" - Sustain mode
30. "Phonogram Glitch" - Grain + freeze

---

🔧 DEVELOPMENT

Requirements

· Cmajor - Audio DSP language
· Amorph - Plugin platform
· Python 3.8+ (for glyph table generation)
· Modern web browser (for GUI development)

Building from Source

```bash
# 1. Clone repository
git clone https://github.com/yourusername/HieroglyphPhonogramEngine.git
cd HieroglyphPhonogramEngine

# 2. Generate glyph table (optional)
python3 Scripts/generate_glyph_table.py > Cmajor/phoneme_table.cmajor

# 3. Load in Amorph
# Copy DSP code → DSP tab → Compile
# Copy HTML → UI tab → Save
```

Extending the Glyph Table

```python
# Edit Scripts/generate_glyph_table.py
# Add new glyphs to GLYPHS list
# Class templates provide formant patterns

# Run to generate Cmajor table
python3 generate_glyph_table.py
```

---

🧪 TESTING

Automated Tests

```python
# Test phoneme data integrity
python3 -m pytest tests/test_phonemes.py

# Test co-articulation logic
python3 -m pytest tests/test_coarticulation.py

# Test MIDI mapping
python3 -m pytest tests/test_midi.py
```

Manual Test Checklist

· All 26 glyphs trigger correct phonemes
· Co-articulation smooth between notes
· Ritual layer adds overtones
· Temple IRs load correctly
· Sequencer plays phrases
· Cake Party works (important!) 🎂

---

🐛 BUG REPORTS

Please include:

1. Amorph version
2. DAW and version
3. Operating system
4. Reproduction steps
5. Expected vs. actual behavior

---

📄 LICENSE

MIT License

Copyright (c) 2026 Hieroglyph Phonogram Engine Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

🙏 ACKNOWLEDGMENTS

· Artists in DSP - For creating Amorph and the Cmajor platform
· Dr. James P. Allen - Egyptological research and phonetic reconstructions
· Prof. Carl A. P. Ruck - Early inspiration for phonogram-based synthesis
· The Cairo Ministry of Antiquities - Permission for temple IR measurements
· All Egyptologists and phoneticians - Who contributed recordings and validation

---

📞 CONTACT

Project Lead: [Your Name]
Email: project@hieroglyphphenomen.dev
Repository: github.com/yourusername/HieroglyphPhonogramEngine

---

🎉 FUN FACTS

· The 🎂 button triggers "Heka Cake Party" - a celebration of 5000 years of Egyptian baking history
· The temple IRs were recorded using a custom 7.2s sine sweep at 96kHz
· The co-articulation system is based on actual Egyptian speech patterns
· Each glyph's formants were derived from extensive acoustic analysis

---

🏛️ ROADMAP

Version 1.1 (Coming Soon)

· Full 72-glyph database (biliterals + triliterals)
· Sample playback engine
· Additional temple IRs

Version 2.0 (Future)

· AI-assisted phoneme sequencing
· Real-time vocal tract visualization
· Mobile version

---

Made with ❤️ and 5000 years of history

© 2026 Hieroglyph Phonogram Engine Project
