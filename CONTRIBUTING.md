# Independent mathematical and software review welcome

This is an AI-assisted, not-yet-peer-reviewed research artifact. We value counterexamples and prior-art discoveries.

- **Proof review:** Identify the lemma, equation or inference you believe fails; propose a correction if possible.
- **Counterexamples:** Supply `scores`, `edges` (u,v,capacity), `B`, `k`, and a feasible signed flow or an LP output showing why the algorithm misclassifies.
- **Prior art:** Link the relevant paper and specify the theorem, page, algorithm or equation matching the proposed result.
- **Test improvements:** Supply additional deterministic edge cases, seeds, exact-rational tests, large-graph benchmarks, or independent LP models.
- **Documentation:** Improve clarity, with care not to weaken the stated assumptions.

To reproduce checks:

    python -m pip install -r requirements-test.txt
    python edge_transfer_topk.py

Open a GitHub issue for feedback, or propose a pull request containing a reproducible change. The repository owner should verify all contributions and decide how to represent them in subsequent publications.
