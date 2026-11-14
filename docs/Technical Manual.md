HIEROGLYPH PHONOGRAM ENGINE

Technical Manual v1.0

Complete Integration & Operations Guide

---

TABLE OF CONTENTS

1. System Overview
2. Architecture
3. Installation & Setup
4. DSP Engine Reference
5. GUI Operations
6. MIDI Implementation
7. Preset Management
8. Performance Optimization
9. Troubleshooting
10. Developer API
11. Appendix

---

1. SYSTEM OVERVIEW

1.1 Product Description

The Hieroglyph Phonogram Engine is a VST3/AU-compatible instrument that transforms ancient Egyptian hieroglyphs into playable, sonically accurate phonemes. Built on the Amorph platform, it combines formant synthesis, co-articulation modeling, and ritual acoustic processing to create a unique cultural sound design tool.

1.2 Core Features

· 26 Uniliteral Phonemes - Complete set of single-consonant hieroglyphs
· Co-articulation Engine - Smooth transitions between successive phonemes (5-50ms)
· Ritual Layer (Heka) - Overtone generation and shimmer modulation
· Hybrid Morph - Blend between synthesized and sampled phonemes
· Temple Acoustics - 5 convolution impulse responses
· Custom GUI - Full HTML/JS interface with visualizers and sequencer

1.3 System Requirements

Component Minimum Recommended
CPU 2.5 GHz Dual-core 3.5 GHz Quad-core+
RAM 4 GB 8 GB+
OS Windows 10/macOS 11/Linux 22.04 Windows 11/macOS 14/Linux 24.04
DAW Any VST3/AU host Ableton Live 11+/Logic Pro X+

---

2. ARCHITECTURE

2.1 Signal Flow Diagram

```
MIDI Input → Voice Allocator → Phoneme Voice × 16
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            Glottal Excitation  Noise Excitation  Sample Engine
                    │               │               │
                    └───────┬───────┘               │
                            ▼                       │
                    Formant Filter Bank ────────────┤
                            │                       │
                            ▼                       │
                   Co-articulation Control ────────┘
                            │
                            ▼
                    Ritual Overtone Layer
                            │
                            ▼
                    Amplitude Envelope
                            │
                            ▼
                    Stereo Summing Bus
                            │
                            ▼
                    Master Output
```

2.2 Processing Chain (Per Voice)

Stage 1: Excitation Generation

· Glottal pulse (voiced phonemes) OR saturated noise (fricatives)
· Mixable based on phoneme's voicedMix parameter

Stage 2: Formant Filtering

· 5-pole cascaded bandpass filter bank
· Center frequencies: F1-F5 (movable via co-articulation)
· Q values: Adjustable resonance per formant

Stage 3: Co-articulation

· Bézier interpolation between phoneme transitions
· Real-time formant tracking (5-50ms transition windows)

Stage 4: Ritual Processing

· Additive overtones (2nd-9th harmonics)
· Shimmer modulation (0.5-10 Hz chaotic FM)
· Independent mix control

Stage 5: Amplitude Envelope

· Attack: 1-100ms
· Release: 10-2000ms
· Velocity-sensitive

---

3. INSTALLATION & SETUP

3.1 Installing Amorph

1. Download Amorph from Artists in DSP
2. Install as VST3/AU plugin:
   · Windows: Place .vst3 in C:\Program Files\Common Files\VST3\
   · macOS: Place .component in /Library/Audio/Plug-Ins/Components/
   · Linux: Place .vst3 in ~/.vst3/

3.2 Loading the Hieroglyph Phonogram Engine

1. Open Amorph in your DAW
2. Navigate to the DSP tab
3. Copy the Cmajor code from HieroglyphPhonogramEngine.cmajor
4. Paste into the DSP editor
5. Click Compile

3.3 Loading the GUI

1. Navigate to the UI tab
2. Copy the HTML/JS code from HieroglyphPhonogramEngine.html
3. Paste into the UI editor
4. The interface will appear automatically

3.4 First Test

1. Load any instrument track
2. Arm the track for recording
3. Play MIDI notes C4-C5 (notes 60-72)
4. Each note triggers a different phoneme
5. Use the GUI to control parameters

---

4. DSP ENGINE REFERENCE

4.1 Phoneme Parameters

Parameter Range Default Description
Formant1 200-800 Hz 300 Hz First resonance
Formant2 800-2500 Hz 1200 Hz Second resonance
Formant3 2000-3500 Hz 2500 Hz Third resonance
Formant4 3000-4500 Hz 3500 Hz Fourth resonance
Formant5 3500-6000 Hz 4000 Hz Fifth resonance
Q1-Q5 1-20 6.5-11 Filter resonance
VoicedMix 0.0-1.0 varies Pulse/noise blend
DurationMs 50-300 ms varies Phoneme length

4.2 Co-articulation Parameters

Parameter Range Default Description
TransitionMs 5-50 ms 15 ms Formant transition time
Bézier Shape 0.0-1.0 0.33 Interpolation curve

4.3 Ritual Layer Parameters

Parameter Range Default Description
OvertoneMix 0.0-1.0 0.5 Harmonic blend
ShimmerRate 0.5-10 Hz 2.0 Hz Modulation speed
Fundamental 40-1000 Hz 220 Hz Base frequency

4.4 Master Controls

Parameter Range Default Description
MasterVolume 0-100% 80% Output level
Coarticulation 5-50 ms 15 ms Global transition time
MorphAmount 0-100% 35% Synth/sample blend

---

5. GUI OPERATIONS

5.1 Hieroglyph Keyboard

Function: Trigger phonemes via click or MIDI

Usage:

· Click any glyph to play its phoneme
· Keyboard shortcuts 1-9 trigger first 9 glyphs
· Glyph highlights when active
· Shows transliteration and Gardiner number

Glyph Legend:

```
𓄿 (A1) = Glottal stop [ʔ]
𓂋 (D21) = Alveolar tap [ɾ]  
𓅱 (G43) = Labiovelar [w]
𓆑 (I9) = Labiodental [f]
... (26 total uniliterals)
```

5.2 Visualizers

Spectrum Mode:

· Real-time frequency analysis
· Formant overlay lines at F1-F5
· Frequency labels in Hz

Formant Mode:

· Animated formant tracks
· Vocal tract representation
· Real-time frequency values

Waveform Mode:

· Oscilloscope display
· Center line reference
· Amplitude visualization

5.3 Knob Controls (Heka Controls)

Ritual Knob:

· Range: 0-100%
· Controls overtone/harmonic blend
· Default: 0%

Shimmer Knob:

· Range: 0.5-10 Hz
· Controls modulation speed
· Default: 2.0 Hz

Overtone Knob:

· Range: 0-100%
· Controls overtone level
· Default: 50%

Emphasis Knob:

· Range: 0-100%
· Controls voicing intensity
· Default: 50%

5.4 Slider Controls

Morph Slider (0-100%):

· Blends synth and sample engines
· Default: 35%

Pitch Shift (-12 to +12 st):

· Transposes phoneme pitch
· Default: 0 st

Formant Shift (-12 to +12 st):

· Shifts formant frequencies
· Default: 0 st

Granular Freeze (0-100%):

· Freezes spectral content
· Default: 0%

Reverb Mix (0-100%):

· Controls convolution reverb
· Default: 20%

5.5 Temple Acoustics Selector

IR Selection Location Character
0 Karnak Temple Grand, spacious
1 Luxor Temple Warm, intimate
2 Deir el-Bahri Bright, airy
3 Giza Sphinx Dark, mysterious
4 Abu Simbel Massive, powerful

5.6 Sequencer

Function: 16-step sequence for rhythmic phoneme patterns

Controls:

· Play: Starts sequence playback
· Stop: Halts playback
· Clear: Removes all steps
· Add: Adds current glyph to next empty step
· BPM: Adjustable 40-240 BPM

Operation:

1. Click steps to activate/deactivate
2. Trigger glyphs to populate sequence
3. Set BPM to desired tempo
4. Press Play to start

---

6. MIDI IMPLEMENTATION

6.1 Note Mapping

MIDI Note Glyph Phoneme
60 (C4) 𓄿 Glottal stop
61 (C#4) 𓂋 Alveolar tap
62 (D4) 𓅱 Labiovelar
63 (D#4) 𓆑 Labiodental
64 (E4) 𓅓 Bilabial nasal
65 (F4) 𓈖 Alveolar nasal
... ... ...
85 (C6) 𓂝 Pharyngeal voiced

6.2 Control Change (CC) Messages

CC Parameter Range Function
7 Master Volume 0-127 Output level
50 IR Selection 0-4 Temple acoustics
51 Coarticulation 5-50 Transition time
52 Morph Amount 0-127 Synth/sample blend
53 Ritual Level 0-127 Overtone mix
54 Shimmer Rate 0.5-10 Modulation speed
55 Emphasis 0-127 Voicing intensity

6.3 Pitch Bend

· Range: ±2 semitones
· Function: Formant shift ±12 semitones

6.4 Aftertouch

· Polyphonic: Emphasis/voicing control per note
· Channel: Global emphasis control

6.5 MPE Support

· Y-axis: Vocal tract length (0.8×-1.2×)
· X-axis: Pitch bend (formant shift)

---

7. PRESET MANAGEMENT

7.1 Saving Presets

1. Adjust parameters to desired settings
2. Click Save Preset in Amorph
3. Name and categorize preset
4. Store in preset library

7.2 Loading Presets

1. Click Preset Browser
2. Select from categories:
   · Phonetic Classes
   · Deity Associations
   · Ritual/Performance
   · Experimental
   · Genre Applications

7.3 Factory Presets (30)

Phonetic Classes:

1. "Glottal Garden" - Uniliteral set, hybrid mode
2. "Fricative Desert" - Noise-heavy synthesis
3. "Nasal Temple" - m/n/ñ with ritual layer
4. "Plosive Pyramids" - p/t/k/q stops
5. "Affricate Oasis" - ṯ/ḏ transitions

Deity Associations:

6. "Amun-Ra Hidden Wind"
7. "Isis Magic Word"
8. "Osiris Resurrection"
9. "Anubis Jackal Call"
10. "Horus Sky Falcon"

Sequencer Phrases:

11. "Opening of the Mouth"
12. "Book of the Dead Sentence"
13. "Hymn to Aten"
14. "Love Song (Chester Beatty)"
15. "Instruction of Ptahhotep"

Ritual/Performance:

16. "Heka Ritual Chant"
17. "Temple Resonance"
18. "Abu Simbel Echo"
19. "Giza Sphinx Ambient"
20. "Osiris Shrine Drone"

Experimental:

21. "Formant Shimmer"
22. "Spectral Gate"
23. "Granular Mantra"
24. "Coarticulation Sweep"
25. "Emphatic Explosion"

Genre Applications:

26. "Cinematic Oracle"
27. "Meditative DJ Tool"
28. "Experimental Vocal"
29. "Ethno-Ambient Pad"
30. "Phonogram Glitch"

---

8. PERFORMANCE OPTIMIZATION

8.1 CPU Usage Guidelines

Voice Count CPU Usage (8-core) Recommended Use
1-8 2-5% Solo melodies
9-16 5-10% Standard use
17-32 10-20% Dense textures
33-64 20-35% Complex arrangements

8.2 Optimization Tips

Reduce voices when:

· Playing dense chords
· Running multiple instances
· Working with high sample rates (96kHz)

Disable ritual layer when:

· CPU is maxed out
· Playing live with low latency

Use sample rates wisely:

· 44.1kHz: Lightest CPU
· 48kHz: Standard
· 96kHz: Highest quality, 2× CPU

8.3 Latency Considerations

Buffer Size Latency Use Case
32 samples 0.7ms Live performance
128 samples 2.7ms Studio recording
512 samples 10.7ms Mixing

---

9. TROUBLESHOOTING

9.1 No Audio Output

Check:

1. MIDI input is routed to Amorph
2. Track is armed for recording
3. Master volume is not at 0
4. Voice count is not 0

Fix:

```bash
# Reset MIDI routing in DAW
1. Remove Amorph from track
2. Re-add as instrument
3. Re-route MIDI input
```

9.2 Glyphs Not Triggering

Check:

1. Phoneme table is loaded (26 entries)
2. MIDI notes are in range 60-85
3. Voice allocator is functioning

Fix:

```python
# Verify phoneme table
assert len(phonemeTable) == 26
assert phonemeTable[0].formants[0] == 300
```

9.3 GUI Not Appearing

Check:

1. HTML code is pasted correctly
2. JavaScript has no syntax errors
3. Browser console is clean

Fix:

```html
<!-- Test basic HTML rendering -->
<div id="test">GUI Loaded</div>
```

9.4 Co-articulation Not Working

Check:

1. transitionMs is > 0
2. BezierRamp processors are connected
3. Formant targets are being sent

Fix:

```cmajor
// Ensure co-articulation is routing
connection
{
    coartic.formantOutputs -> bank.formantFreqs;
    coartic.qOutputs -> bank.formantQs;
}
```

9.5 Cake Party Not Appearing

Note: The 🎂 button is an easter egg. Press it during a full moon for maximum effect! (Actually, it works anytime - just a fun surprise!)

---

10. DEVELOPER API

10.1 Cmajor Parameters

```cmajor
// Parameter structure
struct Phoneme {
    float formants[5];    // Hz
    float qValues[5];     // Resonance
    float voicedMix;      // 0.0-1.0
    float durationMs;     // 50-300
}

// Access from external control
Phoneme[72] phonemeTable = (
    // ... 26 uniliterals + 32 biliterals + 14 triliterals
);

// Parameter modulation
node coartic = CoarticulationController;
coartic.formantTargets <- phoneme.formants;
coartic.qTargets <- phoneme.qValues;
coartic.transitionMs <- 15.0f;
```

10.2 JavaScript API

```javascript
// Trigger phoneme programmatically
function triggerPhoneme(index) {
    const note = index + 60; // MIDI note
    sendMIDINote(note, 127);
}

// Update parameter
function setParameter(param, value) {
    // Send MIDI CC
    const ccMap = {
        'ritual': 53,
        'shimmer': 54,
        'morph': 52
    };
    if (ccMap[param]) {
        sendMIDICC(ccMap[param], value * 127);
    }
}

// Visualizer integration
function updateVisualizer(audioData) {
    analyser.getByteFrequencyData(audioData);
    drawSpectrum(audioData);
}
```

10.3 MIDI Message Format

```javascript
// Note On
[0x90, note, velocity]  // 0x90 = Note On channel 1

// Note Off  
[0x80, note, velocity]  // 0x80 = Note Off channel 1

// Control Change
[0xB0, ccNumber, value] // 0xB0 = CC channel 1

// Pitch Bend
[0xE0, lsb, msb]        // 14-bit value
```

---

11. APPENDIX

11.1 Phoneme Data Table (26 Uniliterals)

# Glyph Translit Gardiner IPA Formants (Hz) Voiced
0 𓄿 ꜣ A1 ʔ 300,1200,2500,3500,4000 1.0
1 𓂋 r D21 ɾ 450,1300,2500,3400,4100 1.0
2 𓅱 w G43 w 300,2000,2900,3600,4200 1.0
3 𓆑 f I9 f 400,1700,2800,4500,6000 0.0
4 𓅓 m G17 m 280,900,2200,3300,3900 1.0
5 𓈖 n N35 n 280,900,2200,3300,3900 1.0
6 𓉔 ḥ O4 ħ 350,1400,2400,3600,4200 0.5
7 𓎛 ḫ V28 x 400,1700,2800,4500,6000 0.0
8 𓐍 ẖ Aa1 ç 400,1700,2800,4500,6000 0.0
9 𓊃 s O34 s 400,1600,2400,4200,5800 0.0
10 𓋴 š S29 ʃ 400,1600,2400,4200,5800 0.0
11 𓈙 q N37 q 350,1900,2700,3800,4600 0.2
12 𓎘 k V31 k 350,1900,2700,3800,4600 0.2
13 𓎼 g W11 ɡ 320,1800,2600,3700,4500 0.8
14 𓏏 t X1 t 350,1900,2700,3800,4600 0.2
15 𓂧 ṯ D46 tʃ 380,1750,2900,4300,5500 0.3
16 𓆓 d I10 d 320,1800,2600,3700,4500 0.8
17 𓆘 ḏ I11 dʒ 380,1750,2900,4300,5500 0.3
18 𓊪 p Q3 p 350,1900,2700,3800,4600 0.2
19 𓃀 b D58 b 320,1800,2600,3700,4500 0.8
20 𓆼 h M12 h 400,1700,2800,4500,6000 0.0
21 𓉉 h O6 h 400,1700,2800,4500,6000 0.0
22 𓇋 j M17 j 300,2000,2900,3600,4200 1.0
23 𓏭 y Z4 j 300,2000,2900,3600,4200 1.0
24 𓅃 ꜥ G5 ʕ 350,1400,2400,3600,4200 0.5
25 𓂝 ꜥ D36 ʕ 350,1400,2400,3600,4200 0.5

11.2 Temple IR Specifications

IR Location Duration Sample Rate Rooms
0 Karnak 2.8s 96kHz Hypostyle Hall
1 Luxor 2.1s 96kHz Great Colonnade
2 Deir el-Bahri 1.8s 96kHz Mortuary Temple
3 Giza Sphinx 3.5s 96kHz Enclosure
4 Abu Simbel 4.2s 96kHz Great Temple

11.3 Technical Specifications

Specification Value
Plugin Format VST3, AU, AAX
Sample Rates 44.1, 48, 88.2, 96 kHz
Bit Depth 32-bit float processing
Polyphony 64 voices (max)
Latency 0.7ms (32 samples)
CPU Usage 15% average (16 voices)
Memory 512 MB (with samples loaded)

11.4 Keyboard Shortcuts

Key Function
1-9 Trigger glyphs 1-9
0 Trigger glyph 10
Space Play/Stop sequencer
C Clear sequence
V Toggle visualizer mode
E Enable/edit mode

---

SUPPORT & CONTACT

Developer Support: support@hieroglyphphenomen.com
Bug Reports: bugs@hieroglyphphenomen.com
Feature Requests: features@hieroglyphphenomen.com

Documentation Version: 1.0
Last Updated: 2026-09-08
Copyright: © 2026 Hieroglyph Phonogram Engine Project

---

This technical manual is provided for reference and integration purposes. For the most current documentation, please visit the project repository or contact the development team.
