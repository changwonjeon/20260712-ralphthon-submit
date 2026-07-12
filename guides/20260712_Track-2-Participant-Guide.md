---
type: Participant Guide
title: Ralphthon ICML Track 2 실행 가이드
description: 공식 참가자 가이드에서 Track 2 Review Agent에 필요한 제출, 평가, 실행 요건을 정리한 운영 문서.
tags: [ralphthon, track-2, review-agent, icml-2026]
timestamp: 2026-07-12T11:21:46+09:00
---

# 목표

Track 2 팀은 Review Agent의 접근 방식과 개발 과정을 설명하는 익명 기술 보고서를 제출하고, 16:35-17:00 동안 후보 논문을 claim-read-review-post 순서로 처리해 유효한 ICML 형식 리뷰를 게시한다.

# 필수 제출물

- 익명 Technical Report PDF.
- Title.
- Abstract.
- 팀당 하나의 결과물.
- 팀 규모 1-4명.
- 정확히 하나의 트랙만 선택.

Technical Report 본문은 최대 4페이지 하드리밋이다. References와 Appendix는 제한에서 제외되며, [공식 ICML 2026 LaTeX 스타일](../attachments/icml2026/)을 사용하고 저자와 소속을 제거해야 한다.

# 리뷰 평가 항목

| 항목 | 범위 | 판단 대상 |
|---|---:|---|
| Soundness | 1-4 | 기술적 주장, 방법론, 증거의 충분성 |
| Presentation | 1-4 | 글의 명료성, 구조, 선행연구 맥락화 |
| Significance | 1-4 | 문제의 중요성, 연구·실무에 미치는 영향 |
| Originality | 1-4 | 새로운 통찰, 방법, 데이터, 관점 및 차별성 |
| Overall Recommendation | 1-6 | Strong Reject부터 Strong Accept까지의 종합 판정 |
| Confidence | 1-5 | 관련 분야 이해와 세부 검증 수준에 대한 확신 |
| Comment | 서술형 | 인간 참가자가 에이전트와 논문을 개선할 수 있는 건설적 의견 |

Overall Recommendation의 중간 점수인 4와 3은 각각 Weak Accept와 Weak Reject이며 공식 가이드에서 제한적으로 사용하도록 요구한다.

# 실행 순서

1. Agent에 행사 skill guide를 제공한다.
2. OpenAgentReview에 로그인한다.
3. 후보 논문을 탐색한다.
4. 논문을 claim한다.
5. PDF 전체를 읽고 핵심 주장과 증거를 확인한다.
6. 모든 정량 점수와 Comment를 포함한 유효한 리뷰를 작성한다.
7. 리뷰 종료 시각 전에 OpenAgentReview에 게시한다.
8. 다음 논문에 같은 claim-read-review-post 루프를 반복한다.

# 시간 제약

| 시간 | 작업 |
|---|---|
| 11:00-12:30 | Research specification |
| 12:30-15:30 | Ralph Loop |
| 15:30-16:30 | Human editing 및 최종 제출 |
| 16:30 | 제출 하드 컷과 매칭 스냅샷 |
| 16:35-17:00 | Track 2 Review Agent 실행 |
| 17:00-17:30 | 1차 심사와 파이널리스트 선정 |

Track 2 리뷰 실행 시간은 25분이다. 기존 오전 Q&A 기록에 10편 배정이 명시되어 있으므로 현재 설계 기준은 논문당 평균 2분 30초 이내 완료다. 다만 최종 배정 수나 운영 방식이 변경될 수 있으므로 Luma와 Discord 공지를 우선한다.

# 시작 전 검증

- Codex, GitHub, W&B, VESSL 계정에 로그인할 수 있는지 확인한다.
- Agent에 `skill.md`를 넣는다.
- 테스트 환경에서 login → browse → claim → PDF read → review post 전체 흐름을 검증한다.
- PDF 저자와 소속이 제거되었는지 확인한다.
- 실패한 논문이 전체 실행을 멈추지 않도록 개별 작업의 시간 상한과 복구 경로를 둔다.
- 공식 제출과 리뷰는 Discord가 아니라 OpenAgentReview에서 완료한다.

# 필수 주소

- [OpenAgentReview](https://openagentreview.org) - 제출, 리뷰, 상태 확인.
- [Ralphthon ICML Auto Research skills](https://github.com/team-attention/ralphthon-icml) - 행사 스킬 저장소.
- [VESSL credits](https://claim-vessl-credits.team-attention.com) - 승인 참가자 크레딧.
- [Morning session deck](https://ralphthon-icml-presentation.team-attention.com/slides.bi.html) - 한영 발표 자료.
- [Event page](https://luma.com/hjuo7auc) - 공식 행사 공지.

# 우선순위

1. 16:30까지 익명 Technical Report, Title, Abstract 제출.
2. 리뷰 창 종료 전 배정된 모든 논문의 유효 리뷰 게시.
3. 리뷰 점수와 Comment가 논문의 실제 주장과 증거에 근거하도록 유지.
4. 실행 로그와 W&B 링크는 선택 사항이지만 에이전트 워크플로 심사 근거로 활용.

# Citations

[1] [Ralphthon @ICML Participant Guide 원문 전사](../references/notion-participant-guide/20260712_Ralphthon-ICML-Participant-Guide-transcript.md)

[2] [2026-07-12 제출 가이드라인 Q&A](../sessions/20260712_Ralphthon-3.overview-QA.md)
