#!/usr/bin/env python3
"""Create the universal, minimal base for a spec-first project."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


DIRECTORIES = ("spec", "src", "docs", "results", "tests")


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

## 현재 범위

`{platform}` 기반 프로젝트의 초기 아키텍처와 첫 번째 기능 spec을 정의한
상태입니다. 애플리케이션 구현은 아직 포함하지 않습니다.

## 구조

- `spec/`: 승인된 기능 개발서
- `src/`: 승인된 spec의 구현
- `docs/`: 사용자 제공 배경지식과 결정 자료
- `results/`: 재현 가능한 검토·사용자 산출물
- `tests/`: 실서비스 인증정보 없이 실행하는 자동 테스트

실행 및 검증 명령은 첫 실행 가능한 기능과 함께 추가합니다.
"""


def build_agents(name: str, summary: str, platform: str) -> str:
    return f"""# {name} 작업 지침

## 목표

{summary}

대상 플랫폼은 `{platform}`이며 승인된 `spec/`을 구현의 단일 기준으로 삼는다.

## 먼저 읽을 순서

1. 루트 `README.md`
2. 작업 대상 `spec/*.md`
3. 관련 `docs/`
4. 외부 연동 문서와 하위 `AGENTS.md`

## 폴더 책임

- `spec/`: 입력, 처리 규칙, 출력, 오류, 보안, 수용 기준
- `src/`: 승인된 spec 구현
- `docs/`: 제공받은 배경지식. 모르는 내용을 추정해 생성하지 않음
- `results/`: 실행으로 재현 가능한 산출물만 저장
- `tests/`: 실제 인증정보와 실사용자 데이터 없이 실행

## 개발 루프

요구사항 → 계획 → 구현 → 관련 테스트 → 산출물 검토 → 수정 순서로 짧게
반복한다. 동작 변경이 필요하면 코드를 임의로 보완하지 말고 spec 변경을
먼저 제안한다.

## 품질과 안전

- 시간, 로케일, 무작위 값은 테스트에서 명시적으로 주입한다.
- 외부 시스템과 장치 기능은 교체 가능한 경계로 격리한다.
- 토큰, 키, 개인정보, 실제 사용자 원문을 소스·테스트·결과에 넣지 않는다.
- 외부 쓰기나 파괴적 작업은 dry-run 또는 가짜 구현으로 먼저 검증한다.
- 변경 후 가장 좁은 관련 테스트를 실행하고, 완료 전 전체 검증을 실행한다.
- UI나 파일 산출물이 바뀌면 실제 렌더링 결과도 검토한다.
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
        target.mkdir(exist_ok=True)
        (target / ".gitkeep").touch()

    write_text(root / "README.md", build_readme(name, summary, platform))
    write_text(root / "AGENTS.md", build_agents(name, summary, platform))
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
