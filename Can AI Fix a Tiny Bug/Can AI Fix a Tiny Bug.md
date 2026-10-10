# Can AI Fix a Tiny Bug?

## Research question

How should three AI bug-fix attempts be compared when the visible patches look correct but their test runs cannot be independently verified? This case records an evidence-aware review of three referenced sessions, labeled **apodex**, **DeepSeek**, and **GPT**, for a small timestamp-boundary bug.

## Method and recorded findings

The user requested independent scores out of 100, weighted as correctness (40), test evidence (25), patch quality (20), and explanation (15), plus a winner and a brief reason. The reviewer inspected the accessible session transcripts and explicitly distinguished quoted test results from authenticated execution output.

The visible fixes changed a timestamp comparison from `<=` to `<`. The archived review gave all three attempts the same static correctness score and no verified test-evidence points:

| Session label | Correctness /40 | Test evidence /25 | Patch quality /20 | Explanation /15 | Total /100 |
| --- | ---: | ---: | ---: | ---: | ---: |
| apodex | 35 | 0 | 20 | 13 | 68 |
| DeepSeek | 35 | 0 | 20 | 14 | 69 |
| GPT | 35 | 0 | 18 | 12 | 65 |

The review named **DeepSeek the provisional winner**, citing its minimal patch and clearer boundary example. It noted that apodex omitted warning lines from its quoted output, while GPT removed an additional comment and initially described an amount threshold instead of a timestamp threshold. These are findings reported by the archived reviewer, not new benchmark results from this integration.

## Assumptions and limits

The transcript API available during the recorded review hid raw execution output. Although all three attempts quoted passing results, the reviewer could not independently authenticate their tests. **Zero verified test-evidence points does not mean that the tests failed.** The recorded review concluded that an execution-verified winner could not be established from the accessible records.

The labels identify the referenced sessions; they do not establish exact model versions or a controlled comparison of model families. This is one small task assessed with a user-specified rubric, not evidence of general coding ability. Scores and rankings are the archived reviewer's judgments, and neither the original bug-fix sessions nor their test suites were rerun when importing this case.

## Package contents and provenance

The package contains the review conversation, Notebook run and dependency-analysis data, execution-file evidence JSON, and original session metadata. Those evidence files preserve the review's record; their presence does not resolve the stated lack of independently authenticated test output from the three compared sessions.

The original `.science` package and PNG are imported unchanged from [aipoch/open-science-usecases at a1d1bfcb7d1c7a85d3e4a465060fa87fddc6d284](https://github.com/aipoch/open-science-usecases/tree/a1d1bfcb7d1c7a85d3e4a465060fa87fddc6d284/Can%20AI%20Fix%20a%20Tiny%20Bug). The case was contributed by 单偌宇 in [bbd8c940](https://github.com/aipoch/open-science-usecases/commit/bbd8c940bedbfa6bed4ba1e4c37322e82ca4e36a). This introduction summarizes the packaged conversation and its stated limitations.
