---
type: Archived Implementation Roadmap
title: 랄프톤 Track 2 구현 계획 v3
description: 장기형 Critic–Verifier 하네스 계획. 행사 MVP는 v4를 우선한다.
tags: [ralphthon, track-2, archived, critic-verifier]
timestamp: 2026-07-12T11:28:00+09:00
status: superseded
superseded_by: implementation_roadmap_v4_event_mvp.md
---

# 랄프톤 @ICML Track 2 구현 계획 v3
## Critic–Verifier 리뷰 하네스: 3단계 개발 로드맵

> 목표: 단순히 논문 리뷰를 생성하는 에이전트가 아니라, **발견·검증·판정·평가·복구가 분리된 신뢰 가능한 리뷰 하네스**를 구현한다.
>
> 포트폴리오 메시지: **“에이전트를 만든 것이 아니라, 에이전트가 측정 가능하고 통제 가능한 방식으로 일하도록 실행 환경과 검증 규율을 설계했다.”**

---

## 0. v2에서 반영한 핵심 수정

### 유지하는 핵심 컨셉

- Critic과 Verifier의 역할 분리
- LLM이 아닌 결정적 코드가 다음 단계를 선택
- 에이전트 간 직접 대화 대신 파일 기반 상태 전달
- seeded-error 평가 세트와 정량 평가
- 역할별 모델·비용 라우팅
- 실행 로그와 trace를 통한 provenance 제공
- Git 기반 복구와 실험 이력 관리

### 수정한 부분

- ICML 평가 축을 `soundness / presentation / significance / originality`로 정정
- CriticGPT는 논문 리뷰 효과의 직접 근거가 아니라 **설계에 영감을 준 사례**로 표현
- `Evidence-Dropout`을 자동 기각 규칙에서 **Evidence Sensitivity 보조 신호**로 변경
- `verified / plausible_unverified / refuted / insufficient_evidence / duplicate` 상태로 세분화
- `plausible_unverified`는 삭제하지 않고 `Key Questions for Authors`로 이동
- `verify.py`와 권한 통제를 분리: 품질 게이트와 sandbox·permission은 서로 다른 계층
- `/side`는 주최 측 허용 확인 전 사용하지 않음
- `runtime 리뷰 루프`와 `Autoresearch 메타 최적화 루프`를 분리
- 역할 설정과 권한 설정을 별도 관리
- Weave는 하네스 stage와 Codex JSON event를 추적하며, Codex 내부 모든 호출을 감싼다고 표현하지 않음
- OKF는 필수 기능이 아닌 **0.1 Draft 기반 실험적 확장 기능**으로 3단계에 배치

---

# 1. 전체 시스템 정의

## 1.1 한 문장 아키텍처

```text
논문 입력
→ 구조 추출
→ ICML 4축 이슈 후보 생성
→ 위치·근거·수치·논리 검증
→ 검증 상태별 리뷰 항목 분류
→ ICML 형식 리뷰 생성
→ seeded-error 평가와 trace 기록
```

## 1.2 두 종류의 루프를 명확히 분리

### A. Runtime Review Loop

한 편의 논문을 끝까지 리뷰하기 위한 실행 루프다.

```text
Ingestor → Critic → Verifier → Judge → Artifact Validator
```

- 목적: 한 편의 논문 리뷰 완주
- 성공 기준: 리뷰 산출물 완결성과 형식 검증 통과
- 실패 대응: 해당 stage 원복 또는 재시도
- Git 의미: 실행 이력과 복구 지점

### B. Autoresearch Optimization Loop

프롬프트나 workflow 자체를 반복 개선하는 메타 루프다.

```text
가설 생성
→ mutable 영역 수정
→ dev 평가 세트 실행
→ baseline과 비교
→ keep 또는 revert
```

- 목적: 리뷰 파이프라인 품질 개선
- 성공 기준: baseline보다 정량 지표 향상
- 실패 대응: Git revert
- Git 의미: 개선된 pipeline lineage

두 루프를 하나의 `ralph.sh`에 섞지 않는다.

---

# 2. 권장 저장소 구조

```text
ralphthon-reviewer/
├── README.md
├── AGENTS.md
├── program.md
├── pyproject.toml
│
├── input/                         # 리뷰 대상 논문, 읽기 전용
│   └── paper.pdf
│
├── policies/                      # 공개 규칙·스키마, 읽기 전용
│   ├── icml_rubric.yaml
│   ├── review_schema.json
│   └── scoring_policy.yaml
│
├── private_eval/                  # 정답 라벨·holdout, 에이전트 접근 금지
│   ├── dev_labels.json
│   └── holdout_labels.json
│
├── harness/                       # 결정적 실행 코드, 에이전트 쓰기 금지
│   ├── next_stage.py
│   ├── validate_stage.py
│   ├── validate_artifact.py
│   ├── evaluate_review.py
│   └── permissions.py
│
├── mutable/                       # 메타 루프만 수정 가능
│   ├── workflow.py
│   ├── prompts.yaml
│   └── routing.yaml
│
├── prompts/                       # Runtime 역할 프롬프트
│   ├── ingestor.md
│   ├── critic.md
│   ├── verifier.md
│   └── judge.md
│
├── state/                         # 현재 run의 결정적 상태
│   ├── progress.json
│   ├── sections.json
│   └── issues.jsonl
│
├── output/                        # 최종 산출물
│   ├── review.json
│   └── review.md
│
├── runs/                          # append-only 실행 기록
│   ├── events.jsonl
│   ├── metrics.jsonl
│   ├── traces/
│   └── experiments.jsonl
│
├── scripts/
│   ├── run_review.sh
│   └── optimize_harness.sh
│
└── knowledge/                     # 3단계 확장: OKF 0.1 Draft 번들
```

### 디렉터리 원칙

- `input/`, `policies/`: 에이전트가 읽어야 하는 불변 영역
- `private_eval/`: evaluator만 읽을 수 있는 비공개 평가 영역
- `harness/`: 에이전트는 실행할 수 있으나 수정할 수 없음
- `mutable/`: Autoresearch Optimizer만 수정
- `state/`: 역할별 제한적 쓰기
- `output/`: Judge만 최종 쓰기
- `runs/`: harness가 append, Observer는 읽기 중심

`immutable/` 하나에 모든 것을 넣고 “읽지 말라”고 지시하지 않는다. 읽어야 하는 자료와 비공개 평가 자료를 물리적으로 분리한다.

---

# 3. 역할과 책임

| 역할 | 주요 책임 | 쓰기 가능 영역 | 권장 실행 성격 |
|---|---|---|---|
| Orchestrator | 다음 stage 결정 | `state/progress.json` 제한적 | LLM이 아닌 Python |
| Ingestor | 논문 구조·위치 추출 | `state/sections.json` | 반복적·구조적 작업 |
| Critic | ICML 4축 이슈 후보 생성 | `state/issues.jsonl` candidate 추가 | 높은 추론 품질 |
| Verifier | 후보별 근거·위치·수치·논리 검사 | issue 상태·검증 필드 갱신 | 코드 우선, LLM 보조 |
| Judge | ICML 형식 최종 리뷰 구성 | `output/review.*` | 최종 조립·캘리브레이션 |
| Observer | 실행 후 trace 요약 | `runs/observer_notes.md` | 초기에는 Python 후처리 |
| Optimizer | prompt·workflow 개선 | `mutable/` | 3단계 메타 루프 |

## 3.1 ICML 네 축

Critic은 다음 축을 독립적으로 검토한다.

1. `soundness`
2. `presentation`
3. `significance`
4. `originality`

외부 문헌 검색을 사용하지 않는 경우 originality의 범위를 다음처럼 제한한다.

> 제공된 논문과 reference corpus를 기준으로 한 originality 평가

전 세계 선행연구 대비 완전한 novelty 판정을 주장하지 않는다.

---

# 4. 이슈 상태머신

```text
candidate
  ↓
checking
  ├── verified
  ├── plausible_unverified
  ├── insufficient_evidence
  ├── refuted
  └── duplicate
```

| 상태 | 의미 | 최종 리뷰 반영 |
|---|---|---|
| `verified` | 위치와 근거가 확인되고 지적이 뒷받침됨 | Strength 또는 Weakness |
| `plausible_unverified` | 중요한 가능성이 있으나 확정 근거 부족 | Key Questions for Authors |
| `insufficient_evidence` | 현재 논문 정보만으로 판단 불가 | 내부 로그 또는 제한적 질문 |
| `refuted` | 검사 결과 지적이 성립하지 않음 | 리뷰에서 제외, trace 보존 |
| `duplicate` | 기존 이슈와 실질적으로 동일 | 대표 이슈에 병합 |

## 4.1 issue 레코드 예시

```json
{
  "issue_id": "ISSUE-0042",
  "axis": "soundness",
  "status": "verified",
  "claim": "표 3의 합계가 본문 설명과 일치하지 않는다.",
  "location": {
    "section": "4.2",
    "page": 7,
    "anchor": "Table 3"
  },
  "evidence": [
    {
      "source": "paper",
      "text": "...",
      "entailment": "supports"
    }
  ],
  "checks": {
    "location_exists": true,
    "numeric_consistency": false,
    "evidence_entailment": 0.94,
    "sensitivity_delta": 0.31
  },
  "severity": "major",
  "confidence": 0.91
}
```

---

# 5. 검증 계층

## 5.1 L1 — 결정적 검사

가장 먼저 코드로 확인한다.

- 섹션·페이지·표·그림 위치 존재 여부
- 인용문이 원문에 존재하는지
- 숫자 합계·비율·범위 일관성
- 스키마 유효성
- 중복 이슈 탐지
- 필수 필드 누락

## 5.2 L2 — 의미 검증

LLM을 보조적으로 사용한다.

- 인용 근거가 지적을 실제로 뒷받침하는가
- 지적이 논문의 주장과 관련 있는가
- severity가 과장되지 않았는가
- 질문으로 남겨야 하는지 확정 이슈인지

## 5.3 L3 — Evidence Sensitivity

기존 Evidence-Dropout을 자동 기각 규칙으로 사용하지 않는다.

```text
전체 문맥 판단 신뢰도
- 핵심 근거를 마스킹한 판단 신뢰도
= sensitivity_delta
```

이 값은 다음과 같이 사용한다.

- confidence를 조정하는 보조 신호
- 근거 의존성을 보여주는 trace
- 단독 reject 조건으로 사용하지 않음

Paraphrase-Survival 역시 확립된 표준 기법이 아니라 이 프로젝트의 custom heuristic으로 명시한다.

---

# 6. 최종 리뷰 스키마

```yaml
summary: string

strengths:
  - claim: string
    evidence_locations: []

weaknesses:
  soundness: []
  presentation: []
  significance: []
  originality: []

key_questions_for_authors:
  - question: string
    why_it_matters: string
    evaluation_change_if_resolved: string

limitations_assessment:
  adequately_discussed: boolean
  comments: string

ratings:
  soundness: 1..4
  presentation: 1..4
  significance: 1..4
  originality: 1..4
  overall_recommendation: 1..6
  confidence: 1..5
```

---

# 7. 평가 설계

## 7.1 산출물 완결성 게이트

```text
schema_pass
AND required_sections_complete
AND all_accepted_issues_have_location
AND all_accepted_issues_have_evidence
AND citation_targets_exist
AND no_unresolved_runtime_error
```

이 게이트는 리뷰가 완성됐는지를 판단하지만, 리뷰의 질을 단독으로 보장하지 않는다.

## 7.2 품질 지표

- seeded issue recall
- issue precision
- issue-level F1
- evidence entailment accuracy
- location accuracy
- severity calibration
- ICML form completeness
- latency
- token 또는 API cost
- failure rate

## 7.3 데이터 분리

```text
dev set
  매 실험의 keep/revert에 사용

hidden holdout
  최종 후보 비교에만 사용

demo paper
  발표에서 사람이 직접 검토
```

초기 논문 수가 적다면, 논문 2~3편 안에 20~40개의 독립적인 seeded-error micro-case를 구성한다.

## 7.4 메타 루프 acceptance rule

```text
candidate_score > baseline_score + epsilon
AND issue_precision >= precision_floor
AND evidence_entailment >= evidence_floor
AND no_schema_regression
AND cost <= budget
```

예시 종합 점수:

```text
quality_score
- cost_penalty
- latency_penalty
- failure_penalty
```

---

# 8. 권한과 보안

## 8.1 세 계층을 분리

### Approval

에이전트가 언제 사람에게 확인할지에 대한 정책이다.

### Sandbox·Permission

에이전트가 어떤 파일과 명령에 접근할 수 있는지 통제한다.

### Evaluator

실행 결과가 품질 기준을 만족하는지 사후 판정한다.

`verify.py`는 quality approval 일부를 자동화할 수 있지만 sandbox와 permission을 대체하지 않는다.

권장 발표 문구:

> 사람의 품질 승인 일부는 acceptance test로 자동화했지만, 행동 권한은 별도의 sandbox와 permission profile로 통제했습니다.

## 8.2 Role configuration과 Permission configuration 분리

```text
역할 설정
- ingestor.config.toml
- critic.config.toml
- verifier.config.toml
- judge.config.toml

권한 설정
- review-reader
- review-state-writer
- review-output-writer
- evaluator-only
```

## 8.3 네트워크

- 기본값: 외부 네트워크 차단
- 필요한 경우: W&B 업로드 도메인만 허용
- private_eval과 secret label은 외부 trace에 포함 금지
- 논문 본문 전체를 remote trace에 기록하지 않고 hash·section ID 중심으로 기록

## 8.4 행사 중 관찰

`/side`가 코딩 에이전트 직접 개입으로 해석될 수 있으므로 주최 측의 명시적 허용 전에는 사용하지 않는다.

대신 다음으로 관찰한다.

```text
state/progress.json
runs/events.jsonl
runs/metrics.jsonl
Weave dashboard
git log
```

---

# 9. 실행 스크립트 설계

## 9.1 Runtime 루프: `scripts/run_review.sh`

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

MAX_ITERS="${MAX_ITERS:-30}"
RUN_ID="$(date +%Y%m%d-%H%M%S)"

mkdir -p runs
CODEX_LOG="runs/${RUN_ID}.codex.jsonl"
METRIC_LOG="runs/${RUN_ID}.metrics.jsonl"

[[ -z "$(git status --porcelain)" ]] || {
  echo "Working tree must be clean before starting." >&2
  exit 2
}

rollback() {
  local base="$1"
  git reset --hard "$base" >/dev/null
  git clean -fd -- state output >/dev/null
}

for ((iter=0; iter<MAX_ITERS; iter++)); do
  stage="$(python harness/next_stage.py)"

  case "$stage" in
    done)
      break
      ;;
    ingestor|critic|verifier|judge)
      ;;
    *)
      echo "Invalid stage: $stage" >&2
      exit 3
      ;;
  esac

  base="$(git rev-parse HEAD)"

  if ! codex exec \
      --profile "$stage" \
      --sandbox workspace-write \
      --json - \
      < "prompts/${stage}.md" \
      >> "$CODEX_LOG"; then
    rollback "$base"
    continue
  fi

  if ! metric="$(
    python harness/validate_stage.py \
      --stage "$stage" \
      --json
  )"; then
    rollback "$base"
    continue
  fi

  if ! jq -e . >/dev/null <<< "$metric"; then
    rollback "$base"
    continue
  fi

  printf '%s\n' "$metric" >> "$METRIC_LOG"

  if jq -e '.passed == true' >/dev/null <<< "$metric"; then
    git add -- state output

    if ! git diff --cached --quiet; then
      git commit -m "run ${RUN_ID} iter ${iter}: ${stage}"
    fi
  else
    rollback "$base"
  fi
done

python harness/validate_artifact.py --json
```

### Runtime 루프의 핵심

- 명령 실패 시 다음 stage로 진행하지 않음
- stage 이름 whitelist 적용
- 검증 실패 시 rollback
- `git add -A` 금지
- JSONL 형식 검증
- 변경이 있을 때만 커밋
- evaluator와 private label은 커밋 대상이 아님

## 9.2 Meta 루프: `scripts/optimize_harness.sh`

3단계에서 구현한다.

```text
baseline 측정
→ Optimizer가 mutable/에서 가설 1개 구현
→ dev 평가
→ acceptance rule 적용
→ keep 또는 revert
→ experiments.jsonl 기록
```

---

# 10. AGENTS.md 초안

```markdown
# AGENTS.md

## Project
This repository implements a file-coordinated ICML review harness.
Read state/progress.json before acting.

## General rules
- Read before write.
- Perform only the current assigned stage.
- Never modify harness/, policies/, or private_eval/.
- Never read private_eval/.
- Do not claim completion. Completion is decided by deterministic validators.
- Record outputs only in the paths permitted for your role.
- Do not expose credentials, secret labels, or full paper text to remote traces.
- Do not use external network access unless explicitly allowed by the permission profile.

## Role boundaries
- Ingestor writes state/sections.json.
- Critic appends candidate issues to state/issues.jsonl.
- Verifier updates validation fields and status.
- Judge writes output/review.json and output/review.md.

## Failure handling
- On malformed input, record the failure in state/progress.json.
- Do not silently invent missing sections, tables, citations, or results.
- Use degraded mode only when the policy explicitly allows it.
```

---

# 11. Weave 추적 원칙

## 11.1 추적 대상

```text
run_review
  ├── ingest_paper
  ├── generate_critic_candidates
  │   ├── soundness
  │   ├── presentation
  │   ├── significance
  │   └── originality
  ├── verify_candidate
  ├── aggregate_review
  └── evaluate_review
```

## 11.2 구현 방식

- 하네스의 stage 함수는 가능한 범위에서 `@weave.op()`으로 감싼다.
- Codex CLI 자체는 `codex exec --json` event stream으로 수집한다.
- 동일 `run_id`로 stage trace와 Codex event를 연결한다.
- secret label과 private holdout은 trace에 포함하지 않는다.
- remote logging이 불확실하면 local JSONL을 원본 기록으로 유지한다.

---

# 12. 3단계 구현 로드맵

# 단계 1. 전체 틀과 End-to-End Thin Slice

## 목표

가장 단순한 입력 한 편을 대상으로, **Ingestor → Critic → Verifier → Judge → Validator**가 한 번 끝까지 흐르는 구조를 만든다.

이 단계에서는 높은 리뷰 품질보다 **하네스가 중단 없이 완주하고, 실패를 감지하고, 상태를 남기는 것**이 우선이다.

## 구현 범위

### 필수

- 저장소 구조 생성
- `AGENTS.md`, `program.md`, 공개 review schema 작성
- `state/progress.json` 기반 결정적 상태머신
- Ingestor 1개
- Critic 1개: 네 축을 한 번에 처리해도 됨
- Verifier 최소 검사
  - 위치 존재 여부
  - 인용 실재성
  - 스키마 검사
- Judge 1개
- `run_review.sh`
- `validate_stage.py`
- `validate_artifact.py`
- local JSONL 로그
- 최종 `review.json`, `review.md`

### 아직 하지 않을 것

- Critic 4축 병렬 subagent
- Evidence Sensitivity
- Autoresearch prompt 최적화
- hidden holdout
- LLM Observer
- OKF
- Desktop `/goal` 대체 경로

## 단계 1 산출물

```text
한 편의 논문 입력
→ 완성된 review.json / review.md
→ stage별 events.jsonl
→ 실패 시 rollback 기록
```

## 종료 기준

- fresh clone에서 단일 명령으로 실행 가능
- 입력 논문 한 편에 대해 3회 연속 완주
- stage 실패를 인위적으로 발생시켰을 때 rollback 확인
- 최종 review schema 통과
- Critic 후보가 Verifier를 우회해 Judge에 들어갈 수 없음

## 데모 포인트

> “에이전트가 순서를 결정하지 않습니다. 상태머신이 현재 stage를 결정하고, 각 stage는 자신의 제한된 파일만 변경합니다.”

## 예상 작업 비중

- 하네스·상태머신: 40%
- 최소 역할 구현: 30%
- 스키마·검증: 20%
- 로그·데모: 10%

---

# 단계 2. 중요 모듈의 품질과 검증 강화

## 목표

단계 1의 thin slice를 **실제로 평가 가능한 리뷰 시스템**으로 확장한다.

이 단계가 해커톤 제출의 핵심 완성본이다.

## 2.1 Critic 세부화

- ICML 4축별 후보 생성 구조
- 각 후보에 위치·근거·severity·confidence 요구
- 중복 후보 병합
- 근거 없는 확정 표현 금지
- originality 평가 범위 제한 명시

초기에는 하나의 Critic 호출이 네 축을 순차 처리해도 된다. 병렬 subagent는 3단계다.

## 2.2 Verifier 세부화

### 결정적 검사

- section·page·table·figure anchor 확인
- 인용문 존재 여부
- 숫자·비율·합계 검사
- 필수 필드·schema 검사
- duplicate 탐지

### 의미 검사

- evidence entailment
- claim relevance
- severity calibration
- verified와 plausible_unverified 구분

### 상태 라우팅

```text
verified → Weakness/Strength
plausible_unverified → Key Questions for Authors
insufficient_evidence → 내부 기록 또는 제한적 질문
refuted → 최종 리뷰 제외
```

## 2.3 Evaluation Harness

- seeded-error micro-case 20~40개
- dev set과 demo paper 분리
- recall·precision·F1·evidence accuracy 계산
- cost·latency·failure rate 기록
- baseline 결과 저장

hidden holdout은 가능하면 이 단계 말미에 추가하되, 시간 부족 시 3단계로 미룬다.

## 2.4 Trace와 관찰성

- run_id 통일
- stage 시작·종료·실패 이벤트
- issue provenance
- Codex JSON event 수집
- Weave stage trace
- remote trace에 논문 전체와 secret label을 남기지 않음

## 2.5 권한 테스트

- Critic이 `output/`을 수정하지 못함
- Judge가 `private_eval/`을 읽지 못함
- 에이전트가 `harness/`를 수정하지 못함
- network off에서도 리뷰가 완주함

## 단계 2 산출물

- ICML 형식 최종 리뷰
- seeded-error 평가 리포트
- issue별 provenance 화면
- baseline과 현재 품질 비교
- 권한·실패·복구 테스트 결과

## 종료 기준

- seeded issue recall과 precision을 모두 제시
- 모든 최종 Weakness가 evidence와 location을 가짐
- refuted 이슈가 최종 리뷰에 포함되지 않음
- plausible 이슈가 질문으로 이동함
- cost·latency·failure rate가 자동 기록됨
- 데모에서 하나의 이슈 lineage를 끝까지 추적 가능

## 데모 포인트

> “Critic이 지적을 만들었다고 바로 믿지 않습니다. 검증된 이슈는 Weakness로, 확정할 수 없는 이슈는 저자 질문으로 이동하고, 반박된 이슈는 trace에만 남습니다.”

---

# 단계 3. 확장 기능과 Autoresearch 메타 최적화

## 목표

단계 2의 안정된 시스템 위에서 차별화 기능을 추가한다. 이 단계는 시간이 남을 때 순차적으로 구현한다.

## 우선순위 3-1. Autoresearch Meta Loop

가장 먼저 추가할 확장이다.

### 수정 가능 영역

```text
mutable/prompts.yaml
mutable/workflow.py
mutable/routing.yaml
```

### 고정 영역

```text
harness/
policies/
private_eval/
```

### 실험 단위

- 가설 1개
- coherent change 1개
- 실험 1회
- 결과 1개
- keep 또는 revert

### 예시 가설

- Critic에게 section anchor를 먼저 요구하면 location accuracy가 개선된다.
- Verifier의 evidence entailment rubric을 구체화하면 precision이 개선된다.
- 질문과 확정 지적의 threshold를 분리하면 F1이 개선된다.

### 종료 기준

- baseline 대비 향상된 커밋 최소 1개
- 실패한 실험의 자동 revert 확인
- `runs/experiments.jsonl`에 가설·diff·지표·판정 기록

## 우선순위 3-2. Critic 병렬화

- soundness
- presentation
- significance
- originality

각 축은 별도 결과 파일에 기록하고 parent aggregator가 atomic merge한다.

```text
runs/candidates/soundness.json
runs/candidates/presentation.json
runs/candidates/significance.json
runs/candidates/originality.json
```

동일 JSONL 파일에 subagent가 동시에 append하지 않는다.

병렬화는 품질 개선이 아니라 latency·coverage·비용 관점에서 baseline과 비교한다.

## 우선순위 3-3. Evidence Sensitivity

- 원문 판단 confidence
- 핵심 evidence 마스킹 후 confidence
- sensitivity delta 계산
- 자동 reject가 아닌 보조 신호로 활용

## 우선순위 3-4. Hidden Holdout

- Optimizer가 접근할 수 없는 평가 세트
- 최종 후보를 한 번 비교
- dev set 과적합 여부 확인

## 우선순위 3-5. OKF 0.1 Draft 번들

OKF는 최종 리뷰 품질을 직접 높이는 핵심 기능이 아니므로 후순위다.

표현:

> Google Cloud가 공개한 OKF 0.1 Draft를 실험적으로 적용했다.

### 지식 번들 예시

```text
knowledge/
├── index.md
├── log.md
├── papers/
├── reviews/
├── issues/
├── runs/
└── experiments/
```

`resource`에는 안정적인 URI를 사용한다.

```yaml
resource: "urn:ralphthon:run:20260712-1:issue:0042"
run_id: "20260712-1"
issue_id: "0042"
source_log: "../runs/issues.jsonl"
```

“모든 에이전트가 소비 가능”이라고 단정하지 않고, 최소 규격 기반의 잠재적 상호운용성을 제공한다고 표현한다.

## 우선순위 3-6. Desktop `/goal` 보조 경로

- CLI가 정식·재현 가능한 실행 경로
- Desktop `/goal`은 데모·비상용 보조 경로
- CLI와 기능적으로 동일하다고 주장하지 않음
- 행사 규칙상 허용 여부를 사전 확인

## 우선순위 3-7. LLM Observer

초기 Observer는 Python 집계기로 충분하다.

LLM Observer는 다음이 필요할 때만 추가한다.

- 여러 run의 failure mode를 자연어로 군집화
- 실험 결과를 자동 회고
- 다음 Autoresearch 가설 후보 제안

Observer가 runtime 상태를 직접 변경하지 못하게 한다.

---

# 13. 단계별 일정표

## 1단계: 전체 틀

| 작업 | 예상 시간 | 완료 증거 |
|---|---:|---|
| 저장소·권한 구조 | 1시간 | 디렉터리와 permission matrix |
| 상태머신·runner | 2시간 | 한 명령 완주 |
| 최소 4역할 | 2시간 | review.json 생성 |
| validator·rollback | 2시간 | 실패 주입 테스트 |
| 데모 로그 | 1시간 | events.jsonl |

## 2단계: 중요 모듈

| 작업 | 예상 시간 | 완료 증거 |
|---|---:|---|
| 4축 Critic | 2시간 | 축별 후보 |
| Verifier 계층 | 3시간 | verified/refuted 분류 |
| seeded-error 평가 | 3시간 | recall·precision |
| Weave·trace | 2시간 | issue lineage |
| 권한·스트레스 테스트 | 2시간 | 테스트 리포트 |

## 3단계: 확장

| 우선순위 | 기능 | 예상 시간 |
|---:|---|---:|
| 1 | Autoresearch Meta Loop | 3~5시간 |
| 2 | Critic 병렬화 | 2~3시간 |
| 3 | Evidence Sensitivity | 1~2시간 |
| 4 | Hidden Holdout | 1~2시간 |
| 5 | OKF 번들 | 2~3시간 |
| 6 | Desktop 보조 경로 | 1~2시간 |
| 7 | LLM Observer | 2시간 |

---

# 14. 단계별 Go / No-Go 기준

## 1단계에서 2단계로 넘어가는 조건

- end-to-end 리뷰 완주
- failure rollback 동작
- 역할별 쓰기 경계 확인
- review schema 통과

하나라도 실패하면 기능을 추가하지 않고 1단계를 고친다.

## 2단계에서 제출 가능한 조건

- seeded-error 지표 제공
- issue provenance 제공
- verified·plausible·refuted 분리
- 권한과 복구 시나리오 시연

이 조건을 만족하면 3단계 기능이 없어도 제출 가능한 완성본이다.

## 3단계 기능 추가 조건

- 새 기능이 baseline 품질이나 데모 메시지를 실제로 개선함
- 핵심 파이프라인의 안정성을 해치지 않음
- 추가 기능 실패 시 제거 가능한 feature flag 구조

---

# 15. 발표 구조

## 90초 피치

> “LLM 리뷰어는 중요한 문제를 놓치기도 하고, 존재하지 않는 문제를 그럴듯하게 만들어내기도 합니다.
>
> 그래서 발견과 판정을 분리했습니다. Critic은 ICML의 soundness, presentation, significance, originality 축에서 이슈 후보를 만들고, Verifier는 인용 위치, 수치 일관성, 그리고 근거가 실제로 지적을 뒷받침하는지를 검사합니다.
>
> 에이전트끼리는 직접 대화하지 않습니다. 결과는 파일 상태로 기록되고, 다음 단계와 완료 여부는 LLM이 아니라 결정적 상태머신과 acceptance test가 판단합니다.
>
> 검증된 문제는 Weakness로, 가능성은 있지만 증거가 부족한 문제는 Key Questions for Authors로 이동합니다. 반박된 문제도 삭제하지 않고 trace에 남깁니다.
>
> 이 화면은 오류를 미리 심어둔 평가 세트에서 측정한 recall, precision, evidence accuracy입니다. 각 지적이 어느 문장과 검사 결과를 거쳐 최종 리뷰에 포함됐는지도 추적할 수 있습니다.
>
> 핵심은 리뷰를 작성하는 모델이 아닙니다. 리뷰를 믿을 수 있게 만드는 하네스입니다.”

## 데모 순서

1. `program.md`와 permission matrix
2. `state/progress.json` 상태 전이
3. Critic candidate 생성
4. Verifier가 한 후보를 verified 또는 refuted로 판정
5. 최종 review의 Weakness와 Questions 분리
6. seeded-error 평가 지표
7. issue provenance trace
8. 시간이 남으면 Autoresearch 실험 keep/revert

---

# 16. 이력서 표현

## 간결형

> Codex 기반 멀티에이전트 ICML 리뷰 하네스를 설계하고, 결정적 상태머신·역할별 권한·검증 게이트·Git rollback을 통해 리뷰 생성 과정을 통제 및 추적 가능하게 구현.

## 평가 강조형

> Seeded-error 평가 세트로 issue recall·precision·evidence accuracy를 측정하고, Critic–Verifier 분리 및 provenance trace를 통해 LLM 리뷰의 오탐과 근거 없는 지적을 관리.

## Autoresearch 확장형

> Immutable evaluator와 constrained mutable workspace를 분리한 Autoresearch 메타 루프를 구현하여 prompt·workflow 변경을 자동 평가하고 개선된 실험만 Git lineage에 유지.

---

# 17. 최종 우선순위

## 반드시 완성

1. 결정적 상태머신
2. Critic–Verifier 분리
3. 실패 감지와 rollback
4. ICML 스키마
5. seeded-error 정량 평가
6. issue provenance

## 완성 후 추가

1. Autoresearch 메타 루프
2. Critic 4축 병렬화
3. Evidence Sensitivity
4. hidden holdout
5. OKF 0.1 Draft
6. Desktop 보조 경로
7. LLM Observer

프로젝트의 성공 기준은 기능 수가 아니다.

> **하나의 이슈가 생성되고, 검증되고, 최종 리뷰에 반영되거나 제외되는 전 과정을 재현 가능하게 보여주는 것**이 가장 중요하다.

---

# 참고 링크

- 랄프톤 이벤트 페이지: https://luma.com/hjuo7auc
- ICML Reviewer Instructions: https://icml.cc/Conferences/2026/ReviewerInstructions
- CriticGPT 논문: https://arxiv.org/abs/2407.00215
- Codex 문서: https://developers.openai.com/codex/
- Codex non-interactive mode: https://learn.chatgpt.com/codex/non-interactive-mode
- W&B Skills: https://github.com/wandb/skills
- W&B Weave Tracing: https://weave-docs.wandb.ai/guides/tracking/tracing/
- OKF 0.1 Draft: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
