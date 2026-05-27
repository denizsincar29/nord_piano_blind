# PROGRAM Section

The PROGRAM section is roughly at the center of the front panel. It contains the OLED display, program navigation, storage, transpose, split, and menus. All settings for both the Piano and Sample Synth sections — as well as effects, split, and transpose configurations — are managed here.

---

## The Display

A rectangular **OLED display** at the center of the PROGRAM section. It shows:
- The current program name and number (e.g., **A:23 Pearl Drops**)
- The names of selected piano and sample instruments
- Parameter hints when panel controls are adjusted
- Menu settings
- List views when browsing programs, pianos, or samples
- The keyboard split position when setting a split

An "**E**" appears next to the program number whenever any parameter has been edited but not yet saved.

---

## TRANSPOSE

Above the display. A round **green** indicator, the label **ON/SET** with a down arrow, and a black button.

- **Press once:** toggles the stored transpose value on or off for the current program
- **Hold down (or Shift + button):** opens the transpose settings page on the display. Use the **PROGRAM** dial to select a value from −6 to +6 semitones. Press **EXIT (Shift)** to close.
- The transpose value is stored with each individual program.

**Global Transpose** (separate from this button) is set in the **System Menu** and applies to the whole instrument, adding to any per-program transpose value.

**PANIC** (Shift + TRANSPOSE): sends an "All Notes Off" MIDI message and resets all incoming CC messages. Use this if notes get stuck during a MIDI performance.

---

## KB SPLIT

Upper-left of the PROGRAM section, above the display.

A round **green** indicator, the label **ON/SET** with a down arrow, and a black button.

- **Press once:** turns the keyboard split on or off
- **Hold down (or Shift + button):** opens the keyboard split position page. Turn the **PROGRAM** dial to choose a split point from **F2** to **C7**. The active position is indicated by LEDs above the keyboard.

### Keyboard Zones

When Split is on, the keyboard is divided into **LO (lower)** and **UP (upper)** zones. Each Piano and Sample Synth layer can be assigned to one or both zones using **KB ZONE** (Shift + Layer button).

### X-FADE (Shift + KB SPLIT button)

Two round indicators labeled **1** and **2** below the main split indicator.

Cross-fade creates a smooth volume blend between sounds at the split point instead of an abrupt transition.

- **Off** — no crossfade; sounds switch instantly at the split point
- **1** — crossfade range of ±6 semitones around the split point
- **2** — crossfade range of ±12 semitones around the split point

---

## MIDI Indicator

A small round indicator labeled **MIDI**, located below the KB SPLIT area.

Blinks whenever MIDI messages arrive at the **MIDI In** port or via the **USB** connection. Useful for confirming that external MIDI data is being received.

---

## Program Buttons (1–6)

At the bottom of the PROGRAM section: six buttons in a row, each with a round indicator above it numbered **1** through **6**. Below each button is a secondary function label.

**Primary function:** Press any button to instantly select one of the 6 programs on the current program page.

**Secondary (Shift) functions:**
- **PROG INIT** (Shift + 1): initializes the program — loads a single piano layer with no effects, giving a blank starting point
- **SYSTEM** (Shift + 2): opens the System Menu
- **SOUND** (Shift + 3): opens the Sound Menu
- **MIDI** (Shift + 4): opens the MIDI Menu
- **PEDAL** (Shift + 5): opens the Pedal Menu
- **ORGANIZE** (Shift + 6): enters Organize Mode for moving and swapping programs

**Soft buttons:** When any menu is open, buttons 2–5 act as "soft buttons" to select or toggle options displayed at the bottom of the screen.

---

## LIVE MODE

A round indicator and a black button to the left of the program buttons row, labeled **LIVE MODE** above and **NUM PAD** below.

**Press LIVE MODE:** enters a set of 6 dedicated live programs. Select any live program with buttons 1–6. Live programs **auto-save all changes instantly** — no manual Store needed. Exit Live Mode by pressing the button again.

**NUM PAD** (Shift + LIVE MODE): switches to **Numeric Pad** navigation mode. In this mode, use the program buttons as a number pad to type a program number directly. Press again to exit.

---

## PROG VIEW (Program View)

A black button to the right of the TRANSPOSE area.

- **Press:** toggles between two display layouts:
  - **Default view:** large program name and number at the top; bottom half shows parameter hints as you adjust controls
  - **Detail view:** smaller program name/number; bottom half shows the current sound selected for each active layer

---

## STORE

A **red button** with a round indicator above it and **STORE AS...** printed below.

### Store a Program (simple overwrite)
1. Press **STORE** once — the STORE LED begins flashing and the display shows the current storage location
2. To save to the same location, press **STORE** again to confirm
3. To save to a different location, use the **PROGRAM** dial or page buttons to navigate to the desired slot, then press **STORE** to confirm

> As you scroll through locations during a Store operation, each program becomes active on the keyboard, letting you audition existing programs before deciding where to save.

> Press **Shift/Exit** once to cancel a Store operation.

### Name a Program — STORE AS... (Shift + STORE)
1. Hold **Shift** and press **STORE** to open the naming page
2. Use the **PROGRAM** dial to scroll through characters; use **PAGE** buttons to move the cursor left and right
3. Press **STORE** again to confirm

**Memory Protection:** When shipped from the factory, Memory Protect is **On**, which prevents any Store operations. To allow saving, go to the **System Menu → Memory Protect → Off**.

---

## PROGRAM Dial

A round encoder knob to the right of the display, below the STORE button. Below it: the list icon and the word **PROGRAM**.

- **Turn:** navigate through programs on the current page
- **Shift + turn:** enter **List View** showing all programs across all banks as a scrollable list

**List View sorting options** (soft buttons at bottom of screen):
- Default — sorted by bank/page order
- **Abc** — alphabetical by program name
- **Cat** — sorted by category

Press **Shift** again to exit List View.

---

## PAGE/CAT and BANK Buttons

Two buttons side by side, labeled **PAGE** with left/right arrows, below the display. The label **BANK** with left/right arrows appears between them at the bottom.

- **PAGE buttons:** move one page at a time (each page = 6 programs). Navigate left or right through the 6 pages within a bank.
- **BANK** (Shift + PAGE): move between program banks (A through P = 16 banks, each with 36 programs = 576 total)
- **In List View mode:** the PAGE buttons switch between sorting modes (name order, alphabetical, category)

---

## ORGANIZE Mode (Shift + Program Button 6)

Allows rearranging programs within banks without using a computer.

**Enter Organize:**
1. Press **Shift + Program 6** to enter Organize mode
2. The display shows a list of programs

**Swap two programs:**
1. Navigate to the first program using the PROGRAM dial
2. Press the soft button labeled **Swap** (Program button 2)
3. Navigate to the second program
4. Press **Swap** again to confirm

**Move a program:**
1. Navigate to the program
2. Press the soft button labeled **Move** (Program button 3)
3. Navigate to the target location
4. Press **Move** again to confirm

> Programs can also be organized using the **Nord Sound Manager** application on a computer.

---

## SHIFT / EXIT Button

A gray button in the lower-right corner of the PROGRAM section, on a white background. Labeled **SHIFT** above and **EXIT** below.

- **Hold SHIFT** while operating any panel control to access its secondary function
- **Press EXIT** (tap SHIFT) to exit any open menu or cancel a Store operation

This is the most important modifier button on the instrument. Its position — lower right of the PROGRAM section — is the reference point for the center of the panel.
