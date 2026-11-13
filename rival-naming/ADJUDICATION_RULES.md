# Adjudication rules: rival-naming study

Committed before the second labeler's labels were seen.

## Labelers
- Labeler 1: GnomeMan4201. Labels committed as a hash; file published after Labeler 2 posts.
- Labeler 2: Rudratosh Shastri. Labels via GitHub issue, blind to Labeler 1's labels.

## Which labels count as Labeler 1
Added Nov 13, 2026, before Labeler 2's labels were posted.
- Labeler 1's labels are the hashed set in `LABELER1_COMMITMENT.md`. These are the labels compared with Labeler 2's.
- The draft labels in `cases.json` (Nov 11) are a reference only. Any case where they differ from Labeler 1's committed labels is reported and goes through the same outcomes below.

## Case outcomes
Every case ends in exactly one of these:

| Outcome | Rule | In main result? |
|---|---|---|
| Agree | Both labelers give the same surviving set | Yes |
| Badly written | Either labeler flags the case as flawed, with a reason | No: dropped, reason published |
| Excluded vs dominated | The split depends on whether a rival is excluded or only dominated | No: kept and reported as its own category |
| Other disagreement | Any other split | No: dropped, reason published |

## Constraints
- No case is edited after labeling to produce agreement.
- No rule here changes after either set of labels is revealed.
- The false-confidence rate before and after the rival-naming rule is computed on agreed cases only.
- Results are published whatever they show.
