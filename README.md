# Smart CSV Cleaner

A small, beginner-friendly Python project for cleaning **CSV** files.

## What it does
- Removes spaces at the beginning/end of headers and cell values.
- Removes **exact duplicate rows after trimming spaces**.
- Preserves text values such as customer IDs (`001` stays `001`).
- Keeps the original input file unchanged.
- Saves a new cleaned CSV and prints a summary.

## Requirements
- Python 3.9+ (no third-party packages needed).

## Windows quick start
1. Extract the ZIP.
2. Open the extracted folder in File Explorer.
3. Click the address bar, type `cmd`, press Enter.
4. Check Python: `py --version`
5. Run the sample:
   `py clean_csv.py samples\sample_dirty.csv --output samples\sample_cleaned.csv`
6. Open `samples\sample_cleaned.csv` in Excel or Notepad.

If `py` isn't recognized, try `python` in place of `py`.

## Clean a customer's file (after testing)
`py clean_csv.py "C:\path\to\customers.csv" --output "C:\path\to\customers_cleaned.csv"`

Use **copies** of customer files and keep them private. Never upload customer data to public GitHub.

## Run automated tests
`py -m unittest discover -s tests -v`

## Limitations
- Only UTF-8 CSV with a header row.
- Rejects inconsistent column counts and duplicate/empty headers.
- Removes only *exact* duplicate rows after whitespace trimming. It does not guess that
  similar names refer to the same person, fix incorrect facts, fill missing values,
  or standardize dates/phone numbers.
- Row comparisons are case-sensitive.
- No Excel `.xlsx` support.
- Does not overwrite existing output files unless `--force` is explicitly provided.
- No guarantees for malformed or extremely large files.

## Fiverr demonstration
Use the fictional sample CSV in `samples/`. Never claim this is real client work.
Publish screenshots of the original and cleaned sample, along with test results.
