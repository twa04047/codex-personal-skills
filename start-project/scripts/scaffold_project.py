#!/usr/bin/env python3
"""Create the universal, minimal base for a spec-first project."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


DIRECTORIES = (
    "spec",
    "src/common",
    "src/spec",
    "docs",
    "results",
    "tests",
)


def ensure_empty_target(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    unexpected = [entry for entry in root.iterdir() if entry.name != ".git"]
    if unexpected:
        names = ", ".join(sorted(entry.name for entry in unexpected))
        raise ValueError(f"대상 폴더가 비어 있지 않습니다: {names}")


def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def build_readme(name: str, summary: str, platform: str) -> str:
    return f"""# {name}

{summary}

## 처음 사용하는 경우

개발 경험이 없어도 괜찮습니다. 먼저
[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)를 읽어보세요. 파일을 준비하는 방법,
Codex에 요청하는 짧은 문장, 개발 결과를 확인하고 수정하는 방법을 설명합니다.

## 현재 범위

`{platform}` 기반 프로젝트의 초기 아키텍처와 첫 번째 기능 spec을 정의한
상태입니다. 애플리케이션 구현은 아직 포함하지 않습니다.

## 구조

- `spec/`: 승인된 기능 개발서
- `src/spec/NN_기능명/`: 같은 이름의 번호형 spec 구현
- `src/common/`: 둘 이상의 기능이 실제로 공유하는 코드
- `docs/`: 사용자 제공 배경지식과 결정 자료
- `results/`: 재현 가능한 검토·사용자 산출물
- `tests/`: 실서비스 인증정보 없이 실행하는 자동 테스트

spec은 `01_`, `02_`처럼 개발 순서가 보이는 번호를 붙입니다. 예를 들어
`spec/02_main_page.md`는 `src/spec/02_main_page/`에서 구현합니다.

실행 및 검증 명령은 첫 실행 가능한 기능과 함께 추가합니다.
"""


def build_agents(name: str, summary: str, platform: str) -> str:
    return f"""# {name} 작업 지침

목표: {summary}
플랫폼: `{platform}`

## 작업 기준

- `README.md` → 대상 `spec/*.md` → spec이 링크한 `docs/*.md` 순서로 읽는다.
- 승인된 spec을 동작의 기준으로 삼고, 동작 변경은 spec부터 수정한다.
- spec은 `NN_기능명.md`, 구현은 같은 stem의 `src/spec/NN_기능명/`에 둔다.
- 기능 코드를 `src/` 바로 아래에 두지 않는다. 실제 공통 코드만
  `src/common/`에 둔다.

## 짧은 요청 해석

- `<docs 경로> md파일로 수정해줘`: 해당 문서를 의미를 유지하며 읽기 쉽게
  정리하고, 영향을 받는 spec과 지침도 확인한다.
- `<spec 경로> src로 개발해줘`: spec과 연결 문서를 읽고 대응 폴더에 구현한
  뒤 테스트와 실제 결과 확인까지 수행한다.
- 언어가 지정되지 않았고 플랫폼·기존 코드가 다른 언어를 요구하지 않으면
  Python을 사용한다.
- 후속 수정 요청은 대화와 변경 상태에서 대상을 추론한다. 결과를 바꾸는
  수정이면 spec과 코드·테스트를 함께 갱신한다.

## 품질과 안전

- 토큰, 키, 개인정보, 실제 사용자 원문을 소스·테스트·결과에 넣지 않는다.
- 외부 쓰기나 파괴적 작업은 dry-run 또는 가짜 구현으로 먼저 검증한다.
- 가장 좁은 관련 테스트 후 전체 검증을 실행한다.
- UI·웹페이지·파일은 실행하거나 렌더링해 실제 결과를 확인한다.
"""


def build_development_guide(name: str) -> str:
    return f"""# {name} 개발 가이드라인

개발을 처음 해도 괜찮습니다. 무엇을 어떻게 구현할지 완벽하게 설명할
필요도 없습니다. 원하는 내용을 일반적인 문장으로 적거나 파일 경로와 짧은
요청만 알려주면 Codex가 관련 파일을 읽고 다음 작업을 이어갑니다.

## 프로젝트 폴더를 쉽게 이해하기

- `docs/`: 아이디어, 참고자료, 업무 규칙처럼 기능을 이해하는 데 필요한 글
- `spec/`: 무엇을 만들지 합의한 기능별 설계 문서
- `src/spec/`: 각 spec을 실제로 구현한 코드
- `src/common/`: 여러 기능이 함께 사용하는 코드
- `tests/`: 코드가 약속대로 동작하는지 확인하는 자동 검사
- `results/`: 실행 화면, 생성 파일 등 사람이 확인할 수 있는 결과물

spec 파일명은 `01_`, `02_`처럼 번호로 시작합니다. 이 번호로 개발 순서를
쉽게 확인할 수 있습니다. 예를 들어 `spec/02_main_page.md`의 코드는
`src/spec/02_main_page/`에 작성됩니다.

## 가장 쉬운 개발 순서

1. **자료를 정리합니다.** 메모를 `docs/`의 Markdown 파일에 붙여 넣습니다.
2. **작은 기능 하나를 정합니다.** 한 번에 검토할 수 있는 크기로 spec을
   하나 만듭니다.
3. **spec을 확인합니다.** 원하는 동작, 제외할 내용, 오류 상황, 완료 기준이
   맞는지 읽고 수정할 부분만 말합니다.
4. **구현을 요청합니다.** 승인한 spec 경로를 알려주면 Codex가 대응하는
   `src/spec/` 폴더에 코드를 작성합니다.
5. **결과를 확인합니다.** Codex가 테스트를 실행하고 화면이나 파일 같은
   실제 결과도 확인합니다.
6. **편하게 수정합니다.** 마음에 들지 않는 부분만 평소 문장으로 말합니다.
   동작이 바뀌면 Codex가 관련 spec, 코드, 테스트를 함께 수정합니다.

중요한 선택이 빠져 결과가 크게 달라질 수 있을 때만 Codex가 짧게 질문할
수 있습니다.

## 문서 정리 요청

정리되지 않은 글을 `docs/example.md`에 붙여 넣은 다음 아래처럼 말하면
됩니다.

> `docs/example.md md파일로 수정해줘`

Codex는 원래 의미를 유지하면서 제목, 문단, 목록과 링크를 정리합니다.
관련 spec이나 프로젝트 지침에 반영할 내용이 있는지도 함께 확인합니다.

다른 예시:

> `docs/customer_rules.md 읽기 쉽게 정리해줘`

> `docs/meeting_notes.md md파일로 수정하고 관련 spec에도 반영해줘`

## 기능 spec 요청

기능을 설명하는 문서는 간단한 문장만으로 요청할 수 있습니다.

> `docs/main_page.md를 참고해서 다음 번호의 메인페이지 spec 만들어줘`

조금 더 자세히 말하고 싶다면 다음 정도면 충분합니다.

> 목표는 HTML 메인페이지 제작이야. 카드를 클릭하면 각 기능 페이지로
> 이동해야 해. 관련 자료는 docs/main_page.md야. 다음 번호의 spec으로
> 작성해줘.

Codex가 목표, 주요 동작, 비범위, 오류 상황, 완료 기준을 정리합니다.
내용을 읽고 빠진 부분이나 바꾸고 싶은 부분만 이야기하면 됩니다.

## 구현 요청

spec이 준비되면 경로와 요청 한 문장만 보내면 됩니다.

> `spec/01_example.md src로 개발해줘`

이 요청에는 spec과 연결 문서 읽기, 대응하는 `src/spec/01_example/` 구현,
테스트 실행, 실제 결과 확인이 포함됩니다. 언어가 따로 정해지지 않았고
플랫폼이나 기존 코드가 다른 언어를 요구하지 않으면 Python을 사용합니다.

다른 언어가 필요하면 짧게 덧붙이면 됩니다.

> `spec/02_main_page.md src로 개발해줘. 이 기능은 HTML, CSS, JavaScript로 해줘`

## 결과 확인과 수정 요청

결과를 다시 확인하고 싶다면 다음처럼 요청합니다.

> `방금 만든 기능 실행해서 결과 확인해줘`

수정할 때는 기존 결과나 파일 목록을 다시 설명하지 않아도 됩니다.
현재 대화의 문맥에서 바꾸고 싶은 부분만 자연스럽게 말합니다.

> `카드 사이 간격을 조금 넓히고 제목 글씨를 더 크게 해줘`

> `파일이 없을 때 오류 대신 안내 문구가 나오게 해줘`

> `저장 버튼을 누른 뒤 목록 화면으로 돌아가게 바꿔줘`

Codex는 현재 작업과 관련 파일을 확인해 대상을 파악합니다. 여러 기능 중
어느 것을 뜻하는지 확실하지 않아 결과가 크게 달라질 때만 대상 spec을
질문합니다.

## 기억하면 좋은 세 문장

> `docs/example.md md파일로 수정해줘`

> `docs/example.md 참고해서 다음 기능 spec 만들어줘`

> `spec/01_example.md src로 개발해줘`

이후에는 원하는 수정만 평소처럼 말하면 됩니다.
"""


def build_spec(name: str, summary: str, platform: str) -> str:
    return f"""# 01. 프로젝트 기반

## 1. 목적

`{name}`의 첫 개발 기반을 정의한다.

제품 요약: {summary}

대상 플랫폼: `{platform}`

## 2. 첫 번째 범위

- 사용자에게 가장 작은 완결된 결과를 제공하는 한 가지 흐름을 구현한다.
- 세부 입력, 처리 규칙, 출력은 구현 전에 이 문서에 확정한다.

## 3. 비범위

- 사용자가 요청하지 않은 계정, 동기화, 분석, 배포, 관리 기능
- 선택되지 않은 프레임워크와 외부 서비스의 선행 구현

## 4. 아키텍처 원칙

- UI, 도메인 규칙, 저장소, 외부 연동은 실제 필요 경계에서 분리한다.
- 현재 시각과 외부 I/O는 테스트에서 교체 가능하게 한다.
- 첫 번째 기능에 필요하지 않은 계층과 폴더는 생성하지 않는다.

## 5. 오류·보안

- 권한 거부, 빈 데이터, 외부 연동 실패를 정상 상태와 구분한다.
- 실제 인증정보와 사용자 데이터는 소스·테스트·결과물에 포함하지 않는다.

## 6. 수용 기준

- 첫 기능의 입력, 처리, 출력, 오류 기준이 구현 전에 구체화되어 있다.
- 자동 테스트는 외부 실서비스 없이 실행 가능하다.
- 생성 결과는 같은 입력에서 재현 가능하다.

## 7. 구현 전 결정

- 첫 번째 사용자 흐름과 완료 조건
- 저장 방식과 외부 연동 범위
- 플랫폼별 최소 지원 환경
"""


def build_gitignore() -> str:
    return """.DS_Store
.env
.env.*
!.env.example
*.local
__pycache__/
*.py[cod]
.venv/
node_modules/
DerivedData/
build/
dist/
coverage/
"""


def scaffold(
    root: Path,
    *,
    name: str,
    summary: str,
    platform: str,
    init_git: bool,
) -> None:
    ensure_empty_target(root)
    for directory in DIRECTORIES:
        target = root / directory
        target.mkdir(parents=True, exist_ok=True)
        (target / ".gitkeep").touch()

    write_text(root / "README.md", build_readme(name, summary, platform))
    write_text(root / "AGENTS.md", build_agents(name, summary, platform))
    write_text(
        root / "DEVELOPMENT_GUIDE.md",
        build_development_guide(name),
    )
    write_text(root / ".gitignore", build_gitignore())
    write_text(
        root / "spec" / "01_project_foundation.md",
        build_spec(name, summary, platform),
    )
    (root / "spec" / ".gitkeep").unlink()

    if init_git and not (root / ".git").exists():
        subprocess.run(["git", "init", "-b", "dev"], cwd=root, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--init-git", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        scaffold(
            args.root.resolve(),
            name=args.name.strip(),
            summary=args.summary.strip(),
            platform=args.platform.strip(),
            init_git=args.init_git,
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"프로젝트 생성을 중단했습니다: {error}")
        return 1
    print(f"프로젝트 기반 생성 완료: {args.root.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
