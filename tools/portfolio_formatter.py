"""Command-line utility to normalize client portfolio spreadsheets.

This script helps convert ad-hoc client position spreadsheets into the
standard schema used across other models:

- Classe de ativos
- Fatores
- Instrumentos
- Produto
- Emissor
- Segmento
- Risco
- Fronteira
- Rating
- Instituição
- Posição
- % alocado

Usage example:

    python tools/portfolio_formatter.py \
        --input raw_positions.xlsx \
        --output formatted_positions.xlsx \
        --mapping column_mapping.json

The mapping file should be a JSON object whose keys are the column names in the
source spreadsheet and whose values are the corresponding standard columns.
Columns not present in the source will be created as empty columns so that the
output keeps a predictable structure.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import pandas as pd

TARGET_COLUMNS: List[str] = [
    "Classe de ativos",
    "Fatores",
    "Instrumentos",
    "Produto",
    "Emissor",
    "Segmento",
    "Risco",
    "Fronteira",
    "Rating",
    "Instituição",
    "Posição",
    "% alocado",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize client portfolio spreadsheets into the standard schema.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the input Excel file containing client positions.",
    )
    parser.add_argument(
        "--sheet",
        default=0,
        help="Sheet name or index to read from the input workbook.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Path to the Excel file that will receive the normalized data.",
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        help=(
            "Optional JSON file mapping source column names to the standard ones. "
            "Keys are columns in the input; values must be one of the target columns."
        ),
    )
    return parser.parse_args()


def load_mapping(path: Path | None) -> Dict[str, str]:
    if path is None:
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_dataframe(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """Rename columns using the mapping and ensure the standard order exists.

    Any missing target columns are appended as empty columns. Extra columns in the
    source are preserved but ordered after the standard set to avoid data loss.
    """

    if mapping:
        df = df.rename(columns=mapping)

    for column in TARGET_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    ordered_columns = TARGET_COLUMNS + [col for col in df.columns if col not in TARGET_COLUMNS]
    return df[ordered_columns]


def main() -> None:
    args = parse_args()
    mapping = load_mapping(args.mapping)

    dataframe = pd.read_excel(args.input, sheet_name=args.sheet)
    normalized = normalize_dataframe(dataframe, mapping)

    normalized.to_excel(args.output, index=False)


if __name__ == "__main__":
    main()
