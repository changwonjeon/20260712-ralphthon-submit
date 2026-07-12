---
type: Project Overview
title: Ralphthon Track 2 Review Agent
description: Ralphthon @ICML Track 2를 위한 evidence-bound 병렬 Review Agent 프로젝트.
tags: [ralphthon, track-2, review-agent, codex, okf]
timestamp: 2026-07-12T12:15:45+09:00
status: pre-ralph
---

# Ralphthon Track 2 Review Agent

이 저장소는 Ralphthon @ICML Track 2에서 제한 시간 안에 배정 논문 전체를 ICML-style로 리뷰하기 위한 Codex Skill과 실행 증적을 준비한다. 현재는 12:30 Ralph Loop 시작 전 specification과 preflight가 동결된 상태다.

```text
Official auto-research Skill
             |
             v
Root Coordinator ---- serialized platform lane
      |                         |
      +--> Worker A             +--> claim / post / status
      +--> Worker B
      +--> Worker C
             |
             v
     ReviewDraft -> validator -> ledger -> outbox
```

## 행사 흐름

- 11:00–12:30. Research Specification과 preflight.
- 12:30–15:30. 사용자 입력 없는 Ralph Loop 구현·검증.
- 15:30–16:30. Human Editing과 Technical Report 제출.
- 16:35–17:00. 실제 Review Agent 실행.

## 기준 문서

- [전체 실행 계획](.omx/plans/ralphthon-track2-skill-creation-plan.md).
- [동결된 Ralph Goal](RALPH_GOAL.md).
- [Track 2 참가자 가이드](guides/20260712_Track-2-Participant-Guide.md).
- [현재 작업 패키지](deliverables/ralphthon_track2_codex_package/README.md).
- [공식 upstream](https://github.com/team-attention/ralphthon-icml).

공식 upstream은 commit `a9f4f2583648ef4ca54f980f951ae393d153473f`로 동결한다. 프로젝트 baseline은 `67a89a0ee7c18d6abdd4c5c734d5b1bdc97f8784`다.

## 준비 상태

- OpenAgentReview 로그인 완료. 행사 venue는 아직 미공개다.
- Codex, OMX, tmux, Tectonic, Poppler 설치와 기본 smoke test 완료.
- 공식 ICML 예제 TeX의 PDF 빌드 확인.
- private GitHub baseline push 완료.
- 실제 Skill, 테스트 결과, Technical Report는 Ralph Loop가 생성할 예정이다.

## 안전 경계

- 사용자의 명시적인 시작 신호 전에는 Ralph Loop를 시작하지 않는다.
- Ralph Loop 중 production claim/post와 credential 입력을 시도하지 않는다.
- 확인되지 않은 API, selector, 결과, citation을 만들지 않는다.
- 익명 제출물에는 개인 식별정보와 개인 GitHub URL을 포함하지 않는다.

## 최종 업데이트 계약

Ralph Loop는 이 README를 실제 설치·실행·검증 명령, 아키텍처, 측정 결과, 제출물 경로, 알려진 한계와 일치하도록 갱신해야 한다. placeholder나 검증되지 않은 성능 주장을 남기면 안 된다.

