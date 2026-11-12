# Publication readiness and external-review dependencies — 12 November 2026

**Important:** This is an internal project checklist, not a certificate of publication acceptance, independent peer review, originality, legal status, or patent eligibility.

## Current confirmed scientific state

- A mathematical proof for the **fixed-score, independent signed-edge transfer model** is in [PROOF.md](PROOF.md).
- An exact quantitative margin extension with a full proof is in [MARGIN_THEOREM.md](MARGIN_THEOREM.md).
- Source code and tests are public; GitHub Actions verifies the claimed formulas against linear programs and exact finite-grid enumeration.
- Novelty/priority remains **UNCONFIRMED** after the documented [literature audit](NOVELTY_AUDIT_2026-11-12.md).
- An AI-assisted internal [self-audit](SELF_AUDIT_2026-11-12.md) is not independent external referee review.
- Independent reviewers are invited through [Issue #1](https://github.com/sonii-shivansh/edgeflow-topk/issues/1); publication of the invitation does not establish their participation.

## Venue due diligence

### Journal of Graph Algorithms and Applications (JGAA)

Official aims and scope: https://jgaa.info/index.php/jgaa/about . JGAA is a graph-algorithm journal offering diamond open access without author fees. Its standards require **substantial original research**, not just a correct theorem. Our specific proof and algorithm might be considered a straightforward specialization of established robust-optimization methods. Submission without a stronger comparison and independent human verification is therefore **NOT RECOMMENDED YET**.

Official author requirements and AI policy: https://jgaa.info/index.php/jgaa/about/submissions . JGAA calls for a PDF manuscript with line/page numbers, LaTeX preparation and appropriate citations, including available DOIs. Its policy requires transparency about generative-AI assistance and human responsibility for all mathematical/scientific content. The project manuscript was substantially AI-assisted; we cannot honestly present it as independently authored or verified by a human referee.

### arXiv

Official submission policy: https://info.arxiv.org/help/submit/index.html . arXiv requests topical, refereeable scientific contributions. The endorsement system (https://info.arxiv.org/help/endorsement.html) may apply to a first submission or new category. No arXiv author account, endorsement, formal submission, identifier, or acceptance has been verified for this project.

### Zenodo DOI

Official instructions: https://help.zenodo.org/docs/github/enable-repository/ and https://help.zenodo.org/docs/github/archive-software/github-upload/ . Zenodo's automatic GitHub archiving requires a linked, enabled repository under an authorized Zenodo account. Publishing a GitHub release does **not by itself** register a Zenodo DOI. The available connected tools do not expose the user's Zenodo authorization or deposit action; no Zenodo DOI was verified.

## Research-publication next action, in priority order

1. Keep both GitHub research releases versioned and traceable, with proof and tests tied to the release commit hash.
2. Obtain an **external** algorithmist's proof and originality assessment. Reviewer contact and acceptance must be real; do not simulate a signed referee report.
3. Expand the related-work comparison if an exact predecessor is located, correcting the manuscript promptly.
4. Identify a real application dataset satisfying the **signed independent transfer** model, and benchmark the certified margin on that model.
5. Only after authorship responsibility and novelty are resolved, consider a formal scholarly preprint or journal submission; use real author credentials and disclose AI help.
6. A persistent DOI remains optional archiving metadata, not a scientific correctness or novelty guarantee, and requires authorized Zenodo publication.

## Status terminology

- **PROVEN (mathematical, conditional on model):** derivation is self-contained, internal proof audit performed.
- **VERIFIED NUMERICALLY:** finite test suites passed.
- **NOT EXTERNALLY REFEREED:** no independent human referee verdict established.
- **NOVELTY UNCONFIRMED:** no exact published match identified, but classical robust-optimization machinery overlaps materially.
- **DOI NOT VERIFIED:** a GitHub release tag is not a DOI.

The research is accessible now; scientific standing depends on independent assessment and comparison to prior work, not the number of GitHub releases.
