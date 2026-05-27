# Menus

The Nord Piano 6 has four menus: **System**, **Sound**, **MIDI**, and **Pedal**. All menu settings (except Local Control) take effect immediately and are stored permanently until changed again.

**Open a menu:** Hold **Shift** and press the corresponding Program button below the display.

| Menu | Button |
|---|---|
| System | Shift + Program 2 (SYSTEM) |
| Sound | Shift + Program 3 (SOUND) |
| MIDI | Shift + Program 4 (MIDI) |
| Pedal | Shift + Program 5 (PEDAL) |

**Navigate within a menu:** Use the **PAGE** buttons (left/right) to move between settings.

**Change a value:** Turn the **PROGRAM** dial.

**Use soft buttons:** When a setting has sub-options, the PROGRAM buttons 2–5 act as soft buttons shown at the bottom of the display.

**Exit a menu:** Press **Shift/Exit**.

---

## System Menu

### 1 — Memory Protect

Prevents accidental overwriting of programs when **On**.

- **On** (factory default): Store operations are blocked
- **Off**: Storing programs is allowed

> Menu settings and Live programs are not affected by Memory Protect.

### 2 — Global Transpose

Transposes the entire instrument in semitone steps. This value is added to any per-program transpose value stored with a program.

- Range: **−6 to +6 semitones**
- Default: **Off** (0)

### 3 — Fine Tune

Adjusts overall pitch in fine increments, useful when playing with instruments that are slightly off standard pitch.

- Range: **±50 cents** (±half a semitone)
- Default: **0**

### 4 — LED Intensity

Sets the brightness of all panel LEDs. Useful when performing in very bright or very dark environments.

- Range: **Low**, **High** (default)

### 5 — Version and Model Info

Shows the full version number of the currently installed operating system.

- Turn the **PROGRAM** dial to switch between Version info and hardware Model info.

---

## Sound Menu

### 1 — Program Level

Adjusts the total output level of the currently loaded program by scaling all of its layer levels simultaneously.

- Range: **±12 dB**
- The program must be **stored** for this adjustment to persist.

### 2 — Output

Sets whether the audio outputs carry a stereo or mono signal.

- **Stereo** (default): Left Out and Right Out carry separate left and right channels
- **Mono**: Both outputs carry the same combined mono signal

### 3 — Piano Pedal Noise Level

Sets the volume of the Pedal Noise effect (the mechanical sound of pressing a piano sustain pedal), for pianos that support this feature.

- Requires a **Nord Triple Pedal** or **Nord Single Pedal 2** to be connected.
- Range: **±6 dB** (default: 0 dB)

---

## MIDI Menu

### 1 — Local Control

Determines whether the keyboard and panel control the internal sound engine.

- **On** (default): keyboard and panel play the internal sounds normally
- **Off**: keyboard and panel send MIDI only; the internal sounds are silent unless MIDI is routed back from an external device

> Local Control always resets to **On** at power-on.

### 2 — MIDI Channel

Sets the single global channel used for all MIDI transmit and receive.

- Range: **1–16**, or **Off**
- Default: **1**

### 3 — MIDI Control / Program / Device Change

Three separate sub-settings, each configuring whether the Nord Piano 6 sends and/or receives that type of MIDI message.

**Control Change Mode**
- Covers all CC messages (knobs, buttons) and NRPN messages (Piano/Sample Select dials)
- Range: **Off**, **Send**, **Receive**, **Send & Receive** (default)

**Program Change Mode**
- Whether loading programs sends/receives MIDI Program Change messages
- Range: **Off**, **Send**, **Receive**, **Send & Receive** (default)

**Device Change Mode**
- Covers physical controllers (pedals) which generate their own MIDI independently of the CC filter
- Range: **Off**, **Send**, **Receive**, **Send & Receive** (default)

### 4 — Transpose MIDI At

Controls whether any active transpose values (global or per-program) apply to MIDI output or MIDI input.

- **In** (default): transpose is applied to **incoming** MIDI; outgoing MIDI notes are sent at their original pitch
- **Out**: transpose is applied to **outgoing** MIDI; incoming MIDI notes are received at their original pitch

### 5 — MIDI Out Velocity Curve

Controls how hard you need to press keys to generate high MIDI velocity values.

- **Heavy** (default): matches the dynamic range of the Nord Piano 6 piano engine; intended for use in Local Control Off mode
- **Medium**: less effort required for high velocities
- **Light**: easiest to generate maximum velocity

---

## Pedal Menu

### 1 — Control Pedal

**Type:** Selects which expression pedal model is connected to the **VOL/CTRL PEDAL** input.

> If you operate the connected pedal while this menu page is open, the display shows a percentage value indicating the detected range of the pedal. This helps confirm the pedal is communicating correctly.

Supported models:
- Roland EV-7 (default)
- Yamaha FC-7
- Korg
- Fatar / Studiologic
- Nord SP-2

**Gain:** Adds gain to the pedal signal if the pedal does not reach its full range.
- Range: **1–10**

### 2 — Sustain Pedal Type

Selects the type of pedal connected to the **SUSTAIN PEDAL** input. Also sets polarity if the pedal's on/off states are reversed.

Options:
- Nord SP-1 (default)
- Nord SP-2
- Nord TP-1
- Normally Open
- Normally Closed

### 3 — Triple Pedal Function

When a Nord Triple Pedal 1 (via Sustain Pedal input) or Nord Triple Pedal 2 (via Triple Pedal input) is connected, the **Left** and **Middle** pedals can be assigned to additional functions. The Right pedal always functions as Sustain.

**Left pedal options:**
- **Una Corda** (default) — soft pedal
- Synth Vibrato
- Program Up
- Program Down

**Middle pedal options:**
- **Sostenuto** (default) — sustains only notes held at the moment of pressing
- Synth Vibrato
- Program Up
- Program Down

### 4 — Foot Switch

Configures the **FOOT SWITCH** jack for a momentary one- or two-button pedal.

**Type:** Set according to the connected pedal model and its polarity.

> The Nord SP-2 and other continuous expression pedals are **not** compatible with the Foot Switch jack.

- Range: **Single Open**, **Single Closed**, **Dual Open**, **Dual Closed**

**SW A:** Function of a single pedal, or the first switch of a dual pedal.
- Options: Synth Vibrato, Program Up, Program Down

**SW B:** Function of the second switch of a dual pedal only (no effect for single pedals).
- Options: Synth Vibrato, Program Up, Program Down
