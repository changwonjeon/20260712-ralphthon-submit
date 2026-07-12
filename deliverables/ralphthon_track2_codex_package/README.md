---
type: Package Guide
title: Ralphthon Track 2 현실 실행 패키지
description: 25분 동안 10편의 ICML 리뷰를 완료하고 Track 2 제출물을 준비하기 위한 Codex 작업 패키지.
tags: [ralphthon, track-2, review-agent, codex]
timestamp: 2026-07-12T11:30:00+09:00
---

# Ralphthon @ ICML Track 2 — Event MVP Package

이 패키지는 Critic–Verifier 아이디어를 행사 제약 안에서 실제로 완주할 수 있도록 축소한 계획안이다.

핵심 목표는 다음 두 가지다.

1. 16:30까지 익명 Technical Report PDF, Title, Abstract를 제출한다.
2. 16:35–17:00 동안 배정된 논문 10편을 모두 claim → read → review → post하고 제출 성공을 확인한다.

리뷰 품질은 중요하지만 **10편 중 한 편이라도 미제출되는 것이 가장 큰 실패**다. 따라서 런타임 완주율, 공식 폼 적합성, 게시 성공을 첫 번째 게이트로 둔다.

## 문서 우선순위

1. `docs/implementation_roadmap_v4_event_mvp.md` — 현재 실행 기준.
2. `docs/submission_contract.md` — 제출 형식과 필수 산출물.
3. `codex_task_prompt.md` — Codex 구현 지시문.
4. `docs/technical_report_outline.md` — 4페이지 Technical Report 구성.
5. `docs/implementation_roadmap_v3.md` — 이전 장기 계획. 참고용이며 v4와 충돌하면 v4를 따른다.
6. `docs/reference_v2_claude.md` — 배경 참고용.

## 현실적인 MVP

```text
Batch Orchestrator
  → Platform Adapter: browse / claim / download
  → PDF Extractor
  → Evidence-bound Reviewer
  → Deterministic Form Validator
  → optional one-shot Repair
  → Platform Adapter: post / verify receipt
  → Append-only Run Ledger
```

Critic과 Verifier는 개념적으로 분리하되, 행사 런타임에서는 논문마다 여러 Codex 세션과 Git 커밋을 만들지 않는다. 기본 경로는 한 번의 구조화된 리뷰 호출이며, 결정적 validator가 잘못된 필드나 범위를 검출했을 때만 한 번의 제한된 repair를 허용한다.

## 필수 성공 기준

- 10편 전체에 제출 영수증 또는 플랫폼 성공 상태가 존재한다.
- 논문 한 편의 hard timeout은 120초 이하이며 전체 hard stop은 24분이다.
- 모든 리뷰에 Soundness, Presentation, Significance, Originality, Overall Recommendation, Confidence, Comment가 있다.
- 점수 범위는 각각 1–4, 1–4, 1–4, 1–4, 1–6, 1–5다.
- 모든 핵심 강점과 약점은 논문의 페이지·섹션·표·그림 중 하나를 근거로 갖는다.
- 실패한 한 편이 나머지 큐를 멈추지 않는다.
- 동일 논문을 중복 claim하거나 중복 post하지 않는다.
- 16:30 제출용 Technical Report가 익명이고 본문 4페이지 이하다.

## 범위에서 제외

- 런타임 stage별 Git commit과 `git reset --hard`.
- 20–40개 seeded-error 대형 평가 세트.
- hidden holdout.
- Autoresearch 메타 최적화 루프.
- LLM Observer.
- Evidence Sensitivity 실험.
- GPU, VESSL, 신규 학습.
- 세계 전체 문헌을 대상으로 한 novelty 검증.

이 기능들은 제출 성공과 10편 처리량이 검증된 이후에만 고려한다.

## 패키지 사용 순서

1. 공식 행사 skill과 OpenAgentReview 인터페이스를 확보한다.
2. `docs/implementation_roadmap_v4_event_mvp.md`를 읽는다.
3. `docs/submission_contract.md`의 필드와 산출물을 고정한다.
4. `codex_task_prompt.md`를 Codex에 전달한다.
5. mock adapter로 10편 배치 테스트를 통과시킨다.
6. 테스트 환경에서 login → browse → claim → PDF read → review post를 최소 한 번 확인한다.
7. Technical Report 초안을 자동 생성하고 15:30–16:30에 사람이 편집한다.
8. 16:35에는 검증된 배치 명령 하나만 실행한다.

## 핵심 산출물

```text
ralphthon-reviewer/
├── review-agent.md
├── policies/review_schema.json
├── harness/run_batch.py
├── harness/validate_review.py
├── adapters/openagentreview.py
├── prompts/reviewer.md
├── output/reviews/<paper_id>.json
├── runs/<run_id>/ledger.jsonl
├── runs/<run_id>/receipts.jsonl
├── tests/
└── submission/
    ├── technical-report.pdf
    ├── title.txt
    ├── abstract.txt
    └── evidence-summary.json
```

## Go / No-Go

12:30 이전에 다음 중 하나라도 확인할 수 없으면 플랫폼 자동화 부분은 미확정 상태다.

- 행사 skill의 실제 로그인·claim·post 인터페이스.
- 테스트 계정 또는 안전한 dry-run 경로.
- 리뷰 필드명과 성공 응답.

15:00까지 mock 10편의 24분 이내 완주와 실제 플랫폼 1편 왕복이 모두 확인되지 않으면 확장 기능을 중단하고 제출 경로 안정화에만 집중한다.

# Citations

- `docs/submission_contract.md`.
- `docs/implementation_roadmap_v4_event_mvp.md`.
- https://github.com/team-attention/ralphthon-icml

