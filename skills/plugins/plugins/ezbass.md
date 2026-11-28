# EZbass

Observed on version 1.3.4 (VST3) in FL Studio 26.1.7, with the EZbass Vintage model and its `Clean DI` preset unless
noted. The manual is behind a login and wasn't read. The installed `EZbass Key Switch Layout.pdf`, in the program
folder, lists the keyswitches.

## Check which build FL loads

FL listed EZbass under its VST plugins and loaded a VST2 build from 2020 (1.0.5) left in
`C:\Program Files\Common Files\VST2\Toontrack\`, while the standalone and the VST3 were 1.3.4. The old build refused
the EZbass Modern library with a dialog asking for version 1.1.0. The version shows under the logo at the bottom
left. Removing the old DLL and rescanning in Options > Manage plugins made FL use the VST3.

## Controlling it

- A new instance opened on EZbass Modern with the `Clean DI` preset.
- The model selector next to the preset name is a JUCE menu. It closes as soon as FL leaves the front, so the bridge
  can only reach it with `fl_click(..., focus=True)`, on the selector and again on the row.
- The bridge sees only four named parameters (Bridge, Neck, Tone and Sub-Bass level). Settings has no option for
  release or fret noise.
- In REAPER 7.86 the same VST3 build showed six named parameters, `1. Bass Control - Bridge`, `2. Bass Control - Neck`,
  `3. Bass Control - Low`, `4. Bass Control - High`, `5. Comp - Threshold` and `6. Sub-Bass - Level`. A new instance
  opened at 100%, 91%, 74%, 82%, 0% and 0%.

## Model and preset through the state

Observed in REAPER 7.86 on 1.3.4.

- The state is the same kind of block as EZdrummer 3's (see `ezdrummer-3.md`), with readable text after
  `PlugVersion` and size fields at bytes 0, 28 and 180 that follow the text's length.
- The text names the model in `SAMPLER { soundlib "EZB-EZbassModern" ...` and the preset in
  `BassPresetName "Clean DI"`. The mixer has `Bridge` and `Neck` channels and buss effects stored as base64 blocks.
- In the Clean DI state those effects were two Toontrack EQs (one saved as an "Alembic Preamp" preset), with stored
  gains of 11.1 to 11.6 dB on three bands at the default Low and High, and a Toontrack compressor whose threshold
  control sat at 0%.
- Changing `soundlib` to `EZB-EZbassVintage` and moving the size fields by the change in length switched the instance
  to the Vintage model with no interface. The state read back named Vintage, and the same notes changed their
  harmonic profile by up to 7 dB above the 6th harmonic.
- The preset name, mixer and effects stay those of the state that was edited, so both models then play through the
  same Clean DI chain. Whether that matches Vintage's own Clean DI preset wasn't checked.

## Pitch bend and slides

Observed in REAPER 7.86 on 1.3.4 (Vintage and Modern).

- It follows MIDI pitch bend. A C2 bent fully down read 2.2 semitones lower and fully up 2.0 higher (CREPE). No
  setting for the range was found.
- A slide longer than the bend range stays continuous when the notes are chained in legato. Each time the target
  pitch curve reaches 2 semitones from the sounding note, a new note starts on the semitone the curve has reached,
  overlapping the previous one by 20 ms, and the bend returns to 0 at the same instant.
- In one bass line the bend followed the curve measured in the reference every 10 ms. Slides and falls of up to 5
  semitones then followed it within a median of 0.07 to 0.28 semitone per slide.
- A bend reset while a released note still rings moves its tail. After a fall at the end of a note, the bend went
  back to 0 5 ms before the next note, or 80 ms after the fall when the next note was farther away.
- A bend left away from 0 carries over to every note after it. In one build a missed reset left 13 s of notes about a
  semitone sharp, so check that every note outside a slide starts with the bend at 0.
- Legato entries (overlapping notes) mostly added no attack, a median of +0.2 dB at 1 to 4 kHz against +9 dB for a
  plucked note. Five of 18 still showed a step of 5 to 15 dB there.

## Level, attack and decay by model

Measured in REAPER 7.86 on A#1, C2, D#2, F2, G2 and C3, twice each, through the Clean DI chain with High at 82%:

- From velocity 127 down to 40, the attack level fell 26.5 dB on Vintage and 16.7 dB on Modern. The attack level was
  the highest point of a 25 ms envelope from 35 to 250 Hz in the first 300 ms.
- The attack peak in that band (the highest 5 ms RMS in the first 40 ms over the median from 60 to 150 ms) barely
  followed velocity on Vintage, 3.9 dB at velocity 55 and 4.7 dB at 127. In one bass line it sat about 1.7 dB above
  the reference's, so softer velocities couldn't soften the attack.
- From 80 to 560 ms after the attack the low band fell 3.4 dB/s on Vintage and 4.2 dB/s on Modern.
- Repeats of one note and velocity differed by a median of 0.13 to 0.18 dB.
- Two renders whose notes were the same from the start came out sample-identical (residual of −186 dB).

## Pitch and keyswitches

- It sounds an octave under the MIDI note written, as bass notation does. Note 47 sounded B1 (61.7 Hz) and 35
  sounded B0, so to play a pitch heard in a reference write it 12 semitones up.
- The PDF names keys with C3 = 60. In MIDI numbers the keyswitches sit on 21 to 32 and playing starts at 33.

| Note | PDF name | Behavior heard in renders |
| --- | --- | --- |
| 21 | A-1 Polyphony (hold) | overlapping notes each get their own attack |
| 27 | D#0 Loud Mute (press) | repeats the last note as a short percussive mute |
| 28 | E0 Ghost Note (press) | repeats the last note as a soft ghost |
| 29 | F0 Slide Down (press) | the sounding note falls about 10 semitones at about 22 semitones per second |
| 30 | F#0 Slide (hold) | slides to the next note when the two notes overlap, in about 100 ms for a fifth |
| 31 | G0 Slide Up (press) | the sounding note rises about 8 semitones at about 17 semitones per second |
| 32 | G#0 Legato (hold) | same as the default for overlapping notes |

The PDF also lists A#-1 Harmonic, B-1 Slap/Pop, C#0 Middle Finger and D0 Repeater, which weren't tried.

- Overlapping notes play legato by default, with no new attack, so notes meant to be plucked must end before the
  next one starts.
- The slide speed is fixed. It didn't change with the keyswitch's velocity or with the note's length, and the glide
  starts about 30 ms after the key. Without overlapping notes, Slide (30) only jumped to the next note.
- Every note-off plays a release with a small rise in pitch (under a semitone) that stays audible for 40 to 70 ms.
  Before a rest it reads as a short extra event, so end such notes earlier to match a muted reference.
- A Slide Down (29) pressed at the very end of a note, before a rest, kept sounding into the rest. Its fall of about
  10 semitones lasted 200 to 300 ms after the note-off, while the reference only bent 1 or 2 semitones and stopped.
  In one of three such places it left no sound in the rest, so check each in a render. For a short fall at the end
  of a muted note, leave the key out.
- Two renders whose notes were identical in a passage, but differed earlier in the part, differed there by up to 1
  to 2 dB per hit. Whether the round robin follows note order or chooses at random wasn't tested, so treat
  differences of that size between renders as noise.

## Velocity

Measured on notes 47, 54 and 59 with instrument-calibrate, three hits per velocity:

- The attack level (RMS of the first 30 ms) went from about -50 dB at velocity 1 to -15 dB at 127, a 35 dB range,
  monotonic and not straight.
- Hits of one velocity differed by 2.5 to 6.7 dB, with no pattern by repetition, so the round robin isn't a fixed
  alternation of fingers.
- Note 59 sat 2 to 6 dB under note 47 at low velocities, while 54 stayed within 2 dB of 47. Interpolating the curves
  in pitch predicted notes 44, 51 and 56 and unmeasured velocities within 0.87 dB (median, worst 3.1 dB).
- Timing an attack as the rise out of the dip in the low-band envelope put it 0 ms after the note-on for an isolated
  hit and 7.7 ms after it among other notes, where the previous note's release fills the dip.

## Tone controls

Measured in REAPER on EZbass Vintage with `Clean DI`, on the same notes, as band energy after matching the RMS:

- `Tone` lowered only the top. At 40 % the 1 to 4 kHz band fell 3 to 4 dB and nothing below 1 kHz moved.
- Turning `Bridge` down to 30 % or to 0 (neck pickup only) raised 300 to 1000 Hz by 6 to 7 dB, so for a darker bass
  keep both pickups and use `Tone` and an EQ after.
- `Sub-Bass Level` at 30 % changed 20 to 80 Hz by under 1 dB.
- A render of the same notes in FL Studio and in REAPER gave the same band profile within 1.3 dB.

## Audio Tracker in the standalone

Observed in the standalone `EZbass.exe` 1.3.4, which has the same tracker as the plugin and no host in the way.

- Under the `Audio Tracker` tab, `Select Audio File` opens a small menu whose `Open...` brings a standard Windows
  dialog. Its file name edit (ID 1148) took the path by `EM_SETSEL` and `EM_REPLACESEL`, so no file drag is needed.
- A `Tracker Session Setup` window follows, with `Bass Audio to MIDI` selected, the tempo and four switches for extra
  articulations (percussive mute, grace note, slide and ghost note), all on. The tempo field kept only the integer
  part. Note times in seconds don't depend on it, because the exported file carries the same tempo.
- The tracker came out with `Quantize 0`, so the notes keep the times detected.
- The `File` menu has no MIDI export. The way out is dragging the small MIDI handle beside `Add MIDI to Song Track`.
  A real left-button drag from that handle to a folder window in Explorer wrote `Untitled.mid`.
- A saved project (`.ezbp`) is plain text. Its `MidiEvents` block lists the song track as triples of a packed
  integer and the start and end in beats, where the integer is velocity × 65536 + note × 256 + status (6633104 is
  0x653690, a note-on of note 54 at velocity 101).
- The notes are written for EZbass, an octave above the pitch heard.
- Slides were written as fast chromatic staircases of short notes (about 35 ms each), marked by notes 17 (down) and
  19 (up) under the keyswitch range, plus some holds of the slide key 30. Notes 17 and 19 aren't in the keyswitch
  PDF.
- On a bass line with many repeated notes of one pitch, it joined about half of the repeats into long notes.

## Rendering in REAPER

Observed in REAPER 7.86 (VST3 and VST2 builds of 1.3.4) on four notes rendered in a new process. With no load delay the file
was pure silence in both runs, and with `fx_delay` 5 the notes sounded. Give the project a load delay
(`docs/render-standard.md`).
