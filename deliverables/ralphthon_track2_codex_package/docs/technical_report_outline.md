---
type: Submission Template
title: Track 2 Technical Report 4페이지 구성안
description: Review Agent의 방법, 평가, 결과와 한계를 4페이지에 담기 위한 보고서 구조.
tags: [ralphthon, track-2, technical-report, icml]
timestamp: 2026-07-12T11:30:00+09:00
---

# Technical Report Outline

## Title 초안

Evidence-Bound Review at Deadline: A Critic–Verifier Harness for Reliable and Throughput-Constrained ICML Reviews

## Abstract 구성

1. 문제는 LLM reviewer가 근거 없는 지적을 만들거나 중요한 오류를 놓칠 수 있다는 점이다.
2. 방법은 Critic–Verifier 규율, 결정적 form validator, bounded batch orchestrator의 결합이다.
3. 평가는 소규모 seeded issue와 10편 batch 처리량을 측정한다.
4. 결과에는 실제 측정한 precision, location accuracy, schema pass, latency, completion rate만 넣는다.
5. 결론은 25분 운영 제약에서 얻은 장점과 남은 한계를 함께 말한다.

## 1페이지 — Problem and Method

- Track 2 문제와 10편·25분 제약.
- 단일-pass reviewer의 hallucinated criticism 위험.
- Critic–Verifier 책임 분리.
- 전체 시스템 그림.

## 2페이지 — System and Runtime

- claim-read-review-post 배치 흐름.
- 공식 리뷰 스키마.
- deterministic validation과 one-shot repair.
- worker pool, timeout, idempotency, receipt.
- evidence trace 예시 하나.

## 3페이지 — Evaluation

- baseline 정의.
- 4–8개 seeded micro-case 구성.
- mock 10편 batch 3회.
- issue precision, seeded recall, location accuracy.
- schema pass, p50/p95 latency, post completion.
- 표와 간단한 failure case.

## 4페이지 — Results, Limitations, Conclusion

- 실제 측정 결과.
- 확인된 실패 모드.
- originality 판정 범위의 한계.
- 작은 평가 표본과 실제 심사위원 correlation 미확인의 한계.
- Track 2 런타임에서 얻은 결론.

## References와 Appendix

References에는 ICML Reviewer Instructions, 공식 행사 가이드, 관련 Critic–Verifier 영감 자료를 넣는다.

Appendix에는 전체 스키마, reviewer prompt, agent version, 추가 trace, 실행 명령을 넣을 수 있다. Appendix가 자유롭더라도 핵심 방법과 결과를 본문 밖으로 밀어내지 않는다.

## 작성 금지

- 실행하지 않은 평가 결과.
- 심사위원 점수와의 확인되지 않은 correlation.
- 전 세계 문헌을 검증했다는 주장.
- 10편 전체를 완료하지 않았는데 완주했다고 표현하는 문장.
- W&B 또는 Weave를 실제 확인하지 않고 관찰 가능성을 확보했다는 주장.

