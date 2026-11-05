# Codex Personal Skills

개인 개발 방식과 검증 원칙을 여러 PC에서 동일하게 사용하는 Codex 스킬
저장소입니다.

## 포함 스킬

- `start-project`: 짧은 제품 아이디어에서 spec 중심의 최소 프로젝트 구조와
  프로젝트별 `AGENTS.md`를 생성합니다.
- `cofa-sprint`: README 기반 개발 지도와 상세 명세를 작성하고, 확정 spec을
  기준으로 구현·검증·설명을 수행하는 스펙 중심 개발 스킬입니다.
- `obsidian-daily`: 사용자가 지정한 시간 범위의 Codex·ChatGPT 활동을
  Obsidian Daily 노트에 요약하고 완료 상태로 표시합니다.
- `obsidian-docs`: 대화에서 선택한 핵심 내용을 Obsidian Docs 문서로 만들고
  해당 날짜의 Daily 노트와 양방향 링크합니다.

## 설치

저장소를 clone한 폴더에서 실행합니다.

```bash
python3 install.py
```

기본 설치는 `$CODEX_HOME/skills` 아래에 포함된 모든 스킬의 심볼릭 링크를
만듭니다. `CODEX_HOME`을 지정하지 않았으면 `~/.codex/skills/`를 사용합니다.
원본과 설치본이 연결되므로 저장소에서 `git pull`하면 스킬도 함께 갱신됩니다.

심볼릭 링크를 사용할 수 없는 환경에서는 복사 방식으로 설치합니다.

```bash
python3 install.py --copy
```

복사 방식은 `git pull` 후 명령을 다시 실행한다고 기존 설치본을 덮어쓰지
않습니다. 기존 설치본을 직접 확인하고 제거한 뒤 다시 설치해야 합니다.
다른 기존 파일·폴더도 덮어쓰지 않으며, 같은 원본을 가리키는 심볼릭 링크는
이미 설치된 것으로 처리합니다. `--skills-dir`로 설치 대상 폴더를 지정할 수
있습니다.

## 스킬 선택과 사용

### 빈 폴더에서 새 프로젝트 시작

Codex를 다시 시작하거나 새 작업을 열고 다음처럼 사용합니다.

```text
$start-project 일기 앱을 작성할 거야. iOS 기반이고 Photos와 연동해
일기를 적은 날의 사진과 영상을 불러와야 해.
```

스킬은 빈 대상 폴더에서 프로젝트 골격과 첫 spec을 만들며, 애플리케이션
구현은 별도로 요청한 경우에만 진행합니다.

### README 기반 스펙 개발

README와 프로젝트 자료가 있으면 `cofa-sprint`로 **README → spec00 → 상세
spec → 구현 → 인수 조건 검증** 순서로 진행합니다. `start-project`는 빈
폴더의 초기 구성용이고, `cofa-sprint`는 명세를 기준으로 개발하는 작업에
사용합니다.

| 요청 예시 | 수행 범위 |
| --- | --- |
| `$cofa-sprint 준비` | README 기반의 큰 개발 순서·내용을 spec00.md에 정의하고 폴더 역할 정리 |
| `$cofa-sprint 명세 spec01` | spec00의 해당 단계를 바탕으로 동작·데이터·계약·인수 조건을 상세히 작성 |
| `$cofa-sprint 개발 spec01` | 확정된 명세 구현과 실제 검증 |
| `$cofa-sprint 점검` | 실행 근거와 사용자가 직접 확인할 핵심 항목 정리 |

명세 작성 요청은 문서 작성까지 수행합니다. 기능 구현은 관련 spec을 확인한
뒤 진행하고, 요구나 동작 규칙이 바뀌면 spec을 먼저 갱신합니다. 각 단계가
끝나면 핵심 선택과 이유, 실제 검증 결과와 남은 한계를 쉽게 설명합니다.

### 프로젝트에 cofa-sprint 설치

프로젝트의 작업 폴더에서 실행합니다.

```bash
git clone https://github.com/twa04047/codex-personal-skills.git skill-source
python3 -c 'import shutil; shutil.copytree("skill-source/cofa-sprint", ".agents/skills/cofa-sprint")'
```

위 명령은 `cofa-sprint`만 현재 작업 폴더의 `.agents/skills`에 복사합니다.
대상 폴더가 이미 있으면 실패하므로 기존 설치본을 덮어쓰지 않습니다.
모든 스킬을 설치하려면 `python3 skill-source/install.py --copy --skills-dir .agents/skills`를
사용합니다. 설치기의 특정 스킬 선택 옵션은 없습니다.
설치 후 Codex를 다시 시작하거나 새 작업을 열어 스킬을 사용합니다.

### Obsidian 기록

Obsidian 스킬은 Codex 작업공간을 Vault 또는 Vault 내부 폴더에서 열었을 때
`.obsidian`, `Daily`, `Docs`, `Templates` 구조를 기준으로 Vault를 찾습니다.
Vault를 하나로 결정할 수 없으면 파일을 변경하기 전에 경로를 요청합니다.
