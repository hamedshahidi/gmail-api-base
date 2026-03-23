"""Helpers for reading and exporting Gmail labels."""

from __future__ import annotations

from pathlib import Path

from gmail_base.service import get_gmail_service


def get_all_labels() -> list[dict]:
    """Return all labels available for the authenticated Gmail account."""
    service = get_gmail_service()
    response = service.users().labels().list(userId="me").execute()
    return response.get("labels", [])


def get_all_label_names() -> list[str]:
    """Return the names of all labels for the authenticated Gmail account."""
    return [label["name"] for label in get_all_labels() if "name" in label]


def export_label_names_to_txt(output_path: str = "output/labels.txt") -> str:
    """Write Gmail label names to a UTF-8 text file and return its path."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    label_names = get_all_label_names()
    contents = "\n".join(label_names)

    if contents:
        contents += "\n"

    output_file.write_text(contents, encoding="utf-8")
    return output_file.as_posix()
