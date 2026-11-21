# Processing and masking in a mix

Read this when a processor's effect on a part has to be judged, or when a part gets lost in a mix and the question
is which other part covers it and where.

The examples come from one vocal mix over a band. Their values show what the measures can say, not targets.

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

## Limits

- Every number depends on the bands, the frame length, how active frames are picked and the gain matching. Report
  them with the result.
- These measures say where the part competes, not whether it sounds clear. Clarity and taste are for listening.
