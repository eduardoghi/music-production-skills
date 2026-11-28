# PRISM (Aurally Sound)

Audio to MIDI transcription. Observed on version 1.2.01 (VST3 with an ARA factory) in REAPER 7.86 on Windows. The
official documentation is at docs.aurallysound.com/prism.

## Using it with ARA in REAPER

- Insert it as a track effect. It analyzed the audio item on the track by itself, with no capture step, as soon as it
  was added.
- Every PRISM window shows one shared ARA document. The `Track:` selector at the top decides which track the window
  edits, analyzes and exports, whatever track the window belongs to. A window opened on one track came up showing
  another. Pick the track in that selector before changing the algorithm or saving.
- The algorithm selector (`Algo:`) offers `general`, `guitar dist` and `grand piano`. Changing it reanalyzes the
  selected track at once, and the choice stays with that track.
- The host sees only five parameters (bypass, wet, delta), so the track, the algorithm, the sensitivity and the export
  can't be reached as parameters.

## Controlling the window

- The window is drawn with JUCE and ignored posted clicks on `SAVE MIDI`. Real clicks worked on the buttons and on
  both selectors, but they move the user's pointer.
- Windows UI Automation reaches the same controls without touching the pointer. Observed with pywinauto's UIA backend
  on 1.2.01 in REAPER 7.86.
  - Under the REAPER window's `reaperPluginHostWrapProc` pane, the plugin is a `Custom` element named `Prism`. Its
    `Track:` and `Algo:` selectors (and `Snap:`) are `ComboBox` elements with the ExpandCollapse and Value patterns,
    so Value reads the current track and algorithm.
  - Expanding a selector opens a popup whose entries are `MenuItem` elements (`general`, `guitar dist`, `grand
    piano` for the algorithm). Invoking an entry selects it, and the selector's Value then reads it.
  - JUCE reuses the popup window from an earlier expand. Looking only at windows created after the expand found no
    entries the second time, so search every window of the process and keep the visible `MenuItem` elements.
  - `Save MIDI` is a `Button` with the Invoke pattern, and invoking it opened the save dialog below.
  - The cursor position read the same right before and right after each call.
- To export one track, pick the track, then the algorithm, and wait until two captures of the window taken 3 s apart
  are the same (at least 20 s after a change of algorithm, while it reanalyzes). Then invoke `Save MIDI` and fill in
  the dialog as below. Four exports (two stems, two algorithms) ran this way with no real input.

## Saving the MIDI

- `SAVE MIDI` opens a standard Windows save dialog (`Select file to save midi to`) in Documents, with the track name
  as the file name and the `.midi` extension.
- Setting the text of the edit with control ID 1001 didn't change the name. The file was saved under the default name.
- Typing with real keys was unreliable. A select-all didn't select, and the path landed after the default name.
- What worked was finding the edit that holds the default name, replacing its whole text with `EM_SETSEL` and
  `EM_REPLACESEL`, reading it back, and only then pressing `Save`. Check the name before saving every time.
- The file had 960 ticks per quarter note, the project's tempo and time signature, and note times counted from the
  start of the audio item, not of the project.

## What the general algorithm gave on a bass

On a separated bass stem of two minutes with mostly repeated eighth notes:

- It found 280 notes and split repeated notes of one pitch about as often as an envelope-based segmenter did (77 % of
  the attacks within 50 ms).
- It read 13 notes a semitone low (F2 and G2 where three pitch trackers, Melodyne and the EZbass tracker all read F#2
  and G#2). Check its pitches against another tracker before using them.

## What it gave on a polyphonic guitar

- The `guitar dist` model, run on the whole separated guitar stem and used with no correction, was the first
  transcription a listener accepted as the part (see `references/transcription.md` in the audio-verification skill).
- It followed the reference's pitches better than `general` in most sections (chroma 0.89 against 0.86 in one, 0.92
  against 0.87 in another, a tie in two), but it plays some notes an octave below the recording, which leaves a gap
  in the upper midrange that EQ can't fill.
