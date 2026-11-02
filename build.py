"""Build the static site and the CV from content.py.

    python build.py          # HTML pages, Markdown CVs, sitemap
    python build.py --pdf    # the same, plus PDF CVs and og.png (needs Playwright and Microsoft Edge)
"""

import json
import sys
from html import escape
from pathlib import Path

from content import BASE_URL, CONTACTS, CV_FILES, JOBS, LINK_LABELS, PROJECTS, SKILLS, TEXT

ROOT = Path(__file__).parent
LANGS = ("en", "uk")
PAGE_PATH = {"en": "", "uk": "uk/"}


def e(text):
    return escape(str(text), quote=True)


def icon(name):
    return f'<svg class="icon" aria-hidden="true"><use href="#i-{name}"/></svg>'


ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M7 17 17 7M8 7h9v9"/></symbol>
  <symbol id="i-down" viewBox="0 0 24 24"><path d="M12 4v15m-6-6 6 6 6-6"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5"/></symbol>
  <symbol id="i-theme" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5v17a8.5 8.5 0 0 0 0-17Z" fill="currentColor"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 8h16M4 16h16"/></symbol>
</svg>"""


def json_ld(lang):
    t = TEXT[lang]
    url = BASE_URL + PAGE_PATH[lang]
    person = {
        "@type": "Person",
        "@id": BASE_URL + "#person",
        "name": TEXT["en"]["name"],
        "alternateName": [TEXT["uk"]["name"], "Mosly"],
        "jobTitle": "Manual QA Engineer",
        "description": t["description"],
        "url": BASE_URL,
        "email": "mailto:" + CONTACTS["email"],
        "telephone": CONTACTS["phone_href"][4:],
        "address": {"@type": "PostalAddress", "addressLocality": "Zhytomyr", "addressCountry": "UA"},
        "knowsAbout": ["Manual testing", "Mobile testing", "Web testing", "API testing", "Regression testing",
                       "Test design", "Jira", "TestRail", "Postman", "Chrome DevTools", "SQL", "Python", "Flutter"],
        "knowsLanguage": ["uk", "en"],
        "sameAs": [CONTACTS["github_url"], CONTACTS["linkedin_url"], CONTACTS["telegram_url"]],
    }
    page = {
        "@type": "ProfilePage",
        "@id": url + "#page",
        "url": url,
        "name": t["title"],
        "inLanguage": lang,
        "mainEntity": {"@id": BASE_URL + "#person"},
    }
    return json.dumps({"@context": "https://schema.org", "@graph": [person, page]}, ensure_ascii=False)


def head(lang):
    t = TEXT[lang]
    r = "../" if lang == "uk" else "./"
    url = BASE_URL + PAGE_PATH[lang]
    alt_locale = TEXT["uk" if lang == "en" else "en"]["og_locale"]
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["description"])}">
<meta name="author" content="{e(t["name"])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{BASE_URL}">
<link rel="alternate" hreflang="uk" href="{BASE_URL}uk/">
<link rel="alternate" hreflang="x-default" href="{BASE_URL}">
<meta name="theme-color" content="#f4f2ec" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121211" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="{e(t["name"])}">
<meta property="og:locale" content="{t["og_locale"]}">
<meta property="og:locale:alternate" content="{alt_locale}">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["description"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE_URL}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(t["name"])} — {e(t["role"])}">
<meta property="profile:first_name" content="Maksym">
<meta property="profile:last_name" content="Kasianov">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(t["title"])}">
<meta name="twitter:description" content="{e(t["description"])}">
<meta name="twitter:image" content="{BASE_URL}og.png">
<link rel="icon" href="{r}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{r}assets/site.css">
<script>try{{var s=localStorage.getItem("theme");if(s)document.documentElement.dataset.theme=s}}catch(_){{}}document.documentElement.classList.add("js")</script>
<script src="{r}assets/site.js" defer></script>
<script type="application/ld+json">{json_ld(lang)}</script>
</head>"""


def header(lang):
    t = TEXT[lang]
    other, label, title = t["lang_switch"]
    other_href = ("../" if lang == "uk" else "./") + PAGE_PATH[other]
    nav = "".join(f'<li><a href="#{i}">{e(n)}</a></li>' for i, n in t["nav"])
    return f"""<a class="skip" href="#main">{e(t["skip"])}</a>
<header class="site-header">
  <div class="wrap header-row">
    <a class="brand" href="#top" aria-label="{e(t["name"])}"><span class="brand-mark">MK</span><span class="brand-name">{e(t["name"])}</span></a>
    <nav class="nav" id="nav" aria-label="{e(t["menu"])}"><ul>{nav}</ul></nav>
    <div class="header-tools">
      <a class="tool lang" href="{other_href}" hreflang="{other}" lang="{other}" title="{e(title)}">{label}</a>
      <button class="tool" type="button" data-theme-toggle aria-label="{e(t["theme"])}">{icon("theme")}</button>
      <button class="tool menu-toggle" type="button" aria-controls="nav" aria-expanded="false" aria-label="{e(t["menu"])}">{icon("menu")}</button>
    </div>
  </div>
</header>"""


def hero(lang):
    t = TEXT[lang]
    r = "../" if lang == "uk" else "./"
    other = "uk" if lang == "en" else "en"
    rows = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in t["status"][:-1])
    k, v = t["status"][-1]
    rows += f'<div><dt>{e(k)}</dt><dd><span class="dot" aria-hidden="true"></span>{e(v)}</dd></div>'
    facts = "".join(f'<li><span class="fact-num">{e(n)}</span><span class="fact-text">{e(x)}</span></li>' for n, x in t["facts"])
    return f"""<section class="hero wrap" id="top" aria-labelledby="name">
  <div class="hero-main">
    <p class="eyebrow">{e(t["role"])}</p>
    <h1 id="name">{e(t["name"])}</h1>
    <p class="lead">{e(t["lead"])}</p>
    <div class="actions">
      <a class="btn btn-primary" href="{r}cv/{CV_FILES[lang]}" download>{icon("down")}{e(t["cta_cv"])} <span class="btn-meta">PDF</span></a>
      <a class="btn" href="mailto:{CONTACTS["email"]}">{e(t["cta_mail"])}</a>
      <a class="text-link" href="{r}cv/{CV_FILES[other]}" download hreflang="{other}">{e(t["cta_cv_alt"])}</a>
    </div>
  </div>
  <aside class="profile" aria-label="{e(t["status_label"])}">
    <p class="profile-label">{e(t["status_label"])}</p>
    <dl>{rows}</dl>
  </aside>
  <ul class="facts">{facts}</ul>
</section>"""


def section_head(num, sid, title, intro=""):
    p = f'<p class="section-intro">{e(intro)}</p>' if intro else ""
    return f'<div class="section-head"><span class="section-num">{num}</span><h2 id="{sid}-title">{e(title)}</h2>{p}</div>'


def projects(lang):
    t = TEXT[lang]
    items = []
    for i, p in enumerate(PROJECTS, 1):
        c = p[lang]
        links = "".join(
            f'<a href="{e(u)}" target="_blank" rel="noopener">{e(LINK_LABELS[lang][k])}{icon("arrow")}</a>'
            for k, u in p["links"])
        links = f'<p class="project-links">{links}</p>' if links else ""
        stack = "".join(f"<li>{e(s)}</li>" for s in p["stack"])
        checks = "".join(f"<li>{icon('check')}<span>{e(x)}</span></li>" for x in c["checks"])
        items.append(f"""<article class="project reveal" id="{p["id"]}">
  <div class="project-id">
    <span class="project-num">{i:02d}</span>
    <h3>{e(c.get("name", p["name"]))}</h3>
    <p class="project-kind">{e(c["kind"])}</p>
    {links}
  </div>
  <div class="project-body">
    <p>{e(c["summary"])}</p>
    <ul class="tags" aria-label="Stack">{stack}</ul>
  </div>
  <div class="project-checks">
    <p class="mini-label">{e(t["checked"])}</p>
    <ul>{checks}</ul>
  </div>
</article>""")
    return f"""<section class="section wrap" id="work" aria-labelledby="work-title">
  {section_head("01", "work", t["work_title"], t["work_intro"])}
  <div class="projects">{"".join(items)}</div>
  <p class="more"><a class="text-link" href="{CONTACTS["github_url"]}?tab=repositories" target="_blank" rel="noopener">{e(t["more_repos"])}{icon("arrow")}</a></p>
</section>"""


def approach(lang):
    t = TEXT[lang]
    b = t["bug"]
    steps = "".join(
        f'<li class="reveal"><span class="step-num">{i:02d}</span><h3>{e(h)}</h3><p>{e(x)}</p></li>'
        for i, (h, x) in enumerate(t["steps"], 1))
    fields = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in b["fields"])
    bsteps = "".join(f"<li>{e(s)}</li>" for s in b["steps"])
    return f"""<section class="section wrap" id="approach" aria-labelledby="approach-title">
  {section_head("02", "approach", t["approach_title"], t["approach_intro"])}
  <ol class="steps">{steps}</ol>
  <figure class="bug reveal">
    <figcaption><span class="mini-label">{e(t["bug_label"])}</span><span class="bug-note">{e(t["bug_note"])}</span></figcaption>
    <div class="bug-card">
      <p class="bug-title">{e(b["title"])}</p>
      <dl class="bug-fields">{fields}</dl>
      <div class="bug-grid">
        <div><p class="mini-label">{e(b["steps_label"])}</p><ol>{bsteps}</ol></div>
        <div>
          <p class="mini-label">{e(b["expected_label"])}</p><p>{e(b["expected"])}</p>
          <p class="mini-label">{e(b["actual_label"])}</p><p class="bug-actual">{e(b["actual"])}</p>
          <p class="mini-label">{e(b["attach_label"])}</p><p>{e(b["attach"])}</p>
        </div>
      </div>
    </div>
  </figure>
</section>"""


def all_jobs(lang):
    return [TEXT[lang]["exp_current"]] + [j[lang] for j in JOBS]


def experience(lang):
    t = TEXT[lang]
    rows = []
    for j in all_jobs(lang):
        pts = "".join(f"<li>{e(x)}</li>" for x in j["points"])
        rows.append(f"""<li class="job reveal">
  <p class="job-period">{e(j["period"])}</p>
  <div><h3>{e(j["title"])}</h3><p class="job-org">{e(j["org"])}</p><ul>{pts}</ul></div>
</li>""")
    return f"""<section class="section wrap" id="experience" aria-labelledby="experience-title">
  {section_head("03", "experience", t["exp_title"])}
  <ol class="jobs">{"".join(rows)}</ol>
</section>"""


def skills(lang):
    t = TEXT[lang]
    rows = "".join(f"<div class=\"reveal\"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in SKILLS[lang])
    return f"""<section class="section wrap" id="skills" aria-labelledby="skills-title">
  {section_head("04", "skills", t["skills_title"])}
  <dl class="skills">{rows}</dl>
</section>"""


def contact(lang):
    t = TEXT[lang]
    L = t["contact_labels"]
    c = CONTACTS
    items = [
        (L["phone"], c["phone"], c["phone_href"], False),
        (L["telegram"], c["telegram"], c["telegram_url"], True),
        (L["linkedin"], "maksym-kasianov", c["linkedin_url"], True),
        (L["github"], "MoslyHarmless", c["github_url"], True),
    ]
    blank = ' target="_blank" rel="noopener"'
    lis = "".join(
        f'<li><span class="mini-label">{e(k)}</span><a href="{e(h)}"{blank if ext else ""}>{e(v)}</a></li>'
        for k, v, h, ext in items)
    return f"""<section class="section wrap contact" id="contact" aria-labelledby="contact-title">
  {section_head("05", "contact", t["contact_title"], t["contact_text"])}
  <a class="contact-mail" href="mailto:{c["email"]}">{c["email"]}{icon("arrow")}</a>
  <ul class="contact-list">{lis}</ul>
</section>"""


def page(lang):
    t = TEXT[lang]
    body = "\n".join([hero(lang), projects(lang), approach(lang), experience(lang), skills(lang), contact(lang)])
    return f"""{head(lang)}
<body>
{ICONS}
{header(lang)}
<main id="main" tabindex="-1">
{body}
</main>
<footer class="site-footer"><div class="wrap"><div class="footer-row">
  <p>© <span data-year>2026</span> {e(t["name"])}</p>
  <p class="footer-note">{e(t["footer"])}</p>
  <a class="text-link" href="#top">{e(t["top"])} ↑</a>
</div></div></footer>
</body>
</html>
"""


# ---------- CV ----------

def cv_contact_line(lang):
    c = CONTACTS
    return [TEXT[lang]["cv_location"], c["phone"], c["email"], c["linkedin"], "t.me/moslyharmless", c["github"],
            f'{TEXT[lang]["cv_portfolio"]}: {c["portfolio"]}']


def cv_html(lang):
    t = TEXT[lang]
    contact = " | ".join(e(x) for x in cv_contact_line(lang))
    skills_rows = "".join(f"<li><b>{e(k)}:</b> {e(v)}</li>" for k, v in SKILLS[lang])
    jobs = ""
    for j in all_jobs(lang):
        pts = "".join(f"<li>{e(x)}</li>" for x in j["points"])
        jobs += f'<div class="item"><h3>{e(j["title"])} — {e(j["org"])}</h3><p class="meta">{e(j["period"])}</p><ul>{pts}</ul></div>'
    projs = ""
    for p in PROJECTS:
        c = p[lang]
        urls = ", ".join("Google Play" if k == "play" else u.replace("https://", "").rstrip("/") for k, u in p["links"])
        meta =e(c["kind"]) + " | " + e(", ".join(p["stack"])) + (f" | {e(urls)}" if urls else "")
        pts = "".join(f"<li>{e(x)}</li>" for x in c["checks"][:3])  # keeps the PDF to two pages
        projs += f'<div class="item"><h3>{e(c.get("name", p["name"]))}</h3><p class="meta">{meta}</p><p>{e(c["summary"])}</p><ul>{pts}</ul></div>'
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<title>{e(t["name"])} — CV</title>
<style>
@page {{ size: A4; margin: 12mm 14mm; }}
body {{ font-family: Arial, Helvetica, sans-serif; font-size: 10pt; line-height: 1.38; color: #111; margin: 0; }}
h1 {{ font-size: 20pt; margin: 0; }}
.title {{ font-size: 11.5pt; font-weight: bold; margin: 2pt 0 4pt; }}
.contact {{ font-size: 9pt; margin: 0 0 6pt; }}
h2 {{ font-size: 11pt; text-transform: uppercase; letter-spacing: .04em; border-bottom: 1px solid #111; padding-bottom: 2pt; margin: 10pt 0 5pt; }}
h3 {{ font-size: 10.5pt; margin: 0; }}
.meta {{ font-size: 9pt; color: #333; margin: 1pt 0 2pt; }}
p {{ margin: 0 0 3pt; }}
ul {{ margin: 0; padding-left: 14pt; }}
li {{ margin: 0 0 1.5pt; }}
.item {{ margin-bottom: 6pt; break-inside: avoid; }}
.skills li {{ margin-bottom: 2pt; }}
</style></head>
<body>
<h1>{e(t["name"])}</h1>
<p class="title">{e(t["cv_title"])}</p>
<p class="contact">{contact}</p>
<h2>{e(t["cv_summary_h"])}</h2>
<p>{e(t["cv_summary"])}</p>
<h2>{e(t["cv_skills_h"])}</h2>
<ul class="skills">{skills_rows}</ul>
<h2>{e(t["cv_exp_h"])}</h2>
{jobs}
<h2>{e(t["cv_projects_h"])}</h2>
{projs}
<p><b>{e(t["cv_footer"])}</b></p>
</body></html>
"""


def cv_md(lang):
    t = TEXT[lang]
    out = [f"# {t['name']}", f"**{t['cv_title']}**", "", " | ".join(cv_contact_line(lang)), "",
           f"## {t['cv_summary_h']}", t["cv_summary"], "", f"## {t['cv_skills_h']}"]
    out += [f"- **{k}:** {v}" for k, v in SKILLS[lang]]
    out += ["", f"## {t['cv_exp_h']}"]
    for j in all_jobs(lang):
        out += ["", f"### {j['title']} — {j['org']}", f"*{j['period']}*"] + [f"- {x}" for x in j["points"]]
    out += ["", f"## {t['cv_projects_h']}"]
    for p in PROJECTS:
        c = p[lang]
        urls = ", ".join(u for _, u in p["links"])
        out += ["", f"### {c.get('name', p['name'])}", f"*{c['kind']} | {', '.join(p['stack'])}*" + (f" | {urls}" if urls else ""),
                c["summary"]] + [f"- {x}" for x in c["checks"]]
    out += ["", f"**{t['cv_footer']}**", ""]
    return "\n".join(out)


def sitemap():
    urls = ""
    for lang in LANGS:
        alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{BASE_URL}{PAGE_PATH[l]}"/>' for l in LANGS)
        alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE_URL}"/>'
        urls += f"  <url>\n    <loc>{BASE_URL}{PAGE_PATH[lang]}</loc>{alts}\n  </url>\n"
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            f"{urls}</urlset>\n")


def write(path, text):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    print("wrote", path.relative_to(ROOT))


def main():
    write("index.html", page("en"))
    write("uk/index.html", page("uk"))
    write("sitemap.xml", sitemap())
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /cv/print/\n\nSitemap: {BASE_URL}sitemap.xml\n")
    md_names = {"en": "CV_Maksym_Kasianov_QA_EN.md", "uk": "CV_Maksym_Kasianov_QA_UK.md"}
    for lang in LANGS:
        write(f"cv/print/{lang}.html", cv_html(lang))
        write(md_names[lang], cv_md(lang))
    if "--pdf" in sys.argv:
        render_files()


def render_files():
    # Playwright drives the installed Edge, so web fonts finish loading before capture.
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1200, "height": 630})
        for lang in LANGS:
            pdf = ROOT / "cv" / CV_FILES[lang]
            page.goto((ROOT / "cv/print" / f"{lang}.html").as_uri())
            page.pdf(path=str(pdf), format="A4", prefer_css_page_size=True, print_background=True)
            print("wrote", pdf.relative_to(ROOT))
        page.goto((ROOT / "og.html").as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(ROOT / "og.png"))
        print("wrote og.png")
        browser.close()


if __name__ == "__main__":
    main()
