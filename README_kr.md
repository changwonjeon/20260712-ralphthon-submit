---
type: Project Overview
title: Ralphthon Track 2 리뷰 에이전트
description: 동결된 논문과 근거를 바탕으로 제한 시간 안에 ICML 형식 리뷰를 생성하는 증거 기반 Codex Skill과 분산 실행 구조.
tags: [ralphthon, track-2, review-agent, codex, okf]
timestamp: 2026-07-12T16:15:52+09:00
status: build-installed-discovered-live-unverified
---

# Ralphthon Track 2 리뷰 에이전트

[English README](README.md)

이 저장소는 주최측 공식 `auto-research` Skill의 Track 2-only frozen-paper 경로를 보존하면서, 배정된 논문을 제한 시간 안에 ICML 형식으로 리뷰하기 위한 Codex Skill과 실행 증적을 제공한다. 각 논문과 근거 묶음을 Worker 실행 전에 동결하고, 플랫폼 부작용은 하나의 Root Coordinator만 수행한다.

현재 구현은 결정론적 synthetic fixture, 실행 가능한 risk-gated mock verifier 경로, 동결된 공개 arXiv PDF 두 편에 대한 분리된 reviewer/verifier 정성 시험으로 검증되었다. 실제 OpenAgentReview 논문을 claim하거나 리뷰를 post한 적은 없으며, 일반적인 리뷰 정확도, 사람 평가와의 일치, 실제 플랫폼 처리 속도를 주장하지 않는다.

## 현재 상태

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| 공식 `auto-research` Skill | PASS INSTALLED | upstream commit `a9f4f2583648ef4ca54f980f951ae393d153473f`, 11개 파일 manifest와 recursive diff 일치. |
| Wrapper Skill과 native agents | PASS INSTALLED AND DISCOVERED | project-local `.codex` 설치와 fresh-session discovery 완료. |
| 결합 패키지 | PASS | staging과 설치본 29/29 일치. |
| 회귀검사와 성능 정책 evaluator | PASS LOCALLY | 회귀 70건과 `tests/performance_evaluator.py` 통과. |
| 정상 synthetic mock | PASS IN MOCK | 10편을 3회 실행해 30/30 완료, schema 100%, 중복 post 0건. |
| 실패 복구와 재시작 | PASS IN MOCK | malformed JSON, Worker·claim·post timeout, ledger reopen, 실제 2-process 재개 검증. |
| Evidence-first 및 risk-gated calibration | PASS IN EXECUTABLE DRY-RUN | 명시적 risk sidecar로 cap, gate, PASS/REPAIR, fail-open verifier 장애, 공유 repair 1회, 재검증, ledger, summary 경로 실행. |
| 실제 논문 reviewer/verifier 시험 | PASS QUALITATIVE, NOT GOLD-LABELED | 공개 arXiv PDF 두 편에 논문별 리뷰를 생성하고 독립 verifier가 모두 PASS 판정. |
| 영문 Technical Report | PASS LOCAL PDF | ICML 형식 4페이지, PDF metadata Author `Anonymous`, 글꼴·텍스트·전 페이지 렌더 검증 완료. |
| 한국어 이해용 리포트 | PASS LOCAL PDF | 제출 양식과 분리한 A4 단일 열 6페이지 동반본, PDF metadata Author `Anonymous`, 글꼴·텍스트·전 페이지 렌더 검증 완료. |
| Production adapter와 live 완료 | **NOT RUN** | 16:35 KST 이후 실제 UI 계약을 관찰해야 함. |

## 아키텍처

```text
Official auto-research Track 2 contract
                    |
                    v
Root Coordinator --+-- serialized status / claim / post / reconcile
        |
        +-- Review Worker 1 --+
        +-- Review Worker 2 --+--> ReviewDraft --> validator --> risk gate --+
        +-- Review Worker 3 --+                         |                  |
                                                        | fast path        | high risk only
                                                        v                  v
                                             atomic ledger + outbox   bounded verifier
                                                        ^                  |
                                                        +-- one repair ----+
```

Root는 assignment discovery, bounded queue, lease, manifest, status, claim, post, receipt, outbox와 atomic ledger를 소유한다. Worker 3개는 각각 동결된 manifest와 활성 lease 하나만 받아 `ReviewDraft`를 반환하며 플랫폼과 공유 상태를 변경할 권한이 없다.

## 실행 계약

- 각 논문에 대해 paper, evidence, schema, prompt, agent version의 SHA-256을 동결한다.
- `paper_id`, `lease_id`, `input_hash`, `evidence_hash`, `prompt_hash`, `agent_version` 불일치는 repair하지 않고 즉시 차단한다.
- 공식 `contribution`과 행사 필드 `significance`, `originality`, `comment`를 독립적으로 보존하며 서로 환산하지 않는다.
- deterministic validator가 identity, schema, 점수 범위, evidence location과 필수 문장을 먼저 검사한다.
- schema repair와 calibration repair는 논문당 targeted repair 1회를 공유한다.
- Worker는 내부적으로 claim map, falsification pass, score anchoring, consistency pass를 수행한 뒤 canonical JSON만 반환한다.
- 낮은 confidence나 극단 recommendation 값만으로 verifier를 호출하지 않는다. 복합 risk score가 3 이상인 schema-valid draft만 calibration 후보가 된다.
- Calibration은 `min(3, ceil(assigned_count * 0.3))`편, verifier 1개, 논문당 20초·finding 3개, T+15 이전, validated backlog 2 이하로 제한한다.
- Pending draft가 있는 동안 Worker 3개를 verifier 때문에 줄이지 않는다. fast/emergency mode, 느린 posting pace, 기존 repair 사용 논문은 calibration을 우회한다.
- Claim과 post timeout 뒤에는 재시도 전에 status를 확인하며, 성공 또는 reconciliation된 post를 반복하지 않는다.
- 성공 조건은 `posted_verified == assigned_count`다.

## 저장소 구조

- `src/ralphthon_track2_review_agent/`에는 runtime, contract, manifest와 ledger 구현이 있다.
- `.codex/skills/`와 `.codex/agents/`에는 설치된 두 Skill과 세 native agent 정의가 있다.
- `staging/.codex/`에는 설치 기준이 되는 동결 패키지가 있다.
- `fixtures/`에는 throughput 논문, seeded quality case, naive baseline과 frozen manifest가 있다.
- `fixtures/calibration/`에는 실행형 verifier DRY-RUN용 명시적 risk-sidecar plan이 있다.
- `tests/`에는 contract, runtime, failure, restart, CLI, quality와 evidence consistency 검사가 있다.
- `evidence/mock-validation-final-20260712T1335KST/`에는 기준 synthetic-mock 결과가 있다.
- `evidence/process-restart-proof/`에는 실제 두 프로세스 중단·재개 증적이 있다.
- `evidence/performance-optimization.json`에는 최신 calibration 정책과 evaluator 결과가 있다.
- `review_trials/20260712-real-paper-trial/`에는 동결된 실제 논문 두 편의 리뷰, manifest와 독립 verifier 기록이 있다.
- `manifests/`, `outbox/`, `clipboard/`, `ledger.jsonl`에는 mock 실행 및 manual fallback artifact가 있다.
- `submission/`에는 제출용 영문 Technical Report와 이해용 한국어 동반본, 각 Title과 Abstract가 있다.
- `review-agent.md`, `MANUAL_PLATFORM.md`, `HANDOFF.md`에는 agent 정의, live fallback과 운영 인계가 있다.

## 설치 및 검증

Staging 패키지와 공식 upstream을 검증한다.

```bash
python3 scripts/install-track2-codex.py --check-staging

diff -qr \
  tmp/ralphthon-icml-official/skills/auto-research \
  staging/.codex/skills/auto-research

(cd staging/.codex/skills/auto-research && \
  shasum -a 256 -c ../../../auto-research.sha256)

(cd staging && \
  shasum -a 256 -c ralphthon-track2-review-agent.sha256)
```

Project-local `.codex`에 idempotent하게 설치하고 read-back한다.

```bash
python3 scripts/install-track2-codex.py --install
python3 scripts/install-track2-codex.py --check
```

회귀검사와 최신 quality-per-minute 정책 evaluator를 실행한다.

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/performance_evaluator.py
```

## BUILD와 DRY-RUN

플랫폼 부작용 없이 manifest만 만든다.

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode BUILD \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-build
```

Mock adapter와 bounded Worker 3개를 실행한다.

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode DRY-RUN \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-dry-run \
  --workers 3
```

명시적 synthetic sidecar로 실행 가능한 risk-gated verifier 경로를 시험한다. Calibration은 기본적으로 꺼져 있으며, Python adapter는 결정론적 test double일 뿐 native Codex verifier를 흉내 내지 않는다.

```bash
python3 staging/.codex/skills/ralphthon-track2-review-agent/scripts/run_batch.py \
  --mode DRY-RUN \
  --papers fixtures/throughput/papers.json \
  --root-dir . \
  --output-dir /tmp/ralphthon-track2-calibration \
  --workers 3 \
  --calibration mock \
  --calibration-plan fixtures/calibration/high-risk-pass.json
```

기준 evidence를 만든 명령은 다음과 같다. 기존 동결 디렉터리를 덮어쓰지 말고 재검증에는 다른 출력 경로를 사용한다.

```bash
python3 tests/run_mock_evidence.py \
  --output evidence/mock-validation-final-20260712T1335KST \
  --process-restart-evidence evidence/process-restart-proof/aggregate.json
```

## Skill 사용법

새 Codex session에서 먼저 공식 Skill을 호출하고 Track 2-only frozen-paper 경로를 선택한다.

```text
$auto-research
```

그다음 wrapper Skill을 호출한다.

```text
$ralphthon-track2-review-agent
```

로컬 shell CLI는 `BUILD`와 `DRY-RUN` 전용이며 `LIVE`를 항상 거부한다. DRY-RUN의 `--calibration mock`은 명시적 sidecar에서 정책과 상태 전이를 실행한다. Native Codex 실행에서는 Root가 `track2-review-verifier`를 별도로 호출하며, Python이 shell-out으로 독립성을 모방하지 않는다. 실제 live 작업은 Skill 실행 계약과 관찰된 UI만 사용한다.

## 검증 결과와 주장 범위

| 측정값 | Synthetic-mock 결과 |
| --- | ---: |
| 정상 반복 | 3회. |
| 완료 및 schema-valid | 30/30, 100%. |
| 중복 post attempt와 idempotency key | 0, 0. |
| Fault run | 10/10 완료, schema 10/10, 중복 0. |
| 실제 process resume | 첫 process exit 75·4편, 새 process exit 0·10/10. |
| Seeded quality | TP 20, FP 0, FN 0, F1 1.0. |
| Naive seeded baseline | TP 10, FP 0, FN 10, F1 0.6667. |
| 실행형 calibration evaluator | risk 10건 평가, 제한된 subset 선택, verifier 최대 동시실행 1, 10/10 posted. |
| 실제 논문 정성 시험 | 2/2 schema·manifest 유효, 독립 verifier 2/2 PASS, repair 0. |

기준 runtime·quality evidence는 `evidence/mock-validation-final-20260712T1335KST/aggregate.json`이며 SHA-256은 `239f2de62fcc5a1671b6cf86efc4f3a63077c3e3d2c81ccd2ad04e25a2077910`이다. Process-resume evidence는 `evidence/process-restart-proof/aggregate.json`이며 SHA-256은 `18d536ca72f87e03117af28d5534d10de1b316a3a0dc26b52fd5a2849e0de5d2`다. Wrapper manifest SHA-256은 `b9fc57b4755c00d273a999be3c7900d2fc7d85c1c897f8fd91a6e8149bc3eaba`다.

Synthetic 결과는 의도적으로 만든 문제를 포함한 fixture 측정이다. 두 편 정성 시험은 분리된 reviewer/verifier context가 논문별 finding을 만들고 감사할 수 있음을 보여주지만 gold review, 저자 반론, 원시 실험 실행, 사람 정답 label이 없다. 어느 결과도 일반적인 리뷰 품질, 평가자와의 일치, 브라우저·네트워크 지연 또는 OpenAgentReview 완료를 입증하지 않는다. Worker-timeout fault는 mock adapter의 `TimeoutError` 복구를 검증하며 실행 중인 thread를 강제 종료했다는 증거가 아니다.

## 영문 제출물과 한국어 이해용 동반본

| 구분 | 제출용 영문 | 이해용 한국어 |
| --- | --- | --- |
| Technical Report PDF | `submission/technical-report.pdf` | `submission/technical-report_kr.pdf` |
| Technical Report source | `submission/technical-report.tex` | `submission/technical-report_kr.tex` |
| Title | `submission/TITLE.txt` | `submission/TITLE_kr.txt` |
| Abstract | `submission/ABSTRACT.txt` | `submission/ABSTRACT_kr.txt` |

공식 제출 기준은 영문 ICML 보고서다. `_kr` 파일은 사용자의 이해를 위한 한국어 동반본이며 ICML 페이지·단 구성 제약을 따르지 않는다. 공통 제출·운영 artifact는 `review-agent.md`, `HANDOFF.md`, `MANUAL_PLATFORM.md`다. 실제 업로드 직전에 영문 PDF, Title과 Abstract가 서로 일치하는지 확인하고 다음 명령으로 최종 해시를 새로 기록한다.

```bash
shasum -a 256 \
  submission/technical-report.pdf \
  submission/technical-report.tex \
  submission/TITLE.txt \
  submission/ABSTRACT.txt \
  submission/technical-report_kr.pdf \
  submission/technical-report_kr.tex \
  submission/TITLE_kr.txt \
  submission/ABSTRACT_kr.txt
```

검증된 영문 offline Tectonic 빌드 명령은 다음과 같다.

```bash
cd submission
TECTONIC_CACHE_DIR=../tmp/pdfs/tectonic-work-cache \
  tectonic -C -b ../tmp/pdfs/tectonic-cache.zip \
  technical-report.tex --keep-logs --keep-intermediates
```

## 16:35 LIVE 운영과 manual fallback

16:35 KST 이후 새 Codex session에서 다음과 같이 호출한다.

```text
$ralphthon-track2-review-agent LIVE: perform at most 45 seconds of read-only LIVE_DISCOVERY, use only the observed platform contract, and switch to MANUAL_PLATFORM.md if automation is not verified.
```

최대 45초 동안 read-only `LIVE_DISCOVERY`로 실제 assigned count, claim semantics, PDF 접근 경로, 허용 필드와 점수 범위, 복수 claim 허용 여부, posted-success marker를 확인한다. 관찰하지 않은 endpoint나 selector는 만들지 않는다.

Automation이 검증되지 않으면 즉시 `MANUAL_PLATFORM.md`로 전환한다.

1. 사람은 로그인된 UI에서 claim과 download를 수행한다.
2. Root는 각 논문과 근거 manifest를 동결하고 read-back한다.
3. Worker는 `ReviewDraft`만 반환한다.
4. Root는 deterministic validation 후 outbox JSON과 clipboard text를 만든다.
5. 사람은 UI가 실제로 받는 필드만 한 번 제출하고 posted 상태를 확인한다.
6. Claim 또는 post 상태가 불명확하면 재시도 전에 UI status를 확인한다.

Platform 우선순위는 `reconcile/post > download > claim > browse`다. Queue high-water는 3으로 시작하며 복수 claim이 허용된 사실을 확인한 뒤에만 높인다. 현재 production adapter와 live 완료 상태는 **NOT RUN**이다.
