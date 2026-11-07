#!/usr/bin/env python3
"""Generates the bilingual blog into dist/. Usage: build.py [--serve] [--drafts]"""
import functools
import html
import http.server
import json
import re
import shutil
import sys
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from string import Template

import markdown

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
SITE = "https://blog.barm.dev"
AUTHOR = "Benoît Armbruster"
LINKEDIN = "https://www.linkedin.com/in/beno%C3%AEt-armbruster-a573332b"
GITHUB = "https://github.com/barm-dev"
PORT = 4321

# French is served at the root, English under /en/.
TEXT = {
    "fr": {
        "prefix": "",
        "locale": "fr_FR",
        "job": "Architecte data",
        "site": f"{AUTHOR}, data et BI · barm.dev",
        "description": "Blog de Benoît Armbruster, dans la data et la BI depuis 2010, data engineer devenu architecte data\u00a0: entrepôts de données, Snowflake, dbt, Qlik, Power BI, SQL Server.",
        "headline": "Data et BI depuis 2010",
        "intro": "Data engineer hier, architecte data aujourd’hui. Je conçois des entrepôts de données et des solutions décisionnelles, en partant toujours du besoin métier.",
        "note": "Ce blog est mon journal de bord : ce que j’apprends sur le terrain, et quelques projets personnels.",
        "fields": (("Aujourd’hui", "Architecte data"), ("Avant", "Data engineer"),
                   ("Domaines", "Entrepôts de données, business intelligence"),
                   ("Outils", "Snowflake, dbt, Qlik, Power BI, SQL Server (SSIS, SSAS)")),
        "posts": "Articles", "about": "À propos",
        "col_date": "Date", "col_post": "Article", "col_topic": "Sujet",
        "previous": "Précédent", "next": "Suivant", "other_posts": "Autres articles",
        "skip": "Aller au contenu", "theme": "Changer de thème", "menu": "Navigation",
        "switch_label": "English version", "switch": "EN", "feed": "Flux RSS",
        "months": "janv. févr. mars avr. mai juin juil. août sept. oct. nov. déc.".split(),
        "date": "{day} {month} {year}", "done": "Fait", "todo": "À faire",
    },
    "en": {
        "prefix": "/en",
        "locale": "en_GB",
        "job": "Data architect",
        "site": f"{AUTHOR}, data and BI · barm.dev",
        "description": "Blog by Benoît Armbruster, in data and BI since 2010, data engineer turned data architect: data warehouses, Snowflake, dbt, Qlik, Power BI, SQL Server.",
        "headline": "Data and BI since 2010",
        "intro": "Data engineer yesterday, data architect today. I design data warehouses and business intelligence solutions, always starting from the business need.",
        "note": "This blog is my logbook: what I learn in the field, and a few personal projects.",
        "fields": (("Today", "Data architect"), ("Before", "Data engineer"),
                   ("Areas", "Data warehouses, business intelligence"),
                   ("Tools", "Snowflake, dbt, Qlik, Power BI, SQL Server (SSIS, SSAS)")),
        "posts": "Posts", "about": "About",
        "col_date": "Date", "col_post": "Post", "col_topic": "Topic",
        "previous": "Previous", "next": "Next", "other_posts": "Other posts",
        "skip": "Skip to content", "theme": "Switch colour theme", "menu": "Main",
        "switch_label": "Version française", "switch": "FR", "feed": "RSS feed",
        "months": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),
        "date": "{month} {day}, {year}", "done": "Done", "todo": "To do",
    },
}
OTHER = {"fr": "en", "en": "fr"}

BASE = Template((ROOT / "templates/base.html").read_text(encoding="utf-8"))
esc = html.escape


def french_spacing(text):
    """Non-breaking space before French double punctuation, outside tags and code."""
    parts = re.split(r"(<pre>.*?</pre>|<code>.*?</code>|<[^>]+>)", text, flags=re.S)
    parts[::2] = [re.sub(r" ([!?:;»])", " \\1", part).replace("« ", "« ") for part in parts[::2]]
    return "".join(parts)


def format_date(value, lang):
    t = TEXT[lang]
    return t["date"].format(day=value.day, month=t["months"][value.month - 1], year=value.year)


def read_markdown(path, lang):
    """Returns (metadata, html) for a Markdown file with a `key: value` header."""
    t = TEXT[lang]
    _, header, body = path.read_text(encoding="utf-8").split("---\n", 2)
    meta = dict(line.split(": ", 1) for line in header.strip().splitlines())
    rendered = markdown.markdown(body, extensions=["fenced_code", "tables", "attr_list", "sane_lists"])
    rendered = re.sub(
        r"<li>\[( |x)\] ",
        lambda m: (f'<li class="task"><span class="check on" role="img" aria-label="{t["done"]}"></span> '
                   if m[1] == "x" else
                   f'<li class="task"><span class="check" role="img" aria-label="{t["todo"]}"></span> '),
        rendered,
    )
    rendered = rendered.replace("<img ", '<img loading="lazy" ')
    if lang == "fr":
        rendered = french_spacing(rendered)
        meta = {key: french_spacing(value) for key, value in meta.items()}
    return meta, rendered


def load_posts():
    """Returns {lang: posts, newest first}. A post is NNN-slug.fr.md and/or NNN-slug.en.md."""
    posts = {"fr": [], "en": []}
    for path in (ROOT / "content/posts").glob("*.md"):
        slug, lang = path.stem.rsplit(".", 1)
        meta, body = read_markdown(path, lang)
        if meta.get("draft") == "true" and "--drafts" not in sys.argv:
            continue
        posts[lang].append({**meta, "slug": slug, "date": date.fromisoformat(meta["date"]),
                            "path": f"/blog/{slug}/", "body": body})
    for items in posts.values():
        items.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def write(path, content):
    target = DIST / path.lstrip("/")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def link(lang, path):
    return TEXT[lang]["prefix"] + path


def person(lang):
    return {
        "@type": "Person", "name": AUTHOR, "jobTitle": TEXT[lang]["job"],
        "url": SITE + link(lang, "/about/"), "image": SITE + "/img/avatar.png",
        "sameAs": [LINKEDIN, GITHUB],
    }


def json_ld(data):
    data = {"@context": "https://schema.org", **data}
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>\n'


def page(lang, path, title, description, main, image=None, kind="website",
         nav="", translated=True, structured=""):
    """Writes one page. `translated` says whether `path` exists in the other language."""
    t = TEXT[lang]
    other = OTHER[lang]
    links = "".join(
        f'<a href="{link(lang, href)}"{" aria-current=page" if nav == key else ""}>{t[key]}</a>'
        for key, href in (("posts", "/"), ("about", "/about/"))
    )
    alternates = ""
    if translated:
        alternates = "".join(
            f'<link rel="alternate" hreflang="{code}" href="{SITE}{link(code, path)}">\n' for code in TEXT
        ) + f'<link rel="alternate" hreflang="x-default" href="{SITE}{path}">\n'
    content = BASE.substitute(
        lang=lang, title=esc(title), description=esc(description, quote=True),
        url=SITE + link(lang, path), image=SITE + (image or f"/img/og-{lang}.png"), kind=kind, locale=t["locale"],
        alternates=alternates, structured=structured, nav=links, main=main,
        home=link(lang, "/"), author=AUTHOR, rss=link(lang, "/rss.xml"), feed=t["feed"],
        switch_href=link(other, path if translated else "/"), switch_lang=other,
        switch_label=t["switch_label"], switch=t["switch"], skip=t["skip"], menu=t["menu"],
        theme=t["theme"],
        linkedin=LINKEDIN, github=GITHUB, year=date.today().year,
    )
    write(link(lang, path) + "index.html", content)


def home(lang, posts):
    t = TEXT[lang]
    fields = "".join(f"<div><dt>{key}</dt><dd>{value}</dd></div>" for key, value in t["fields"])
    rows = "".join(f"""
<li><a href="{link(lang, p["path"])}">
  <time datetime="{p["date"]}">{format_date(p["date"], lang)}</time>
  <span class="row-text"><span class="row-title">{esc(p["title"])}</span>
  <span class="row-desc">{esc(p["description"])}</span></span>
  <span class="topic">{esc(p["topic"])}</span>
</a></li>""" for p in posts)
    main = f"""
<section class="intro">
  <div>
    <h1>{t["headline"]}</h1>
    <p class="lede">{t["intro"]}</p>
    <p>{t["note"]}</p>
  </div>
  <dl class="facts">{fields}</dl>
</section>
<section class="index" aria-labelledby="posts-title">
  <h2 id="posts-title" class="sr-only">{t["posts"]}</h2>
  <div class="row-head" aria-hidden="true"><span>{t["col_date"]}</span><span>{t["col_post"]}</span><span>{t["col_topic"]}</span></div>
  <ol>{rows}</ol>
</section>"""
    structured = json_ld(person(lang))
    page(lang, "/", t["site"], t["description"], main, nav="posts", structured=structured)


def neighbour(lang, post, key):
    if not post:
        return "<span></span>"
    return (f'<a class="neighbour {key}" href="{link(lang, post["path"])}"><small>{TEXT[lang][key]}</small>'
            f'{esc(post["title"])}</a>')


def post_page(lang, post, newer, older, translated):
    t = TEXT[lang]
    hero = ""
    if post.get("hero"):
        hero = f'<img class="hero" src="{post["hero"]}" alt="" width="900" height="200">'
    main = f"""
<article class="post">
  <aside class="post-meta">
    <time datetime="{post["date"]}">{format_date(post["date"], lang)}</time>
    <span class="topic">{esc(post["topic"])}</span>
  </aside>
  <div class="post-body">
    <h1>{esc(post["title"])}</h1>
    <p class="lede">{esc(post["description"])}</p>
    {hero}
    <div class="prose">{post["body"]}</div>
  </div>
</article>
<nav class="neighbours" aria-label="{t["other_posts"]}">{neighbour(lang, older, "previous")}{neighbour(lang, newer, "next")}</nav>"""
    structured = json_ld({
        "@type": "BlogPosting", "headline": post["title"], "description": post["description"],
        "datePublished": post["date"].isoformat(), "inLanguage": lang,
        "url": SITE + link(lang, post["path"]), "image": SITE + f"/img/og-{lang}.png",
        "author": person(lang),
    })
    # Share previews use the 1200x630 card: post heroes are too wide for LinkedIn.
    page(lang, post["path"], f'{post["title"]} · {AUTHOR}', post["description"], main,
         kind="article", nav="posts", translated=translated, structured=structured)


def static_page(lang, name, nav=""):
    path = ROOT / f"content/pages/{name}.{lang}.md"
    meta, body = read_markdown(path, lang)
    main = f"""
<article class="post">
  <div class="post-body">
    <h1>{esc(meta["title"])}</h1>
    <div class="prose">{body}</div>
  </div>
</article>"""
    translated = (ROOT / f"content/pages/{name}.{OTHER[lang]}.md").exists()
    structured = json_ld({"@type": "ProfilePage", "mainEntity": person(lang)}) if name == "about" else ""
    page(lang, f"/{name}/", f'{meta["title"]} · {AUTHOR}', meta["description"], main, nav=nav,
         translated=translated, structured=structured)


def rss(lang, posts):
    t = TEXT[lang]
    items = "".join(f"""
    <item>
      <title>{esc(p["title"])}</title>
      <link>{SITE}{link(lang, p["path"])}</link>
      <guid isPermaLink="true">{SITE}{link(lang, p["path"])}</guid>
      <description>{esc(p["description"])}</description>
      <pubDate>{format_datetime(datetime.combine(p["date"], datetime.min.time(), timezone.utc), usegmt=True)}</pubDate>
    </item>""" for p in posts)
    write(link(lang, "/rss.xml"), f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{esc(t["site"])}</title>
    <description>{esc(t["description"])}</description>
    <link>{SITE}{link(lang, "/")}</link>
    <language>{lang}</language>{items}
  </channel>
</rss>
""")


def sitemap(posts):
    entries = []
    for lang, items in posts.items():
        latest = items[0]["date"].isoformat() if items else None
        entries += [(link(lang, "/"), latest), (link(lang, "/about/"), None)]
        entries += [(link(lang, p["path"]), p["date"].isoformat()) for p in items]
    urls = "".join(
        f"\n  <url><loc>{SITE}{path}</loc>" + (f"<lastmod>{day}</lastmod>" if day else "") + "</url>"
        for path, day in entries)
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}
</urlset>
""")


def build():
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(ROOT / "static", DIST, dirs_exist_ok=True)
    posts = load_posts()
    for lang, items in posts.items():
        slugs = {p["slug"] for p in posts[OTHER[lang]]}
        home(lang, items)
        for index, post in enumerate(items):
            newer = items[index - 1] if index else None
            older = items[index + 1] if index + 1 < len(items) else None
            post_page(lang, post, newer, older, post["slug"] in slugs)
        static_page(lang, "about", nav="about")
        rss(lang, items)
    sitemap(posts)
    print(f'{len(posts["fr"])} FR and {len(posts["en"])} EN posts written to {DIST}')


def serve():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
    print(f"http://localhost:{PORT}")
    http.server.ThreadingHTTPServer(("localhost", PORT), handler).serve_forever()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
