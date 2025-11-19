"""Create a portable zip bundle of the FastAPI tool app.

Usage:
    python scripts/package_app.py --output dist/tool-app.zip

The bundle includes source code, templates, static assets, tool configs, and
metadata files required to run the application.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "dist" / "tool-app.zip"

# Directories and files to include in the bundle (relative to repo root)
INCLUDE_DIRS = ["app", "static", "templates", "tools", "data"]
INCLUDE_FILES = ["requirements.txt", "README.md"]
EXCLUDE_SUFFIXES = {".pyc"}
EXCLUDE_NAMES = {"__pycache__"}


def should_include(path: Path) -> bool:
    """Return True if the path should be packaged."""
    if path.name in EXCLUDE_NAMES:
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    return True


def iter_included_paths(base: Path):
    """Yield all files to include from the configured directories/files."""
    for rel_dir in INCLUDE_DIRS:
        dir_path = base / rel_dir
        if not dir_path.exists():
            continue
        for path in dir_path.rglob("*"):
            if path.is_file() and should_include(path):
                yield path
    for rel_file in INCLUDE_FILES:
        file_path = base / rel_file
        if file_path.exists() and file_path.is_file():
            yield file_path


def create_bundle(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in iter_included_paths(ROOT):
            arcname = path.relative_to(ROOT)
            zf.write(path, arcname)
    print(f"Bundle created at: {output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package the tool app into a zip file.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output zip path (default: dist/tool-app.zip)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_bundle(args.output)


if __name__ == "__main__":
    main()

