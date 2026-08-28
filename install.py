#!/usr/bin/env python3
"""Install repository skills into the current user's Codex skill directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


SKILL_NAMES = ("start-project", "obsidian-daily", "obsidian-docs")


def default_skills_dir() -> Path:
    codex_root = os.environ.get("CODEX_HOME")
    return (
        Path(codex_root).expanduser() / "skills"
        if codex_root
        else Path.home() / ".codex" / "skills"
    )


def install(skills_dir: Path, *, copy: bool) -> list[Path]:
    repository = Path(__file__).resolve().parent
    resolved_skills_dir = skills_dir.expanduser().resolve()
    planned: list[tuple[str, Path, Path]] = []
    installed: list[Path] = []

    for skill_name in SKILL_NAMES:
        source = repository / skill_name
        target = resolved_skills_dir / skill_name
        if not source.is_dir():
            raise FileNotFoundError(f"스킬 원본이 없습니다: {source}")
        if target.is_symlink() and target.resolve() == source.resolve():
            installed.append(target)
            continue
        if target.exists() or target.is_symlink():
            raise FileExistsError(
                f"기존 설치본이 있습니다: {target}\n"
                "내용을 확인하고 직접 제거한 뒤 다시 실행하세요."
            )
        planned.append((skill_name, source, target))

    resolved_skills_dir.mkdir(parents=True, exist_ok=True)
    for skill_name, source, target in planned:
        if copy:
            shutil.copytree(source, target)
        else:
            target.symlink_to(source, target_is_directory=True)
        installed.append(target)
        print(f"{skill_name} 설치 완료: {target}")

    for target in installed:
        if target not in {item[2] for item in planned}:
            print(f"이미 연결되어 있습니다: {target}")
    return installed


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
