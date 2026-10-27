import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from clean_csv import clean_csv


class CleanCSVTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.src = self.base / "input.csv"
        self.dst = self.base / "output.csv"

    def test_trim_deduplicate_and_preserve_original(self):
        content = "id,name\n001, Alice \n001,Alice\n002,Bob\n"
        self.src.write_text(content, encoding="utf-8")
        stats = clean_csv(self.src, self.dst)
        self.assertEqual(stats["duplicates_removed"], 1)
        self.assertEqual(stats["output_rows"], 2)
        self.assertEqual(self.src.read_text(), content)
        with self.dst.open(newline="", encoding="utf-8") as file:
            self.assertEqual(list(csv.reader(file)), [["id", "name"], ["001", "Alice"], ["002", "Bob"]])

    def test_header_only(self):
        self.src.write_text("id,name\n", encoding="utf-8")
        stats = clean_csv(self.src, self.dst)
        self.assertEqual(stats["output_rows"], 0)

    def test_bom(self):
        self.src.write_text("\ufeffid,name\n001, Alice\n", encoding="utf-8")
        clean_csv(self.src, self.dst)
        self.assertTrue(self.dst.read_text(encoding="utf-8").startswith("id,name"))

    def test_reject_overwrite_input(self):
        self.src.write_text("id\n1\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "different file"):
            clean_csv(self.src, self.src)

    def test_reject_existing_output(self):
        self.src.write_text("id\n1\n", encoding="utf-8")
        self.dst.write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "already exists"):
            clean_csv(self.src, self.dst)
        self.assertEqual(self.dst.read_text(), "keep")

    def test_reject_bad_row_without_output(self):
        self.src.write_text("id,name\n1,Alice,extra\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "columns"):
            clean_csv(self.src, self.dst)
        self.assertFalse(self.dst.exists())

    def test_reject_duplicate_headers(self):
        self.src.write_text("id, id \n1,2\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unique"):
            clean_csv(self.src, self.dst)

    def test_case_sensitive_deduplication(self):
        self.src.write_text("id\nABC\nabc\n", encoding="utf-8")
        stats = clean_csv(self.src, self.dst)
        self.assertEqual(stats["output_rows"], 2)

    def test_preserve_quoted_commas(self):
        self.src.write_text('id,note\n001,"Hi, there"\n', encoding="utf-8")
        clean_csv(self.src, self.dst)
        with self.dst.open(newline="", encoding="utf-8") as file:
            self.assertEqual(list(csv.reader(file))[1], ["001", "Hi, there"])


if __name__ == "__main__":
    unittest.main()
