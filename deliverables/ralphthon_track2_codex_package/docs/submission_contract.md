---
type: Submission Contract
title: Ralphthon Track 2 제출 계약
description: 최신 참가자 가이드와 공식 Track 2 자료를 결합한 필수 및 보조 제출물 계약.
tags: [ralphthon, track-2, submission]
timestamp: 2026-07-12T11:30:00+09:00
---

# Track 2 Submission Contract

## 행사 필수 제출물

16:30까지 다음을 OpenAgentReview에 제출한다.

- 익명 Technical Report PDF.
- Title.
- Abstract.

Technical Report는 Review Agent의 접근 방식과 개발 과정을 설명한다. ICML 2026 스타일을 사용하며 본문은 최대 4페이지다. References와 Appendix는 본문 제한에서 제외된다.

16:35–17:00에는 배정된 논문을 에이전트로 리뷰해 OpenAgentReview에 게시한다. 오전 Q&A 기준 배정 수는 10편이며 모두 완료하지 못하면 탈락할 수 있다.

## 공식 리뷰 필드

| 필드 | 범위 | 필수 |
|---|---:|---|
| Soundness | 1–4 | 예 |
| Presentation | 1–4 | 예 |
| Significance | 1–4 | 예 |
| Originality | 1–4 | 예 |
| Overall Recommendation | 1–6 | 예 |
| Confidence | 1–5 | 예 |
| Comment | 서술형 | 예 |

Comment는 인간 참가자가 에이전트와 논문을 개선할 수 있는 건설적인 의견이어야 한다.

## 보조 제출 및 심사 증거

공식 행사 저장소는 Track 2 agent 정의와 리뷰 결과를 별도 아티팩트로 동결하도록 안내한다. 다음을 준비하되 플랫폼이 별도 업로드를 요구하는지는 당일 UI를 따른다.

- `review-agent.md`.
- agent name과 version 또는 Git SHA.
- frozen paper hash.
- review result hash.
- evidence trace.
- 실행 시간, latency, 실패 기록.
- 평가 결과 요약.
- code 또는 repository 링크.
- 검증된 경우에만 W&B 또는 Weave 링크.

## 제출 전 게이트

- [ ] PDF에 저자명과 소속이 없다.
- [ ] 본문이 4페이지 이하이다.
- [ ] Title과 Abstract가 PDF와 일치한다.
- [ ] 보고서의 모든 수치가 저장된 실행 결과에서 재계산 가능하다.
- [ ] 예정된 결과를 실제 결과처럼 쓰지 않았다.
- [ ] 플랫폼 reviewer form의 실제 필드명과 값 범위를 확인했다.
- [ ] 리뷰 게시 성공 상태를 조회할 수 있다.
- [ ] Discord 메시지를 제출로 간주하지 않는다.

## 출처 우선순위

1. 당일 OpenAgentReview UI와 운영진 실시간 공지.
2. 2026-07-12 Notion Participant Guide.
3. 오전 제출 Q&A 기록.
4. `team-attention/ralphthon-icml` 공식 저장소의 Track 2 템플릿.

