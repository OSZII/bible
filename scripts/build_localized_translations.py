"""Build localized chapter files aligned to the English verse layout."""

from __future__ import annotations

import argparse
import html
import re
import urllib.request
import zipfile
from collections.abc import Iterable
from pathlib import Path
from xml.etree import ElementTree


SRP1868_USFM_URL = "https://ebible.org/Scriptures/srp1868_usfm.zip"
LUTH1912AP_OSIS_URL = (
    "https://raw.githubusercontent.com/gratis-bible/bible/master/de/luth1912ap.xml"
)
OPEN_BIBLES_BULGARIAN_OSIS_URL = (
    "https://raw.githubusercontent.com/seven1m/open-bibles/master/"
    "bul-bulgarian.osis.xml"
)
SVETOSAVLJE_BASE_URL = "https://svetosavlje.org/"
EBIBLE_SCRIPTURES_BASE_URL = "https://ebible.org/Scriptures/"

EBIBLE_USFM_TRANSLATIONS = {
    "be": "bel",
    "es": "spablm",
    "fr": "frasbl",
    "it": "ita1927",
    "ro": "ronbtf",
    "ru": "russyn",
    "uk": "ukrfb",
}

BOOKS_66 = [
    ("1_Genesis", "Genesis", "Gen", "GEN"),
    ("2_Exodus", "Exodus", "Exod", "EXO"),
    ("3_Leviticus", "Leviticus", "Lev", "LEV"),
    ("4_Numbers", "Numbers", "Num", "NUM"),
    ("5_Deuteronomy", "Deuteronomy", "Deut", "DEU"),
    ("6_Joshua", "Joshua", "Josh", "JOS"),
    ("7_Judges", "Judges", "Judg", "JDG"),
    ("8_Ruth", "Ruth", "Ruth", "RUT"),
    ("9_1 Samuel", "1 Samuel", "1Sam", "1SA"),
    ("10_2 Samuel", "2 Samuel", "2Sam", "2SA"),
    ("11_1 Kings", "1 Kings", "1Kgs", "1KI"),
    ("12_2 Kings", "2 Kings", "2Kgs", "2KI"),
    ("13_1 Chronicles", "1 Chronicles", "1Chr", "1CH"),
    ("14_2 Chronicles", "2 Chronicles", "2Chr", "2CH"),
    ("15_Ezra", "Ezra", "Ezra", "EZR"),
    ("16_Nehemiah", "Nehemiah", "Neh", "NEH"),
    ("17_Esther", "Esther", "Esth", "EST"),
    ("18_Job", "Job", "Job", "JOB"),
    ("19_Psalm", "Psalm", "Ps", "PSA"),
    ("20_Proverbs", "Proverbs", "Prov", "PRO"),
    ("21_Ecclesiastes", "Ecclesiastes", "Eccl", "ECC"),
    ("22_Song of Solomon", "Song of Solomon", "Song", "SNG"),
    ("23_Isaiah", "Isaiah", "Isa", "ISA"),
    ("24_Jeremiah", "Jeremiah", "Jer", "JER"),
    ("25_Lamentations", "Lamentations", "Lam", "LAM"),
    ("26_Ezekiel", "Ezekiel", "Ezek", "EZK"),
    ("27_Daniel", "Daniel", "Dan", "DAN"),
    ("28_Hosea", "Hosea", "Hos", "HOS"),
    ("29_Joel", "Joel", "Joel", "JOL"),
    ("30_Amos", "Amos", "Amos", "AMO"),
    ("31_Obadiah", "Obadiah", "Obad", "OBA"),
    ("32_Jonah", "Jonah", "Jonah", "JON"),
    ("33_Micah", "Micah", "Mic", "MIC"),
    ("34_Nahum", "Nahum", "Nah", "NAM"),
    ("35_Habakkuk", "Habakkuk", "Hab", "HAB"),
    ("36_Zephaniah", "Zephaniah", "Zeph", "ZEP"),
    ("37_Haggai", "Haggai", "Hag", "HAG"),
    ("38_Zechariah", "Zechariah", "Zech", "ZEC"),
    ("39_Malachi", "Malachi", "Mal", "MAL"),
    ("52_Matthew", "Matthew", "Matt", "MAT"),
    ("53_Mark", "Mark", "Mark", "MRK"),
    ("54_Luke", "Luke", "Luke", "LUK"),
    ("55_John", "John", "John", "JHN"),
    ("56_Acts", "Acts", "Acts", "ACT"),
    ("57_Romans", "Romans", "Rom", "ROM"),
    ("58_1 Corinthians", "1 Corinthians", "1Cor", "1CO"),
    ("59_2 Corinthians", "2 Corinthians", "2Cor", "2CO"),
    ("60_Galatians", "Galatians", "Gal", "GAL"),
    ("61_Ephesians", "Ephesians", "Eph", "EPH"),
    ("62_Philippians", "Philippians", "Phil", "PHP"),
    ("63_Colossians", "Colossians", "Col", "COL"),
    ("64_1 Thessalonians", "1 Thessalonians", "1Thess", "1TH"),
    ("65_2 Thessalonians", "2 Thessalonians", "2Thess", "2TH"),
    ("66_1 Timothy", "1 Timothy", "1Tim", "1TI"),
    ("67_2 Timothy", "2 Timothy", "2Tim", "2TI"),
    ("68_Titus", "Titus", "Titus", "TIT"),
    ("69_Philemon", "Philemon", "Phlm", "PHM"),
    ("70_Hebrews", "Hebrews", "Heb", "HEB"),
    ("71_James", "James", "Jas", "JAS"),
    ("72_1 Peter", "1 Peter", "1Pet", "1PE"),
    ("73_2 Peter", "2 Peter", "2Pet", "2PE"),
    ("74_1 John", "1 John", "1John", "1JN"),
    ("75_2 John", "2 John", "2John", "2JN"),
    ("76_3 John", "3 John", "3John", "3JN"),
    ("77_Jude", "Jude", "Jude", "JUD"),
    ("78_Revelation", "Revelation", "Rev", "REV"),
]

DE_DEUTEROCANON = [
    ("40_Tobit", "Tobit", "Tob"),
    ("41_Judith", "Judith", "Jdt"),
    ("42_Wisdom", "Wisdom", "Wis"),
    ("43_Sirach", "Sirach", "Sir"),
    ("44_Baruch", "Baruch", "Bar"),
    ("45_1 Maccabees", "1 Maccabees", "1Macc"),
    ("46_2 Maccabees", "2 Maccabees", "2Macc"),
    ("48_Prayer of Manasseh", "Prayer of Manasseh", "PrMan"),
]

USFM_DEUTEROCANON = [
    ("40_Tobit", "Tobit", "TOB"),
    ("41_Judith", "Judith", "JDT"),
    ("42_Wisdom", "Wisdom", "WIS"),
    ("43_Sirach", "Sirach", "SIR"),
    ("44_Baruch", "Baruch", "BAR"),
    ("45_1 Maccabees", "1 Maccabees", "1MA"),
    ("46_2 Maccabees", "2 Maccabees", "2MA"),
    ("47_1 Esdras", "1 Esdras", "1ES"),
    ("48_Prayer of Manasseh", "Prayer of Manasseh", "MAN"),
    ("49_3 Maccabees", "3 Maccabees", "3MA"),
    ("50_2 Esdras", "2 Esdras", "2ES"),
    ("51_4 Maccabees", "4 Maccabees", "4MA"),
]

VerseMap = dict[tuple[str, str, int], dict[int, str]]

SERBIAN_PAGE_BOOKS = [
    ("1_Genesis", "Genesis", "sveto-pismo-1/1/"),
    ("2_Exodus", "Exodus", "sveto-pismo-1/2/"),
    ("3_Leviticus", "Leviticus", "sveto-pismo-1/3/"),
    ("4_Numbers", "Numbers", "sveto-pismo-1/4/"),
    ("5_Deuteronomy", "Deuteronomy", "sveto-pismo-1/5/"),
    ("6_Joshua", "Joshua", "sveto-pismo-1/6/"),
    ("7_Judges", "Judges", "sveto-pismo-1/7/"),
    ("8_Ruth", "Ruth", "sveto-pismo-2/1/"),
    ("9_1 Samuel", "1 Samuel", "sveto-pismo-2/2/"),
    ("10_2 Samuel", "2 Samuel", "sveto-pismo-2/3/"),
    ("11_1 Kings", "1 Kings", "sveto-pismo-2/4/"),
    ("12_2 Kings", "2 Kings", "sveto-pismo-2/5/"),
    ("13_1 Chronicles", "1 Chronicles", "sveto-pismo-2/6/"),
    ("14_2 Chronicles", "2 Chronicles", "sveto-pismo-2/7/"),
    ("15_Ezra", "Ezra", "sveto-pismo-2/8/"),
    ("16_Nehemiah", "Nehemiah", "sveto-pismo-2/9/"),
    ("18_Job", "Job", "sveto-pismo-3/1/"),
    ("19_Psalm", "Psalm", "sveto-pismo-3/2/"),
    ("20_Proverbs", "Proverbs", "sveto-pismo-3/3/"),
    ("21_Ecclesiastes", "Ecclesiastes", "sveto-pismo-3/4/"),
    ("22_Song of Solomon", "Song of Solomon", "sveto-pismo-3/5/"),
    ("23_Isaiah", "Isaiah", "sveto-pismo-4/1/"),
    ("24_Jeremiah", "Jeremiah", "sveto-pismo-4/2/"),
    ("25_Lamentations", "Lamentations", "sveto-pismo-4/3/"),
    ("26_Ezekiel", "Ezekiel", "sveto-pismo-4/4/"),
    ("27_Daniel", "Daniel", "sveto-pismo-4/5/"),
    ("28_Hosea", "Hosea", "sveto-pismo-4/6/"),
    ("29_Joel", "Joel", "sveto-pismo-4/7/"),
    ("30_Amos", "Amos", "sveto-pismo-4/8/"),
    ("31_Obadiah", "Obadiah", "sveto-pismo-4/9/"),
    ("32_Jonah", "Jonah", "sveto-pismo-4/10/"),
    ("33_Micah", "Micah", "sveto-pismo-4/11/"),
    ("34_Nahum", "Nahum", "sveto-pismo-4/12/"),
    ("35_Habakkuk", "Habakkuk", "sveto-pismo-4/13/"),
    ("36_Zephaniah", "Zephaniah", "sveto-pismo-4/14/"),
    ("37_Haggai", "Haggai", "sveto-pismo-4/15/"),
    ("38_Zechariah", "Zechariah", "sveto-pismo-4/16/"),
    ("39_Malachi", "Malachi", "sveto-pismo-4/17/"),
    ("47_1 Esdras", "1 Esdras", "sveto-pismo-5/1/"),
    ("40_Tobit", "Tobit", "sveto-pismo-5/3/"),
    ("41_Judith", "Judith", "sveto-pismo-5/4/"),
    ("42_Wisdom", "Wisdom", "sveto-pismo-5/5/"),
    ("43_Sirach", "Sirach", "sveto-pismo-5/6/"),
    ("45_1 Maccabees", "1 Maccabees", "sveto-pismo-6/3/"),
    ("46_2 Maccabees", "2 Maccabees", "sveto-pismo-6/4/"),
    ("49_3 Maccabees", "3 Maccabees", "sveto-pismo-6/5/"),
    ("51_4 Maccabees", "4 Maccabees", "sveto-pismo-6/6/"),
    ("52_Matthew", "Matthew", "sveto-pismo-7/1/"),
    ("53_Mark", "Mark", "sveto-pismo-7/2/"),
    ("54_Luke", "Luke", "sveto-pismo-7/3/"),
    ("55_John", "John", "sveto-pismo-7/4/"),
    ("56_Acts", "Acts", "sveto-pismo-8/1/"),
    ("57_Romans", "Romans", "sveto-pismo-8/2/"),
    ("58_1 Corinthians", "1 Corinthians", "sveto-pismo-8/3/"),
    ("59_2 Corinthians", "2 Corinthians", "sveto-pismo-8/4/"),
    ("60_Galatians", "Galatians", "sveto-pismo-8/5/"),
    ("61_Ephesians", "Ephesians", "sveto-pismo-8/6/"),
    ("62_Philippians", "Philippians", "sveto-pismo-8/7/"),
    ("63_Colossians", "Colossians", "sveto-pismo-8/8/"),
    ("64_1 Thessalonians", "1 Thessalonians", "sveto-pismo-8/9/"),
    ("65_2 Thessalonians", "2 Thessalonians", "sveto-pismo-8/10/"),
    ("66_1 Timothy", "1 Timothy", "sveto-pismo-8/11/"),
    ("67_2 Timothy", "2 Timothy", "sveto-pismo-8/12/"),
    ("68_Titus", "Titus", "sveto-pismo-8/13/"),
    ("69_Philemon", "Philemon", "sveto-pismo-8/14/"),
    ("70_Hebrews", "Hebrews", "sveto-pismo-8/15/"),
    ("71_James", "James", "sveto-pismo-8/16/"),
    ("72_1 Peter", "1 Peter", "sveto-pismo-8/17/"),
    ("73_2 Peter", "2 Peter", "sveto-pismo-8/18/"),
    ("74_1 John", "1 John", "sveto-pismo-8/19/"),
    ("75_2 John", "2 John", "sveto-pismo-8/20/"),
    ("76_3 John", "3 John", "sveto-pismo-8/21/"),
    ("77_Jude", "Jude", "sveto-pismo-8/22/"),
    ("78_Revelation", "Revelation", "sveto-pismo-8/23/"),
]


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


def download(url: str, cache_path: Path) -> Path:
    if cache_path.exists():
        return cache_path

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Bible localized translation builder"},
    )
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=30) as response:
        cache_path.write_bytes(response.read())
    return cache_path


def svetosavlje_page(slug: str, cache_dir: Path) -> Path:
    filename = "svetosavlje_" + slug.strip("/").replace("/", "_") + ".html"
    return download(SVETOSAVLJE_BASE_URL + slug, cache_dir / filename)


def parse_svetosavlje_numeric_chapters(path: Path) -> dict[int, dict[int, str]]:
    marked = parse_svetosavlje_marked_verses(path)
    chapters: dict[int, dict[int, str]] = {}
    for (chapter, verse_marker), text in marked.items():
        if verse_marker.isdigit():
            chapters.setdefault(chapter, {})[int(verse_marker)] = text
    return chapters


def parse_svetosavlje_marked_verses(path: Path) -> dict[tuple[int, str], str]:
    page = path.read_text(encoding="utf-8")
    anchor_pattern = re.compile(
        r'<a\s+name="[^"]+?_(\d+)_(\d+[A-Za-z]*)"\s*></a>',
        flags=re.IGNORECASE,
    )
    matches = list(anchor_pattern.finditer(page))
    verses: dict[tuple[int, str], str] = {}

    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(page)
        paragraph_end = page.find("</p>", match.end(), next_start)
        end = paragraph_end if paragraph_end != -1 else next_start
        text = clean_svetosavlje_html(page[match.end() : end])
        if text:
            verses[(int(match.group(1)), match.group(2).lower())] = text

    return verses


def clean_svetosavlje_html(fragment: str) -> str:
    fragment = re.sub(r"<span\b[^>]*>.*?</span>", "", fragment, flags=re.DOTALL)
    fragment = re.sub(
        r'<a\s+href="#_ftn[^"]*"[^>]*>\[[^\]]+\]</a>',
        "",
        fragment,
        flags=re.DOTALL,
    )
    fragment = fragment.replace("<br />", " ").replace("<br/>", " ").replace("<br>", " ")
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    text = html.unescape(fragment)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[*†‡]+", " ", text)
    text = re.sub(r"^\[\d+\.\]\s*", "", text)
    text = re.sub(r"^\[?\d+\]?\s*[^\W\d_]*\.\s*", "", text)
    text = re.sub(r"^[IVXLCDM]+\.[^\W\d_]\.\s*", "", text)
    text = clean_spacing(text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return text.strip(" -–")


def add_page_sources(
    sources: VerseMap,
    directory: str,
    file_book: str,
    chapters: dict[int, dict[int, str]],
) -> None:
    for chapter, verses in chapters.items():
        sources[(directory, file_book, chapter)] = dict(verses)


def expected_layout(root: Path) -> dict[tuple[str, str, int], int]:
    layout: dict[tuple[str, str, int], int] = {}
    for path in sorted((root / "en").glob("*/*.txt")):
        match = re.fullmatch(r"(.+?)(\d+)\.txt", path.name)
        if match is None:
            raise ValueError(f"Unexpected chapter filename: {path}")
        file_book, chapter = match.group(1), int(match.group(2))
        layout[(path.parent.name, file_book, chapter)] = count_lines(path)
    return layout


def count_lines(path: Path) -> int:
    with path.open(encoding="utf-8") as file:
        return sum(1 for _ in file)


def load_usfm_zip(zip_path: Path, suffix: str) -> dict[str, dict[int, dict[int, str]]]:
    books: dict[str, dict[int, dict[int, str]]] = {}
    with zipfile.ZipFile(zip_path) as archive:
        for _, _, _, usfm_code in BOOKS_66:
            name = find_usfm_member(archive.namelist(), usfm_code, suffix)
            usfm = archive.read(name).decode("utf-8")
            books[usfm_code] = parse_usfm_verses(usfm)
    return books


def load_optional_usfm_books(
    zip_path: Path,
    suffix: str,
    usfm_codes: Iterable[str],
) -> dict[str, dict[int, dict[int, str]]]:
    books: dict[str, dict[int, dict[int, str]]] = {}
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        for usfm_code in usfm_codes:
            name = find_usfm_member(names, usfm_code, suffix, required=False)
            if name is None:
                continue
            usfm = archive.read(name).decode("utf-8")
            books[usfm_code] = parse_usfm_verses(usfm)
    return books


def find_usfm_member(
    names: Iterable[str],
    usfm_code: str,
    suffix: str,
    *,
    required: bool = True,
) -> str | None:
    pattern = re.compile(rf"^\d+-{re.escape(usfm_code)}{re.escape(suffix)}\.usfm$")
    matches = [name for name in names if pattern.match(name)]
    if not matches and not required:
        return None
    if len(matches) != 1:
        raise ValueError(f"Expected one {usfm_code} USFM file, found {matches}")
    return matches[0]


def build_serbian_sources(cache_dir: Path) -> VerseMap:
    sources: VerseMap = {}
    for directory, file_book, slug in SERBIAN_PAGE_BOOKS:
        chapters = parse_svetosavlje_numeric_chapters(svetosavlje_page(slug, cache_dir))
        add_page_sources(sources, directory, file_book, chapters)

    add_serbian_esther(sources, svetosavlje_page("sveto-pismo-2/10/", cache_dir))
    add_serbian_baruch(sources, cache_dir)
    add_serbian_psalm_151(sources, svetosavlje_page("psaltir/152/", cache_dir))
    return sources


def add_serbian_baruch(sources: VerseMap, cache_dir: Path) -> None:
    add_page_sources(
        sources,
        "44_Baruch",
        "Baruch",
        parse_svetosavlje_numeric_chapters(
            svetosavlje_page("sveto-pismo-6/2/", cache_dir)
        ),
    )

    letter_path = svetosavlje_page("sveto-pismo-6/1/", cache_dir)
    page = letter_path.read_text(encoding="utf-8")
    heading_match = re.search(
        r'<a\s+name="[^"]+_1"\s*></a><em>(.*?)</em>',
        page,
        flags=re.DOTALL,
    )
    heading = clean_svetosavlje_html(heading_match.group(1)) if heading_match else ""
    letter = parse_svetosavlje_numeric_chapters(letter_path).get(1, {})
    sources[("44_Baruch", "Baruch", 6)] = {
        1: heading,
        **{verse + 1: text for verse, text in letter.items()},
    }


def add_serbian_psalm_151(sources: VerseMap, path: Path) -> None:
    page = path.read_text(encoding="utf-8")
    ordered_list = re.search(r"<ol>(.*?)</ol>", page, flags=re.DOTALL)
    if ordered_list is None:
        return

    verses: dict[int, str] = {}
    for index, match in enumerate(
        re.finditer(r"<li>(.*?)</li>", ordered_list.group(1), flags=re.DOTALL),
        start=1,
    ):
        verses[index] = clean_svetosavlje_html(match.group(1))
    sources[("19_Psalm", "Psalm", 151)] = verses


def add_serbian_esther(sources: VerseMap, path: Path) -> None:
    marked = parse_svetosavlje_marked_verses(path)
    chapters: dict[int, dict[int, str]] = {}
    for (chapter, marker), text in marked.items():
        if marker.isdigit():
            chapters.setdefault(chapter, {})[int(marker)] = text

    chapter_1_preface = extract_esther_chapter_1_preface(path)
    if chapter_1_preface:
        chapters.setdefault(1, {})[1] = join_verses(
            chapter_1_preface,
            chapters.get(1, {}).get(1, ""),
        )

    chapter_3_addition = split_lettered_text(marked.get((3, "13a"), ""), 13)
    if chapter_3_addition:
        chapters.setdefault(3, {})[13] = join_verses(
            chapters.get(3, {}).get(13, ""),
            join_verses(chapter_3_addition),
        )

    chapter_4_addition = split_serbian_esther_4_addition(
        marked.get((4, "17a"), "")
    )
    chapters.setdefault(4, {}).update(chapter_4_addition)

    chapter_8 = chapters.setdefault(8, {})
    canonical_8_12, addition_8_12 = split_inline_marker(
        chapter_8.get(12, ""),
        "12а.",
    )
    if addition_8_12:
        chapter_8[12] = canonical_8_12
        chapter_8[13] = join_verses(chapter_8.get(13, ""), addition_8_12)

    chapter_10 = chapters.setdefault(10, {})
    canonical_10_3, addition_10_3 = split_inline_marker(
        chapter_10.get(3, ""),
        "3а.",
    )
    if addition_10_3:
        chapter_10[3] = canonical_10_3
        for line, text in split_lettered_text(addition_10_3, 3).items():
            chapter_10[line + 3] = text

    remove_esther_inline_markers(chapters)
    add_page_sources(sources, "17_Esther", "Esther", chapters)


def extract_esther_chapter_1_preface(path: Path) -> str:
    page = path.read_text(encoding="utf-8")
    match = re.search(
        r"<p>(I\.[^<]*?<a\s+href=\"#_ftn1\".*?</a>)</p>\s*<p><a\s+name=\"jest_1_1\"",
        page,
        flags=re.DOTALL,
    )
    if match is None:
        match = re.search(
            r"<p>(I\..*?)</p>\s*<p><a\s+name=\"jest_1_1\"",
            page,
            flags=re.DOTALL,
        )
    return clean_svetosavlje_html(match.group(1)) if match else ""


def split_inline_marker(text: str, marker: str) -> tuple[str, str]:
    index = text.find(marker)
    if index == -1:
        return text, ""
    return clean_spacing(text[:index]), clean_spacing(text[index:])


def remove_esther_inline_markers(chapters: dict[int, dict[int, str]]) -> None:
    for verses in chapters.values():
        for verse, text in list(verses.items()):
            text = re.sub(
                r"(?<!\w)\d+[а-яђћљњџј]+\.\s*(?:[–-]\s*)?",
                "",
                text,
                flags=re.IGNORECASE,
            )
            text = re.sub(
                r"(?<!\w)[IVXLCDM]+\.[а-яђћљњџј]\.\s*(?:[–-]\s*)?",
                "",
                text,
                flags=re.IGNORECASE,
            )
            verses[verse] = clean_spacing(text)


def split_lettered_text(text: str, verse: int) -> dict[int, str]:
    marker_pattern = re.compile(rf"(?<!\w){verse}[а-яђћљњџј]+\.\s*", re.IGNORECASE)
    matches = list(marker_pattern.finditer(text))
    if not matches:
        stripped = clean_spacing(text).strip(" -–")
        return {1: stripped} if stripped else {}

    parts: dict[int, str] = {}
    offset = 0
    preamble = clean_spacing(text[: matches[0].start()]).strip(" -–")
    if preamble:
        parts[1] = preamble
        offset = 1

    for index, match in enumerate(matches, start=1 + offset):
        next_match_index = index - offset
        end = (
            matches[next_match_index].start()
            if next_match_index < len(matches)
            else len(text)
        )
        parts[index] = clean_spacing(text[match.end() : end]).strip(" -–")
    return parts


def split_serbian_esther_4_addition(text: str) -> dict[int, str]:
    parts = split_lettered_text(text, 17)
    if not parts:
        return {}

    lines: dict[int, str] = {
        18: parts.get(1, ""),
        19: parts.get(2, ""),
        24: parts.get(5, ""),
        25: parts.get(6, ""),
        26: parts.get(7, ""),
        27: parts.get(8, ""),
        28: parts.get(9, ""),
        33: parts.get(12, ""),
        38: parts.get(15, ""),
        39: parts.get(16, ""),
        40: parts.get(17, ""),
        41: parts.get(18, ""),
        42: parts.get(19, ""),
        43: parts.get(20, ""),
        44: parts.get(21, ""),
        45: parts.get(22, ""),
        46: parts.get(23, ""),
        47: parts.get(24, ""),
    }

    line_20, line_21 = split_inline_marker(parts.get(3, ""), "и Господар си свега")
    lines[20] = line_20
    lines[21] = line_21

    line_22, line_23 = split_inline_marker(parts.get(4, ""), "јер бих био")
    lines[22] = line_22
    lines[23] = line_23

    line_29, rest = split_inline_marker(parts.get(10, ""), "и скинувши")
    line_30, line_31_intro = split_inline_marker(rest, "и мољаше се")
    line_31_prayer, line_32 = split_inline_marker(parts.get(11, ""), "јер је")
    lines[29] = line_29
    lines[30] = line_30
    lines[31] = join_verses(line_31_intro, line_31_prayer)
    lines[32] = line_32

    line_34, line_35 = split_inline_marker(parts.get(13, ""), "зато што")
    lines[34] = line_34
    lines[35] = line_35

    line_36, line_37 = split_inline_marker(parts.get(14, ""), "да би истргли")
    lines[36] = line_36
    lines[37] = line_37

    return {line: text for line, text in lines.items() if text}


def direct_usfm_sources(usfm_books: dict[str, dict[int, dict[int, str]]]) -> VerseMap:
    sources: VerseMap = {}
    for directory, file_book, _, usfm_code in BOOKS_66:
        for chapter, verses in usfm_books[usfm_code].items():
            sources[(directory, file_book, chapter)] = dict(verses)
    return sources


def add_usfm_sources_for_books(
    sources: VerseMap,
    usfm_books: dict[str, dict[int, dict[int, str]]],
    books: Iterable[tuple[str, str, str]],
    *,
    code_overrides: dict[str, str] | None = None,
) -> None:
    overrides = code_overrides or {}
    for directory, file_book, usfm_code in books:
        source_code = overrides.get(usfm_code, usfm_code)
        if source_code not in usfm_books:
            continue
        for chapter, verses in usfm_books[source_code].items():
            sources[(directory, file_book, chapter)] = dict(verses)


def build_ebible_usfm_sources(zip_path: Path, suffix: str) -> VerseMap:
    sources = direct_usfm_sources(load_usfm_zip(zip_path, suffix))
    optional_books = load_optional_usfm_books(
        zip_path,
        suffix,
        [
            *(code for _, _, code in USFM_DEUTEROCANON),
            "DAG",
            "ESG",
            "LJE",
            "PS2",
        ],
    )
    add_usfm_sources_for_books(sources, optional_books, USFM_DEUTEROCANON)

    if "ESG" in optional_books:
        add_usfm_sources_for_books(
            sources,
            optional_books,
            [("17_Esther", "Esther", "ESG")],
        )

    if "DAG" in optional_books:
        add_usfm_sources_for_books(
            sources,
            optional_books,
            [("27_Daniel", "Daniel", "DAG")],
        )

    if "LJE" in optional_books:
        sources[("44_Baruch", "Baruch", 6)] = dict(
            optional_books["LJE"].get(1, {})
        )

    psalm_151 = optional_books.get("PS2", {}).get(1)
    if psalm_151:
        sources[("19_Psalm", "Psalm", 151)] = dict(psalm_151)

    return sources


def build_greek_sources(lxx_zip_path: Path, nt_zip_path: Path) -> VerseMap:
    sources: VerseMap = {}
    lxx_books = load_optional_usfm_books(
        lxx_zip_path,
        "grclxx",
        [
            *(code for _, _, _, code in BOOKS_66[:39]),
            *(code for _, _, code in USFM_DEUTEROCANON if code != "2ES"),
            "DAG",
            "ESG",
            "LJE",
            "PSA",
            "2ES",
        ],
    )
    add_usfm_sources_for_books(
        sources,
        lxx_books,
        [
            (directory, file_book, usfm_code)
            for directory, file_book, _, usfm_code in BOOKS_66[:39]
        ],
        code_overrides={"EZR": "2ES"},
    )
    add_usfm_sources_for_books(
        sources,
        lxx_books,
        [
            (directory, file_book, code)
            for directory, file_book, code in USFM_DEUTEROCANON
            if code != "2ES"
        ],
    )

    if "ESG" in lxx_books:
        add_usfm_sources_for_books(
            sources,
            lxx_books,
            [("17_Esther", "Esther", "ESG")],
        )
    if "DAG" in lxx_books:
        add_usfm_sources_for_books(
            sources,
            lxx_books,
            [("27_Daniel", "Daniel", "DAG")],
        )
    if "LJE" in lxx_books:
        sources[("44_Baruch", "Baruch", 6)] = dict(lxx_books["LJE"].get(1, {}))

    psalm_151 = lxx_books.get("PSA", {}).get(151)
    if psalm_151:
        sources[("19_Psalm", "Psalm", 151)] = dict(psalm_151)

    nt_books = load_optional_usfm_books(
        nt_zip_path,
        "grcbyz",
        [usfm_code for _, _, _, usfm_code in BOOKS_66[39:]],
    )
    add_usfm_sources_for_books(
        sources,
        nt_books,
        [
            (directory, file_book, usfm_code)
            for directory, file_book, _, usfm_code in BOOKS_66[39:]
        ],
    )
    return sources


def remap_daniel_3(
    sources: VerseMap,
    usfm_code_or_osis: str,
    *,
    song: dict[int, str] | None = None,
) -> None:
    chapter_key = ("27_Daniel", "Daniel", 3)
    canonical = sources.get(chapter_key, {})
    remapped: dict[int, str] = {}

    for verse in range(1, 24):
        if verse in canonical:
            remapped[verse] = canonical[verse]

    if song:
        for verse in range(1, 64):
            if verse in song:
                remapped[verse + 24] = song[verse]

    for verse in range(24, 31):
        if verse in canonical:
            remapped[verse + 67] = canonical[verse]

    sources[chapter_key] = remapped


def build_german_sources(osis_path: Path) -> VerseMap:
    osis_books = parse_osis_verses(osis_path)
    sources = direct_osis_sources(osis_books)
    remap_daniel_3(sources, "Dan", song=osis_books.get("AddDan", {}).get(3))
    add_german_daniel_additions(sources, osis_books)
    add_german_esther_additions(sources, osis_books)
    return sources


def build_bulgarian_sources(osis_path: Path) -> VerseMap:
    return direct_osis_sources(
        parse_osis_verses(osis_path),
        include_deuterocanon=False,
    )


def parse_osis_verses(path: Path) -> dict[str, dict[int, dict[int, str]]]:
    namespace = {"osis": "http://www.bibletechnologies.net/2003/OSIS/namespace"}
    root = ElementTree.parse(path).getroot()
    books: dict[str, dict[int, dict[int, str]]] = {}

    for book in root.findall(".//osis:div[@type='book']", namespace):
        book_id = book.attrib["osisID"]
        chapters: dict[int, dict[int, str]] = {}
        for chapter in book.findall("osis:chapter", namespace):
            chapter_id = int(chapter.attrib["osisID"].split(".")[-1])
            verses: dict[int, str] = {}
            for verse in chapter.findall("osis:verse", namespace):
                verse_id = int(verse.attrib["osisID"].split(".")[-1])
                verses[verse_id] = clean_spacing(osis_text(verse))
            chapters[chapter_id] = verses
        books[book_id] = chapters

    return books


def osis_text(node: ElementTree.Element) -> str:
    pieces: list[str] = []
    if node.text:
        pieces.append(node.text)

    for child in node:
        if child.tag.rsplit("}", 1)[-1] != "note":
            pieces.append(osis_text(child))
        if child.tail:
            pieces.append(child.tail)

    return normalize_ascii("".join(pieces)).replace(">", "")


def direct_osis_sources(
    osis_books: dict[str, dict[int, dict[int, str]]],
    *,
    include_deuterocanon: bool = True,
) -> VerseMap:
    sources: VerseMap = {}
    for directory, file_book, osis_id, _ in BOOKS_66:
        for chapter, verses in osis_books[osis_id].items():
            sources[(directory, file_book, chapter)] = dict(verses)

    if include_deuterocanon:
        for directory, file_book, osis_id in DE_DEUTEROCANON:
            if osis_id not in osis_books:
                continue
            for chapter, verses in osis_books[osis_id].items():
                sources[(directory, file_book, chapter)] = dict(verses)

    return sources


def add_german_daniel_additions(
    sources: VerseMap,
    osis_books: dict[str, dict[int, dict[int, str]]],
) -> None:
    add_daniel = osis_books.get("AddDan", {})
    if 1 in add_daniel:
        sources[("27_Daniel", "Daniel", 13)] = dict(add_daniel[1])
    if 2 in add_daniel:
        sources[("27_Daniel", "Daniel", 14)] = dict(add_daniel[2])


def add_german_esther_additions(
    sources: VerseMap,
    osis_books: dict[str, dict[int, dict[int, str]]],
) -> None:
    additions = osis_books.get("AddEsth", {})
    if not additions:
        return

    esther_1 = dict(sources.get(("17_Esther", "Esther", 1), {}))
    esther_1[1] = join_verses(additions.get(6, {}), esther_1.get(1, ""))
    sources[("17_Esther", "Esther", 1)] = esther_1

    esther_3 = dict(sources.get(("17_Esther", "Esther", 3), {}))
    esther_3[13] = join_verses({0: esther_3.get(13, "")}, additions.get(1, {}))
    sources[("17_Esther", "Esther", 3)] = esther_3

    esther_4 = dict(sources.get(("17_Esther", "Esther", 4), {}))
    add_2 = additions.get(2, {})
    if add_2:
        esther_4[18] = add_2.get(1, "")
        for source_verse in range(2, 8):
            esther_4[source_verse + 18] = add_2.get(source_verse, "")
        esther_4[28] = add_2.get(8, "")

    add_3 = additions.get(3, {})
    for source_verse in range(1, 13):
        esther_4[source_verse + 28] = add_3.get(source_verse, "")
    sources[("17_Esther", "Esther", 4)] = esther_4

    esther_5 = dict(sources.get(("17_Esther", "Esther", 5), {}))
    add_4 = additions.get(4, {})
    if add_4:
        esther_5[1] = join_verses({verse: add_4[verse] for verse in range(1, 7)})
        esther_5[2] = join_verses({verse: add_4[verse] for verse in range(7, 13)})
    sources[("17_Esther", "Esther", 5)] = esther_5

    esther_8 = dict(sources.get(("17_Esther", "Esther", 8), {}))
    esther_8[13] = join_verses({0: esther_8.get(13, "")}, additions.get(5, {}))
    sources[("17_Esther", "Esther", 8)] = esther_8

    esther_10 = dict(sources.get(("17_Esther", "Esther", 10), {}))
    add_7 = additions.get(7, {})
    for line, source_verse in {
        4: 1,
        5: 2,
        6: 3,
        7: 4,
        8: 5,
        9: 6,
        13: 7,
        14: 8,
    }.items():
        esther_10[line] = add_7.get(source_verse, "")
    sources[("17_Esther", "Esther", 10)] = esther_10


def join_verses(*verse_maps_or_text: dict[int, str] | str) -> str:
    parts: list[str] = []
    for item in verse_maps_or_text:
        if isinstance(item, str):
            if item:
                parts.append(item)
            continue
        parts.extend(text for _, text in sorted(item.items()) if text)
    return clean_spacing(" ".join(parts))


def write_language(root: Path, language: str, sources: VerseMap) -> None:
    layout = expected_layout(root)
    output_root = root / language
    for (directory, file_book, chapter), expected_count in sorted(layout.items()):
        source = sources.get((directory, file_book, chapter), {})
        lines = [source.get(verse, "") for verse in range(1, expected_count + 1)]
        write_chapter(output_root / directory / f"{file_book}{chapter}.txt", lines)


def write_chapter(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_against_english(root: Path, languages: Iterable[str]) -> list[str]:
    errors: list[str] = []
    layout = expected_layout(root)
    for language in languages:
        for (directory, file_book, chapter), expected_count in layout.items():
            path = root / language / directory / f"{file_book}{chapter}.txt"
            if not path.exists():
                errors.append(f"{language}: missing {path.relative_to(root)}")
                continue
            actual_count = count_lines(path)
            if actual_count != expected_count:
                errors.append(
                    f"{language}: {path.relative_to(root)} has {actual_count} lines, "
                    f"expected {expected_count}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build localized chapter files aligned to en/ verse counts."
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--cache-dir", default="/tmp/bible-verse-source-cache")
    args = parser.parse_args()

    root = Path(args.root)
    cache_dir = Path(args.cache_dir)
    de_osis = download(LUTH1912AP_OSIS_URL, cache_dir / "luth1912ap.xml")
    bg_osis = download(
        OPEN_BIBLES_BULGARIAN_OSIS_URL,
        cache_dir / "bul-bulgarian.osis.xml",
    )
    greek_lxx = download(
        EBIBLE_SCRIPTURES_BASE_URL + "grclxx_usfm.zip",
        cache_dir / "grclxx_usfm.zip",
    )
    greek_nt = download(
        EBIBLE_SCRIPTURES_BASE_URL + "grcbyz_usfm.zip",
        cache_dir / "grcbyz_usfm.zip",
    )

    write_language(root, "sr", build_serbian_sources(cache_dir))
    write_language(root, "de", build_german_sources(de_osis))
    write_language(root, "bg", build_bulgarian_sources(bg_osis))
    write_language(root, "el", build_greek_sources(greek_lxx, greek_nt))

    generated_languages = ["sr", "de", "bg", "el"]
    for language, translation_id in sorted(EBIBLE_USFM_TRANSLATIONS.items()):
        zip_path = download(
            EBIBLE_SCRIPTURES_BASE_URL + f"{translation_id}_usfm.zip",
            cache_dir / f"{translation_id}_usfm.zip",
        )
        write_language(
            root,
            language,
            build_ebible_usfm_sources(zip_path, translation_id),
        )
        generated_languages.append(language)

    errors = validate_against_english(root, generated_languages)
    if errors:
        for error in errors:
            print(error)
        return 1

    layout = expected_layout(root)
    languages = ", ".join(sorted(generated_languages))
    print(f"Wrote {len(layout)} chapter files for each language: {languages}.")
    print("All generated chapter line counts match en.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
