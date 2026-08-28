# Codex Personal Skills

개인 개발 방식과 검증 원칙을 여러 PC에서 동일하게 사용하는 Codex 스킬
저장소입니다.

## 포함 스킬

- `start-project`: 짧은 제품 아이디어에서 spec 중심의 최소 프로젝트 구조와
  프로젝트별 `AGENTS.md`를 생성합니다.
- `obsidian-daily`: 사용자가 지정한 시간 범위의 Codex·ChatGPT 활동을
  Obsidian Daily 노트에 요약하고 완료 상태로 표시합니다.
- `obsidian-docs`: 대화에서 선택한 핵심 내용을 Obsidian Docs 문서로 만들고
  해당 날짜의 Daily 노트와 양방향 링크합니다.

## 설치

저장소를 clone한 폴더에서 실행합니다.

```bash
python3 install.py
```

기본 설치는 `~/.codex/skills/` 아래에 포함된 세 스킬의 심볼릭 링크를
만듭니다. 원본과 설치본이 연결되므로 저장소에서 `git pull`하면 스킬도 함께
갱신됩니다.

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

Obsidian 스킬은 Codex 작업공간을 Vault 또는 Vault 내부 폴더에서 열었을 때
`.obsidian`, `Daily`, `Docs`, `Templates` 구조를 기준으로 Vault를 찾습니다.
Vault를 하나로 결정할 수 없으면 파일을 변경하기 전에 경로를 요청합니다.
