#!/usr/bin/env python3
"""Validate the universal contract of a start-project scaffold."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_DIRECTORIES = (
    "spec",
    "src",
    "src/common",
    "src/spec",
    "docs",
    "results",
    "tests",
)
REQUIRED_FILES = ("AGENTS.md", "DEVELOPMENT_GUIDE.md", "README.md", ".gitignore")
REQUIRED_AGENTS_SECTIONS = ("작업 기준", "짧은 요청 해석", "품질과 안전")
REQUIRED_GUIDE_SECTIONS = ("가장 쉬운 개발 순서", "문서 정리 요청", "기능 spec 요청", "구현 요청", "결과 확인과 수정 요청")
SPEC_NAME_PATTERN = re.compile(r"^\d{2}_[\w-]+\.md$")


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
        for spec in specs:
            if not SPEC_NAME_PATTERN.fullmatch(spec.name):
                errors.append(
                    "spec 파일명은 'NN_feature_name.md' 형식이어야 합니다: "
                    f"{spec.name}"
                )
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
        for rule in ("src/spec/NN_기능명", "Python", "md파일로 수정해줘", "src로 개발해줘"):
            if rule not in agents:
                errors.append(f"AGENTS.md에 필수 개발 규칙이 없습니다: {rule}")

    guide_path = root / "DEVELOPMENT_GUIDE.md"
    if guide_path.is_file():
        guide = guide_path.read_text(encoding="utf-8")
        for heading in REQUIRED_GUIDE_SECTIONS:
            if heading not in guide:
                errors.append(f"DEVELOPMENT_GUIDE.md에 '{heading}' 항목이 없습니다.")
        for example in (
            "docs/example.md md파일로 수정해줘",
            "spec/01_example.md src로 개발해줘",
        ):
            if example not in guide:
                errors.append(f"DEVELOPMENT_GUIDE.md에 요청 예시가 없습니다: {example}")

    readme_path = root / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        if "[DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)" not in readme:
            errors.append("README.md에 DEVELOPMENT_GUIDE.md 첫 사용 안내가 없습니다.")

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
