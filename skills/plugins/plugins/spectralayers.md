# SpectraLayers (Steinberg)

Observed with SpectraLayers used by a person on one guitar stem, with the results exported as files. REAPER's
scripting API has no ARA access (see Known limits in the `reaper` skill), so an agent works with what is exported.

- **Unmix Components.** The manual for version 13 describes two layers, tonal and noise. The processing produced
  three, Tonal, Noise and Transient, as 32-bit float stereo WAVs aligned with the input. Their sum reproduced the stem
  at −138.8 dB, so the split loses nothing and the layers can be used as targets.
- **What each layer held.** The pick's highs were in Transient, and separation noise dominated all layers above
  8 kHz. Tonal plus Transient below 8 kHz worked as the target for a guitar chain.
- **Pitched content in Noise.** A dense rhythm centred on one pitch showed up in Noise and not in Tonal. It looked like
  a quiet saturated guitar, but a second guitar built on it was refuted once the approved guitar went through the same
  separators. Treat it as a hypothesis to test, not as a part.

How to use the layers to locate a mismatch is in `references/separated-stems.md` of the audio-verification skill.
