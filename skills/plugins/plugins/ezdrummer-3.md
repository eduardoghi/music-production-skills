# EZdrummer 3

Observed on version 3.1.2 in FL Studio 26.1.7 with the Post-Rock kit, and in REAPER 7.86 with Post-Rock, the
EZdrummer 3 core library (BrightRoom, MainRoom and TightRoom) and the EZdrummer 3 Percussion pack. The manual is behind
a login and wasn't read.

## Note map

The default MIDI In preset is `Toontrack Standard`, in Settings > E-Drums/MIDI In. Each note below was written as one
hit, rendered and measured, so the piece is identified by its sound and not only by its name in a list.

| Note | Piece | What the render showed |
|---|---|---|
| 36 | Kick | 99% of the energy below 150 Hz, 0.19 s |
| 38 | Snare, center | Body at 141 Hz, 0.20 s |
| 40 | Snare, rimshot | Same body, 4.5 dB louder than 38 |
| 37 | Snare, sidestick | Mostly 150 Hz to 5 kHz, quieter |
| 42 | Hi-hat, closed | 72% above 5 kHz, 0.29 s |
| 44 | Hi-hat, pedal | Quiet, 25% above 5 kHz |
| 46 | Hi-hat, open | 64% above 5 kHz, 1.0 s |
| 49, 57 | Crash 1 and 2 | Broad band, long |
| 51 | Ride, bow | Long, centroid near 1 kHz |
| 53 | Ride, bell | Long, brighter than 51 |
| 48, 47, 45 | Toms, high to low | Pitched at 124, 105 and 108 Hz |
| 43, 41 | Floor toms | Pitched at 67 and 59 Hz |

47 and 45 sounded nearly the same pitch on this kit, so check toms by ear on another one. The cymbals came out about
20 dB below the kick with the kit's mixer preset, which is a mixer setting rather than the map.

## Controlling it

- Through the bridge it reports 245 parameters, and only 5 are real (`1. Bleed - OH`, `2. Bleed - Ambience`,
  `3. Bleed - Crunch`, `4. Tape - Drive` and `Bypass`). `fl_plugin_params` hides the rest. Kits, grooves and the map
  have no parameters, but kits and pieces can be set in the state text (see "Building kits through the state").
- The kit selector and the Settings menu are JUCE menus. They close as soon as FL leaves the front, which is the
  plugin's behavior, so the bridge can only reach them with `fl_click(..., focus=True)` on both the selector and the
  row. See "Working without focus" in `fl-studio-scripting`.
- In the E-Drums/MIDI In panel, the Velocity and Mapping tabs ignored posted clicks even with FL in front, while the
  panel's selectors answered. The map was read from renders instead.
- Choosing a kit loads its own mixer preset, `Basic Rogers` for Post-Rock.
- In REAPER 7.86 the kit selector took a real click on the selector and on the row, and Post-Rock loaded its mixer
  preset there too. The same MIDI rendered in REAPER came out 2.1 dB louder than FL's render in every band, with the
  same band profile and stereo, so match the level when moving a part between hosts. With the level matched, the two
  differed by -7.4 dB of residual against -13.5 dB between two REAPER renders, from different round robin samples.
- A new instance feeds the Master and follows the host tempo (`Follow Host` is on). It plays the notes it receives
  without anything in its own timeline.

## Separate outputs without the interface

Seen on 3.1.2 only (the state header reads `EZd3` followed by the bytes 03 01 02) in REAPER 7.86, with Post-Rock and
its Basic Rogers mixer. Check the state and the result again on any other version before relying on this.

- The plugin has 32 outputs, and its internal mixer is stored as text inside the state (`fx.state_get`). Each mic
  routes to a bus (`route buss N`). The buses come in left and right pairs (here Kick 0/1, Snare 2/3, Hi-Hat 4/5, Toms
  6/7, OH 8/9, Ambience 10/11, FX 12/13, a shared Comp 14/15 and a shared Reverb 16/17). Each one has its own effect,
  and the channels feed the shared pairs through `send 7` (Comp) and `send 8` (Reverb). Every bus pair, the shared
  ones included, had `route output 0`, which is outputs 1/2, and nothing processed the sum after the outputs.
- Changing that 0 to a single digit N for both halves of a pair moves the bus to output N (channels 2N+1 and 2N+2).
  A single digit keeps the state the same length. A longer edit has to move the size fields of the header too (see
  "Building kits through the state"). Leave the original state on the approved track and put the edited copy in a
  new instance.
- To hear the outputs in REAPER, give the instrument's track as many channels as the outputs use (`track.set
  channels`), turn its send to the parent off and capture each pair on its own track with a post-FX send from that
  pair (`send.add src_channel`).
- Moving nine pairs left output 0 digitally silent. The sum of the outputs matched the same kit rendered in stereo
  within 0.06 dB per section and 0.06 dB of band error, the same as two stereo renders. The shared Comp and Reverb come
  out on their own outputs, so the sum keeps the parallel compression and the reverb, and each channel keeps its own
  bleed. The outputs measured as expected (Kick centroid 59 Hz, Hi-Hat 8.8 kHz). The FX bus was silent in that song.
- The separated version is a new performance. Against an FL render of the same MIDI, both REAPER versions stayed
  within 0.16 dB per section but left -7 dB of residual from other round robin samples. Keep the approved render
  playing when its exact samples matter.
- There's no fixed offset between the hosts to correct. Correlating the band below 150 Hz over 15 s windows put the
  REAPER render -3 to +6 samples from the FL render depending on the window, against 0 to 2 samples between two REAPER
  renders. Above 2 kHz the two hosts correlated under 0.2, since the samples differ.
- Each render picks other samples, so outputs rendered in separate passes aren't one performance. Nine outputs
  rendered one per pass summed to -14 dB of residual against the sum rendered in one pass, close to the -10 dB between
  two whole renders. To get every output of one performance, render once to a multichannel master. Give the master as
  many channels as the instrument's track (`MASTER_NCH 20 2` in the .rpp, which the bridge doesn't set), leave the
  instrument's send to the parent on, drop the capture tracks, and render 20 channels (`render.configure` with
  `channels` 20, then `mps render --channels 20 --allow-nonstandard`). Each pair of the file is one output, and the
  pairs sum to the stereo performance of that pass.

## Building kits through the state

Seen on 3.1.2 in REAPER 7.86 with the core library, Post-Rock and the Percussion pack installed. Check again on any
other version.

### What the state holds

- `fx.state_get` returns a block with a little-endian size at byte 0, the JUCE wrapper's `VstW` chunk with big-endian
  sizes at bytes 28 and 180, the plugin's text from `PlugVersion 3.1.2` to a zero byte, and a short binary tail. In
  every state read, each size differed from the total length by the same constant (−16, −40 and −192).
- An edit of the same length loads as it is. An edit that changes the length loaded when all three sizes moved by the
  change in length.
- In a saved .rpp, REAPER writes the state as base64 lines that each decode alone, with a segment of its own before
  the plugin's block. The block starts 8 bytes before `VstW` and is as long as the size at its first byte plus 16, and
  the .rpp segment carried 6 more bytes after it. A block taken with REAPER's segment in front was ignored, and the
  plugin kept the kit it had.
- The text holds the whole sampler:
  - the library in `soundlib`;
  - one `instbox N "<position>"` per position, with `xpad 0 <library>`, the piece in `drum "<code>" "<tool>" 1`, and
    the pads with the mics each one uses;
  - the mixer (`mixer { <channel> { pan … volume … solo … mute … route buss N … } … buss N { … } }`);
  - `drumProps3`, with one `<instbox index> pitch <factor>` line per position;
  - the song and window settings, such as `DrumsMixerPresetName`.
- The mixer's effects are XML inside base64 chunks that name the modules, such as `TA_EQP1A`, `TA_TOONTRACK_EQ2`,
  `TA_LA2A`, `TA_CONSOLEEMU` and `TA_TAPEEMU`. Changing `active 1` to `active 0` turns a slot off, and `mute 0` to
  `mute 1` mutes a channel, both without changing the length.
- A new instance came up with the MainRoom's `Studio Basic` kit and mixer and the Percussion pack's Shaker, Tambourine
  and Oneshot positions. That mixer had an LA-2A on the overheads and console and tape emulation on a bus.

### Changing pieces

- Changing the code in a position's `drum` line changes the piece. A piece from another of the three core rooms loaded
  when the position's `xpad 0 <library>` changed with it. A render confirmed it (a kick moved from 45 to 51 Hz with
  another kick of the same room and to 38 Hz with one from another room), and the state read back showed the new code.
- Each code belongs to the position it was recorded in, given by its last two digits. `CRxx_01` goes in Crash1,
  `CRxx_02` in Crash2, `TOxx_01` to `TOxx_03` in the rack toms, `TOxx_04` and `TOxx_05` in the floor toms, and
  `RIxx_04` in Ride4.
  - Asked for another position, the plugin loaded the piece of the same room recorded there (CR03_01 asked in Crash2
    came back as CR03_02).
  - A code already used in another position was refused, and the old piece stayed.
  - So read the state back after each change.
- Each library's `soundDB` is an SQLite file with the codes and names (`SOUNDENTITY.Name`, joined by `SDXDrumID` to
  `SDXDRUMS.Name`, which is the code, and by `KitpieceID` to `KITPIECES`). The factory kit presets are text blocks in
  the library's `Configs`, each with a `kit { s3kit … }` list of position, library and code.
- A pitch factor of 0.8 on the kick's `drumProps3` line moved its fundamental from 45.1 to 37.5 Hz in a render.

### Note map of the core library kits

Measured in the MainRoom's `Studio Basic` kit by swapping one position's piece at a time and comparing a sweep of
notes 21 to 108 with the default render. Most were then confirmed by rendering the note with several pieces in that
position. Long tails change the following notes too. The cymbal and ride swaps also changed notes between 26 and 37
and above 83, which may be other articulations and weren't identified.

| Position | Note | Confirmed with several pieces |
|---|---:|---|
| Crash1 | 55 | yes |
| Crash2 | 49 | yes |
| Crash5 | 57 | yes |
| Crash6 | 95 | yes |
| Racktom1 | 48 | yes |
| Racktom2 | 47 | yes |
| Racktom3 | 45 | yes |
| Floortom1 | 43 | no |
| Floortom2 | 41 | no |
| Ride4 | 51, with 53 and 59 changing too | no |

- In these kits note 49 plays the position named Crash2, not Crash1.
- With the MainRoom's 15" Paiste 602 Heavy at velocity 110, the hi-hat answered notes 21 to 26, 42, 44, 46 and 60 to
  65. The time to fall 20 dB went from 32 ms (21 and 44) and 85 ms (42) to 224 ms (46), 421 ms (26) and 732 ms (60).
- The same note decayed differently on other hi-hats (46 took 435 ms on a Paiste 2002 Sound Edge 15" and 290 ms on a
  Paiste 2002 Big Beat 16"), so pick an open note by measuring the hat in use.

### Percussion pack

- The tambourine plays on note 3 and the shaker on note 2. The pack's `Configs` also lists a one-shot pad as note 1,
  which wasn't measured. Both instruments are shaken strokes.
- The velocity picks the stroke in six zones, read from the pads' `velrange` (1-21 `onE`, 22-42 `on2E`, 43-63 `on`,
  64-84 `off`, 85-105 `on2` and 106-127 `after`). Inside a zone it sets the level. On isolated notes the level rose
  about 1 dB per velocity step (the tambourine's `off` from −50.8 to −32.3 dB over 65 to 83, the shaker's `on2E` from
  −52.3 to −34.8 dB over 23 to 41).
- Timing, on isolated notes 2 s apart at 120 BPM:
  - Up to velocity 42 the sample starts at the note and peaks 6 to 24 ms after it.
  - From 43 up it starts after the note, 96 to 100 ms on the tambourine and 57 to 87 ms on the shaker depending on
    the zone, and peaks 100 to 140 ms after it.
  - In a song at 71 BPM, the tambourine's `off` zone started 74 to 82 ms after the note on hits after a rest, about
    20 ms earlier than in the probe, so measure the delay in the project itself.
- To land the strokes on time, write the notes earlier by the measured delay, then check the lag by correlating the
  energy envelopes with the target over the song. On a 16th note pattern a peak search can lock on the neighbouring
  stroke a 16th away, and hits after a rest settle it.
- Don't measure the delay with dense notes. With 250 ms between notes, each note's delayed sample fell in the next
  note's window, and the measure read as an advance of 35 to 48 ms.

### Repeatability

With the core library, two renders of the same state and MIDI, made in separate render processes at different times,
were identical sample by sample (a whole-song kick part and hi-hat part). Blocks of the same piece in renders whose
kits differed in other positions stayed within −70 dB of each other. That differs from the Post-Rock renders above,
which left −10 to −13.5 dB of residual between two REAPER renders, so check repeatability per library before relying
on it.
