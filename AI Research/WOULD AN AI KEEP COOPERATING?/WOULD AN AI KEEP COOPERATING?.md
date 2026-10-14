# WOULD AN AI KEEP COOPERATING?

## Research question

Can a one-round change in an opponent’s timeline alter a fixed strategy’s long-run cooperation?

Explores repeated prisoner's-dilemma play under an explicit win-stay, lose-shift rule. The conversation changes the opponent's timing and isolated defections and traces how cooperation patterns change.

## Data and comparison design

Trace win-stay, lose-shift under the explicit payoff matrix and vary only the opponent’s switch date or one isolated relapse. The decision rule is unchanged, so each later action can be explained from the preceding payoff.

## Recorded findings

Yes. Under the unchanged win-stay, lose-shift rule, both a one-round timing change and one isolated relapse can completely reverse the long-run outcome.

Rule: the AI starts with C. It repeats its previous move after payoff ≥3; otherwise it switches. Payoffs are C/C = 3, D/C = 5, D/D = 1, C/D = 0.

| Version | Opponent timeline | AI timeline | Final AI cooperation |
|---|---|---|---:|
| 1 | D1–48, C49–100 | C1, then D/C alternating through 48; C49–100 | **76%** |
| 2 | D1–49, C50–100 | C1, then D/C alternating through 49; D50–100 | **25%** |
| 3 | D1–48, C49–59, D60, C61–100 | C1, then D/C alternating through 48; C49–60; D61–100 | **36%** |
| 4 | D1–49, C50–59, D60, C61–100 | C1, then D/C alternating through 49; D50–60; C61–100 | **65%** |

The decisive transitions:

| Version | Critical sequence | Result |
|---|---|---|
| 1: switch at 49 | Round 49: AI C vs C → payoff 3 → stays C | Cooperation locks in |
| 2: switch at 50 | Round 50: AI D vs C → payoff 5 → stays D | Defection locks in |
| 3: switch 49 + relapse 60 | Round 60: AI C vs D → 0; round 61: AI D vs C → 5 → stays D | One relapse destroys cooperation |
| 4: switch 50 + relapse 60 | Round 60: AI D vs D → 1; round 61: AI switches to C vs C → 3 → stays C | One relapse restores cooperation |

So the answer is emphatically yes:

- Moving the opponent’s initial switch from round 49 to 50 changes the AI from **76% cooperation** to **25%**.
- A single defection at round 60 changes the round-49 case from stable cooperation to **36%**, but changes the round-50 case from stable defection to **65% cooperation**.

The mechanism is timing: the AI only sees past outcomes, and the opponent’s change happens to meet whichever AI action was already scheduled.

## What the comparison shows

The case illustrates repeated-game dynamics. It is not evidence that an unspecified AI system has cooperative intentions.

## Assumptions and limits

The decision-maker is a specified deterministic rule, not a measured language-model policy. Timing-sensitive paths illustrate the rule and payoff assumptions rather than a general claim about AI cooperation.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
