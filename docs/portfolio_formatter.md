# Portfolio formatter utility

The script `tools/portfolio_formatter.py` converts client position spreadsheets
into the standard column layout used in the example screenshot. It keeps the
canonical column order and optionally renames incoming columns through a JSON
mapping.

## Standard columns

```
Classe de ativos, Fatores, Instrumentos, Produto, Emissor, Segmento,
Risco, Fronteira, Rating, Instituição, Posição, % alocado
```

## Usage

```bash
python tools/portfolio_formatter.py \
  --input raw_positions.xlsx \
  --output formatted_positions.xlsx \
  --mapping column_mapping.json
```

> Requirements: `pandas` and `openpyxl` (for Excel I/O).

- `--input`: path to the spreadsheet that needs normalization. The default
  sheet is the first one; use `--sheet` to target another sheet.
- `--output`: path where the normalized workbook will be written.
- `--mapping` (optional): JSON file where **keys** are the column titles in the
  raw spreadsheet and **values** are the target column titles. Missing target
  columns are appended as empty columns so the output schema is predictable.

### Sample mapping file

```json
{
  "Classe": "Classe de ativos",
  "Fator": "Fatores",
  "Instrumento": "Instrumentos",
  "Produto": "Produto",
  "Emissor": "Emissor",
  "Segmento": "Segmento",
  "Risco": "Risco",
  "País": "Fronteira",
  "Rating": "Rating",
  "Custodiante": "Instituição",
  "Valor": "Posição",
  "%": "% alocado"
}
```

Run the script with the mapping to reshape your workbook into the desired
layout. Extra columns from the source are preserved after the standard ones to
avoid data loss.
