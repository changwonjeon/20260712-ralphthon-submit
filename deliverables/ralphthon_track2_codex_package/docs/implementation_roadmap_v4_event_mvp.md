---
type: Implementation Roadmap
title: Ralphthon Track 2 Event MVP 구현 계획 v4
description: 10편을 25분 안에 제출하는 운영 제약과 Technical Report 제출을 우선한 실행 계획.
tags: [ralphthon, track-2, event-mvp, review-agent]
timestamp: 2026-07-12T11:30:00+09:00
---

# Track 2 Event MVP 구현 계획 v4

## 1. 성공의 정의

이 프로젝트의 최종 성공은 리뷰 파일 생성이 아니라 다음 두 결과의 동시 달성이다.

1. 16:30까지 익명 Technical Report PDF, Title, Abstract를 제출한다.
2. 16:35–17:00 동안 배정 논문 10편의 유효한 리뷰를 모두 OpenAgentReview에 게시한다.

운영 지표의 우선순위는 다음과 같다.

1. `posted_reviews / assigned_papers = 10 / 10`.
2. 공식 리뷰 스키마 통과율 100%.
3. 중복 claim과 중복 post 0건.
4. 전체 wall time 24분 이하.
5. 근거가 확인된 강점·약점 비율.
6. 심사위원 점수와의 상관관계.

## 2. 설계 원칙

- 제출 성공이 기능 수보다 우선한다.
- Critic–Verifier는 논리적 책임 분리이며 반드시 별도 장기 세션일 필요는 없다.
- LLM은 리뷰 내용을 판단하고 결정적 코드는 상태, 시간, 스키마, retry, posting을 통제한다.
- 한 논문의 실패가 큐 전체를 중단하지 않는다.
- 모든 외부 side effect는 idempotency key와 receipt를 남긴다.
- 근거가 없으면 confidence를 낮추고 Comment에 한계를 밝힌다.
- 실제 플랫폼 계약을 추측하지 않는다.

## 3. 런타임 아키텍처

```text
Candidate Queue
  ↓
Bounded Worker Pool
  ↓
OpenAgentReview Adapter
  ├── claim
  └── download PDF
  ↓
Page-aware PDF Extractor
  ↓
Evidence-bound Reviewer
  ├── Critic discipline
  └── Verifier discipline
  ↓
Deterministic Review Validator
  ├── pass → post
  └── fail → one-shot targeted repair → validate → post or fail
  ↓
Receipt Verification + Append-only Ledger
```

기본 worker 수는 3이다. 실제 플랫폼이 동시 claim이나 post를 제한하면 2 또는 1로 낮춘다. 동시성은 반드시 테스트로 결정한다.

## 4. 논문당 시간 예산

| 단계 | 목표 | Hard cap |
|---|---:|---:|
| browse / claim / download | 15초 | 25초 |
| PDF 추출 | 10초 | 20초 |
| 리뷰 호출 | 55초 | 75초 |
| validation / optional repair | 20초 | 35초 |
| post / receipt 확인 | 15초 | 25초 |
| 합계 | 115초 | 120초 |

전체 batch deadline은 24분으로 설정해 마지막 1분을 상태 확인에 남긴다. 3개 worker 기준 네 번의 wave로 10편을 처리하면 목표 wall time은 약 8–10분이며, 나머지는 플랫폼 지연과 한 번의 retry를 위한 여유다.

## 5. 상태와 복구

논문 상태는 다음 단방향 전이를 따른다.

```text
queued → claimed → downloaded → reviewed → validated → posted
   └────────────── failure at any stage ──────────────→ failed
```

모든 전이는 `ledger.jsonl`에 append한다. 런타임 중 Git rollback은 사용하지 않는다. 재시작 시 ledger와 플랫폼 status를 대조해 `posted` 논문은 건너뛰고, claim된 미완료 논문만 안전하게 재개한다.

플랫폼 작업은 다음 idempotency key를 사용한다.

```text
sha256(event_id + paper_id + agent_version + review_hash)
```

## 6. 리뷰 생성 규율

한 번의 reviewer 호출에서 다음을 모두 생성한다.

- 논문 요약.
- 근거 위치가 있는 강점.
- 네 축에 매핑된 근거 위치가 있는 약점.
- Soundness 1–4.
- Presentation 1–4.
- Significance 1–4.
- Originality 1–4.
- Overall Recommendation 1–6.
- Confidence 1–5.
- 건설적인 Comment.
- 한계와 확인하지 못한 사항.

Critic 규율은 중요한 이슈 후보를 찾는다. Verifier 규율은 각 최종 이슈가 실제 페이지·섹션·표·그림에 연결되는지 확인하고, 확인하지 못한 내용은 확정 약점에서 제거하거나 불확실성으로 표시한다.

원 논문과 참고문헌만 읽는 경우 Originality는 전 세계 문헌에 대한 완전한 novelty 판정이 아니라 제출물에 나타난 차별화의 명확성과 설득력을 평가한다.

## 7. 결정적 Validation

다음 조건은 post 전에 코드로 검사한다.

- 모든 필수 필드 존재.
- 점수의 타입과 범위.
- 빈 Summary 또는 Comment 금지.
- Strength와 Weakness의 근거 위치 존재.
- `overall_recommendation`과 Comment의 극단적 모순 탐지.
- paper ID와 hash 일치.
- credential 또는 private data 패턴 부재.
- 플랫폼 payload 변환 성공.

repair는 누락되거나 잘못된 필드만 대상으로 한 번 수행한다. 전체 리뷰를 무제한 재생성하지 않는다.

## 8. 플랫폼 Adapter 계약

```python
class ReviewPlatform:
    def list_candidates(self) -> list[PaperRef]: ...
    def claim(self, paper_id: str) -> ClaimReceipt: ...
    def download_pdf(self, paper_id: str) -> bytes: ...
    def post_review(self, paper_id: str, payload: dict, idempotency_key: str) -> PostReceipt: ...
    def get_status(self, paper_id: str) -> SubmissionStatus: ...
```

mock adapter와 실제 adapter가 같은 contract test를 통과해야 한다. 실제 API가 없고 브라우저 UI만 있다면 행사 skill의 절차를 adapter로 감싸되 DOM selector를 문서에서 추측하지 않는다.

## 9. 단계별 실행 계획

### Phase A — Research Specification, 11:00–12:30

- 성공 지표와 리뷰 스키마를 고정한다.
- 공식 skill과 OpenAgentReview 인터페이스를 확보한다.
- Technical Report의 가설을 고정한다.

연구 가설은 다음과 같이 제한한다.

> Evidence-bound Critic–Verifier 규율과 결정적 form validator가 단일-pass reviewer보다 근거 없는 핵심 지적을 줄이면서, 10편·25분 제출 제약을 만족할 수 있는가.

### Phase B — Ralph Loop, 12:30–15:30

우선순위 순서대로 구현한다.

1. P0 실제 플랫폼 한 편 왕복.
2. P1 mock 10편 batch와 deadline.
3. P2 evidence-bound reviewer와 validator.
4. P3 소규모 seeded micro-case와 측정.
5. Technical Report 초안과 evidence summary.

P0 또는 P1이 통과하지 않으면 P3을 진행하지 않는다.

### Phase C — Human Editing, 15:30–16:30

- 코드 feature freeze.
- Technical Report 익명화와 4페이지 확인.
- Title과 Abstract 확정.
- 실제 platform smoke test.
- 실행 명령, credentials 상태, clock sync 확인.
- 16:30 이전 제출 및 receipt 확인.

### Phase D — Review Run, 16:35–17:00

- 검증된 batch 명령 하나를 실행한다.
- 인간은 직접 수정하지 않고 허용된 관찰 채널만 본다.
- 24분 deadline에서 batch를 종료한다.
- 마지막 1분에 10편 status와 receipt를 자동 재확인한다.

## 10. 평가 설계

### 필수 운영 평가

- mock 10편 batch 3회.
- 실제 플랫폼 1편 claim-post 왕복.
- malformed LLM output repair.
- 한 worker timeout 이후 나머지 큐 완주.
- 재시작 후 중복 post 방지.

### 최소 연구 평가

4–8개의 seeded micro-case만 사용한다.

- 존재하지 않는 표를 지적하는 hallucinated location.
- 본문 수치와 표 수치 불일치.
- 지원되지 않는 인과 주장.
- 명시된 limitation을 누락으로 잘못 비판.
- 관련 연구와의 차별화가 불명확한 사례.

보고 지표는 issue precision, seeded recall, location accuracy, schema pass, p50/p95 latency, post success다. 표본이 작으므로 일반화를 주장하지 않는다.

## 11. 제출물

행사 필수 제출물은 다음과 같다.

- 익명 Technical Report PDF.
- Title.
- Abstract.
- OpenAgentReview에 게시된 배정 논문의 리뷰.

심사와 재현을 위한 보조 산출물은 다음과 같다.

- `review-agent.md`.
- agent version과 입력 hash.
- review schema.
- evaluation summary.
- latency와 failure ledger.
- evidence trace 예시.
- W&B 또는 Weave 링크는 실제로 검증됐을 때만 포함.

## 12. Technical Report 핵심 주장

보고서가 주장할 수 있는 범위는 실제 측정 결과로 제한한다.

- Critic–Verifier 책임 분리가 근거 추적을 제공한다.
- 결정적 validator가 폼 누락과 범위 오류를 차단한다.
- bounded batch orchestration이 10편 처리량을 통제한다.
- 소규모 seeded test에서 관찰된 precision과 location accuracy.

심사위원 점수와의 상관관계는 실제 심사 결과를 받기 전에는 목표 지표로만 표현한다.

## 13. Go / No-Go 게이트

| 시각 | Go 조건 | 실패 시 |
|---|---|---|
| 12:30 | 플랫폼 계약과 리뷰 필드 확인 | adapter를 blocker로 명시하고 즉시 확보 |
| 13:30 | 한 편 end-to-end receipt | 품질 기능 중단, 플랫폼 경로 집중 |
| 14:30 | mock 10/10, schema 100% | 병렬도·timeout·repair 단순화 |
| 15:00 | mock batch 3회, 실제 smoke test | 새 기능 freeze, 제출 안정화 |
| 15:30 | 코드 freeze와 보고서 초안 | 문서 편집과 smoke test만 수행 |
| 16:20 | PDF·Title·Abstract 업로드 완료 | 즉시 제출 완료와 receipt 확인 |

## 14. 최종 acceptance criteria

- `pytest`가 통과한다.
- mock 10편 batch가 3회 연속 24분 이내 10/10 완료된다.
- 리뷰 스키마 통과율이 100%다.
- 중복 claim과 post가 0건이다.
- 한 논문 timeout에도 나머지 논문이 완료된다.
- 실제 플랫폼 한 편 왕복 또는 명시적인 platform blocker가 기록된다.
- Technical Report 본문이 4페이지 이하이고 익명이다.
- Title과 Abstract 파일이 존재한다.
- 최종 10편 status 검증 명령이 존재한다.

# Citations

- `submission_contract.md`.
- `technical_report_outline.md`.
- https://github.com/team-attention/ralphthon-icml

