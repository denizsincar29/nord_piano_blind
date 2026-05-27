# MIDI Controller List

The Nord Piano 6 implements both standard single-value **MIDI CC messages** and multi-message **NRPN** (Non-Registered Parameter Number) messages.

**NRPN parameters** are identified in the table below by the use of a colon (**:**) in their CC column entry. The first number corresponds to **CC#99** (NRPN MSB) and the second to **CC#98** (NRPN LSB). The parameter value is sent as **CC#38** (Data Entry LSB). Data Entry MSB (**CC#6**) is expected to be **0** unless otherwise noted.

A complete NRPN package consists of four messages: CC#99, CC#98, CC#6, and CC#38.

---

## Global Controllers

| Parameter | MIDI CC # |
|---|---|
| Volume | 7 |
| Pan | 10 |
| Sustain | 64 |
| Soft Pedal | 67 |
| Sostenuto | 66 |
| Ctrl Pedal (Expression) | 11 |

---

## FX Focus and Groups

| Parameter | MIDI CC # |
|---|---|
| FX Focus | 31 |
| FX Group Piano | 75 |
| FX Group Sample Synth | 76 |

---

## Piano Section

| Parameter | MIDI CC # |
|---|---|
| Piano Layer Focus | 109 |
| Piano Layer Enable | 72 |
| Piano Layer A Level | 34 |
| Piano Layer B Level | 56 |
| Piano Octave Shift | 35 |
| Piano Sustain Pedal | 36 |
| Piano Volume Pedal | 37 |
| Piano Timbre | 27 |
| Piano KB Touch | 24 |
| Piano Pedal Noise | 23 |
| Piano Unison | 25 |
| Piano Dyn Comp | 26 |
| Piano Select | 2:33 (NRPN) |

---

## Sample Synth Section

| Parameter | MIDI CC # |
|---|---|
| Sample Synth Layer Focus | 115 |
| Sample Synth Layer Enable | 61 |
| Sample Synth Layer A Level | 43 |
| Sample Synth Layer B Level | 57 |
| Sample Synth Octave Shift | 44 |
| Sample Synth Sustain Pedal | 42 |
| Sample Synth Volume Pedal | 47 |
| Sample Synth Vibrato Mode | 50 |
| Sample Synth Vibrato Rate | 45 |
| Sample Synth Vibrato Amount | 46 |
| Sample Synth Vibrato Delay | 51 |
| Sample Synth Vib Btn Activate | 16 |
| Sample Synth Vib Btn Enable | 49 |
| Sample Synth Voice Mode | 52 |
| Sample Synth Glide Rate | 48 |
| Sample Synth Unison | 53 |
| Sample Synth Attack | 68 |
| Sample Synth Decay/Sustain | 69 |
| Sample Synth Release | 71 |
| Sample Synth Dynamics | 54 |
| Sample Synth Sample Select | 3:4 (NRPN) |

---

## Effects — Mod 1

| Parameter | MIDI CC # |
|---|---|
| Mod 1 Enable | 79 |
| Mod 1 Type | 80 |
| Mod 1 Amount | 85 |
| Mod 1 Rate | 86 |
| Mod 1 Ctrl Ped | 81 |

---

## Effects — Mod 2

| Parameter | MIDI CC # |
|---|---|
| Mod 2 Enable | 118 |
| Mod 2 Type | 83 |
| Mod 2 Amount | 89 |
| Mod 2 Rate | 90 |
| Mod 2 Mono | 84 |

---

## Effects — Equalizer

| Parameter | MIDI CC # |
|---|---|
| EQ Enable | 105 |
| EQ Bass Gain | 102 |
| EQ Mid Gain | 103 |
| EQ Mid Frequency | 107 |
| EQ Treble | 104 |
| EQ Global | 33 |

---

## Effects — Delay

| Parameter | MIDI CC # |
|---|---|
| Delay Enable | 92 |
| Delay Dry/Wet | 93 |
| Delay Rate | 94 |
| Delay Feedback | 95 |
| Delay Ping Pong | 91 |
| Delay Filter Type | 88 |
| Delay Flam | 87 |
| Delay Global | 29 |

---

## Effects — Amp

| Parameter | MIDI CC # |
|---|---|
| Amp Enable | 108 |
| Amp Type | 110 |
| Amp Drive | 106 |
| Amp Alternate Tone | 119 |

---

## Effects — Compressor

| Parameter | MIDI CC # |
|---|---|
| Compressor Enable | 116 |
| Compressor Amount | 117 |
| Compressor Global | 28 |

---

## Effects — Global Reverb

| Parameter | MIDI CC # |
|---|---|
| Reverb Enable | 17 |
| Reverb Type | 19 |
| Reverb Dry/Wet | 113 |
| Reverb Bright/Dark | 18 |
| Reverb Chorale | 21 |
| Reverb Pre-Delay | 20 |
| Reverb Layer Send Enable | 112 |

---

## Notes on NRPN

For the two NRPN entries:

**Piano Select (2:33)**
- CC#99 = 2, CC#98 = 33
- CC#6 = 0, CC#38 = parameter value
- Used to remotely change the selected piano model

**Sample Select (3:4)**
- CC#99 = 3, CC#98 = 4
- CC#6 = 0, CC#38 = parameter value
- Used to remotely change the selected sample instrument
