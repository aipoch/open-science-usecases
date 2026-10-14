# Can AI Plan a Fair Chinese Shared Dinner

## Research question

Can a shared menu satisfy dietary safety while distributing satisfaction across different preferences?

Builds a Chinese shared-dinner scenario for ten diner profiles and scores menu safety and satisfaction separately. The record includes corrected arithmetic, preference and menu tables, and per-diner validation.

## Data and comparison design

Score food eligibility separately from satisfaction. Evaluate the same eight dishes against all ten diner profiles, retain per-diner results, and recompute the aggregate from its components rather than presenting a fairness score without its rule.

## Recorded findings

| Scoring component | Recorded result | Meaning |
| --- | --- | --- |
| Dietary safety | 10/10 diners; 60 points | All diners can eat safely under the supplied constraints. |
| Satisfaction | 8/10 diners; 32 points | Safety does not imply every diner gets a preferred meal. |
| Penalty | 4 points | Included in the objective rather than silently ignored. |
| Final score | 60 + 32 − 4 = 88.0 | A transparent score for this supplied preference model. |

The corrected archive reports 10/10 diners able to eat safely, 8/10 satisfied, and a score of 88.0: 60 safety points plus 32 satisfaction points minus four penalty points.

The dinner model separates hard dietary safety from preferences. Meeting every allergy or restriction is a feasibility requirement; satisfying preferred dishes contributes a softer objective. The corrected score makes that distinction visible and subtracts the stated penalty explicitly. A menu with a high score is optimal only relative to the supplied diners, dish definitions and scoring weights, not to a universal meaning of fairness.

## What the comparison shows

The score is defined for this scenario, not a validated measure of social fairness or medical food safety.

## Assumptions and limits

The fairness score depends on a chosen rubric. The archive labels everyone safe while some diners remain unsatisfied; its claim that nobody is disadvantaged should not be read as a universal fairness or allergy-safety guarantee.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
