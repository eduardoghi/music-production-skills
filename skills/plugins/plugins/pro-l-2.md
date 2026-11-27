# FabFilter Pro-L 2

Observed in REAPER 7.86, VST3, set through `fx.set_param` by the text each parameter shows, on one mix rendered offline.

## Parameters

- The host sees `Gain`, `Style`, `Lookahead`, `Attack`, `Release`, `Channel Link Transients`, `Channel Link Release`,
  `Oversampling`, `True Peak Limiting`, `Dithering`, `Noise Shaping`, `Unity Gain`, `Output Level` and the meter and
  loudness display settings, by those names.
- A new instance read `Modern`, oversampling off, `True Peak Limiting` on, dithering off and `Output Level` 0.00 dBTP.

## Output Level lowers everything

- **Measured behavior.** `Output Level` set to −1.00 dBTP lowered the whole signal by 1 dB, besides capping the true
  peak there. In three masters with nothing else in the chain, a render with `Gain` equal to the loudness gap came out
  1.0 LU short (1.2 LU with a −1.2 dBTP ceiling), with almost no limiting. So the input gain for a loudness target is
  about the gap plus the distance of the ceiling below 0.
- **Calibration.** The loudness after limiting depends on the material, so measure the render and correct the gain.
  Two renders reached the target within 0.05 LU on each try.

## MP3 overshoot

- **The overshoot.** A master limited to −1.00 dBTP with true-peak limiting and 4x oversampling, encoded to MP3 320
  kbps CBR by LAME through ffmpeg, decoded at −0.975 dBTP measured at 8x. That is 0.025 dB above the ceiling, in two
  oversampled samples.
- **The fix.** A copy limited to −1.2 dBTP, with the gain raised 0.2 dB to keep the loudness, decoded at −1.16 dBTP. So
  decode the MP3 and measure its true peak before calling it within the ceiling, and keep the lossless master at its
  own ceiling. A second master made the same way decoded at −1.07 dBTP, so the margin varies with the music.

## Judging its gain reduction offline

The meter isn't readable through the host. Compare the render with the pre-master times the effective gain (the Gain
minus the drop from Output Level), in 5 ms windows, after checking that the delay between them is 0 (REAPER compensates
the lookahead). Report the maximum reduction, the share of time above 1 dB, where it acts, the median change on kick and
snare hits, and the LRA and PLR. Transparent at 4x with the gain set for −17.3 LUFS on one mix reduced at most 2.6 dB,
more than 1 dB in 0.07 % of the time, and left the hits unchanged (−0.01 dB).
