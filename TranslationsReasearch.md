# Bible Translation Research

Updated: 2026-05-17

## Short Answer

For Serbian, the safest Orthodox-first choice is the Serbian Synodal/SPC line:

- Old Testament protocanonical books: Djura Danicic.
- Old Testament deuterocanonical books: Metropolitan Amfilohije Radovic and Bishop Atanasije Jevtic in the full Holy Synod edition.
- New Testament: Commission of the Holy Synod of Bishops of the Serbian Orthodox Church.

For German, I did not find a single complete, pan-Orthodox German Bible translation equivalent to the Serbian Synodal edition. The best answer is split by use:

- Orthodox school/church education: Orthodoxe Schulbibel, published for the Orthodox School Office in Austria with the Austrian Bible Society.
- Orthodox New Testament/Psalter/Odes: the newer Orthodox-oriented Edition Hagia Sophia / St. Justin edition based on the Greek Patriarchal text of Constantinople.
- Orthodox Old Testament reference: Septuaginta Deutsch, because Orthodoxy receives the Old Testament through the Septuagint tradition, but this is an academic translation and not necessarily ideal for liturgical reading.
- Practical parish fallback: Lutherbibel is sometimes used in German-speaking Orthodox parishes, especially Russian Orthodox contexts, because it is familiar and stylistically strong, but it is not an Orthodox translation.

I would not treat Schlachter as the German Orthodox standard. It is a Protestant/Swiss evangelical translation tradition, and the Austrian Bible Society describes it as an Old Testament without late writings/deuterocanonical books. That is a poor fit for an Orthodox Bible baseline.

## Serbian Findings

The Serbian Orthodox Church's Synodal New Testament has strong authority. Radomir Rakic's article on the Synodal translation says the Holy Synod approved the translation in 1984 as a Church-authorized translation, and later explains that the Holy Assembly of Bishops promulgated it as an authentic translation usable in church services and liturgical rites.

The full Serbian Holy Synod Bible is more complete than the older Danicic-Karadzic pairing because it includes the deuterocanonical books. The Serbian Patriarchate shop lists a Synodal Bible issued by the Holy Synod of Bishops of the Serbian Orthodox Church, with Danicic for the Old Testament, Amfilohije/Atanasije for the deuterocanonical books, and the Holy Synod Commission for the New Testament. Svetosavlje lists the same structure for the 2014 printed edition.

The older Danicic-Karadzic Bible remains historically important and still circulates. Rakic notes that the older Danicic Old Testament plus Vuk Karadzic New Testament combination had long been published together, and that some people and communities still prefer Vuk's New Testament for its language. For this project, though, the Synodal/SPC edition is the better Orthodox recommendation because it includes the Synodal New Testament and the wider Orthodox canon.

## German Findings

German-speaking Orthodoxy does not appear to have one universally received complete Bible translation.

The Orthodox School Office in Austria describes the Orthodoxe Schulbibel as the first Orthodox school Bible in the whole German-speaking area. It includes the four Gospels, Acts, and selected Psalms, and its biblical text was revised according to the Byzantine text. The Orthodox School Office's history page adds that it was published in 2015 for Orthodox religious instruction and that the text started from existing translations and was revised according to the Byzantine text.

For the New Testament and Psalter, Edition Hagia Sophia lists an Orthodox German edition containing the complete New Testament, Orthodox Psalter, Psalm 151, and the nine biblical Odes. The publisher says its basis is the Greek Patriarchal text of Constantinople used in the Orthodox Church's worship, with translation work by S'chi-Archimandrit Justin Rauer and collaborators.

For the Old Testament, Septuaginta Deutsch is relevant because it is the first complete German translation of the Septuagint. The German Bible Society says it is a philological, readable translation of the Greek text. Its shop page says it made the Old Testament available to Orthodox communities in the German-speaking area in a common language. This makes it useful for study/reference, but a Russian Orthodox parish article from Dresden says its closeness to the source syntax makes it less suitable for liturgy.

Lutherbibel has some practical Orthodox use, but it should be treated as a fallback/common-language option, not as an Orthodox translation. The Dresden Russian Orthodox parish article says German-speaking Russian Orthodox communities often use common German translations for Scripture readings and that this is not rarely Lutherbibel. The same article also flags Orthodox concerns: Luther's Old Testament starts from the Masoretic text and lacks the Orthodox Septuagint baseline.

Schlachter does not look like the right Orthodox answer. The Austrian Bible Society describes Schlachter as a translation by Swiss preacher Franz Eugen Schlachter; it uses Hebrew/Greek source-text traditions and contains the Old Testament without late writings/deuterocanonical books. That canon profile is the main reason not to choose it as an Orthodox default.

## Recommendation For This Project

Use these labels internally:

- Serbian: `Serbian Synodal / Holy Synod SPC`.
- German NT/Psalms: `Orthodox German / Byzantine-Patriarchal text` if licensing permits.
- German OT/reference: `Septuaginta Deutsch` if licensing permits and the UI clearly labels it as a Septuagint-based German reference text.

Do not label Schlachter as Orthodox. If a German full Bible is needed before licensing a clearly Orthodox source, use a clear fallback label such as `German reader fallback` and document which source text is being used.

## Sources

- Serbian Synodal NT article by Radomir Rakic: https://hrcak.srce.hr/file/250912
- Serbian Patriarchate shop listing for Synodal Bible: https://patrijarsija.websites.rs/e-prodavnica/knjige/sveto-pismo/biblija-sinodska-luksuzno-izdanje/
- Svetosavlje listing for Serbian Holy Scripture editions: https://svetosavlje.org/sveto-pismo-index/
- Orthodoxe Schulbibel, Austrian Bible Society: https://shop.bibelgesellschaft.at/site/shopadministration/orthodoxe-schulbibel
- Orthodox School Office Austria presentation/history: https://www.orthodoxekirche.at/?p=59 and https://www.orthodoxekirche.at/?page_id=152
- Edition Hagia Sophia Orthodox NT/Psalter/Odes: https://www.edition-hagia-sophia.de/p/das-neue-testament-die-psalmen-und-die-biblischen-oden-der-orthodoxie
- Septuaginta Deutsch, German Bible Society: https://www.die-bibel.de/en/home/scholarly-editions/septuagint/septuaginta-deutsch/
- Septuaginta Deutsch shop page: https://shop.die-bibel.de/Septuaginta-Deutsch-3.-Auflage/5189
- Russian Orthodox parish Dresden on Luther translation: https://orthodox-dresden.de/stsimeon/de/kirche/publikationen/zur-bedeutung-der-luther-uebersetzung-der-heiligen-schrift-in-der-orthodoxen-kirche
- Schlachter Bible, Austrian Bible Society: https://www.bibelgesellschaft.at/schlachter-bibel

## Concrete Local Source Plan

For the Serbian Bible I will use these sources:

- Old Testament protocanonical books: Djura Danicic.
- Old Testament deuterocanonical books: Metropolitan Amfilohije Radovic and Bishop Atanasije Jevtic, following the full Serbian Holy Synod/SPC edition.
- New Testament: Commission of the Holy Synod of Bishops of the Serbian Orthodox Church.
- Label in the project: `Serbian Synodal / Holy Synod SPC`.

For the German Bible I will use these sources:

- Base complete German Bible: Einheitsuebersetzung 2016 for the 73-book Catholic core, including the Catholic deuterocanonical books.
- Orthodox additions: Septuaginta Deutsch for the Septuagint-based Orthodox additions and reference material, especially 1 Esdras, Prayer of Manasseh, Psalm 151, 3 Maccabees, and 4 Maccabees where kept by the project canon.
- Broader appendix material: a German 4 Ezra / 2 Esdras source from the Vulgate-apocrypha tradition, such as Hermann Gunkel's German 4 Esra translation, if the current project canon keeps 2 Esdras.
- Label in the project: `German Catholic core + Orthodox Septuagint additions`.
