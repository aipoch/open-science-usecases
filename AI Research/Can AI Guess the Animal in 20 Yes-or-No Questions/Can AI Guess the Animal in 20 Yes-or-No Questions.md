# Can AI Guess the Animal in 20 Yes-or-No Questions

## Research question

Can successive yes-or-no answers narrow an animal identification within a fixed question budget?

Preserves an interactive animal-guessing conversation using yes-or-no questions. The recorded exchange ends with a macaw identified within the requested question limit.

## Data and comparison design

The record tracks the answers and eliminated possibilities throughout one interactive conversation. Evaluate the identification and the question count separately; broad questions can split candidate sets before more specific distinctions resolve the species.

## Recorded findings

| Decision stage | What the exchange does | Recorded outcome |
| --- | --- | --- |
| Broad classification | Use yes/no answers to narrow the animal class | Retains the animal compatible with the answers. |
| Distinguishing features | Choose follow-up questions rather than guessing a list | Narrows the remaining candidates. |
| Final identification | Name the inferred animal within the question budget | Macaw; the archive does not establish a general guessing benchmark. |

The archived exchange identifies a macaw within the requested question limit.

The task is an adaptive exchange rather than a fixed questionnaire. Each answer restricts the next set of plausible animals, and the following question should distinguish candidates still consistent with earlier answers. The final macaw identification is one successful recorded interaction. The archive does not define a random animal population, repeat the test across many animals, or provide a failure distribution, so no general twenty-question success rate is inferred.

## What the comparison shows

One cooperative conversation cannot establish a general success rate or robustness to ambiguous, inconsistent, or adversarial answers.

## Assumptions and limits

This is one conversation, not a controlled benchmark across animals or participants. The result depends on the answers provided during the exchange.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
