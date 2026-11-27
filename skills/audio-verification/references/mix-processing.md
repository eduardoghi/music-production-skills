# Processing and masking in a mix

Read this when a processor's effect on a part has to be judged, or when a part gets lost in a mix and the question
is which other part covers it and where.

The examples come from one vocal mix over a band and from one instrumental rebuilt against a finished master. Their
values show what the measures can say, not targets.

## Judging a processor at the same level

A processor that raises the level also seems to add what is asked of it, such as presence or warmth. Render the same
chain once more with the processor bypassed (a bypass variant of the project), match the integrated loudness of the
two renders, and compare their band levels after the match. On one vocal, a saturator after the compressor raised the
loudness by 1.2 LU. Matched, three settings moved the 1 to 4 kHz band by −0.4 to +0.05 dB, and one of them added
1.3 dB above 8 kHz, which is brightness rather than presence. It added nothing the EQ wasn't already doing, and it was
left out.

- Compare in the same windows and with active frames chosen the same way, since a gate or long rests weigh on the
  integrated value.
- Judge the processor in context too, by the measure the decision is about (such as the part's presence against the
  rest of the mix, below), with the level of the part matched between versions.
- Several renders of each version are needed when the chain has modulated effects (see Comparing versions in the
  skill).

## Finding what covers a part

Render each top-level group of the project alone, with the same render settings. Variants of the saved project with
the other groups muted are enough, and each one should render to its own absolute path (see the render notes of the
REAPER skill). Before using them, check that the groups add up to the full mix. Modulated reverbs and delays limit how
close the sum gets, so compare the residual with the spread between two renders of the full mix. Both were about
−15 dB in one mix.

Then, for each phrase of the part, take its active frames (50 ms frames within 25 dB of the phrase's loudest) and
the part's level minus each group's level, band by band:

- The group that sits highest in the bands that carry the part's words (for a voice, roughly 600 Hz to 5 kHz) is the
  first place to make room. In that mix the guitars sat 13 to 20 dB above the voice from 600 Hz to 1.2 kHz in most
  phrases, the drums mattered only from 2.5 to 5 kHz in the chorus, and the bass and keys barely competed.
- A gap of 10 or 20 dB isn't closed by a few dB of EQ on the group. Measure the part's own presence (below) after each
  change instead of trying to close the gap.
- The same per-band levels across the takes of one part show which take is darker or brighter than the others. Part
  of that difference is the vowel sung, so correct by take rather than phrase by phrase, and only partly.

## Making room only under the part

A static cut on the covering group changes it everywhere, including where the part rests. An EQ band on the group
automated to dip only within the part's windows (a little before each phrase to a little after, with ramps of about
150 ms) leaves the group untouched elsewhere. In that mix, dips of 2 to 3.5 dB at 2.5 kHz and 1 to 1.5 dB at 1 kHz on
the guitars, and 2 dB at 4 kHz on the drums in the chorus only, cost the instrumental about 0.5 LU in those sections
and nothing elsewhere.

To see the effect, measure the part with its returns against everything else from 1 to 4 kHz, as the median over the
phrase's active frames, before and after. Echoes of a delay that enter at the end of a phrase raise that measure there,
so note where returns overlap the phrase.

## Mixing against a finished master

When the reference is a released master, part of what separates it from a mix is its mastering.
- Compare at one gain that matches the integrated loudness, and set aside what the master did. The reference had a
  crest factor 2 to 6 dB lower per section, a PLR of 13.5 against 18.8 dB, different peaks and LRA, and probably a sub
  cut, all from its mastering. The mix didn't imitate them, and they were measured again after limiting.
- Measure the sum term of kick and bass before claiming they cancel. A low cut on the bass was once discarded because
  "the subs partly cancel". The measured term was +0.7 dB on average from 20 to 40 Hz, so they added, and bar by bar it
  went from −2.6 to +2.3 dB depending on whether the bass note fell in phase with the kick. A term that changes sign
  with the note can't be fixed with one delay.
- EQ can't create energy the source doesn't have. A boost at 75 Hz didn't restore a kick resonance the sample lacked,
  and a deficit from 600 Hz to 1.2 kHz came from notes transcribed an octave low. On a guitar that needed more upper
  harmonics, a cut at 400 Hz before the saturator worked, so the saturator generated them, while a bright shelf alone
  overshot above 2.4 kHz and an EQ on the mids alone made it darker.
- A reference whose brightness changes by section may need production that changes by section. The reference's level
  above 4.8 kHz moved from −40 to −23 dB between sections, while each fixed chain stayed between −30 and −35 dB.
  Switching chains per section, with 0.25 s crossfades starting 30 ms before the downbeat, and feeding reverb and delay
  after the switch so their tails carry across, followed that contour.
- Measure width in windows tied to the notes, in the direct sound (0 to 60 ms after each attack), the reflections (60
  to 250 ms) and the tails, along with the tail's level against the direct sound. This showed a guitar narrower than
  the reference in its direct sound itself, by 2.6 dB in the climax, rather than short of reverb. To find what sounds
  in a pause, measure each return inside it. One tape delay return was the source, so only that return was automated.

## Limits

- Every number depends on the bands, the frame length, how active frames are picked and the gain matching. Report
  them with the result.
- These measures say where the part competes, not whether it sounds clear. Clarity and taste are for listening.
