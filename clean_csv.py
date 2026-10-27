#!/usr/bin/env python3
"""Safely clean one CSV file: trim surrounding spaces and remove duplicate rows."""
import argparse
import csv
from pathlib import Path
import sys


def clean_csv(source: Path, destination: Path, force: bool = False) -> dict:
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()

    if not source.is_file():
        raise ValueError(f"Input file not found: {source}")
    if source.suffix.lower() != ".csv":
        raise ValueError("The input must be a .csv file.")
    if source == destination:
        raise ValueError("Output must be a different file. Your original will not be overwritten.")
    if destination.exists() and not force:
        raise ValueError("Output already exists. Choose another filename or use --force.")

    # Read and validate completely before creating any output.
    with source.open("r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.reader(infile, strict=True)
        try:
            original_header = next(reader)
        except StopIteration:
            raise ValueError("The CSV is empty and has no header row.")

        header = [name.strip() for name in original_header]
        if not header or any(not name for name in header):
            raise ValueError("Each CSV column must have a nonempty header.")
        if len(set(header)) != len(header):
            raise ValueError("Column headers must be unique after removing surrounding spaces.")

        cleaned_rows = []
        seen = set()
        duplicate_count = 0
        changed_cells = sum(a != b for a, b in zip(original_header, header))
        input_count = 0

        for line_number, row in enumerate(reader, start=2):
            input_count += 1
            if len(row) != len(header):
                raise ValueError(
                    f"Row {line_number} has {len(row)} columns; expected {len(header)}. "
                    "Fix this row before cleaning."
                )
            cleaned = [cell.strip() for cell in row]
            changed_cells += sum(a != b for a, b in zip(row, cleaned))
            key = tuple(cleaned)
            if key in seen:
                duplicate_count += 1
                continue
            seen.add(key)
            cleaned_rows.append(cleaned)

    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(cleaned_rows)

    return {
        "input_rows": input_count,
        "output_rows": len(cleaned_rows),
        "duplicates_removed": duplicate_count,
        "cells_trimmed": changed_cells,
        "output": str(destination),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Trim surrounding whitespace and remove identical CSV rows."
    )
    parser.add_argument("input", type=Path, help="CSV file to clean")
    parser.add_argument("--output", type=Path, help="Output CSV path (default: *_cleaned.csv)")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    args = parser.parse_args()
    output = args.output or args.input.with_name(args.input.stem + "_cleaned.csv")
    try:
        result = clean_csv(args.input, output, args.force)
    except (ValueError, OSError, UnicodeError, csv.Error) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("CSV cleanup complete!")
    print(f"Rows received:      {result['input_rows']}")
    print(f"Duplicate rows:     {result['duplicates_removed']}")
    print(f"Rows delivered:     {result['output_rows']}")
    print(f"Cells trimmed:      {result['cells_trimmed']}")
    print(f"Saved clean file:   {result['output']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
