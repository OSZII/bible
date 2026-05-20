import tempfile
import unittest
from pathlib import Path

from scripts.build_serbian_latin import convert_tree, transliterate_serbian


class SerbianLatinTest(unittest.TestCase):
    def test_transliterates_serbian_cyrillic_with_digraphs(self):
        self.assertEqual(
            transliterate_serbian("Љубав Његова и Џинови: Ђ, Ћ, Ч, Ш, Ж."),
            "Ljubav Njegova i Džinovi: Đ, Ć, Č, Š, Ž.",
        )
        self.assertEqual(
            transliterate_serbian("љубав његова и џинови: ђ, ћ, ч, ш, ж."),
            "ljubav njegova i džinovi: đ, ć, č, š, ž.",
        )

    def test_convert_tree_preserves_structure_lines_and_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "sr"
            output = root / "sr-latin"
            chapter = source / "1_Genesis" / "Genesis1.txt"
            chapter.parent.mkdir(parents=True)
            chapter.write_text("У почетку\nЉубав Божја\n\n", encoding="utf-8")

            convert_tree(source, output)

            self.assertEqual(
                (output / "1_Genesis" / "Genesis1.txt").read_text(encoding="utf-8"),
                "U početku\nLjubav Božja\n\n",
            )
            self.assertEqual(
                chapter.read_text(encoding="utf-8"),
                "У почетку\nЉубав Божја\n\n",
            )


if __name__ == "__main__":
    unittest.main()
