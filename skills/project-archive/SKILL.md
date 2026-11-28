---
name: project-archive
description: Clean up a music project as decisions are approved, and archive and validate it when it is paused or finished, so it can be reopened later without losing approved work. Use when a decision has been consolidated and its rejected candidates pile up, when a song is being paused or closed, when a work area has grown with renders and tests, or when a project has to move to an archive drive, before deleting anything.
---

# Archiving a music project

A work area collects far more than the song needs, such as rejected rounds, render variants, separations nobody
chose, listening packages and their ZIPs. Archiving keeps what is needed to reopen and continue the work, proves the copy
works, and only then deletes the work copy. One REAPER project of about 82 GiB (12 000 files) became a 2.8 GiB archive
this way. Nothing is deleted before the archive is validated. The numbers here come from that one project, as
examples of what to expect, not targets.

## Cleaning up during production

Most of an archive's waste can go earlier, one decision at a time, under these rules:
- While a decision is open, keep every candidate, its render and its recipe, even when one looks ahead.
- Once the listener has approved a candidate, it has been consolidated into the working project or a checkpoint, and
  that checkpoint has been validated (rendered and checked against the approved renders), delete the audio of the
  rejected candidates (renders, variants, measurement parts, and listening packages with their ZIPs).
- Keep the stage's notes, recipes, measurements and render records, so a rejected candidate can be rebuilt from its
  recipe if it is ever needed, and keep the alternatives the listener chose to keep.
- Never delete a file another record, project or note cites. Check that first, as in the inventory below.
- Log each deletion (path, size, hash, stage and reason) in the stage's folder.

## 1. Inventory before deciding

- Measure each folder and each file type. Large totals usually come from render runs, variant projects (each one
  carries every plugin state, so they reach megabytes), listening packages, and ZIPs that repeat a package folder.
- Pick the projects worth reopening. These are the final mix and master, the approved reference version, the
  checkpoints that record a consolidation, and the alternatives the user explicitly kept. Read each one's `FILE` lines and resolve them
  (relative paths from the project's folder, and allow for unquoted paths) to get the exact set of media they need.
  In one project the 16 projects worth keeping needed only 31 media files.
- Match only lines that start with `FILE`. A pattern without that anchor also catches `RENDER_FILE`, which is where a
  project renders to and not media it reads. In one cleanup plan that kept four render outputs as if a project needed
  them.
- For each approved render, find the project that produced it from its render record (`.render.json`, `project.path`).
  Instrument projects that play MIDI into a sampler can render the part again, so keep them too, with their own
  media (a re-amp project needs its DI).
- Search the rest of the disk for references to the work folder (records of other projects, READMEs, config comments).
  A test elsewhere may cite files inside it.

## 2. Classify every file, in writing

Write the rules as code and run them in a dry run first. Record for every file its decision (kept, duplicate or
discarded), its destination and the reason, in an inventory CSV that goes into the archive.

| Keep | Discard |
|---|---|
| projects worth reopening and the media they read | renders of rejected rounds, variants, measurement parts |
| delivered masters and their 32-bit float renders, approved stems | separations that weren't chosen, intermediate separations |
| definitive MIDI and every saved plugin state | ZIPs of package folders, packages of rejected rounds |
| original source audio, the chosen reference stems, the user's takes | test projects and render variants |
| alternatives the user said to keep | waveform peaks, automatic backups, logs, caches that regenerate |
| every stage's notes, recipes, measurements, records and local scripts (text, small) | |
| related files outside the work folder (another DAW's project, published files) | |

- Totals of the discarded files by folder show quickly whether something approved fell on the wrong side.
- Remove exact duplicates by SHA-256 (above about 1 MB is enough), keeping the copy in the most central folder, and
  leave a short note in each folder where a copy was left out, saying where it is.
- Keep the stage notes at their original relative paths (`historico/<old path>` or similar), so references between
  notes still make sense and old paths map to new ones directly.

## 3. Lay out the archive

- One folder for the projects, with the media in a `Media` subfolder, and each project's `FILE` lines rewritten as
  paths relative to the project. REAPER resolves those from the project's folder, so the archive can move. Name media
  after what they are.
- Point each project's render target to a new file in an empty folder of the archive, so a render from the archive
  can't overwrite anything. The `mps render` command refuses a relative `RENDER_FILE`, so this one stays absolute.
- Check that each rewritten project differs from the original only in its `FILE` and `RENDER_FILE` lines. Every plugin
  state and envelope then stays exactly as it was.
- At the root, a `LEIA.md` or README with the state, how to reopen, the approved decisions in order, where to resume,
  the validation, what was discarded, and the external dependencies. Add a plugin manifest with the plugin names and
  binary files from the projects' `<VST`/`<JS` lines, the binary versions from the render records, and, by hand, the
  libraries, presets or patches and where each state is stored. Add a file manifest with size, SHA-256 and origin of each file.

## 4. Copy and verify

- Put the archive on the drive meant for archives, usually a large HDD, and say the drive type when proposing it.
- Copy, then hash each copy against its source. Hash the whole archive again at the end, after the last edits, and
  compare with the copy-time hashes.

## 5. Validate in REAPER

- Render the archived projects themselves with `mps render` (a separate process). A missing media file stops the
  render at REAPER's dialog or in `mps render`'s own check, so a clean render also proves the references. Compare each
  render with the original, judged against what repeats normally:
  - a master behind a limiter came out bit-identical (the difference was exactly zero, and the measure's floor read
    −281 dB), while a bass chain without modulation left a residual of −110 dB, negligible but not zero. Report which
    of the two a comparison gave rather than calling both identical;
  - mixes with modulated reverbs matched in loudness per section within 0.12 LU, with a residual of about −14 dB, the
    same as two renders of the original;
  - sampler instruments with round robin or humanization matched in loudness only.
- Open the main projects through the bridge and check that the number of loaded effects equals the `<VST`/`<JS` lines
  and that none is offline.
- Export each MIDI item with `midi.read` to a `.mid` file per track, and read the files back to compare note counts.
- Keep the render records and comparisons. Delete the validation WAVs, which only served the comparison.
- Real-time playback isn't covered by an offline render. Say so if it wasn't tested.

## 6. Scripts

Archived scripts usually hold absolute paths to the work folder that is about to disappear.
- Replace them with a constant read from an environment variable whose default is relative to the script, such as
  a restored work area inside the archive. Tool locations (environments, the bridge checkout) can take their own
  variables with today's paths as defaults.
- Add a restore script that rebuilds the old layout from the inventory (kept files and duplicates back at their old
  relative paths, archived projects with `FILE` lines pointing at the restored media). A restore brings back only
  what the archive kept. Discarded intermediates don't come back, and a script that reads one fails until it is
  regenerated by rerunning the script that made it. Say so in the archive's notes. Copy rather than hard-link, so
  a script that rewrites a file doesn't change the archive.
- Check the rewrite by parsing every file and running a linter for undefined names, then re-run one deterministic
  script against a partial restore and compare its output with the archived one.
- Keep the originals in a ZIP inside the archive.

## 7. Delete, then clean the rest

- Delete the work copy only after the validation, with no DAW instance holding its files.
- On a ReFS Dev Drive the free space appeared only some seconds after the deletion. Read it again before reporting.
- In Documents, Downloads and similar folders, remove a project file only when an identical copy (same SHA-256) is in
  the archive. A ZIP counts when every member is. Archive the project files that have no copy first. Leave unrelated
  and personal files alone, and write a log of what was removed and where its copy is.
- Move evidence that another project's records cite next to those records and update the paths, keeping the old
  project hash in the record.
- Update notes and memories that pointed at the old paths.

## Things that went wrong once

- Restoring into a long folder failed on names past 260 characters on Windows. The `\\?\` prefix fixed it.
- A 48 kHz render is outside the render standard, so it needs `--allow-nonstandard` explicitly.
- Loudness of a window where an instrument is silent has no value. Comparisons per section have to skip it.
- The first classification missed a DI that a re-amp project read, found only because every kept project's media was
  resolved before copying.
