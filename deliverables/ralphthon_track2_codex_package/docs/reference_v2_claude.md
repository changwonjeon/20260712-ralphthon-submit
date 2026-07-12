---
type: Archived Reference
title: Track 2 Claude 통합 참고자료 v2
description: v4 이전의 아이디어와 배경을 보존한 참고 문서.
tags: [ralphthon, track-2, archived, reference]
timestamp: 2026-07-12T11:28:00+09:00
status: reference-only
---

# 랄프톤 @ICML Track 2 최종 통합 자료 v2 (Codex GPT-5.6 반영판)
## Critic–Verifier 리뷰 에이전트 — 멀티에이전트 Loop Engineering + Codex 실행 전략

v1 대비 변경: 최신 Codex 환경(2026-07-09 ChatGPT 데스크톱 통합, GPT-5.6 Sol/Terra/Luna, AGENTS.md·스킬·/goal·subagents·권한 3축)을 실행 계획에 반영. 컨셉·파이프라인·OKR은 v1 그대로 유지.

---

# PART 1. 최종 컨셉 (변경 없음 — 요약)

**"의심(Critic)과 검증(Verifier)을 분리한 멀티에이전트 리뷰 시스템을, 사람 개입 없는 3중 루프로 굴리고, OKR로 스스로의 완성도를 측정하는 하네스"**

- Critic = recall 전담 (CriticGPT 근거: critic은 버그를 더 많이 잡지만 환각 이슈 생성)
- Verifier = precision 전담, 실행형 검사 (GDG 근거: 실행 가능 Verifier 추가 시 오탐 대폭 감소)
- Judge = Verifier 증거만 신뢰 (GDG 조건: 독립 검증, 맹목 수용 금지)
- 시그니처 검사 = Evidence-Dropout Check (근거 제거 후에도 이슈가 나오면 환각 의심 → 기각)
- 운영 규정 = 카파시 Autoresearch (program.md, 고정 evaluator, Git keep/revert, OKR 자동 측정)

---

# PART 2. Codex GPT-5.6 환경 반영 — 실행 전략 재설계

## 2.1 환경 인식: 두 가지 실행 경로를 모두 준비

2026-07-09부로 Codex 앱이 ChatGPT 데스크톱 앱의 Codex 공간으로 통합됐고, 모델은 GPT-5.6 Sol/Terra/Luna 3계열이 됐다. 랄프톤 당일 주최 측이 CLI 기반 루프를 요구할지, 데스크톱 앱 기반을 허용할지 미확정이므로 **둘 다 준비하되 하네스 코드는 공유**한다.

| | 경로 A: Codex CLI (기본) | 경로 B: 데스크톱 앱 |
|---|---|---|
| 루프 구동 | `ralph.sh` (bash while + `codex exec`) | `/goal` + Scheduled(재실행) |
| 역할 격리 | 역할별 profile/exec 호출 | New task 분리 + `/fork` |
| 상태 인계 | state/progress.md (동일) | state/progress.md (동일) |
| Ralph 정합성 | 원형 그대로 — 우선 채택 | 대안 (CLI 불가 시) |

핵심: **파일 기반 상태머신(progress.md, review_log.jsonl)과 verify.py는 경로와 무관하게 동일** — 하네스를 도구 독립적으로 설계했기 때문에 당일 환경이 무엇이든 대응 가능. 이것 자체가 발표 포인트.

## 2.2 역할별 모델·effort 매핑 (Sol/Terra/Luna 비용 최적화)

가이드의 원칙 — Sol은 판단·마감 품질, Terra는 균형, Luna는 "정답 모양이 분명한 반복 작업" — 을 역할에 그대로 대응:

| 에이전트 | 모델 + effort | 근거 |
|----------|---------------|------|
| Orchestrator | (LLM 아님 — next_stage.py 결정적 코드) | 라우팅에 LLM 불필요 |
| Ingestor | **Luna + Light** | 형식 변환·구조 추출 = 정답 모양이 분명한 작업 |
| Critic | **Sol + High** (+ 필요시 Ultra) | 의심 가설의 질이 전체 recall 상한을 결정 |
| Verifier | **Luna/Terra + Medium** | 검사 대부분이 결정적 코드, LLM은 보조 판정만 |
| Judge | **Sol + Medium~High** | 최종 조립·점수 캘리브레이션 = 마감 품질 |
| Observer | **Terra + Medium** | 트레이스 분류 = 일상 분석 작업 |

**Ultra의 정확한 용도**: 가이드 명시 — Ultra는 "더 오래 생각하는 최고 단계"가 아니라 **분리 가능한 부분을 subagent로 나눠 진행하는 설정**. 우리 구조에서 Ultra가 정확히 맞는 곳은 단 하나: **Critic의 rubric 4축(soundness/presentation/contribution/originality) 병렬 탐색**. 축별로 독립적이므로 subagent 분할에 부합. 그 외 역할에 Ultra를 쓰면 비용만 늘어남.

이 매핑은 "비용·품질을 역할 단위로 설계했다"는 시니어 엔지니어링 어필이 됨 — 대부분 참가자는 전부 최고 모델로 돌림.

## 2.3 Codex 기능 → 하네스 구성요소 매핑

| Codex 기능 | 우리 시스템에서의 사용 |
|------------|------------------------|
| **AGENTS.md** | program.md의 불변 원칙을 요약 반영: "읽기 먼저", 쓰기 권한 매트릭스, immutable/ 접근 금지, "완료 선언 전 verify.py 증거 필수", 출력 위치 규칙. 세션마다 자동 주입되는 레일 |
| **/plan** | 리허설 및 당일 루프 시작 전 1회: "program.md를 읽고 관련 파일·순서·위험·검증 방법을 먼저 제안, 아직 수정 금지" → 계획 확인 후 루프 시작 |
| **/goal** | 경로 B의 루프 엔진. program.md의 Termination 조건(kr_1_1==1.00 AND kr_1_2==1.00 AND 스키마 통과)을 측정 가능한 완료 기준으로 그대로 기입 + "멈출 조건"(예산·연속실패) 명시 |
| **subagents (Ultra)** | Critic rubric축 병렬화 전용 (§2.2) |
| **$스킬** | 반복 절차 2개를 스킬로 사전 등록: ① `$review-verify` (verify.py 실행→KR 기록→실패 사유 progress 기록 절차) ② wandb/skills의 `$wandb-primary` (Weave 트레이스·평가) |
| **/fork** | Autoresearch 메타 루프(L2)의 수동 대안: baseline 워크플로우 태스크를 fork해 A안(단일 Critic)/B안(축별 병렬 Critic)을 비교 — worktree 격리로 원본 보존 |
| **/side** | 관전 중 개입하지 않고 상태만 질문 ("지금 어느 stage, 막힌 것, 다음 행동만 요약") — 랍스터 코스튬을 입지 않고도 관찰 가능한 합법적 창구 |
| **/compact** | 경로 B에서 긴 세션의 컨텍스트 위생 (경로 A는 exec별 fresh context라 불필요) |
| **Worktrees** | L2 메타 루프의 실험 격리: 실험 브랜치가 메인 산출물을 건드리지 않게 |
| **Prevent sleep while running** | 당일 필수 설정 (장시간 루프 중 절전 방지) |

## 2.4 권한 3축 설계 (승인/sandbox/network) — 안전 어필 포인트

가이드의 구분 — **승인(언제 멈춰 물을지) / sandbox(파일·시스템 접근 범위) / network(외부 접속)** — 를 무인 Ralph 루프에 맞게 명시적으로 설계:

- **승인**: 루프 특성상 무인 실행(approval 최소화)이 불가피 → 대신 verify.py 게이트가 승인의 역할을 대체한다고 프레이밍. "사람의 승인을 없앤 게 아니라, 승인을 코드화했다"
- **sandbox**: 프로젝트 폴더로 제한. Full access 금지. immutable/은 파일 권한(chmod)으로도 이중 잠금
- **network**: 리뷰 파이프라인은 원칙적으로 불필요(입력 논문은 로컬) → W&B 업로드 등 필요한 도메인만 허용. "네트워크가 필요 없는 작업에 네트워크를 열지 않았다"는 것도 발표 한 줄

이 3축 명시가 program.md의 Safety 섹션을 대체·강화한다. 심사위원(ex-Trust & Safety 포함) 대상 어필 지점.

## 2.5 "증거 요구" 문화의 정합성

가이드의 핵심 습관 — *"Codex가 완료했다고 말해도, 마지막 요청에 증거를 요구하는 문장을 붙여라"* — 는 우리 하네스의 존재 이유와 정확히 같은 철학. program.md의 문장을 이 표현으로 다듬는다:

```
Never claim completion. Claim evidence: the harness runs verify.py
and only its exit code and okr_progress.jsonl decide completion.
```

발표 멘트: "Codex 공식 가이드조차 '완료 주장 대신 증거를 요구하라'고 가르칩니다. 저는 그 습관을 사람이 아니라 하네스가 수행하도록 만들었습니다."

---

# PART 3. 갱신된 실행 파일들

## 3.1 AGENTS.md (신규 — 리포 루트, 세션마다 자동 주입되는 불변 레일)

```markdown
# AGENTS.md

## What this project is
A multi-agent ICML review harness. Roles (ingestor/critic/verifier/
judge/observer) run as separate sessions coordinated only through
files. Read state/progress.md FIRST in every session.

## Non-negotiable rules
- Read before write. Never redo a completed stage.
- Write ONLY within your role's permission (see program.md matrix).
- Never modify or read: immutable/, harness/, verify.py, seed labels.
- Never claim completion — completion is decided by verify.py exit
  code and okr_progress.jsonl, not by your statement.
- Every LLM call wrapped with @weave.op.
- Outputs go to output/, logs to runs/, state to state/.
- On unparseable input: degraded-mode review + log the degradation.
- No credentials. No network beyond W&B upload.
```

## 3.2 ralph.sh 갱신 (경로 A — 모델 매핑 반영)

```bash
#!/usr/bin/env bash
# config.toml profiles: ingestor(Luna/Light), critic(Sol/High),
# verifier(Terra/Medium), judge(Sol/High), observer(Terra/Medium)
iter=0
while [ $iter -lt 30 ]; do
  next=$(python harness/next_stage.py)          # 결정적 라우팅
  [ "$next" = "done" ] && break
  codex exec --profile "$next" "$(cat prompts/$next.md)"
  python verify.py --all >> runs/okr_progress.jsonl
  git add -A && git commit -m "iter $iter: $next"
  iter=$((iter+1))
done
```

## 3.3 /goal 템플릿 (경로 B — 당일 CLI 불가 시)

```
/goal ICML 리뷰 하네스를 무개입으로 완주해줘.
program.md와 AGENTS.md의 규칙을 따라 stage를 진행해.

완료 기준:
- python verify.py --all 이 exit 0
- kr_1_1(근거 커버리지) == 1.00, kr_1_2(인용 실재성) == 1.00
- output/review.json 스키마 통과 + review.md 렌더링 확인

멈출 조건:
- 30회 반복 초과, 또는 동일 실패 3연속 (전략 전환을 progress.md에 기록 후 지속)
- 비용 한도 도달 시 degraded-mode로 마감하고 상태 보고

불확실하거나 민감한 상황은 추측하지 말고 progress.md에 기록해줘.
```

## 3.4 리허설 절차 갱신 (D-2)

1. `/plan` 으로 program.md 투입 → Codex가 제안하는 계획에서 스펙 결함 발견 (파일 수정 전)
2. 경로 A 리허설: ralph.sh 1회 완주 (arXiv 샘플)
3. 경로 B 리허설: 동일 과제를 `/goal` 로 1회 완주 → 두 경로의 결과 차이 기록
4. `$review-verify` 스킬 등록: "방금 검증 흐름을 재사용 스킬로 정리해줘 — 입력, 절차, 수정 금지 조건, KR 기록, 산출물 경로 포함"
5. Prevent sleep while running 켜기, 권한 3축 값 스크린샷 (발표 자료용)

---

# PART 4. 유지 항목 (v1 참조)

아래는 v1 문서 그대로 유효 — 재수록 생략:
- 3중 루프 구조(L0 Ralph / L1 이슈 상태머신 / L2 Autoresearch 메타)와 back-pressure 3종
- 6개 역할과 파일 쓰기 권한 매트릭스, review_log.jsonl 상태 전이(hypothesis→verified/refuted/unverifiable)
- Verifier 검사 계층 L1(결정적)/L2(Evidence-Dropout·Paraphrase-Survival)/L3(교차 확인)
- okr.yaml (O1 무개입 근거-검증 / O2 정량 품질 / O3 자가 개선) + okr_progress.jsonl
- W&B skills 통합 (Observer의 failure mode 분류, seeded-error 세트 = Weave Evaluation labeled dataset)
- 저장소 구조, seeded-error 논문 제작(최우선), 참고 문헌 9종

---

# PART 5. 준비 체크리스트 최종판

### 오늘 — 2시간
- [ ] ChatGPT 데스크톱 앱 최신 업데이트 + Codex 공간 확인, Codex CLI 별도 설치·로그인 (경로 A/B 양쪽)
- [ ] `npx skills add wandb/skills` + WANDB_API_KEY + Weave hello-world
- [ ] 리포 스캐폴드 커밋: AGENTS.md, program.md, okr.yaml, prompts/ 뼈대
- [ ] config.toml 역할 profile 5개 (모델 매핑 §2.2대로)

### D-2 — 4시간
- [ ] seeded-error 논문 2~3편 + 라벨 (최우선 불변)
- [ ] harness/next_stage.py + ralph.sh + verify.py(--metric)
- [ ] 리허설: /plan → 경로 A 완주 → 경로 B 완주 → 스펙 수정
- [ ] $review-verify 스킬 등록

### D-1 — 3시간
- [ ] Evidence-Dropout Check 구현 + 나쁜 입력 스트레스 테스트
- [ ] Weave Evaluation에 seeded-error 등록, recall 대시보드 확인
- [ ] 권한 3축 설정 확정 + 스크린샷, Prevent sleep 켜기, 피치 암기

### 당일
- 환경 확인(CLI 허용 여부) → 경로 선택 → /plan 1회 → 루프 시작 → 관전
- 개입 창구는 /side (상태 질문)만. 수정은 progress.md/프롬프트로만
- Weave·review_log·okr_progress 스크린샷 수집

---

# PART 6. 90초 피치 (Codex 반영 최종)

> "LLM 리뷰어는 얕게 훑거나, 그럴듯한 환각 지적을 만듭니다.
> 저는 역할을 분리했습니다 — Critic은 Sol로 마음껏 의심하고,
> Verifier는 실행 가능한 검사로 판정합니다. 인용이 본문에 실재하는가,
> 근거를 제거하면 이슈도 사라지는가.
> 다섯 에이전트는 대화하지 않습니다. 파일의 상태 전이로 통신하고,
> 결정적 코드가 조율하며, 역할마다 Sol·Terra·Luna를 비용에 맞게 배치했습니다.
> Codex 가이드는 '완료 주장 대신 증거를 요구하라'고 가르칩니다.
> 저는 그 습관을 하네스에 심었습니다 — 완료는 제 에이전트가 선언하는 게 아니라
> verify.py의 exit code와 이 OKR 대시보드가 결정합니다.
> [Weave 화면] 오류를 심은 논문 세트에서 측정한 recall입니다.
> 저는 코드가 아니라 이 규율을 설계했습니다."

---

# PART 7. 전체 구조도 (ASCII)

```
┌──────────────────────────────────────────────────────────────────────┐
│  운영 규정 레이어 (사람이 사전 작성 — 불변)                              │
│  program.md · AGENTS.md · okr.yaml · immutable/{evaluator,seed,schema}│
└───────────────────────────────┬──────────────────────────────────────┘
                                │ 규칙 주입 (세션마다)
┌───────────────────────────────▼──────────────────────────────────────┐
│  L0. RALPH 루프   ralph.sh — bash while (iter ≤ 30)                   │
│                                                                       │
│   ┌───────────────┐  다음 stage 결정  ┌────────────────────────────┐  │
│   │ next_stage.py │◄─────────────────│ state/progress.md          │  │
│   │ (결정적 코드,  │                  │ 유일한 조율 채널             │  │
│   │  LLM 아님)     │                  │ (완료·실패사유 기록)         │  │
│   └──────┬────────┘                  └─────────▲──────────────────┘  │
│          │ codex exec --profile <role>         │                     │
│          ▼                                     │                     │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ L1. 리뷰 파이프라인 — 역할별 stateless 세션 (fresh context)       │  │
│  │                                                                │  │
│  │  [Ingestor]───state/sections.json───►[Critic]                  │  │
│  │   Luna/Light                          Sol/High                 │  │
│  │                                       (Ultra: rubric 4축 병렬)  │  │
│  │                                          │ hypothesis 적재      │  │
│  │                                          ▼                     │  │
│  │        ┌───────────────────────────────────────────┐           │  │
│  │        │ runs/review_log.jsonl  (상태머신 = 큐)      │           │  │
│  │        │ hypothesis → checking →                   │           │  │
│  │        │   verified / refuted / unverifiable       │           │  │
│  │        └───────▲───────────────────┬───────────────┘           │  │
│  │                │ 검사·증거 기록      │ verified만 채택            │  │
│  │  [Verifier]────┘                   ▼                           │  │
│  │   Terra/Medium              [Judge] Sol/High                   │  │
│  │   L1 결정적 검사              │  unverifiable → Questions        │  │
│  │   L2 Evidence-Dropout        │  refuted → 폐기(로그 보존)        │  │
│  │   L3 교차확인(conf 조정)      ▼                                 │  │
│  │                       output/review.json + review.md           │  │
│  └────────────────────────────────────────────────────────────────┘  │
│          │                                                           │
│          ▼                                                           │
│   ┌──────────────┐   KR 측정    ┌──────────────────────────────┐     │
│   │  verify.py   │────────────► │ runs/okr_progress.jsonl      │     │
│   │  게이트 5종   │              │ (목표 달성도 자동 기록 = 로그)  │     │
│   └──────┬───────┘              └──────────────────────────────┘     │
│          │ exit≠0 → 실패사유를 progress.md에 기록 → 루프 재진입         │
│          │ exit=0                                                    │
│          ▼                                                           │
│   git commit(iter별) ──► 종료판정: kr_1_1==1.0 ∧ kr_1_2==1.0 ∧ 스키마  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │ @weave.op 전 호출 트레이스
         ┌──────────────────────▼──────────────────────┐
         │ [Observer]  Terra/Medium · $wandb-primary   │
         │ Weave 트레이스 → failure mode 분류            │
         │ → runs/observer_notes.md → progress에 피드백  │
         └─────────────────────────────────────────────┘

  (stretch) L2. Autoresearch 메타 루프 — git worktree 격리
    [Optimizer] mutable/{pipeline.py, prompts.yaml} 수정 (가설 1개=커밋 1개)
        → immutable/seeded_errors 로 recall·FPR 평가
        → 개선 ∧ kr_1_1/1_2 유지 ∧ 예산 내 → git keep, 아니면 revert
        → runs/results.jsonl (실험 원장)
```

읽는 법: 실선 화살표 = 파일을 통한 데이터 흐름. 에이전트끼리 직접 통신하는 경로는 없음 — 모든 통신은 파일의 상태 전이. LLM이 개입하는 상자는 역할 5개뿐이고, 라우팅(next_stage.py)·게이트(verify.py)·종료판정은 전부 결정적 코드.

---

# PART 8. 산출물·로그 관리 — OKF (Open Knowledge Format) 정식 반영

기준: Google Cloud OKF v0.1 스펙 (github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf). 이 문서에서 "OKF"는 항상 이 스펙을 지칭.

## 8.1 OKF 핵심 규격 요약 (스펙에서 우리가 지킬 것)

- **Knowledge Bundle** = markdown 디렉토리 하나가 배포 단위. Git 리포 권장
- **Concept** = markdown 문서 1개 = 지식 1단위. **Concept ID = 경로에서 .md 제거** (예: runs/run-001.md → `runs/run-001`)
- **Frontmatter**: 모든 concept은 YAML frontmatter 필수, **`type` 필드가 비어있지 않아야 준수**. 관례 필드: title, description, resource, tags, timestamp
- **예약 파일명** (concept으로 사용 금지): `index.md` = 디렉토리 리스팅(progressive disclosure), `log.md` = 시간순 업데이트 이력
- 번들 루트 index.md frontmatter에 `okf_version: "0.1"` 선언
- **본문 내 markdown 크로스링크**가 곧 지식 그래프의 엣지 — 번들 전체를 self-contained HTML 그래프로 시각화하는 viz 도구가 리포에 포함됨

스펙 스스로 "LLM wiki 리포 패턴에 가깝고, 차이는 상호운용을 위한 최소 규칙을 '명세'했다는 점"이라고 밝힘 — 기존 LLM Wiki 설계 경험이 그대로 이식됨.

## 8.2 설계 결정: 2층 분리 — 기계 층(JSONL)과 지식 층(OKF 번들)

review_log.jsonl 같은 고빈도 기계 큐를 markdown으로 바꾸면 루프 성능·파싱 안정성이 나빠진다. 따라서:

- **기계 층 (runs/*.jsonl)**: 루프가 실시간으로 읽고 쓰는 상태머신·측정 데이터. append-only. 그대로 유지
- **지식 층 (knowledge/ = OKF 번들)**: 사람과 미래의 에이전트가 소비하는 정제된 지식. **Observer가 각 stage 완료·완주 시점에 JSONL을 요약해 concept으로 발행**

즉 Observer의 역할이 확장된다: failure mode 분류 + **OKF 지식 발행자(knowledge producer)**.

## 8.3 번들 구조

```
knowledge/                          # OKF v0.1 Knowledge Bundle
├── index.md                        # okf_version: "0.1", 번들 리스팅
├── log.md                          # 시간순 업데이트 이력 (예약 파일, append-only)
├── papers/
│   ├── index.md
│   └── paper-001.md                # type: paper — 리뷰 대상 메타·섹션 요약
├── reviews/
│   ├── index.md
│   └── review-001.md               # type: review — 최종 리뷰 요약,
│                                   #   resource: ../output/review.json
│                                   #   본문에 [paper-001](/papers/paper-001.md) 링크
├── issues/
│   ├── index.md
│   └── issue-0042.md               # type: issue — verified 이슈만 승격
│                                   #   가설→검사→증거 이력 요약, review 링크
├── runs/
│   ├── index.md
│   └── run-20260712-1.md           # type: run — 완주 1회 기록: iter 수,
│                                   #   최종 KR, 실패→회복 지점, Weave 링크
└── experiments/                    # (stretch) L2 메타 루프
    ├── index.md
    └── exp-001.md                  # type: experiment — 가설, diff 요약,
                                    #   전/후 recall, keep/revert 판정
```

concept frontmatter 예시 (issue):

```yaml
---
type: issue
title: "표 3 합계 불일치 (soundness)"
description: "본문 4.2절 주장과 표 3 수치가 모순 — L1 숫자 일관성 검사로 verified"
resource: "../runs/review_log.jsonl#issue-0042"
tags: [soundness, verified, numeric-check]
timestamp: 2026-07-12T14:03:00+09:00
---
```

## 8.4 이 선택이 주는 것 (발표 포인트 3개)

1. **크로스링크 = 추적성 그래프**: run → review → issue → paper 링크가 OKF viz로 **인터랙티브 지식 그래프 HTML 한 장**이 됨 — "이 리뷰의 이 지적이 어느 검사를 통과해 나왔는가"를 심사위원이 클릭으로 탐색. review_log를 날것으로 보여주는 팀과 차원이 다른 데모
2. **표준 준수 자체가 어필**: "산출물을 자체 포맷이 아니라 공개 스펙(OKF v0.1)으로 발행 — 어떤 에이전트·도구도 이 결과를 소비 가능". 엔터프라이즈 상호운용 감각의 증명 (Applied AI Architect 포지셔닝)
3. **log.md 예약 파일 = 기존 append-only 원칙의 표준화**: 우리가 이미 정한 "append-only 이력" 규칙이 OKF 예약 파일 규격과 일치 — 별도 발명 없이 스펙을 따르면 됨

## 8.5 구현 추가분 (D-1 체크리스트에 +1시간)

- [ ] Observer 프롬프트에 OKF 발행 절차 추가: "stage 완료 시 해당 concept을 knowledge/에 생성·갱신하라. 모든 concept은 비어있지 않은 type과 frontmatter 필수. index.md/log.md는 concept으로 쓰지 말 것. 관련 concept은 상대경로 markdown 링크로 연결"
- [ ] verify.py에 OKF 준수 검사 1줄 추가 (게이트 6번): knowledge/ 내 모든 비예약 .md가 파싱 가능한 frontmatter + 비어있지 않은 type 보유 — **비준수 concept은 OKF v0.1 위반이므로 루프가 스스로 고치게 됨**
- [ ] 완주 후 OKF viz로 knowledge/ 번들 → viz.html 생성 (데모 화면)
- [ ] AGENTS.md에 한 줄 추가: "Published knowledge lives in knowledge/ as an OKF v0.1 bundle; machine state stays in runs/*.jsonl"
---
type: Archived Reference
title: Track 2 Claude 통합 참고자료 v2
description: v4 이전의 아이디어와 배경을 보존한 참고 문서.
tags: [ralphthon, track-2, archived, reference]
timestamp: 2026-07-12T11:28:00+09:00
status: reference-only
---
