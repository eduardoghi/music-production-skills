# Vocal takes against a guide

Read this when a sung take has to be placed against a guide vocal and the song's timeline, identified, checked for
pitch and notes, tuned without changing the performance, or cleaned of plosives.

These come from one take sung along with a generated guide, an octave below it and with no processing, as examples
of what to check.

## Placing the take

- **Put the guide on the project's timeline first.** A guide's own accompaniment can run against the project's
  timeline even when the arrangement is the same. Correlate the spectral flux of the guide's accompaniment with the
  project's reference over the whole song, then refine on the waveform below 200 Hz. One set of stems ran 0.444 s
  ahead of the project. Stems exported together share their timeline.
- **Measure the offset where the phrases are.** Correlate in windows along the song before trusting one value. One set
  of stems held within 17 ms of its offset over the whole song, and another, from a different generation of the same
  song, drifted by about 55 ms from start to end. Phrases near the end needed windows measured there. Interpolate
  between window centers, and measure new windows instead of extrapolating past the last one.
- **Align by pitch class, not by level.** A take in another octave and timbre doesn't match the guide's envelope
  well. One level envelope gave phrase offsets that disagreed by up to 500 ms. Track f0 on both (torchcrepe worked),
  turn each voiced frame into a 12-class pitch vector, which ignores the octave, and correlate the two sequences at
  every lag. The peak stood clear of the next candidate (0.32 against 0.21) and agreed with the level envelope's best
  lag within 20 ms.
- **Align a whole recording by its notes.** A correlation over a whole take landed far from the right place because
  a long melisma skewed it, and aligning by the note onsets fixed it.
- **Spot a recorder's gate.** A phone or recording app can gate the take, leaving digital silence between phrases and
  cutting the ends. One word fell from −45 to −80 dBFS in about 0.15 s, against about 0.7 s for a natural decay. A cut
  end can't be restored, so ask for a new take.
- **Correct phrases only when methods agree.** Melody repeats in a song, so a short phrase can lock onto the wrong
  place. In the take, the long phrases sat within −80 to +70 ms of the guide, while some short ones gave 400 to
  600 ms by one method and much less by another. Shift a phrase only when its offset holds across methods. Otherwise
  keep the global offset and leave the phrase to listening.

## Which line a take sings

When a take could hold more than one line (lines that share a melody, a file that may be a duplicate, a take that
starts mid-phrase), check the words before the melody. Compare file hashes first, since two names can hold the same
recording.

- **Transcribe both.** A local recognizer (faster-whisper with a medium English model worked) on the take and on the
  guide over the same region gives words with start times. The guide's voiced runs can merge two lines, so cut the
  guide's lines by its words, not by its pauses alone.
- **Start from the words, then refine.** The median of the differences between the start times of the words both
  share gave a starting offset. Leave out the first word of a file, whose start the recognizer often misplaces. Then
  refine with the pitch-class alignment above in a narrow window. When the automatic alignment ends at the edge of its
  search, or disagrees with the words, compare the onsets of the long notes with the guide's.
- **Choose an anchor and say so.** A singer can stretch the start of a phrase and land its long note where the guide
  does. Anchoring on the long or stressed note and anchoring on the start can differ by a few hundred milliseconds.
  Pick one, report the other, and leave the choice to listening.
- **Limits.** On a low sung voice the recognizer swapped short words ("it" for "you") and words that sound alike. A
  different transcription isn't evidence of different lyrics, and the singer's word settles it. Giving the expected
  lyrics as a prompt and comparing the confidence of each word separates a doubtful word from a clear one, but the
  confidence doesn't measure how clear the word sounds to a listener. On sounds without speech, recognizers can
  produce whole phrases that were never there.

## Pitch and notes

- **Tuning.** Measure tuning against the nearest semitone, on the middle 60 % of each note, so the scoops at the ends
  don't count. The take had a median deviation of 16 cents, and only 5 notes of 250 ms or more were over 25 cents.
- **Notes that differ from the guide.** With the octave removed, a note that sits on a semitone but far from the
  guide's note is a different note, not bad tuning. Check which note the harmony supports with the accompaniment's
  chroma at that moment. Of nine notes that differed from the guide, four had the guide's pitch class clearly stronger
  in the accompaniment (1.00 against 0.30, for example). Those are questions for a new take, and tuning shouldn't
  move them.

## Tuning without changing the performance

- **How.** Shift whole notes, not frames. Praat's PSOLA through parselmouth (`To Manipulation`, multiply the pitch
  tier over each note with ramps of about 40 ms, `Get resynthesis (overlap-add)`) keeps the formants. Because the
  whole contour of the note moves by one factor, the vibrato, the entry and the exit stay as sung.
- **Where.** Take only the corrected notes from the resynthesis, with short crossfades where the factor is still 1,
  and keep the rest of the take sample for sample.
- **Measured on 5 notes corrected by 75 % of their deviation.** They went from −40 to +46 cents to −16 to +2 cents.
  The vibrato changed by at most 3 cents and the level by at most 0.2 dB. The resynthesis left a small coloration in
  those notes, up to −1.6 dB between 800 Hz and 6 kHz, which is worth reporting.
- **Check the two versions.** Run them through the same chain and compare them outside the corrected notes. With the
  same compressor and de-esser, the two differed by −86 to −90 dBFS there.

## Which notes to touch (an experimental method)

Use this to decide what to look at, not as a rule for what to correct. The numbers are working values from one
project, and none of them makes a correction musically right. Always offer the untouched version next to the tuned
one.

- **A measured note may not be a note.** Segmenting by pitch runs merges glides, turns and bends with the notes around
  them, so a "note" whose median sits 40 cents off can be a slide that never stops there. Read the f0 in short windows
  (100 ms worked) before deciding.
- **Sort what's found.**
  - A stopped note keeps its f0 near one value. What was used: the range from the 20th to the 80th percentile inside
    the note, without its first and last 40 ms, at most 60 cents, and the medians of its two halves within 50 cents.
  - A glide or turn crosses semitones on its way. It is part of the performance, so leave it.
  - A passing note is short and leads to the next one. Leave it.
  - A note that sits steady on a semitone other than the guide's is a melodic choice. Judge it against the harmony,
    not as tuning (see Pitch and notes).
- **Short notes fool the statistics.** With the ends trimmed, a falling note of 0.2 s had few frames left and passed
  both tests. Look at its frames.
- **Choose the target from the music.** The nearest semitone isn't always the note the line aims at. A note held
  between two semitones would have gone to the wrong one by that rule. The line settled on the other one right after,
  and other takes sang it there. Check where the line settles, which pitch classes the accompaniment holds at that moment, and
  how other takes sing the passage. When they disagree, leave the note alone.

## Plosives and handling noise

- **Tell a burst from the voice.** A low voice's fundamental can sit near or below 110 Hz, so energy from 20 to 80 Hz
  also rises on sustained low notes and flags them as plosives. Compare the band below about 100 Hz with the band
  above about 150 Hz in 10 ms windows. A plosive or a handling bump shows the low band well above the upper one for
  tens of milliseconds, without a pitch.
- **Check the chain's own filter.** A vocal low cut placed below the lowest sung note leaves most of a burst at 80 to
  90 Hz in place, so measure the burst after the chain.
- **Treat it where it is.** When the bump lies before the singing, move the item's edge. When it is part of a word,
  filter only that span in a copy of the take, with short crossfades, and keep the rest identical to the original.
  One take used a high-pass at 150 Hz over each "p", which brought the low band of the burst near the other phrases'
  level in the mix. That cutoff isn't a rule. It depends on the lowest sung note and on what the consonant carries,
  and a filter can thin the consonant, so measure it in the mix and listen.
