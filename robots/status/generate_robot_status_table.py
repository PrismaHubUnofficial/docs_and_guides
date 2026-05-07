#!/usr/bin/env python3
"""
Generate a Markdown table from the robot_matrix.xlsx file.

This script reads the Excel spreadsheet `robot_matrix.xlsx` located in the project root,
computes the status and completeness of each robot guide, and writes a Markdown table
to `gitpage_template/_includes/robot_status_table.md`. The table can be included in
your index page using Jekyll's `{% include %}` tag.

Usage:
    python generate_robot_status_table.py

The script also prints the generated Markdown to stdout for inspection.
"""

import pandas as pd
from pathlib import Path

# Base directory: la cartella dove risiede questo script
BASE_DIR = Path(__file__).resolve().parent

# File Excel da leggere (posto nella stessa cartella dello script)
EXCEL_FILE = BASE_DIR / 'robot_matrix.xlsx'

# Cartella di output (ad esempio la cartella corrente o una sottocartella)
OUTPUT_DIR = BASE_DIR  # oppure BASE_DIR / 'gitpage_template' / '_includes' come nel template

# File Markdown generato
OUTPUT_FILE = OUTPUT_DIR / 'robot_status_table.md'

def compute_status(completeness: float) -> str:
    """Compute textual status from completeness value."""
    if pd.isna(completeness) or completeness == 0:
        return 'Missing'
    if completeness >= 0.9:
        return 'Complete'
    return 'Partial'

def main():
    # Read data from Excel
    df = pd.read_excel(EXCEL_FILE)

    # Build table header
    header = (
        '| Category | Robot | Status | Document Title |\n'
        '|---|---|---|---|\n'
    )

    rows = []
    for _, row in df.iterrows():
        category = str(row['Categoria']).strip()
        robot = str(row['Robot']).strip()
        compl = row['Completezza standard']
        status = compute_status(compl)
        comp_percent = '' if pd.isna(compl) else str(int(round(compl * 100)))
        doc_title = str(row['Titolo documento']).strip()
        # Escape pipe characters in doc_title to avoid breaking the table
        doc_title = doc_title.replace('|', '\\|')
        rows.append(f'| {category} | {robot} | {status} | {doc_title} |')

    table = header + '\n'.join(rows) + '\n'

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # Write the table to file
    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        f.write(table)

    # Print table for convenience
    print(table)
    print(f"Markdown table saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()