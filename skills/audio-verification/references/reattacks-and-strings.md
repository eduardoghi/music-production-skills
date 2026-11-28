# Re-attacks, sustained notes and strings

Read this when a transcription may be missing re-attacks of notes already sounding, or when the guitar string that
played a note matters. The numbers come from one guitar part and its renders, as examples, not thresholds.

A transcription that gives almost every note the same length, from one attack to the next, may be cutting sustained
notes at each attack and missing re-attacks of notes already sounding. In one guitar part, 35 of 110 transcribed notes
continued the previous note of the same pitch with no new attack, while the recording had about twice as many attacks
as the transcription, many on sixteenth offbeats.

- Count attacks in the recording itself, from the spectral flux of the percussive part (HPSS) above 2.5 kHz, and
  compare their number and the intervals between them with a render of the transcription.
- To tell which known pitch was re-attacked, compare the level of its fundamental band after the attack with the
  minimum just before. On a render with known notes, a rise of 3 dB was right for 87% of the re-attacks it found and
  found 62% of them, and a rise of 1 dB was right for 84% and found 83%.
- Don't search every pitch this way. The pick's transient raises every band at once, and measured at the attack the
  search invented hundreds of pitches on the known render. Measured in the sustain, 60 to 140 ms after the attack, and
  requiring a tonal peak, it still invented about one pitch per attack, scattered over unrelated intervals. Pitches
  missing from a transcription need another source, such as a polyphonic editor.
- An octave above a note sounding at the same time can be the lower note's second harmonic read as a note. Compare the
  even-to-odd harmonic ratio of the lower note with a calibration of that note alone, since a real upper note raises
  the even harmonics well above it. The test only works one way, since a weak real note passes as a harmonic.
- To find the note each attack sounds, against the notes still ringing, compare the spectrum right after the attack
  with the one right before and take the pitch that appeared, summing its harmonics. For its octave, compare the rise
  of the fundamental in each candidate octave (frames centred 60 to 150 ms after the attack against 70 to 50 ms
  before), asking for at least 6 dB. When only the upper octave rises, the struck note is the upper one. The
  measurement worked, though the reading of the part built on it wasn't approved by ear.
- Deciding palm mute per note from the early decay settled only 14 of 57 notes, since a muted and a normal note
  decayed almost alike before the next attack in the other 43.

## A new attack or the gain coming back

A dip in the envelope of a sustained note can be the string played again or the part's gain recovering after a drum
hit, from a compressor or a sidechain in the original mix. Both show a fall and a rise at the same place.

The phase of the fundamental is evidence between the two, not proof.
1. Band-pass the stem from 0.85 to 1.15 times the fundamental (second order, forward and backward) and unwrap the
   phase of its analytic signal.
2. Fit a straight line to the phase from 100 to 30 ms before the dip and extend it to 40 to 100 ms after.
3. Take the circular mean of the difference there, from 0 to π radians.

A change of gain leaves the phase where the line puts it. A string played again usually starts over at another
phase, but it doesn't have to start at a random one, so a continuous phase leans toward a gain change without ruling
out a new attack. The line assumes a steady pitch, so slides and bends break the test.

What it gave on one bass line, in two separated stems, as an example:
- **Controls.** Points inside sustained notes, away from attacks and drum hits, deviated by a median of 0.04 rad
  (90th percentile 0.10) in one stem and 0.11 rad (0.36) in the other. Drum hits inside sustained notes, away from
  slides, reached 0.68 rad.
- **Dips read as attacks.** Of 62 dips that the envelope had taken as new attacks of the same note, 24 kept the phase
  (up to 0.25 and 0.45 rad in the two stems) with a kick or snare from 20 ms before to 80 ms after, 4 kept it with no
  hit nearby, 17 jumped by 0.75 rad or more in both stems and 17 stayed undecided.
- **Repeats after a gap.** Of 79 repeats of one pitch after a short gap in the pitch track, 48 jumped. That those
  mostly read as new attacks is what gave the test some weight.
- **Rise time.** The time to rise to 90% of the following level didn't separate the cases. Attacks that started with
  a drum hit were ducked too and took about 120 ms. The time to 50% separated them better, as a second clue.

Merge the dips that kept their phase at a drum hit into the note before, keep the undecided ones as they were, and
record the class and the measures of each in the transcription, so a later listening can undo any of them.

## Which string played a note

The same pitch on different guitar strings has a different pattern of harmonics, which can suggest the string a
recording used. It worked as a suggestion with confidence, never as a certainty.

1. Render a calibration with the instrument that will play the part, with each pitch of the part alone on every string
   that reaches it, twice.
2. Take each note's profile as the level of harmonics 2 to 8 relative to the fundamental, from 40 to 250 ms after the
   attack, so the pick transient stays out.
3. Compare profiles after removing a straight-line tilt over log2 of the harmonic number, which is what a broad EQ, a
   pickup or a clean amplifier changes. Leave out harmonics within 3% of a partial of another note sounding at the
   same time, and skip notes with fewer than four left.
4. Keep only suggestions whose best string is clearly ahead of the second, and let the fingering's physical
   constraints overrule them.

Measured on one sampled guitar. Each calibration repeat classified by the others was right for 73 of 74 notes. On a
render with known strings, notes whose second-best distance was at least twice the best were right for 20 of 20 dry
and 19 of 21 after synthetic high cut, saturation and reverb, while all notes together were right for 71 to 75%. A
real recording can hold processing or layered takes that this test doesn't cover, and in a dense part few notes start
alone, so expect suggestions for a minority of notes.
