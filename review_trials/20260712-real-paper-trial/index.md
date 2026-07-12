# Real-Paper Review Trial — 2026-07-12

## Outcome

The trial produced two paper-specific, evidence-bound ICML-style reviews. Both canonical JSON drafts match their frozen manifests, pass deterministic validation, and received `PASS` from a separate read-only verifier.

This is evidence that the review workflow can surface non-trivial, paper-specific issues when independent reviewer and verifier contexts are explicitly orchestrated. It is not proof of general reviewer accuracy: there are only two papers, no gold reviews or author rebuttals, no code/raw-data execution, and no external novelty search.

| Paper | Overall | Confidence | Central finding |
| --- | ---: | ---: | --- |
| `2607.08173v1` | 3/6, Weak Reject | 4/5 | The secret-training endpoint construction may contaminate the claimed reasoning vector; alpha=1 and Directional Fisher semantics also require repair. |
| `2607.08256v1` | 3/6, Weak Reject | 4/5 | Evaluator-dependent ranking is supported, but the 2–3x family claim, p-values, fourth evaluator, and N=10 quality evidence are not internally adequate. |

## Workflow

```text
Frozen PDF + SHA-256
        |
        +--> independent paper reviewer A --> ReviewDraft A --+
        |                                                     |
        +--> independent paper reviewer B --> ReviewDraft B --+--> canonical validator
                                                              |
                                             independent evidence auditor
                                                              |
                                                      PASS / scoped REPAIR
                                                              |
                                                        final JSON + Markdown
```

No OpenAgentReview claim or post operation was performed.

## Artifacts

- [Overthinking review](final/2607.08173v1.review.md)
- [Overthinking canonical ReviewDraft](final/2607.08173v1.review.json)
- [Overthinking verifier record](verification/2607.08173v1.verifier.md)
- [Overthinking fresh native verifier JSON](verification/2607.08173v1.native-verifier-result.json)
- [Best-of-N TTS review](final/2607.08256v1.review.md)
- [Best-of-N TTS canonical ReviewDraft](final/2607.08256v1.review.json)
- [Best-of-N TTS verifier record](verification/2607.08256v1.verifier.md)
- [Machine-readable validation summary](verification/validation-summary.json)
- [한국어 결과 요약](index_kr.md)

The `inputs/` directory contains frozen PDF copies and manifests; `extracted/` contains layout-preserving text; `renders/` contains page images used to rule out text-extraction artifacts; `drafts/` preserves the pre-verifier drafts.

## Important implementation boundary

The packaged Python DRY-RUN runtime now has an explicitly enabled deterministic mock verifier branch that executes risk selection, gates, PASS/REPAIR, shared repair budget, revalidation, and ledger/summary transitions. It deliberately does not shell out to or impersonate a native Codex agent. This real-paper trial instead used directly orchestrated independent reviewer contexts and a separate native verifier, so it supplies qualitative independence evidence rather than Python-adapter evidence.
