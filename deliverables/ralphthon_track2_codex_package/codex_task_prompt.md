---
type: Implementation Prompt
title: Track 2 Event MVP Codex 구현 지시문
description: 10편·25분 제약을 우선하는 Review Agent 배치 하네스 구현 지시문.
tags: [ralphthon, track-2, codex, implementation]
timestamp: 2026-07-12T11:30:00+09:00
---

# Codex CLI 구현 지시문

당신은 Ralphthon @ ICML Track 2용 Review Agent 배치 하네스를 구현한다.

## 읽기 순서

1. `README.md`.
2. `docs/implementation_roadmap_v4_event_mvp.md`.
3. `docs/submission_contract.md`.
4. `docs/technical_report_outline.md`.

v2와 v3는 참고 자료다. 충돌하면 v4와 submission contract를 따른다.

## Desired End State

- mock 논문 10편을 24분 이내에 처리한다.
- 실제 운영에서는 16:35–17:00 사이 배정 논문 10편을 claim-read-review-post한다.
- 모든 게시 결과에 paper ID, review hash, status, timestamp, receipt가 남는다.
- 한 논문의 실패나 timeout이 다른 논문 처리를 중단하지 않는다.
- 16:30 제출용 익명 Technical Report, Title, Abstract를 생성할 근거 자료가 남는다.

## Constraints

- 논문당 hard timeout 120초.
- 전체 batch hard stop 24분.
- 논문별 LLM 호출은 기본 1회, schema repair가 필요할 때만 추가 1회.
- retry는 플랫폼 작업별 최대 1회이며 exponential backoff를 사용하지 않는다.
- 런타임 중 Git commit, destructive reset, 메타 최적화, hidden holdout을 실행하지 않는다.
- private participant data, credentials, 전체 논문 본문을 원격 trace에 기록하지 않는다.
- 누락된 근거, 실험, 인용, 저자 의도를 만들지 않는다.
- 플랫폼의 실제 API나 DOM 계약을 추측하지 않는다. 공식 skill 또는 관찰된 인터페이스로 adapter를 구현한다.

## Required Review Contract

각 리뷰는 다음 필드를 반드시 갖는다.

```yaml
paper_id: string
summary: string
strengths:
  - text: string
    evidence_location: string
weaknesses:
  - axis: soundness|presentation|significance|originality
    text: string
    evidence_location: string
scores:
  soundness: 1..4
  presentation: 1..4
  significance: 1..4
  originality: 1..4
  overall_recommendation: 1..6
  confidence: 1..5
comment: string
limitations: string
runtime:
  paper_sha256: string
  agent_version: string
  started_at: ISO-8601
  completed_at: ISO-8601
```

OpenAgentReview 게시 payload는 이 내부 스키마에서 명시적으로 변환한다. 플랫폼 필드명을 내부 필드명과 섞지 않는다.

## 구현 순서

### P0 — 제출 경로 Thin Slice

1. 공식 행사 skill 또는 제공된 인터페이스를 읽고 `adapters/openagentreview.py` 계약을 정의한다.
2. mock adapter로 `list_candidates`, `claim`, `download_pdf`, `post_review`, `get_status`를 구현한다.
3. 논문 한 편에 대해 claim → PDF read → valid review → post → receipt가 완주하도록 한다.
4. 동일 idempotency key로 중복 post가 발생하지 않음을 테스트한다.

P0 종료 증거는 한 편의 성공 receipt와 재실행 시 중복 게시 방지 테스트다.

### P1 — 10편 배치와 시간 제한

1. bounded worker pool을 사용해 10편 큐를 처리한다. 기본 동시성은 3이며 설정 가능하게 한다.
2. 논문별 120초 timeout과 전체 24분 deadline을 강제한다.
3. 각 논문의 상태를 `queued`, `claimed`, `downloaded`, `reviewed`, `validated`, `posted`, `failed`로 기록한다.
4. append-only `ledger.jsonl`과 `receipts.jsonl`을 유지한다.
5. 실패한 작업은 다른 worker와 큐에 영향을 주지 않는다.
6. 10편 mock latency 테스트를 3회 실행한다.

P1 종료 조건은 3회 모두 10/10 완료, schema pass 100%, 중복 post 0건, 전체 24분 이하다.

### P2 — Evidence-bound Review Quality

1. PDF에서 페이지 구분을 유지한 텍스트를 추출한다.
2. reviewer prompt가 네 평가 축과 모든 공식 점수를 한 번에 반환하도록 한다.
3. Critic 역할은 강점·약점 후보를 만들고 Verifier 규율은 각 핵심 항목의 위치와 근거 존재를 확인한다.
4. 결정적 validator가 필드, 범위, 빈 Comment, evidence location을 확인한다.
5. 실패 시 누락 필드만 대상으로 repair를 한 번 수행한다.
6. originality는 제공된 논문과 reference 목록 기준의 제한된 판정임을 명시한다.

P2 종료 조건은 seeded micro-case 4–8개에서 schema 100%, 근거 위치 정확도와 issue precision을 보고할 수 있고, mock 10편 처리량이 회귀하지 않는 것이다.

### P3 — 제출 자료

1. `submission/evidence-summary.json`에 처리량, p50/p95 latency, schema pass, post success, 실패 사례를 기록한다.
2. `docs/technical_report_outline.md`를 기반으로 4페이지 보고서 초안을 만든다.
3. `submission/title.txt`, `submission/abstract.txt` 초안을 만든다.
4. `review-agent.md`에 agent version, output contract, evidence guardrail을 동결한다.
5. 실행 명령과 알려진 한계를 README에 기록한다.

## 우선순위 중단 규칙

- P0가 실패하면 P1–P3 품질 기능을 추가하지 말고 플랫폼 왕복을 고친다.
- P1이 실패하면 seeded 평가와 관찰성 확장을 중단하고 처리량과 실패 격리를 고친다.
- 실제 플랫폼 인터페이스가 없으면 mock adapter를 실제처럼 가장하지 말고 `BLOCKED_PLATFORM_CONTRACT`로 기록한다.
- 15:00 이후에는 새 기능을 추가하지 않는다.
- 15:30 이후에는 코드 변경을 중단하고 제출물 편집과 smoke test만 수행한다.

## 검증 명령

프로젝트의 실제 도구에 맞춰 다음과 동등한 검사를 제공한다.

```bash
pytest -q
python -m harness.validate_review tests/fixtures/valid_review.json
python -m harness.run_batch --adapter mock --papers tests/fixtures/papers --deadline-seconds 1440
python -m harness.verify_receipts --expected 10
```

## 최종 보고

완료 보고에는 다음만 근거와 함께 적는다.

- 실제 실행한 명령과 결과.
- 10편 완료 수와 게시 성공 수.
- p50/p95 및 최대 latency.
- schema 및 evidence validation 결과.
- 실제 플랫폼 왕복 확인 여부.
- Technical Report, Title, Abstract 경로.
- 남은 blocker와 런타임 위험.

