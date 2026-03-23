"""Print Gmail label names for the authenticated account."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gmail_base.services.label_service import get_all_label_names


def main() -> None:
    """Print all Gmail label names, one per line."""
    for label_name in get_all_label_names():
        print(label_name)


if __name__ == "__main__":
    main()
