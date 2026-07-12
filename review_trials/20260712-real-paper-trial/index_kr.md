# 실제 논문 리뷰 시험 — 2026-07-12

## 결론

이번 시험에서는 두 논문 모두 형식적인 문구가 아니라 논문별 핵심 결함을 찾아냈습니다. 각 리뷰는 동결된 PDF와 manifest에 연결되어 있고, canonical JSON 검증을 통과했으며, 초안을 작성하지 않은 별도 evidence verifier도 두 건 모두 `PASS`로 판정했습니다.

따라서 **독립 리뷰어와 verifier를 실제로 분리해 실행하면 제대로 된 리뷰를 수행할 가능성이 높다**고 판단할 수 있습니다. 다만 논문이 두 편뿐이고 정답 리뷰·저자 반론·원시 실험 데이터가 없으므로, 일반적인 리뷰 정확도가 증명됐다고 말할 수는 없습니다.

| 논문 | 종합 점수 | 신뢰도 | 핵심 판정 |
| --- | ---: | ---: | --- |
| `2607.08173v1` | 3/6, Weak Reject | 4/5 | secret LoRA가 reasoning vector에 섞였을 가능성, 비균일 계수에서 alpha=1 의미 붕괴, Directional Fisher 식 문제를 확인했습니다. |
| `2607.08256v1` | 3/6, Weak Reject | 4/5 | evaluator에 따른 순위 변화는 살아 있지만, 2–3배 주장·p-value 충돌·네 번째 evaluator 누락·N=10 품질 주장은 보완이 필요합니다. |

## 실제로 찾아낸 비정형 문제

### `2607.08173v1`

- Section 3.1은 두 endpoint가 reasoning distillation만 다르다고 가정하지만, Section 4.3은 secret LoRA를 reasoning model에서 학습했다고 설명합니다. 동일 LoRA를 양쪽 endpoint에 적용하지 않았다면 중심 인과 주장이 흔들립니다.
- 비균일 layer coefficient에서는 Equation 2의 alpha=1이 원래 reasoning model을 복원하지 않습니다.
- Directional Fisher의 분모가 L2 norm의 제곱이 아니라 norm으로 표시되어 방향만 측정한다는 해석과 맞지 않습니다.
- Figure 8의 collapse 구간과 knee가 caption과 본문에서 충돌하고, Table 6의 두 metric 묶음이 세 모델 크기에서 완전히 동일합니다.

### `2607.08256v1`

- Table 3의 same-family 회복 비율은 실제로 3.29배와 1.43배라서 초록의 일괄적인 2–3배 주장과 맞지 않습니다.
- 동일한 WER 행에 대해 Table 1과 Table 4의 p-value가 서로 다릅니다.
- 본문은 evaluator 네 개를 사용했다고 하지만 main result table에는 세 개만 있습니다.
- 1.61% 결과는 N=10인데 품질 무저하 근거는 N=3 자동 지표만 제시됩니다.

## 실행 구조

```text
PDF 동결 + SHA-256
        |
        +--> 논문별 독립 Reviewer A --> ReviewDraft A --+
        |                                               |
        +--> 논문별 독립 Reviewer B --> ReviewDraft B --+--> 결정론적 schema/manifest 검증
                                                        |
                                          별도 evidence verifier
                                                        |
                                               PASS 또는 제한적 REPAIR
                                                        |
                                                최종 JSON + Markdown
```

OpenAgentReview의 claim/post는 수행하지 않았습니다.

## 결과 파일

- [Overthinking 영문 리뷰](final/2607.08173v1.review.md)
- [Overthinking canonical JSON](final/2607.08173v1.review.json)
- [Overthinking verifier 기록](verification/2607.08173v1.verifier.md)
- [Overthinking fresh native verifier JSON](verification/2607.08173v1.native-verifier-result.json)
- [Best-of-N TTS 영문 리뷰](final/2607.08256v1.review.md)
- [Best-of-N TTS canonical JSON](final/2607.08256v1.review.json)
- [Best-of-N TTS verifier 기록](verification/2607.08256v1.verifier.md)

## 중요한 한계

현재 패키지의 Python DRY-RUN runtime에는 명시적으로 켜는 결정론적 mock verifier 경로가 연결되어 있으며 risk selection, gate, PASS/REPAIR, 공유 repair 예산, 재검증, ledger/summary 상태 전이를 실제로 실행합니다. 다만 Python은 native Codex agent를 shell-out하거나 흉내 내지 않습니다. 이번 실제 논문 시험은 논문별 reviewer context와 별도 native verifier를 직접 분리해 실행했으므로, Python adapter 증거가 아니라 **독립 context에서 리뷰 설계가 작동할 수 있다는 정성 근거**입니다.
