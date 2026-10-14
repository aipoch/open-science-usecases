# How Far Has AI Drug Discovery Really Gotten

## Research question

Which studies move beyond computational prediction to experiments or human dosing?

Builds an evidence table for AI-related drug-discovery papers, distinguishing computational predictions, cell experiments, animal studies, and human trials. The archived review records what each selected paper was reported to demonstrate.

## Data and comparison design

Classify each selected publication by its highest demonstrated stage: computational work, cells, animals, or humans. Keep retrospective prediction of known measurements separate from a new synthesis or experiment, and distinguish trial entry from demonstrated clinical efficacy.

## Recorded findings

**The short answer:** AI drug discovery has genuinely reached human trials — but only barely, and the "AI" label covers a very wide range of evidence quality. Of 12 recent papers, 3 are purely computational, 2 stop at cells, 5 reach animals, and only 2 involve human dosing. Exactly one is a randomized, placebo-controlled efficacy trial.

### The evidence table

**Tier 1 — In silico only**
| # | Paper | Year / Venue | What it actually demonstrated |
|---|---|---|---|
| 1 | **AlphaFold 3** — [10.1038/s41586-024-07487-w](https://doi.org/10.1038/s41586-024-07487-w) | 2024, Nature | Predicts joint structure of protein–ligand–nucleic acid complexes. Entirely computational; no molecule synthesised. |
| 2 | **PCMol** — [10.1021/acs.jcim.4c00309](https://doi.org/10.1021/acs.jcim.4c00309) | 2024, J Chem Inf Model | AlphaFold2-conditioned generative model; generated molecules scored favourably by **docking only**. No wet-lab work. |
| 3 | **Boltz-2** — [github.com/jwohlwend/boltz](https://github.com/jwohlwend/boltz) | 2025, preprint | Joint structure + affinity prediction, ~1000× faster than FEP. Benchmarked against *already-measured* assay data. Preprint, not peer-reviewed. |

**Tier 2 — In vitro**
| # | Paper | Year / Venue | What it actually demonstrated |
|---|---|---|---|
| 4 | **NGT — MC2R inhibitors** — [10.1021/acs.jmedchem.4c01763](https://doi.org/10.1021/acs.jmedchem.4c01763) | 2024, J Med Chem | Generated antagonists for a target with **zero prior training data**; 12 compounds synthesised, cAMP EC50s with full dose–response and LC-MS. No animal work. |
| 5 | **RFdiffusion antibodies** — [10.1038/s41586-025-09721-5](https://doi.org/10.1038/s41586-025-09721-5) | 2025, Nature | Cryo-EM at 3.0–3.6 Å confirmed designed binders matched design models, including all six CDR loops. Binding only — no animal efficacy. |

**Tier 3 — Animal**
| # | Paper | Year / Venue | What it actually demonstrated |
|---|---|---|---|
| 6 | **Wong et al. — new antibiotic class** — [10.1038/s41586-023-06887-8](https://doi.org/10.1038/s41586-023-06887-8) | 2024, Nature | Screened 39,312 compounds, predicted on 12M, tested 283. New class active vs MRSA/VRE; **reduced bacterial titres 10-fold in mouse infection models**. |
| 7 | **Krishnan et al. — de novo antibiotics** — [10.1016/j.cell.2025.07.033](https://doi.org/10.1016/j.cell.2025.07.033) | 2025, Cell | 36M generated → 24 synthesised → 7 validated (~27% hit rate). Leads NG1/DN1 efficacious in **mouse gonorrhoea and MRSA models**, novel mechanisms. |
| 8 | **SK56 — GSDMD pore blocker** — [10.1038/s41590-025-02280-x](https://doi.org/10.1038/s41590-025-02280-x) | 2025, Nat Immunol | AI-designed peptide. In mouse sepsis, **survival rose from 5% → 45%**, effective even 4–16 h after induction. |
| 9 | **ISM5939 — ENPP1 inhibitor** — [10.1038/s41467-025-59874-0](https://doi.org/10.1038/s41467-025-59874-0) | 2025, Nat Commun | Oral inhibitor;**synergised with PD-1/PD-L1 blockade** across five murine tumour models. |
| 10 | **BGM0504 — dual GLP-1/GIP agonist** — [10.1038/s41598-024-66998-8](https://doi.org/10.1038/s41598-024-66998-8) | 2024, Sci Rep | MD-guided redesign, 2–3× more potent than tirzepatide; **db/db mice + cynomolgus monkey PK**. Physics-based, not ML — included as an AI-adjacent comparator. |

**Tier 4 — Human clinical**
| # | Paper | Year / Venue | What it actually demonstrated |
|---|---|---|---|
| 11 | **INS018_055 / rentosertib preclinical + Phase 1** — [10.1038/s41587-024-02143-0](https://doi.org/10.1038/s41587-024-02143-0) | 2024, Nat Biotechnol | AI target ID + generative chemistry in ~18 months. Mouse fibrosis efficacy; **Phase 1 in 78 healthy volunteers — safety and PK only, no efficacy signal.** |
| 12 | **Rentosertib Phase 2a (GENESIS-IPF)** — [10.1038/s41591-025-03743-2](https://doi.org/10.1038/s41591-025-03743-2) | 2025, Nat Med | The milestone: 71 IPF patients, randomized, placebo-controlled. **FVC +98.4 mL vs −20.3 mL placebo.** But see caveat. |

### Three things worth flagging

**The one human efficacy result is weaker than headlines suggest.** The rentosertib FVC improvement was a **secondary endpoint** — the trial was powered for safety, not efficacy. Arms were n=17–18, duration 12 weeks, and the confidence interval (+10.9 to +185.9) is wide enough to include a modest effect. It's a real signal and a genuine first, but not the definitive proof the press coverage implies.

**Attention concentrates at the animal stage.** Five of twelve papers stop there. Two reviews identified in the archived search independently quantified the same gap: a PRISMA review of de novo cancer drug design found only **14% of studies** reached in vivo testing. The high hit rates you see quoted (54–85%) are almost all in vitro.

**Searching is not the same as validating.** A caveat on my own method: the literature and PubMed connectors were unavailable in this session (credential and network failures), so I built this from web search plus publisher pages. Every DOI and PMID above was cross-checked against the publisher's own record, but I did not read the full texts — so the "demonstrated" column reflects what abstracts, figures and supplementary descriptions report, not my own reading of every table. Where a number sits in a supplementary table (e.g. NGT's exact EC50s), I've said so rather than quoting it.

**One more structural point:** only 2 of 12 papers here describe a molecule that ever entered a human. The rest are method papers or preclinical work that may never advance. As of late 2025, ~117 AI-discovered candidates had entered clinical trials, 60 had completed Phase 1, and **8 had completed Phase 2** — and no AI-discovered drug had FDA approval. That's the honest denominator, and it's why the ladder above is so bottom-heavy.

The notebook has the full table with method, target, and a per-paper caveat column, plus the rendered ladder.

## What the comparison shows

This curated evidence table is not an exhaustive count of the field. The role of AI and the strength of validation differ across entries.

## Assumptions and limits

Evidence stages are not interchangeable and the selected papers are not a systematic census. The import preserves a dated literature review; it does not independently validate clinical efficacy or provide treatment advice.

## Sources and research materials

The original `.science` export and matching poster are preserved byte-for-byte from the upstream case. The package contains the conversation, session metadata, and the resources inventoried in its internal manifest. This introduction summarizes the archived record; the research, external sources, and model evaluations were not rerun for this import.
