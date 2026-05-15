"""Rewrite chapter files from verse-marked Bible sources."""

from __future__ import annotations

import argparse
import re
import time
import urllib.parse
import urllib.request
import zipfile
from collections import OrderedDict
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag


BIBLEGATEWAY_URL = "https://www.biblegateway.com/passage/?search={query}&version=NKJV"
VERSE_COUNT_URL = "https://www.livinggreeknt.org/resources/verse-count.php"
WEB_USFM_URL = "https://ebible.org/Scriptures/engwebu_usfm.zip"

ASCII_TRANSLATION = str.maketrans(
    {
        "\u00a0": " ",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "—": "--",
        "–": "-",
        "…": "...",
    }
)

NKJV_LOCAL_BOOKS = [
    ("1_Genesis", "Genesis", "Genesis", "Gen", 50),
    ("2_Exodus", "Exodus", "Exodus", "Exod", 40),
    ("3_Leviticus", "Leviticus", "Leviticus", "Lev", 27),
    ("4_Numbers", "Numbers", "Numbers", "Num", 36),
    ("5_Deuteronomy", "Deuteronomy", "Deuteronomy", "Deut", 34),
    ("6_Joshua", "Joshua", "Joshua", "Josh", 24),
    ("7_Judges", "Judges", "Judges", "Judg", 21),
    ("8_Ruth", "Ruth", "Ruth", "Ruth", 4),
    ("9_1 Samuel", "1 Samuel", "1 Samuel", "1Sam", 31),
    ("10_2 Samuel", "2 Samuel", "2 Samuel", "2Sam", 24),
    ("11_1 Kings", "1 Kings", "1 Kings", "1Kgs", 22),
    ("12_2 Kings", "2 Kings", "2 Kings", "2Kgs", 25),
    ("13_1 Chronicles", "1 Chronicles", "1 Chronicles", "1Chr", 29),
    ("14_2 Chronicles", "2 Chronicles", "2 Chronicles", "2Chr", 36),
    ("15_Ezra", "Ezra", "Ezra", "Ezra", 10),
    ("16_Nehemiah", "Nehemiah", "Nehemiah", "Neh", 13),
    ("18_Job", "Job", "Job", "Job", 42),
    ("19_Psalm", "Psalm", "Psalms", "Ps", 150),
    ("20_Proverbs", "Proverbs", "Proverbs", "Prov", 31),
    ("21_Ecclesiastes", "Ecclesiastes", "Ecclesiastes", "Eccl", 12),
    ("22_Song of Solomon", "Song of Solomon", "Song of Songs", "Song", 8),
    ("23_Isaiah", "Isaiah", "Isaiah", "Isa", 66),
    ("24_Jeremiah", "Jeremiah", "Jeremiah", "Jer", 52),
    ("25_Lamentations", "Lamentations", "Lamentations", "Lam", 5),
    ("26_Ezekiel", "Ezekiel", "Ezekiel", "Ezek", 48),
    ("28_Hosea", "Hosea", "Hosea", "Hos", 14),
    ("29_Joel", "Joel", "Joel", "Joel", 3),
    ("30_Amos", "Amos", "Amos", "Amos", 9),
    ("31_Obadiah", "Obadiah", "Obadiah", "Obad", 1),
    ("32_Jonah", "Jonah", "Jonah", "Jonah", 4),
    ("33_Micah", "Micah", "Micah", "Mic", 7),
    ("34_Nahum", "Nahum", "Nahum", "Nah", 3),
    ("35_Habakkuk", "Habakkuk", "Habakkuk", "Hab", 3),
    ("36_Zephaniah", "Zephaniah", "Zephaniah", "Zeph", 3),
    ("37_Haggai", "Haggai", "Haggai", "Hag", 2),
    ("38_Zechariah", "Zechariah", "Zechariah", "Zech", 14),
    ("39_Malachi", "Malachi", "Malachi", "Mal", 4),
    ("52_Matthew", "Matthew", "Matthew", "Matt", 28),
    ("53_Mark", "Mark", "Mark", "Mark", 16),
    ("54_Luke", "Luke", "Luke", "Luke", 24),
    ("55_John", "John", "John", "John", 21),
    ("56_Acts", "Acts", "Acts", "Acts", 28),
    ("57_Romans", "Romans", "Romans", "Rom", 16),
    ("58_1 Corinthians", "1 Corinthians", "1 Corinthians", "1Cor", 16),
    ("59_2 Corinthians", "2 Corinthians", "2 Corinthians", "2Cor", 13),
    ("60_Galatians", "Galatians", "Galatians", "Gal", 6),
    ("61_Ephesians", "Ephesians", "Ephesians", "Eph", 6),
    ("62_Philippians", "Philippians", "Philippians", "Phil", 4),
    ("63_Colossians", "Colossians", "Colossians", "Col", 4),
    ("64_1 Thessalonians", "1 Thessalonians", "1 Thessalonians", "1Thess", 5),
    ("65_2 Thessalonians", "2 Thessalonians", "2 Thessalonians", "2Thess", 3),
    ("66_1 Timothy", "1 Timothy", "1 Timothy", "1Tim", 6),
    ("67_2 Timothy", "2 Timothy", "2 Timothy", "2Tim", 4),
    ("68_Titus", "Titus", "Titus", "Titus", 3),
    ("69_Philemon", "Philemon", "Philemon", "Phlm", 1),
    ("70_Hebrews", "Hebrews", "Hebrews", "Heb", 13),
    ("71_James", "James", "James", "Jas", 5),
    ("72_1 Peter", "1 Peter", "1 Peter", "1Pet", 5),
    ("73_2 Peter", "2 Peter", "2 Peter", "2Pet", 3),
    ("74_1 John", "1 John", "1 John", "1John", 5),
    ("75_2 John", "2 John", "2 John", "2John", 1),
    ("76_3 John", "3 John", "3 John", "3John", 1),
    ("77_Jude", "Jude", "Jude", "Jude", 1),
    ("78_Revelation", "Revelation", "Revelation", "Rev", 22),
]

WEB_USFM_BOOKS = {
    "41-TOBengwebu.usfm": ("40_Tobit", "Tobit", None),
    "42-JDTengwebu.usfm": ("41_Judith", "Judith", None),
    "43-ESGengwebu.usfm": ("17_Esther", "Esther", None),
    "45-WISengwebu.usfm": ("42_Wisdom", "Wisdom", None),
    "46-SIRengwebu.usfm": ("43_Sirach", "Sirach", None),
    "47-BARengwebu.usfm": ("44_Baruch", "Baruch", None),
    "52-1MAengwebu.usfm": ("45_1 Maccabees", "1 Maccabees", None),
    "53-2MAengwebu.usfm": ("46_2 Maccabees", "2 Maccabees", None),
    "54-1ESengwebu.usfm": ("47_1 Esdras", "1 Esdras", None),
    "55-MANengwebu.usfm": ("48_Prayer of Manasseh", "Prayer of Manasseh", None),
    "56-PS2engwebu.usfm": ("19_Psalm", "Psalm", {1: 151}),
    "57-3MAengwebu.usfm": ("49_3 Maccabees", "3 Maccabees", None),
    "58-2ESengwebu.usfm": ("50_2 Esdras", "2 Esdras", None),
    "59-4MAengwebu.usfm": ("51_4 Maccabees", "4 Maccabees", None),
    "66-DAGengwebu.usfm": ("27_Daniel", "Daniel", None),
}


def extract_biblegateway_verses(html: str, osis: str, chapter: int) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one(".passage-content")
    if content is None:
        raise ValueError("BibleGateway passage content not found")

    pattern = re.compile(rf"^{re.escape(osis)}-{chapter}-(\d+)$")
    verses: OrderedDict[int, list[str]] = OrderedDict()

    for span in content.select("span.text"):
        if span.find_parent(["h1", "h2", "h3", "h4"]):
            continue

        verse_number = None
        for class_name in span.get("class", []):
            match = pattern.match(class_name)
            if match:
                verse_number = int(match.group(1))
                break
        if verse_number is None:
            continue

        text = normalize_ascii(visible_biblegateway_text(span))
        if text:
            verses.setdefault(verse_number, []).append(text)

    if not verses:
        raise ValueError(f"No BibleGateway verses found for {osis} {chapter}")

    verse_numbers = list(verses)
    expected_numbers = list(range(1, len(verse_numbers) + 1))
    if verse_numbers != expected_numbers:
        raise ValueError(
            f"{osis} {chapter}: non-consecutive BibleGateway verse numbers {verse_numbers}"
        )

    return [clean_spacing(" ".join(parts)) for _, parts in verses.items()]


def parse_usfm_verses(usfm: str) -> dict[int, dict[int, str]]:
    text = remove_usfm_notes(usfm)
    chapters: dict[int, dict[int, list[str]]] = {}
    current_chapter: int | None = None
    current_verse: int | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        chapter_match = re.match(r"^\\c\s+(\d+)", line)
        if chapter_match:
            current_chapter = int(chapter_match.group(1))
            current_verse = None
            chapters.setdefault(current_chapter, {})
            continue

        verse_match = re.match(
            r"^\\v\s+(\d+)(?:[a-zA-Z])?(?:-(\d+)(?:[a-zA-Z])?)?\s*(.*)$",
            line,
        )
        if verse_match:
            if current_chapter is None:
                raise ValueError("USFM verse encountered before chapter")
            start_verse = int(verse_match.group(1))
            end_verse = int(verse_match.group(2) or start_verse)
            if end_verse < start_verse:
                raise ValueError(f"USFM verse bridge runs backward: {line}")

            current_verse = start_verse
            content = clean_usfm_text(verse_match.group(3))
            for verse in range(start_verse, end_verse + 1):
                chapters[current_chapter].setdefault(verse, [])
            if content:
                chapters[current_chapter][current_verse].append(content)
            continue

        if current_chapter is not None and current_verse is not None:
            content = clean_usfm_text(line)
            if content:
                chapters[current_chapter][current_verse].append(content)

    return {
        chapter: {
            verse: clean_spacing(" ".join(parts))
            for verse, parts in sorted(verses.items())
        }
        for chapter, verses in sorted(chapters.items())
    }


def refresh_all(root: Path, cache_dir: Path) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    counts = fetch_verse_counts(cache_dir)
    refresh_nkjv_books(root, cache_dir, counts)
    refresh_web_books(root, cache_dir)


def refresh_nkjv_books(
    root: Path,
    cache_dir: Path,
    counts: dict[tuple[str, int], int],
) -> None:
    for directory, file_book, count_book, osis, chapter_count in NKJV_LOCAL_BOOKS:
        chapter_ranges = chunk_chapters(counts, count_book, chapter_count)
        fetched: dict[int, list[str]] = {}

        for start, end in chapter_ranges:
            query = f"{file_book} {start}" if start == end else f"{file_book} {start}-{end}"
            url = BIBLEGATEWAY_URL.format(query=urllib.parse.quote(query))
            html = fetch_url(url, cache_dir / f"biblegateway-{osis}-{start}-{end}.html")
            for chapter in range(start, end + 1):
                verses = extract_biblegateway_verses(html, osis, chapter)
                fetched[chapter] = verses
            time.sleep(0.1)

        for chapter in range(1, chapter_count + 1):
            write_chapter(root / directory / f"{file_book}{chapter}.txt", fetched[chapter])


def refresh_web_books(root: Path, cache_dir: Path) -> None:
    zip_path = cache_dir / "engwebu_usfm.zip"
    if not zip_path.exists():
        zip_path.write_bytes(fetch_url(WEB_USFM_URL, zip_path, binary=True))

    with zipfile.ZipFile(zip_path) as archive:
        for usfm_name, (directory, file_book, chapter_aliases) in WEB_USFM_BOOKS.items():
            usfm = archive.read(usfm_name).decode("utf-8")
            chapters = parse_usfm_verses(usfm)
            for chapter, verses_by_number in chapters.items():
                output_chapter = chapter_aliases.get(chapter, chapter) if chapter_aliases else chapter
                verses = [
                    verses_by_number.get(number, "")
                    for number in range(1, max(verses_by_number) + 1)
                ]
                write_chapter(root / directory / f"{file_book}{output_chapter}.txt", verses)


def fetch_verse_counts(cache_dir: Path) -> dict[tuple[str, int], int]:
    """Fetch a canonical count table used only to keep range requests small."""
    html = fetch_url(VERSE_COUNT_URL, cache_dir / "livinggreek-verse-count.html")
    soup = BeautifulSoup(html, "html.parser")
    counts: dict[tuple[str, int], int] = {}

    for row in soup.select("tr"):
        cells = [cell.get_text(" ", strip=True).replace("\ufeff", "") for cell in row.select("td")]
        if len(cells) >= 3 and cells[1].isdigit() and cells[2].isdigit():
            counts[(cells[0], int(cells[1]))] = int(cells[2])

    if len(counts) != 1189:
        raise ValueError(f"Expected 1189 canonical verse-count rows, found {len(counts)}")
    return counts


def chunk_chapters(
    counts: dict[tuple[str, int], int],
    book: str,
    chapter_count: int,
    *,
    max_verses: int = 850,
) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    start = 1
    total = 0

    for chapter in range(1, chapter_count + 1):
        chapter_total = counts[(book, chapter)]
        if total and total + chapter_total > max_verses:
            ranges.append((start, chapter - 1))
            start = chapter
            total = 0
        total += chapter_total

    ranges.append((start, chapter_count))
    return ranges


def fetch_url(url: str, cache_path: Path, *, binary: bool = False):
    if cache_path.exists():
        return cache_path.read_bytes() if binary else cache_path.read_text(encoding="utf-8")

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 Bible verse split verification script",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(data)
    return data if binary else data.decode("utf-8")


def write_chapter(path: Path, verses: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(verses) + "\n", encoding="utf-8")


def visible_biblegateway_text(node) -> str:
    if isinstance(node, NavigableString):
        return str(node)

    if not isinstance(node, Tag):
        return ""

    classes = set(node.get("class", []))
    if node.name == "sup" or "chapternum" in classes:
        return ""

    text = "".join(visible_biblegateway_text(child) for child in node.children)
    if "divine-name" in classes or "small-caps" in classes:
        return text.upper()
    return text


def remove_usfm_notes(text: str) -> str:
    text = re.sub(r"\\f\b.*?\\f\*", "", text, flags=re.DOTALL)
    text = re.sub(r"\\x\b.*?\\x\*", "", text, flags=re.DOTALL)
    return text


def clean_usfm_text(text: str) -> str:
    text = normalize_ascii(text)
    text = re.sub(r"\\[+a-zA-Z0-9]+\*", "", text)
    text = re.sub(r"\\[+a-zA-Z0-9]+\s*", "", text)
    return clean_spacing(text)


def normalize_ascii(text: str) -> str:
    return text.translate(ASCII_TRANSLATION)


def clean_spacing(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([\"'])\s+([,.;:!?])", r"\1\2", text)
    return text.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rewrite Bible chapter files with authoritative verse-marked sources."
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--cache-dir", default="/tmp/bible-verse-source-cache")
    args = parser.parse_args()

    refresh_all(Path(args.root), Path(args.cache_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
