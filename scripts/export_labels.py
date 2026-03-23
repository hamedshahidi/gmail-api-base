"""Export Gmail label names for the authenticated account."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gmail_base.services.label_service import export_label_names_to_txt


def main() -> None:
    """Export Gmail label names to a text file."""
    output_path = export_label_names_to_txt()
    print(f"Exported labels to: {output_path}")


if __name__ == "__main__":
    main()
