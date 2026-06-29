#!/usr/bin/env python3
# Generates path-based language variants (/, /de/, /ku/) with hreflang from the
# existing trilingual source files. Run from the repo root.
import os
from html.parser import HTMLParser

ROOT = os.getcwd()
BASE = "https://www.glalbacho.de"
IMG = BASE + "/images/new_portrait.jpg"
LASTMOD = "2026-06-29"
LANGS = ["en", "de", "ku"]
VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}

# ---------------------------------------------------------------- language filter
class LangFilter(HTMLParser):
    """Keep only elements of the target language; drop the other languages and comments."""
    def __init__(self, target):
        super().__init__(convert_charrefs=False)
        self.target = target
        self.out = []
        self.skip = 0
    def _lang(self, attrs):
        for k, v in attrs:
            if k == "class" and v:
                for c in v.split():
                    if c in ("lang-en", "lang-de", "lang-ku"):
                        return c[5:]
        return None
    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag not in VOID:
                self.skip += 1
            return
        lang = self._lang(attrs)
        if lang is not None and lang != self.target:
            if tag not in VOID:
                self.skip = 1
            return
        self.out.append(self.get_starttag_text())
    def handle_startendtag(self, tag, attrs):
        if self.skip:
            return
        lang = self._lang(attrs)
        if lang is not None and lang != self.target:
            return
        self.out.append(self.get_starttag_text())
    def handle_endtag(self, tag):
        if self.skip:
            if tag not in VOID:
                self.skip -= 1
            return
        self.out.append("</%s>" % tag)
    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)
    def handle_entityref(self, name):
        if not self.skip:
            self.out.append("&%s;" % name)
    def handle_charref(self, name):
        if not self.skip:
            self.out.append("&#%s;" % name)
    def handle_comment(self, data):
        pass
    def result(self):
        return "".join(self.out)

def filter_lang(html, target):
    p = LangFilter(target)
    p.feed(html)
    p.close()
    return p.result().strip("\n")

# ---------------------------------------------------------------- url helpers
PAGE_SEG = {"home": "", "research": "research/", "cv": "cv/", "impressum": "impressum/"}

def path(lang, page):
    seg = "" if lang == "en" else lang + "/"
    return "/" + seg + PAGE_SEG[page]

def absurl(lang, page):
    return BASE + path(lang, page)

def outfile(lang, page):
    seg = "" if lang == "en" else lang + "/"
    return os.path.join(ROOT, seg + PAGE_SEG[page] + "index.html")

# ---------------------------------------------------------------- strings
NAV = {
    "home":     {"en": "Home", "de": "Startseite", "ku": "Destpêk"},
    "research": {"en": "Research", "de": "Forschung", "ku": "Lêkolîn"},
    "cv":       {"en": "CV", "de": "Lebenslauf", "ku": "CV"},
}
THEME_LIGHT = {"en": "Light mode", "de": "Heller Modus", "ku": "Moda ronî"}
THEME_DARK  = {"en": "Dark mode", "de": "Dunkler Modus", "ku": "Moda tarî"}
THEME_ARIA  = {"en": "Theme", "de": "Farbschema", "ku": "Tema"}
LANG_LABEL  = {"en": "Language", "de": "Sprache", "ku": "Ziman"}
LANG_CODE   = {"en": "EN", "de": "DE", "ku": "KU"}
LANG_ENDONYM = {"en": "English", "de": "Deutsch", "ku": "Kurmancî"}
BACK_HOME   = {"en": "Back to home", "de": "Zur&uuml;ck zur Startseite", "ku": "Vegere destpêkê"}
OG_LOCALE   = {"en": "en_US", "de": "de_DE", "ku": "ku"}

TITLE = {
    "home": {
        "en": "Glal Bacho — PhD Student in Mathematics, RWTH Aachen",
        "de": "Glal Bacho — Doktorand der Mathematik, RWTH Aachen",
        "ku": "Glal Bacho — Xwendekarê doktorayê di matematîkê de, RWTH Aachen",
    },
    "research": {
        "en": "Research · Glal Bacho",
        "de": "Forschung · Glal Bacho",
        "ku": "Lêkolîn · Glal Bacho",
    },
    "cv": {
        "en": "CV · Glal Bacho",
        "de": "Lebenslauf · Glal Bacho",
        "ku": "CV · Glal Bacho",
    },
    "impressum": {
        "en": "Impressum · Glal Bacho",
        "de": "Impressum · Glal Bacho",
        "ku": "Impressum · Glal Bacho",
    },
}
DESC = {
    "home": {
        "en": "Glal Bacho, PhD student in mathematics at the Chair of Applied Analysis, RWTH Aachen. Research on nonlinear PDEs, calculus of variations, and topological solitons — bimerons and Hopfions.",
        "de": "Glal Bacho, Doktorand der Mathematik am Lehrstuhl für Angewandte Analysis, RWTH Aachen. Forschung zu nichtlinearen PDEs, Variationsrechnung und topologischen Solitonen — Bimeronen und Hopfionen.",
        "ku": "Glal Bacho, xwendekarê doktorayê di matematîkê de li Kursiya Analîza Sepandî, RWTH Aachen. Lêkolîn li ser PDE-yên ne-xetî, hesabê varyasyonan û solîtonên topolojîk — bimerons û Hopfions.",
    },
    "research": {
        "en": "Research of Glal Bacho on topological solitons — variational and blow-up methods for the existence, concentration, and asymptotics of bimerons and Hopfions.",
        "de": "Forschung von Glal Bacho zu topologischen Solitonen — Variations- und Blow-up-Methoden für Existenz, Konzentration und Asymptotik von Bimeronen und Hopfionen.",
        "ku": "Lêkolîna Glal Bacho li ser solîtonên topolojîk — rêbazên varyasyonel û blow-upê ji bo hebûn, komkirin û asîmptotîka bimerons û Hopfions.",
    },
    "cv": {
        "en": "Curriculum vitae of Glal Bacho — education and teaching experience in mathematics at RWTH Aachen University.",
        "de": "Lebenslauf von Glal Bacho — Ausbildung und Lehrerfahrung in Mathematik an der RWTH Aachen.",
        "ku": "CV ya Glal Bacho — perwerde û tecrûbeya dersdayînê di matematîkê de li RWTH Aachen.",
    },
    "impressum": {
        "en": "Legal notice (Impressum) for the website of Glal Bacho.",
        "de": "Impressum und Anbieterkennzeichnung der Website von Glal Bacho.",
        "ku": "Agahdariya qanûnî (Impressum) ji bo malpera Glal Bacho.",
    },
}
OG_TYPE = {"home": "profile", "cv": "profile", "research": "website", "impressum": "website"}
END_SCRIPTS = {
    "home": ["/js/hero-slideshow.js"],
    "research": ["/js/collapse.js", "/js/bb-halves.js", "/js/hero-slideshow.js"],
    "cv": ["/js/collapse.js"],
    "impressum": ["/js/collapse.js"],
}

def jsonld(lang):
    u = absurl(lang, "home")
    return (
        '  <script type="application/ld+json">\n'
        '  {\n'
        '    "@context": "https://schema.org",\n'
        '    "@type": "Person",\n'
        '    "name": "Glal Bacho",\n'
        '    "url": "%s",\n'
        '    "image": "%s",\n'
        '    "jobTitle": "PhD Student in Mathematics",\n'
        '    "affiliation": {\n'
        '      "@type": "Organization",\n'
        '      "name": "RWTH Aachen University",\n'
        '      "department": "Chair of Applied Analysis"\n'
        '    },\n'
        '    "knowsAbout": ["Nonlinear PDEs", "Calculus of Variations", "Topological Solitons", "Bimerons", "Hopfions"],\n'
        '    "sameAs": [\n'
        '      "https://orcid.org/0009-0001-9664-8412",\n'
        '      "https://www.linkedin.com/in/glal-bacho-8557bb41a/",\n'
        '      "https://www.math1.rwth-aachen.de/cms/math1/der-lehrstuhl/team/wissenschaftlich-beschaeftigte/~jwpak/glal-bacho/?allou=1"\n'
        '    ]\n'
        '  }\n'
        '  </script>\n'
    ) % (u, IMG)

# ---------------------------------------------------------------- builders
def build_head(lang, page):
    L = []
    L.append("<!DOCTYPE html>")
    L.append('<html lang="%s">' % lang)
    L.append("<head>")
    L.append('  <meta charset="UTF-8">')
    L.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    L.append("  <title>%s</title>" % TITLE[page][lang])
    L.append('  <meta name="description" content="%s">' % DESC[page][lang])
    if page == "impressum":
        L.append('  <meta name="robots" content="noindex, follow">')
    L.append('  <link rel="canonical" href="%s">' % absurl(lang, page))
    for hl in LANGS:
        L.append('  <link rel="alternate" hreflang="%s" href="%s">' % (hl, absurl(hl, page)))
    L.append('  <link rel="alternate" hreflang="x-default" href="%s">' % absurl("en", page))
    L.append('  <meta property="og:type" content="%s">' % OG_TYPE[page])
    L.append('  <meta property="og:title" content="%s">' % TITLE[page][lang])
    L.append('  <meta property="og:description" content="%s">' % DESC[page][lang])
    L.append('  <meta property="og:url" content="%s">' % absurl(lang, page))
    L.append('  <meta property="og:image" content="%s">' % IMG)
    L.append('  <meta property="og:image:alt" content="Portrait of Glal Bacho">')
    L.append('  <meta property="og:locale" content="%s">' % OG_LOCALE[lang])
    L.append('  <meta name="twitter:card" content="summary">')
    L.append('  <meta name="twitter:title" content="%s">' % TITLE[page][lang])
    L.append('  <meta name="twitter:description" content="%s">' % DESC[page][lang])
    L.append('  <meta name="twitter:image" content="%s">' % IMG)
    head = "\n".join(L) + "\n"
    if page == "home":
        head += jsonld(lang)
    head += (
        '  <link rel="stylesheet" href="/css/style.css">\n'
        '  <link rel="icon" type="image/png" href="/favicon.png">\n'
        '  <link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '  <script src="/js/theme.js"></script>\n'
        "</head>"
    )
    return head

def nav_link(lang, page, current):
    cur = ' aria-current="page"' if page == current else ""
    return '      <a href="%s"%s>%s</a>' % (path(lang, page), cur, NAV[page][lang])

def build_nav(lang, page):
    opts = []
    for o in LANGS:
        active = " active" if o == lang else ""
        cur = ' aria-current="true"' if o == lang else ""
        opts.append(
            '            <a class="lang-option%s" role="menuitem" href="%s" hreflang="%s"%s>%s</a>'
            % (active, path(o, page), o, cur, LANG_ENDONYM[o])
        )
    return "\n".join([
        "    <nav>",
        nav_link(lang, "home", page),
        nav_link(lang, "research", page),
        nav_link(lang, "cv", page),
        '      <div class="nav-actions">',
        '        <button id="theme-toggle" class="toolbar-btn" type="button" aria-label="%s" data-label-light="%s" data-label-dark="%s">'
            % (THEME_ARIA[lang], THEME_LIGHT[lang], THEME_DARK[lang]),
        '          <span class="btn-icon" aria-hidden="true"></span>',
        '          <span class="btn-text">%s</span>' % THEME_LIGHT[lang],
        "        </button>",
        '        <div class="lang-menu">',
        '          <button id="lang-toggle" class="toolbar-btn" type="button" aria-haspopup="true" aria-expanded="false">',
        '            <span class="btn-icon" aria-hidden="true">%s</span>' % LANG_CODE[lang],
        '            <span class="btn-text">%s</span>' % LANG_LABEL[lang],
        "          </button>",
        '          <div class="lang-dropdown" role="menu">',
        "\n".join(opts),
        "          </div>",
        "        </div>",
        "      </div>",
        "    </nav>",
    ])

def build_footer(lang, page):
    if page == "impressum":
        inner = '<a href="%s">%s</a>' % (path(lang, "home"), BACK_HOME[lang])
    else:
        inner = '<a href="%s">Impressum</a>' % path(lang, "impressum")
    return "    <footer>\n      <p>\n        %s\n      </p>\n    </footer>" % inner

def build_scripts(page):
    return "\n".join('  <script src="%s"></script>' % s for s in END_SCRIPTS[page])

def build_page(lang, page, content):
    parts = [
        build_head(lang, page),
        "<body>",
        '  <main class="page">',
        build_nav(lang, page),
        "",
        content,
        "",
        build_footer(lang, page),
        "  </main>",
        build_scripts(page),
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(parts)

# ---------------------------------------------------------------- main
# Single source of truth: trilingual page bodies live under src/.
# Edit these, then run this script to regenerate /, /de/ and /ku/.
SOURCES = {
    "home": "src/index.html",
    "research": "src/research.html",
    "cv": "src/cv.html",
    "impressum": "src/impressum.html",
}

# Read content slices first (before we overwrite anything).
content_raw = {}
for page, src in SOURCES.items():
    html = open(os.path.join(ROOT, src), encoding="utf-8").read()
    i = html.index("</nav>") + len("</nav>")
    j = html.index("<footer")
    content_raw[page] = html[i:j]

written = []
for page in SOURCES:
    for lang in LANGS:
        content = filter_lang(content_raw[page], lang)
        out = build_page(lang, page, content)
        dest = outfile(lang, page)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(out)
        written.append(os.path.relpath(dest, ROOT))

# ---------------------------------------------------------------- sitemap
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
PRIORITY = {"home": "1.0", "research": "0.8", "cv": "0.6"}
for page in ["home", "research", "cv"]:  # impressum is noindex -> excluded
    for lang in LANGS:
        sm.append("  <url>")
        sm.append("    <loc>%s</loc>" % absurl(lang, page))
        for hl in LANGS:
            sm.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (hl, absurl(hl, page)))
        sm.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % absurl("en", page))
        sm.append("    <lastmod>%s</lastmod>" % LASTMOD)
        sm.append("    <priority>%s</priority>" % PRIORITY[page])
        sm.append("  </url>")
sm.append("</urlset>")
sm.append("")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sm))

print("Wrote %d HTML files:" % len(written))
for w in sorted(written):
    print("  " + w)
print("Wrote sitemap.xml")
