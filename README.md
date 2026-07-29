# Codex Personal Skills

개인 개발 방식과 검증 원칙을 여러 PC에서 동일하게 사용하는 Codex 스킬
저장소입니다.

## 포함 스킬

- `start-project`: 짧은 제품 아이디어에서 spec 중심의 최소 프로젝트 구조와
  프로젝트별 `AGENTS.md`를 생성합니다.

## 설치

저장소를 clone한 폴더에서 실행합니다.

```bash
python3 install.py
```

기본 설치는 `~/.codex/skills/start-project` 심볼릭 링크를 만듭니다. 원본과
설치본이 연결되므로 저장소에서 `git pull`하면 스킬도 함께 갱신됩니다.

심볼릭 링크를 사용할 수 없는 환경에서는 복사 방식으로 설치합니다.

```bash
python3 install.py --copy
```

복사 방식은 `git pull` 후 명령을 다시 실행한다고 기존 설치본을 덮어쓰지
않습니다. 기존 설치본을 직접 확인하고 제거한 뒤 다시 설치해야 합니다.

Codex를 다시 시작하거나 새 작업을 열고 다음처럼 사용합니다.

```text
$start-project 일기 앱을 작성할 거야. iOS 기반이고 Photos와 연동해
일기를 적은 날의 사진과 영상을 불러와야 해.
```

스킬은 빈 대상 폴더에서 프로젝트 골격과 첫 spec을 만들며, 애플리케이션
구현은 별도로 요청한 경우에만 진행합니다.
