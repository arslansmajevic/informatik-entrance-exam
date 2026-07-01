#!/usr/bin/env python3
"""Assemble the static GitHub Pages site for the stlite (in-browser) app.

This copies the Streamlit app and its data files into ``dist/`` and writes a
``manifest.json`` listing them so ``index.html`` can mount them with stlite.

Run it locally with::

    python scripts/build_site.py
    # then serve the result, e.g.:
    python -m http.server -d dist
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"

# Individual files to include (relative to the repo root).
INCLUDE_FILES = ["app.py"]
# Directories whose files are included recursively.
INCLUDE_DIRS = ["quiz", "questions", "images"]

# Files matching these are skipped.
EXCLUDE_SUFFIXES = {".md"}
EXCLUDE_PARTS = {"__pycache__"}


def _should_include(rel: Path) -> bool:
    if any(part in EXCLUDE_PARTS for part in rel.parts):
        return False
    if rel.suffix in EXCLUDE_SUFFIXES:
        return False
    return True


def collect_files() -> list[Path]:
    """Return repo-relative paths of every file that belongs in the site."""
    paths: list[Path] = []

    for name in INCLUDE_FILES:
        path = ROOT_DIR / name
        if path.is_file():
            paths.append(Path(name))

    for directory in INCLUDE_DIRS:
        base = ROOT_DIR / directory
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT_DIR)
            if _should_include(rel):
                paths.append(rel)

    return paths


def build() -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    files = collect_files()

    for rel in files:
        target = DIST_DIR / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT_DIR / rel, target)

    # index.html is the entry page loaded by GitHub Pages.
    shutil.copy2(ROOT_DIR / "index.html", DIST_DIR / "index.html")

    # Manifest consumed by index.html to mount the files into stlite.
    manifest = {"entrypoint": "app.py", "files": [rel.as_posix() for rel in files]}
    (DIST_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    # Prevent GitHub Pages from running Jekyll (which ignores files/dirs
    # starting with an underscore and slows the build down).
    (DIST_DIR / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Built site with {len(files)} app files into {DIST_DIR}")


if __name__ == "__main__":
    build()
