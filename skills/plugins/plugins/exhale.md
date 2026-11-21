# EXHALE (Output)

Observed in REAPER 7.86 with Kontakt 8 Portable 8.14.1, on one installed copy of the library and its Ambient, Barely
and Indie Vocals expansions. The library's own version wasn't read, and the manual wasn't read for this note.
Loading through Kontakt is in `plugins/kontakt.md`.

## Where things are

- `Instruments/EXHALE.nki` is the instrument.
- `Snapshots/EXHALE/` holds one folder per group of presets, as Kontakt snapshots (`.nksn`) named like the presets.
  There were folders for the factory Notes presets (in two folders), Loops and Slices, and one per expansion.
- `Library Data/Exhale Presets/` holds the same presets as `.nka` files, with a prefix for the expansion in the name
  (`AMB`, `BLV`, `IND` in that copy).

## Loading a preset

A `.nksn` typed into Kontakt's Load dialog loaded EXHALE with that preset, and the instrument header showed the
preset's name with its prefix, such as `IND 07. Plush Pad`. Capture the header to confirm which preset loaded.

## Telling the engines apart

Notes presets play a sustained, pitched sound per key, while Loops and Slices are rhythmic. Before rendering
candidates for a pad, keep only Notes presets.

The metadata in `Library Data/Exhale Meta Data/` is Kontakt array text. Each `.nka` file starts with the array's name
and then has one value per line, in the same order across files. `name.nka` holds the preset names, `n.nka` their
count and `categories.nka` one integer per preset.

**Observed in that copy, possibly different in other versions.** The three `Init` presets had one high bit each in
`categories.nka`, 2^28 for Notes, 2^29 for Slices and 2^30 for Loops. Read that way, the copy held 451 Notes, 126
Loops and 126 Slices presets, which matched the number of snapshots in the Loops and Slices folders, and none of the
Barely Vocals presets were Notes presets. The lower bits weren't decoded. Check the `Init` presets again before relying
on these bits in another version.

## Choosing a preset for a layer

Names don't say how a preset sounds. What worked was to render each candidate alone on the same notes and compare
measures of the renders, without treating any value as a standard:

- **Harmony.** Chroma energy in pitch classes outside the song's scale. Some presets stack fifths on each note, which
  stays inside a major scale, so counting every class other than the ones played overstates the problem.
- **Motion.** The variation of the level inside each note, after its attack, and the strongest amplitude modulation
  between about 0.5 and 12 Hz, which shows pulsing.
- **Attack and brightness.** The time to reach the note's level, and the spectral centroid with the energy above 5 kHz.
- **Mono.** The correlation between the channels. One preset had a negative correlation and would lose much of its
  level in mono.
- **Words.** A local speech recognizer on each render. A recognizer can invent text on sounds without speech (one pad
  came back as a copyright line), so treat isolated, implausible text as a hallucination and listen when in doubt.
