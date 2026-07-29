#!/usr/bin/env python3
"""Install repository skills into the current user's Codex skill directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


SKILL_NAME = "start-project"


def default_skills_dir() -> Path:
    codex_root = os.environ.get("CODEX_HOME")
    return (
        Path(codex_root).expanduser() / "skills"
        if codex_root
        else Path.home() / ".codex" / "skills"
    )


def install(skills_dir: Path, *, copy: bool) -> Path:
    source = Path(__file__).resolve().parent / SKILL_NAME
    target = skills_dir.expanduser().resolve() / SKILL_NAME
    if not source.is_dir():
        raise FileNotFoundError(f"스킬 원본이 없습니다: {source}")

    skills_dir.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() and target.resolve() == source.resolve():
        print(f"이미 연결되어 있습니다: {target}")
        return target
    if target.exists() or target.is_symlink():
        raise FileExistsError(
            f"기존 설치본이 있습니다: {target}\n"
            "내용을 확인하고 직접 제거한 뒤 다시 실행하세요."
        )

    if copy:
        shutil.copytree(source, target)
    else:
        target.symlink_to(source, target_is_directory=True)
    print(f"{SKILL_NAME} 설치 완료: {target}")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=default_skills_dir(),
        help="Codex skills 폴더(기본값: $CODEX_HOME/skills 또는 ~/.codex/skills)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="심볼릭 링크 대신 스킬 폴더를 복사",
    )
    args = parser.parse_args()
    try:
        install(args.skills_dir, copy=args.copy)
    except (FileExistsError, FileNotFoundError, OSError) as error:
        print(f"설치를 중단했습니다: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
