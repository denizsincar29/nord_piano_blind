# MIDI

The Nord Piano 6 can function both as a **master keyboard** to control external hardware or software, and as a **sound module** controlled by an external MIDI device.

MIDI messages are transmitted and received simultaneously on both the **5-pin MIDI connectors** and the **USB connection**.

---

## MIDI Channel

The Nord Piano 6 uses a single **Global MIDI Channel** for both transmitting and receiving.

- All keyboard, pedal, and panel actions are sent on this channel.
- Incoming MIDI on this channel can control the entire instrument (notes, controllers, program changes, etc.).
- Set in the **MIDI Menu → 2 - MIDI Channel**. Range: 1–16, or Off. Default: **1**.

---

## Recording a Performance to a DAW or Sequencer

To record all playing, pedal actions, and panel adjustments to a computer:

1. Connect the Nord Piano 6 to the computer via USB (or 5-pin MIDI cable).
2. In your DAW, set the track to receive MIDI from the Nord Piano 6 on the configured MIDI channel.
3. Set the DAW to route the incoming MIDI back to the Nord Piano 6 on the same channel.
4. Open the **System Menu** (Shift + Program 2) and set **Local Control to Off**. This disconnects the keyboard from the internal sound engine so you only hear the notes after they pass through the DAW (avoiding double-triggering).
5. Select the desired program on the Nord Piano 6.
6. Start recording in the DAW.

> If a Transpose value is active, whether it applies to outgoing MIDI or incoming MIDI depends on the **Transpose MIDI At** setting in the MIDI Menu.

---

## MIDI Messages

### Note On / Note Off

Key presses and releases, including velocity, are transmitted and received as Note On and Note Off messages.

### Controllers

- **Controller 11 (Expression):** sent by the Vol/Ctrl pedal, if connected.
- **Controller 64 (Sustain Pedal):** sent by the Sustain Pedal input and the right pedal of a Nord Triple Pedal.
- **Controller 66 (Sostenuto):** sent by the middle pedal of a Triple Pedal.
- **Controller 67 (Soft Pedal):** sent by the left pedal of a Triple Pedal.
- **All front panel knobs and buttons** also transmit their values as MIDI Control Change messages, allowing panel moves to be recorded in a sequencer. See the [MIDI Controller List](12-midi-controller-list.md) for a full table.

### NRPN Messages

The Piano Select and Sample Select controls transmit using the **NRPN** (Non-Registered Parameter Number) standard, which uses multiple CC messages per parameter:
- CC#99 (NRPN MSB)
- CC#98 (NRPN LSB)
- CC#6 (Data Entry MSB, expected to be 0)
- CC#38 (Data Entry LSB, the parameter value)

---

## Program Change

Loading any program sends a **Program Change** message on the Global MIDI channel. Receiving a Program Change message selects the corresponding program on the Nord Piano 6.

| Message Part | Regular Programs | Live Programs |
|---|---|---|
| Bank MSB (CC# 0) | 0 | 1 |
| Bank LSB (CC# 32) | 0–5 | 0 |
| Program Change | 1–108 | 1–6 |

One MIDI program bank covers three Nord Piano 6 banks of 36 programs each (numbers 1–108).

> A Program Change message received without a preceding Bank Select message will act within the currently selected program or live bank.

Whether the Nord Piano 6 sends and/or receives Program Change messages is set in **MIDI Menu → 3 - Program Change Mode**.

---

## Local Control On / Off

**Local Control On** (default): the keyboard and panel directly play the internal sound engines.

**Local Control Off**: the keyboard and panel are disconnected from the internal sound engines. All actions are sent as MIDI only. Use this in a MIDI loop setup (e.g., routing through a DAW) to avoid double-triggering.

Set in **MIDI Menu → 1 - Local Control**. Range: On (default), Off.

> Local Control always resets to **On** every time the Nord Piano 6 is powered on.

---

## Panic

If notes get stuck during a MIDI performance:

- Press **Shift + TRANSPOSE** (the PANIC function).
- This sends an internal "All Notes Off" message and resets all incoming CC messages.

The display shows "PANIC" briefly while this executes.
