# Список MIDI-контроллеров

Nord Piano 6 поддерживает стандартные **MIDI CC-сообщения** (один контроллер на параметр) и сообщения стандарта **NRPN** (Non-Registered Parameter Number, несколько контроллеров на параметр).

**Параметры NRPN** обозначены в таблице двоеточием (**:**). Первое число соответствует **CC#99** (NRPN MSB), второе — **CC#98** (NRPN LSB). Значение параметра передаётся через **CC#38** (Data Entry LSB). **CC#6** (Data Entry MSB) должен быть равен **0**.

Полный пакет NRPN состоит из четырёх сообщений: CC#99, CC#98, CC#6 и CC#38.

---

## Глобальные контроллеры

| Параметр | MIDI CC # |
|---|---|
| Volume (Громкость) | 7 |
| Pan (Панорама) | 10 |
| Sustain (Сустейн) | 64 |
| Soft Pedal (Мягкая педаль) | 67 |
| Sostenuto (Сосtenuto) | 66 |
| Ctrl Pedal / Expression | 11 |

---

## Фокус и группировка эффектов

| Параметр | MIDI CC # |
|---|---|
| FX Focus | 31 |
| FX Group Piano | 75 |
| FX Group Sample Synth | 76 |

---

## Секция Piano

| Параметр | MIDI CC # |
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

## Секция Sample Synth

| Параметр | MIDI CC # |
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

## Эффекты — Mod 1

| Параметр | MIDI CC # |
|---|---|
| Mod 1 Enable | 79 |
| Mod 1 Type | 80 |
| Mod 1 Amount | 85 |
| Mod 1 Rate | 86 |
| Mod 1 Ctrl Ped | 81 |

---

## Эффекты — Mod 2

| Параметр | MIDI CC # |
|---|---|
| Mod 2 Enable | 118 |
| Mod 2 Type | 83 |
| Mod 2 Amount | 89 |
| Mod 2 Rate | 90 |
| Mod 2 Mono | 84 |

---

## Эффекты — Эквалайзер

| Параметр | MIDI CC # |
|---|---|
| EQ Enable | 105 |
| EQ Bass Gain | 102 |
| EQ Mid Gain | 103 |
| EQ Mid Frequency | 107 |
| EQ Treble | 104 |
| EQ Global | 33 |

---

## Эффекты — Дилэй

| Параметр | MIDI CC # |
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

## Эффекты — Усилитель

| Параметр | MIDI CC # |
|---|---|
| Amp Enable | 108 |
| Amp Type | 110 |
| Amp Drive | 106 |
| Amp Alternate Tone | 119 |

---

## Эффекты — Компрессор

| Параметр | MIDI CC # |
|---|---|
| Compressor Enable | 116 |
| Compressor Amount | 117 |
| Compressor Global | 28 |

---

## Эффекты — Глобальная реверберация

| Параметр | MIDI CC # |
|---|---|
| Reverb Enable | 17 |
| Reverb Type | 19 |
| Reverb Dry/Wet | 113 |
| Reverb Bright/Dark | 18 |
| Reverb Chorale | 21 |
| Reverb Pre-Delay | 20 |
| Reverb Layer Send Enable | 112 |
