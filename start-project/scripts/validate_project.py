#!/usr/bin/env python3
"""Validate the universal contract of a start-project scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_DIRECTORIES = ("spec", "src", "docs", "results", "tests")
REQUIRED_FILES = ("AGENTS.md", "README.md", ".gitignore")
REQUIRED_AGENTS_SECTIONS = ("개발 루프", "품질과 안전")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_DIRECTORIES:
        if not (root / name).is_dir():
            errors.append(f"필수 폴더가 없습니다: {name}/")
    for name in REQUIRED_FILES:
        target = root / name
        if not target.is_file():
            errors.append(f"필수 파일이 없습니다: {name}")
        elif not target.read_text(encoding="utf-8").strip():
            errors.append(f"필수 파일이 비어 있습니다: {name}")

    specs = sorted((root / "spec").glob("*.md")) if (root / "spec").is_dir() else []
    if not specs:
        errors.append("최소 한 개의 spec Markdown 파일이 필요합니다.")
    else:
        first_spec = specs[0].read_text(encoding="utf-8")
        for heading in ("목적", "비범위", "오류", "수용 기준"):
            if heading not in first_spec:
                errors.append(f"첫 spec에 '{heading}' 항목이 없습니다.")

    agents_path = root / "AGENTS.md"
    if agents_path.is_file():
        agents = agents_path.read_text(encoding="utf-8")
        for heading in REQUIRED_AGENTS_SECTIONS:
            if heading not in agents:
                errors.append(f"AGENTS.md에 '{heading}' 항목이 없습니다.")

    for target in root.rglob("*"):
        if target.is_file() and target.name != ".gitkeep":
            try:
                text = target.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "[TODO" in text:
                errors.append(f"미완성 TODO 템플릿이 있습니다: {target.relative_to(root)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate(root)
    if errors:
        print("프로젝트 기반 검증 실패:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"프로젝트 기반 검증 통과: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
