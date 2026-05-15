import unittest

from scripts.accurate_verse_split import (
    extract_biblegateway_verses,
    parse_usfm_verses,
)


class AccurateVerseSplitTest(unittest.TestCase):
    def test_extract_biblegateway_verses_ignores_headings_and_notes(self) -> None:
        html = """
        <div class="passage-content">
          <h3><span class="text Gen-14-1">Lot's Captivity</span></h3>
          <p>
            <span class="text Gen-14-1">
              <span class="chapternum">14&nbsp;</span>And it came to pass
              <sup class="crossreference">(A)</sup>in the days,
            </span>
            <span id="en-NKJV-339" class="text Gen-14-2">
              <sup class="versenum">2&nbsp;</sup><i>that</i> they made war.
            </span>
          </p>
          <div class="poetry">
            <span class="text Gen-14-3">
              <sup class="versenum">3&nbsp;</sup>Blessed be Abram,
            </span><br />
            <span class="text Gen-14-3">Possessor of heaven and earth;</span>
          </div>
        </div>
        """

        self.assertEqual(
            extract_biblegateway_verses(html, "Gen", 14),
            [
                "And it came to pass in the days,",
                "that they made war.",
                "Blessed be Abram, Possessor of heaven and earth;",
            ],
        )

    def test_parse_usfm_verses_removes_notes_and_keeps_continuations(self) -> None:
        usfm = r"""
        \id TOB
        \c 1
        \p
        \v 1 The book of the words of Tobit\f + \fr 1:1 \ft Note text.\f*;
        \v 2 who in the days of Enemessar
        \q1 continued in poetry.
        \p Extra paragraph in the same verse.
        \c 2
        \p
        \v 1 Now when I had come home again.
        """

        self.assertEqual(
            parse_usfm_verses(usfm),
            {
                1: {
                    1: "The book of the words of Tobit;",
                    2: "who in the days of Enemessar continued in poetry. Extra paragraph in the same verse.",
                },
                2: {
                    1: "Now when I had come home again.",
                },
            },
        )

    def test_parse_usfm_verse_bridges_keep_each_verse_number(self) -> None:
        usfm = r"""
        \id SIR
        \c 1
        \v 14 Previous verse.
        \v 15-16 \f + \fr 1:15-16 \ft Omitted in the source text.\f*
        \v 17 Next verse.
        \c 2
        \v 28-29 Combined bridge text.
        """

        self.assertEqual(
            parse_usfm_verses(usfm),
            {
                1: {
                    14: "Previous verse.",
                    15: "",
                    16: "",
                    17: "Next verse.",
                },
                2: {
                    28: "Combined bridge text.",
                    29: "",
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
