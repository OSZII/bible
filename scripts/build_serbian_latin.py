"""Build Serbian Latin chapter files from the Serbian Cyrillic tree."""

from __future__ import annotations

import argparse
from pathlib import Path


SINGLE_LETTER_MAP = str.maketrans(
    {
        "А": "A",
        "а": "a",
        "Б": "B",
        "б": "b",
        "В": "V",
        "в": "v",
        "Г": "G",
        "г": "g",
        "Д": "D",
        "д": "d",
        "Ђ": "Đ",
        "ђ": "đ",
        "Е": "E",
        "е": "e",
        "Ж": "Ž",
        "ж": "ž",
        "З": "Z",
        "з": "z",
        "И": "I",
        "и": "i",
        "Ј": "J",
        "ј": "j",
        "К": "K",
        "к": "k",
        "Л": "L",
        "л": "l",
        "М": "M",
        "м": "m",
        "Н": "N",
        "н": "n",
        "О": "O",
        "о": "o",
        "П": "P",
        "п": "p",
        "Р": "R",
        "р": "r",
        "С": "S",
        "с": "s",
        "Т": "T",
        "т": "t",
        "Ћ": "Ć",
        "ћ": "ć",
        "У": "U",
        "у": "u",
        "Ф": "F",
        "ф": "f",
        "Х": "H",
        "х": "h",
        "Ц": "C",
        "ц": "c",
        "Ч": "Č",
        "ч": "č",
        "Ш": "Š",
        "ш": "š",
    }
)

LOWER_DIGRAPHS = {
    "љ": "lj",
    "њ": "nj",
    "џ": "dž",
}

UPPER_DIGRAPHS = {
    "Љ": ("Lj", "LJ"),
    "Њ": ("Nj", "NJ"),
    "Џ": ("Dž", "DŽ"),
}


def transliterate_serbian(text: str) -> str:
    pieces: list[str] = []
    for index, char in enumerate(text):
        if char in LOWER_DIGRAPHS:
            pieces.append(LOWER_DIGRAPHS[char])
        elif char in UPPER_DIGRAPHS:
            titlecase, uppercase = UPPER_DIGRAPHS[char]
            next_char = text[index + 1] if index + 1 < len(text) else ""
            pieces.append(titlecase if next_char.islower() else uppercase)
        else:
            pieces.append(char.translate(SINGLE_LETTER_MAP))
    return "".join(pieces)


def convert_tree(source_root: Path, output_root: Path) -> int:
    if not source_root.is_dir():
        raise FileNotFoundError(f"Source directory does not exist: {source_root}")

    count = 0
    for source_path in sorted(source_root.glob("**/*.txt")):
        relative_path = source_path.relative_to(source_root)
        output_path = output_root / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        text = source_path.read_text(encoding="utf-8")
        output_path.write_text(transliterate_serbian(text), encoding="utf-8")
        count += 1

    return count


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert Serbian Cyrillic chapter files to Serbian Latin."
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--source", default="sr")
    parser.add_argument("--output", default="sr-latin")
    args = parser.parse_args()

    root = Path(args.root)
    source = root / args.source
    output = root / args.output
    count = convert_tree(source, output)
    print(f"Wrote {count} Serbian Latin chapter files to {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
