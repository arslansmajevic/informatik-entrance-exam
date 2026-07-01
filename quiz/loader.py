"""Loading and validation of quiz question files.

Each part of the entrance exam lives in its own JSON file inside the
``questions`` directory. A file describes a single part of the test and the
questions it contains. See ``questions/README.md`` for the file format.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

# Root of the repository (parent of this ``quiz`` package).
ROOT_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_DIR = ROOT_DIR / "questions"


@dataclass
class Question:
    """A single quiz question."""

    id: str
    text: str
    options: list[str]
    correct: list[int]
    image: str | None = None
    explanation: str | None = None

    @property
    def multiple(self) -> bool:
        """Whether more than one answer is correct."""
        return len(self.correct) > 1

    def is_correct(self, selected: list[int]) -> bool:
        """Return ``True`` when ``selected`` matches the correct answers."""
        return sorted(selected) == sorted(self.correct)


@dataclass
class Part:
    """A part of the exam, i.e. one question file."""

    key: str
    title: str
    description: str
    questions: list[Question] = field(default_factory=list)


def _resolve_image(image: str | None) -> str | None:
    """Turn a relative image path from a question file into an absolute one."""
    if not image:
        return None
    path = Path(image)
    if not path.is_absolute():
        path = ROOT_DIR / path
    return str(path) if path.exists() else None


def load_part(file_path: Path) -> Part:
    """Load and validate a single question file."""
    data = json.loads(file_path.read_text(encoding="utf-8"))

    title = data.get("title", file_path.stem)
    description = data.get("description", "")

    questions: list[Question] = []
    for index, raw in enumerate(data.get("questions", [])):
        options = raw.get("options", [])
        correct = raw.get("correct", [])

        if not options:
            raise ValueError(f"{file_path.name}: question {index} has no options")
        if not correct:
            raise ValueError(f"{file_path.name}: question {index} has no correct answers")
        for c in correct:
            if not 0 <= c < len(options):
                raise ValueError(
                    f"{file_path.name}: question {index} has an out-of-range "
                    f"correct index {c}"
                )

        questions.append(
            Question(
                id=str(raw.get("id", f"{file_path.stem}-{index}")),
                text=raw.get("question", ""),
                options=options,
                correct=list(correct),
                image=_resolve_image(raw.get("image")),
                explanation=raw.get("explanation"),
            )
        )

    return Part(
        key=file_path.stem,
        title=title,
        description=description,
        questions=questions,
    )


def load_parts(directory: Path | None = None) -> list[Part]:
    """Load every ``*.json`` question file from ``directory`` (sorted by name)."""
    directory = directory or QUESTIONS_DIR
    parts: list[Part] = []
    for file_path in sorted(directory.glob("*.json")):
        parts.append(load_part(file_path))
    return parts
