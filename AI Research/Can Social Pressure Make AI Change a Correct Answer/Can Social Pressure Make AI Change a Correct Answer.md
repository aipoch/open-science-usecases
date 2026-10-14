# Can Social Pressure Make AI Change a Correct Answer

## Research question

Can a controlled pressure manipulation make a model abandon a previously correct response?

Designs an experiment testing whether social pressure changes initially correct factual answers. The package preserves the protocol and attempted inference calls for majority and expert-pressure conditions.

## Data and comparison design

Prepare matched neutral and pressure prompts, hold closing wording constant, define correctness scoring, and retain trial-level inputs and responses. Mock-provider runs can test the bookkeeping but cannot answer the behavioral question.

## Recorded findings

| Stage | Recorded status | Why it matters |
| --- | --- | --- |
| Question and condition design | Planned correct-answer and social-pressure comparisons | Defines the behavior to measure. |
| Live model inference | All recorded attempts failed | No real model behavior was collected. |
| Pipeline checks | Harness-only or mock checks | Tests data flow, not conformity behavior. |
| Effect estimate | Not established | A functioning pipeline cannot be reported as a pressure effect. |

The archived live inference attempts all failed, so the planned experiment has no real model-behavior measurements. The completed pipeline checks belong to the test harness, not the research outcome.

A genuine pressure effect requires comparable questions, a recorded initial answer, a defined social-pressure intervention and successful follow-up inference. The intended outcome is whether a correct answer changes after the intervention. Failed inference calls leave that outcome unobserved. Mock responses can confirm that the experiment stores labels and computes a statistic, but they cannot supply a behavioral estimate for a real model.

## What the comparison shows

Any reversal rate or pressure-effect estimate would require successful real inference under the specified protocol.

## Assumptions and limits

The recorded inference channel failed on every attempt, so the planned experiment produced no real measurements. Protocol files and illustrative material must not be reported as experimental results.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
