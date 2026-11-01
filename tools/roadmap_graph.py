"""Draw ROADMAP.md as a radial knowledge graph (roadmap.svg) and build the
interactive site (public/index.html the hub home, public/learn.html the catalog, public/course.html the reader)
from the roadmap, the course READMEs and tools/hub.json.
The site lives in public/ and reads courses/ beside it; tools/build_site.py assembles both for hosting.

Usage:  python tools/roadmap_graph.py
Re-run after editing ROADMAP.md or adding a course. Standard library only.
"""
import json
import math
import re
import urllib.parse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "ROADMAP.md"
PUBLIC = ROOT / "public"
OUT = PUBLIC / "roadmap.svg"
HTML_OUT = PUBLIC / "learn.html"
HUB_OUT = PUBLIC / "index.html"
TEMPLATE = ROOT / "tools" / "roadmap_template.html"
READER_OUT = PUBLIC / "course.html"
READER_TEMPLATE = ROOT / "tools" / "reader_template.html"
LEGAL_TEMPLATE = ROOT / "tools" / "legal_template.html"
SITE = "https://theiehub.com"   # canonical origin; Cloudflare Pages serves /page.html at /page, so canonical URLs drop .html
LEGAL_PAGES = {"privacy": "Privacy Policy", "terms": "Terms of Use", "roadmap": "Site roadmap", "sources": "Sources"}   # tools/legal/<key>.html -> public/<key>.html
ICON_DIR = ROOT / "tools" / "icons"   # Bootstrap Icons (MIT), vendored; see tools/icons/LICENSE
CATEGORY_ICONS = {
    "analytics-data-science-ai": "graph-up-arrow",
    "ergonomics-safety": "shield-check",
    "healthcare-process-improvement": "heart-pulse",
    "leadership-project-management": "people",
    "lean-six-sigma": "arrow-repeat",
    "logistics-supply-chain": "truck",
    "quality-operational-excellence": "patch-check",
    "technical-skills": "wrench-adjustable",
    "work-design-work-measurement": "stopwatch",
    "operations-research-decision-analysis": "diagram-3",
    "microlearning-refreshers": "lightning-charge",
}


def icon(name, size=16):
    """Inline SVG for a vendored Bootstrap icon, sized in CSS pixels and coloured by currentColor."""
    svg = (ICON_DIR / f"{name}.svg").read_text(encoding="utf-8")
    svg = re.sub(r'\s(width|height|class)="[^"]*"', "", svg, count=3)
    svg = svg.replace("<svg ", f'<svg class="bi" width="{size}" height="{size}" aria-hidden="true" focusable="false" ', 1)
    return re.sub(r"\s*\n\s*", "", svg)


LOGO = ROOT / "tools" / "logo" / "header.svg.html"
HUB_DATA = ROOT / "tools" / "hub.json"
NIDHY = "https://nidhy.dev"


def inject_logo(html):
    """Replace __LOGO__ (or __LOGO:id__, which gives the link that id) with the header logo: one inline SVG
    coloured by the page's CSS variables, so it follows the theme. Source: tools/logo/header.svg.html."""
    snippet = LOGO.read_text(encoding="utf-8").strip()
    return re.sub(r"__LOGO(?::([A-Za-z][A-Za-z0-9]*))?__",
                  lambda m: snippet.replace("__LOGO_ATTRS__", f' id="{m.group(1)}"' if m.group(1) else ""), html)


def footer_html():
    """The site footer, the same on every page: brand block, then Learn, The hub, About and Legal columns, then the
    licences. Hub pillars come from tools/hub.json: a live pillar is a link, any other shows as "soon" without one."""
    hub = json.loads(HUB_DATA.read_text(encoding="utf-8"))
    full = re.search(r'<svg class="logo-full".*?</svg>', LOGO.read_text(encoding="utf-8"), re.S).group(0)
    full = full.replace('class="logo-full"', 'class="ft-logo"').replace('width="120" height="27"', 'width="138" height="31"')
    def col(title, items):
        def li(t, h):
            if h is None:
                return f'<li><span class="soon">{t}<i>soon</i></span></li>'
            rel = ' rel="noopener"' if h.startswith("http") else ""
            return f'<li><a href="{h}"{rel}>{t}</a></li>'
        lis = "".join(li(t, h) for t, h in items)
        return f'<nav class="ft-col" aria-label="{title}"><p class="ft-h">{title}</p><ul>{lis}</ul></nav>'
    learn = [("Catalog", "learn.html"), ("Learning path", "learn.html#tab=path"), ("Mind map", "learn.html#tab=graph"),
             ("Course coverage", f"{REPO_URL}/blob/main/ROADMAP.md")]
    hubcol = [(p["name"], p["href"] if p["status"] == "live" else None) for p in hub["pillars"] if p["key"] != "learn"]
    about = [("Site roadmap", "roadmap.html"), ("Sources", "sources.html"), ("__ICON:github:14__GitHub", REPO_URL),
             ("Report an issue", f"{REPO_URL}/issues")]
    legal = [("Notice", f"{REPO_URL}/blob/main/NOTICE.md"), ("Privacy", "privacy.html"), ("Terms", "terms.html")]
    return ('<footer class="ft"><div class="ft-wrap"><div class="ft-top">'
            f'<div class="ft-brand"><a class="ft-home" href="index.html" aria-label="The IE Hub, home">{full}</a>'
            '<p>Industrial engineering, learned and built in the open. Free courses, worked projects and data you can rerun.</p>'
            f'<p class="ft-by">Maintained by <a href="{NIDHY}" rel="noopener">Nidhin Dileepkumar</a></p></div>'
            + col("Learn", learn) + col("The hub", hubcol) + col("About", about) + col("Legal", legal) +
            '</div><div class="ft-bottom"><span>Content CC BY 4.0</span><span>Code MIT</span><span class="ft-domain">theiehub.com</span></div></div></footer>')


STATUS_LABEL = {"done": "done", "next": "next", "along": "in progress", "planned": "planned", "later": "later"}
PILLAR_NAME = {"hub": "Hub", "learn": "Learn", "projects": "Projects", "insights": "Insights", "collaborate": "Collaborate"}


def roadmap_parts():
    """The generated pieces of public/roadmap.html, all from tools/hub.json: the date, the goal, the summary numbers,
    the phase bar, the pillar filter, the phase timeline and the recent updates. Course counts stay as __COURSES__ etc.
    placeholders here; write_html fills them in with the rest of the page."""
    hub = json.loads(HUB_DATA.read_text(encoding="utf-8"))
    phases = hub["phases"]
    done = sum(1 for p in phases if p["status"] == "done")
    seg = {"done": "done", "next": "active", "along": "active"}
    bar = "".join(f'<i class="{seg.get(p["status"], "")}"></i>' for p in phases)
    keys = []
    for p in phases:
        keys += [k for k in p["pillars"] if k not in keys]
    filt = '<button type="button" aria-pressed="true" data-f="">all</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-f="{k}">{k}</button>' for k in PILLAR_NAME if k in keys)
    lis = []
    for i, p in enumerate(phases, 1):
        cls = {"done": "done", "next": "active", "along": "along"}.get(p["status"], "later")
        open_ = p["status"] == "next"
        pill = " · ".join(PILLAR_NAME[k] for k in p["pillars"])
        items = ("<ul>" + "".join(f"<li>{x}</li>" for x in p["items"]) + "</ul>") if p["items"] else ""
        lis.append(f'<li class="{cls}" id="phase-{i}" data-p="{" ".join(p["pillars"])}">'
                   f'<button type="button" class="tl-head" aria-expanded="{str(open_).lower()}" aria-controls="phase-{i}-body">'
                   f'<span class="tl-dot"></span><span class="tl-n">{i}</span><span class="tl-title">{p["title"]}</span>'
                   f'<span class="tl-pill">{pill}</span><span class="tl-status">{STATUS_LABEL[p["status"]]}</span>__ICON:chevron-right:14__</button>'
                   f'<div class="tl-body" id="phase-{i}-body"{"" if open_ else " hidden"}><p>{p["body"]}</p>{items}</div></li>')
    upd = "".join(f'<li><time datetime="{u["date"]}">{u["date"]}</time><div><span class="tag">{u["pillar"]}</span>{u["text"]}</div></li>'
                  for u in hub["updates"])
    return {"RM_UPDATED": hub["updated"], "RM_GOAL": hub["goal"], "RM_DONE": str(done), "RM_PHASES": str(len(phases)),
            "RM_BAR": bar, "RM_FILTER": filt, "RM_TIMELINE": "".join(lis), "RM_UPDATES": upd}


# The home page hero: the old catalog front door's title, map lines and animation, with what the hub is and two ways in.
HUB_HERO = """<section class="hero" id="hero">
  <svg class="bgmap" viewBox="0 0 1000 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <g fill="none" stroke="var(--accent)" stroke-width="1.2"><path d="M500 150 C380 150 380 60 260 60"/><path d="M500 150 C380 150 380 150 260 150"/><path d="M500 150 C380 150 380 240 260 240"/><path d="M500 150 C620 150 620 40 740 40"/><path d="M500 150 C620 150 620 120 740 120"/><path d="M500 150 C620 150 620 200 740 200"/><path d="M500 150 C620 150 620 270 740 270"/><path d="M260 60 C200 60 200 30 140 30"/><path d="M260 60 C200 60 200 90 140 90"/><path d="M260 150 C200 150 200 130 140 130"/><path d="M260 150 C200 150 200 175 140 175"/><path d="M260 240 C200 240 200 225 140 225"/><path d="M740 120 C800 120 800 100 860 100"/><path d="M740 120 C800 120 800 145 860 145"/><path d="M740 200 C800 200 800 185 860 185"/><path d="M740 200 C800 200 800 220 860 220"/></g>
    <g fill="var(--accent)"><circle cx="500" cy="150" r="16"/><circle cx="260" cy="60" r="6"/><circle cx="260" cy="150" r="6"/><circle cx="260" cy="240" r="6"/><circle cx="740" cy="40" r="6"/><circle cx="740" cy="120" r="6"/><circle cx="740" cy="200" r="6"/><circle cx="740" cy="270" r="6"/></g>
    <g fill="var(--green)"><circle cx="140" cy="30" r="4"/><circle cx="140" cy="90" r="4"/><circle cx="140" cy="130" r="4"/><circle cx="140" cy="175" r="4"/><circle cx="140" cy="225" r="4"/><circle cx="860" cy="100" r="4"/><circle cx="860" cy="145" r="4"/><circle cx="860" cy="185" r="4"/><circle cx="860" cy="220" r="4"/></g>
  </svg>
  <div class="hero-in">
    <div class="eyebrow">free · open · original · reviewable</div>
    <h1 aria-label="The IE Hub"><span class="type" aria-hidden="true"><span class="ghost">The IE <span class="md">Hub</span></span><span class="live"><span id="tyA">The IE </span><span class="md" id="tyB">Hub</span><span class="cursor"></span></span></span></h1>
    <p class="lede">Industrial engineering, learned and built in the open.</p>
    <p class="about">__ABOUT__</p>
    <div class="ctas"><a class="btn primary" href="learn.html">Start learning →</a><a class="btn" href="roadmap.html">See what's next</a></div>
  </div>
</section>
<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/4.5.0/anime.umd.min.js" integrity="sha512-dnhflec5WaXvpVYrt0oWfe0iUyWpjNiZbxkjrhNu9WAWWHLX7VqqyxCZHL7dWCrwj6lN+XGN9FtiWIBgX2b/PA==" crossorigin="anonymous"></script>
<script>
  (function () {
    const motion = typeof anime !== 'undefined' && !matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!motion) return;
    try {   // decorative only: a library hiccup must never stop the page
      anime.animate(anime.svg.createDrawable([...document.querySelectorAll('#hero .bgmap path')]), { draw: ['0 0', '0 1'], duration: 900, delay: anime.stagger(30), ease: 'outQuad' });
      anime.animate('#hero .hero-in > *', { opacity: [0, 1], y: [10, 0], duration: 460, delay: anime.stagger(55), ease: 'outCubic' });
      const full = 'The IE Hub', split = 7, tyA = document.getElementById('tyA'), tyB = document.getElementById('tyB'), ty = { n: full.length };
      const showTy = () => { const k = Math.round(ty.n); tyA.textContent = full.slice(0, Math.min(k, split)); tyB.textContent = full.slice(split, Math.max(k, split)); };
      anime.createTimeline({ loop: true, loopDelay: 120, onUpdate: showTy })
        .add(ty, { n: [0, full.length], duration: 1100, ease: 'linear', modifier: anime.utils.round(0) }, 200)
        .add(ty, { n: 0, duration: 550, ease: 'linear', modifier: anime.utils.round(0) }, '+=4200');
    } catch (e) {}
  })();
</script>"""


def hub_page(model):
    """Body of public/index.html, the hub home, all from tools/hub.json: the hero (title typing over the map lines, the
    tagline, the reason in one line, two ways in), why it exists, the four pillars, the audiences and how each can use the hub, and where it
    is going (the phases in progress and the next one). A pillar or audience that is not live links to the roadmap."""
    hub = json.loads(HUB_DATA.read_text(encoding="utf-8"))
    courses = {n["id"][7:]: n for n in model["nodes"] if n["type"] == "course"}
    phase_of = {}
    for i, p in enumerate(hub["phases"], 1):
        for k in p["pillars"]:
            phase_of.setdefault(k, i)
    cards = []
    for p in hub["pillars"]:
        if p["status"] == "live":
            tag, link = '<span class="hp-tag live">live</span>', f'<a class="hp-go" href="{p["href"]}">{p["cta"]} →</a>'
        else:
            tag, link = '<span class="hp-tag soon">coming</span>', f'<a class="hp-go" href="roadmap.html#phase-{phase_of[p["key"]]}">On the roadmap →</a>'
        cards.append(f'<div class="hp-card">{tag}<h3>{p["name"]}</h3><p>{p["blurb"]}</p>{link}</div>')
    live = {p["key"] for p in hub["pillars"] if p["status"] == "live"}
    aud = []
    for a in hub["audiences"]:
        soon = a.get("pillar") and a["pillar"] not in live
        rel = ' rel="noopener"' if a["href"].startswith("http") else ""
        aud.append(f'<div class="hp-card"><h3>{a["title"]}</h3><p>{a["text"]}</p><a class="hp-go{" soon" if soon else ""}" href="{a["href"]}"{rel}>{a["cta"]} →</a></div>')
    def where(label, cls, ps):
        return "".join(f'<a class="hp-where" href="roadmap.html#phase-{i}"><span class="lbl {cls}">{label}</span><h3>{p["title"]}</h3><p>{p.get("short", p["body"])}</p></a>' for i, p in ps)
    phases = list(enumerate(hub["phases"], 1))
    now = [(i, p) for i, p in phases if p["status"] == "along"]
    nxt = [(i, p) for i, p in phases if p["status"] == "next"][:1]
    w = hub["why"]
    why = (f'<p class="w-head"><span>{w["headline"][0]}</span><span class="acc">{w["headline"][1]}</span></p><div class="w-rows">'
           + "".join(f'<div class="w-row"><span class="w-tag">{p["tag"]}</span><p>{p["lead"]} <span class="w-rest">{p["rest"]}</span></p></div>' for p in w["points"])
           + f'</div><p class="w-ans">{w["answer"][0]} <span class="acc">{w["answer"][1]}</span></p><p class="w-open">{w["open"]}</p>')
    return HUB_HERO.replace("__ABOUT__", hub["about"]) + f"""
<h2 id="why">Why it exists</h2>
<div class="hp-why">{why}</div>

<h2 id="pillars">What's here</h2>
<div class="hp-pillars">{"".join(cards)}</div>

<h2 id="audiences">Find your way in</h2>
<div class="hp-pillars">{"".join(aud)}</div>

<h2 id="where">Where it is going</h2>
<div class="hp-two">{where("now", "now", now)}{where("next", "", nxt)}</div>
<p class="hp-more"><a class="hp-go" href="roadmap.html">Full site roadmap →</a></p>
"""



def hubnav_html(current=""):
    """The hub's top-bar navigation, the same on every page: each pillar from tools/hub.json (a live one is a link,
    any other a quiet "soon" label hidden on phones), then Roadmap. `current` is the pillar key or "roadmap"."""
    hub = json.loads(HUB_DATA.read_text(encoding="utf-8"))
    items = []
    for p in hub["pillars"]:
        if p["status"] == "live":
            cur = ' aria-current="page"' if p["key"] == current else ""
            items.append(f'<a href="{p["href"]}"{cur}>{p["name"]}</a>')
        else:
            items.append(f'<span class="soon" title="coming soon">{p["name"]}</span>')
    cur = ' aria-current="page"' if current == "roadmap" else ""
    items.append(f'<a href="roadmap.html"{cur}>Roadmap</a>')
    return '<nav class="hubnav" aria-label="The IE Hub">' + "".join(items) + "</nav>"


def inject_hubnav(html):
    """Replace __HUBNAV__ and __HUBNAV:key__ with the hub navigation, marking that key as the current page."""
    return re.sub(r"__HUBNAV(?::([a-z]+))?__", lambda m: hubnav_html(m.group(1) or ""), html)


def inject_footer(html):
    """Replace every __FOOTER__ with the shared footer (before icons are injected, so its __ICON__ placeholders resolve)."""
    return html.replace("__FOOTER__", footer_html()) if "__FOOTER__" in html else html


def inject_icons(html):
    """Replace __ICON:name__ and __ICON:name:size__ placeholders in a template."""
    return re.sub(r"__ICON:([a-z0-9-]+)(?::(\d+))?__", lambda m: icon(m.group(1), int(m.group(2) or 16)), html)
REPO_URL = "https://github.com/crackcode09/theiehub"

# The site's dark-theme tokens (--green, --todo, --accent, --line, --text, --muted, --bg), so the README
# picture matches the site. Fonts fall back to system faces: GitHub shows the SVG as an image, which
# cannot load web fonts.
DONE, TODO, CAT, HUB, LINK, INK, MUTED, BG = (
    "#9cba7f", "#5c5546", "#d97757", "#d97757", "#3e392f", "#ede6da", "#a79e89", "#1f1d18")
SANS = "Inter, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"
DISPLAY = "'Space Grotesk', Inter, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif"

# Link text may hold one level of brackets, e.g. "[Cost Management [ABC/M]](...)".
LINK_RE = re.compile(r"\[((?:[^\[\]]|\[[^\[\]]*\])+)\]\(([^)\s]+)\)")


def parse(md):
    """ROADMAP.md -> [{name, slug, items: [(title, done, link_path)]}]"""
    cats, cur = [], None
    for line in md.splitlines():
        m = re.match(r"^## (.+?) \(\d+/\d+\)", line)
        if m:
            cur = {"name": m.group(1), "items": [], "slug": None, "tag": ""}
            cats.append(cur)
            continue
        if line.startswith("## "):
            cur = None   # a section without a (k/n) count is prose, not a category; its checkboxes are not topics
            continue
        m = re.match(r"^Folder: \[`courses/([a-z0-9-]+)/`\][^—]*(?:— *(.+))?", line)
        if m and cur is not None:
            cur["slug"] = m.group(1)
            cur["tag"] = (m.group(2) or "").strip()   # e.g. "beyond the IISE catalog"
            continue
        m = re.match(r"^- \[([ x])\] (.+)", line)
        if m and cur is not None:
            rest = m.group(2)
            found = LINK_RE.findall(rest)
            lm = LINK_RE.match(rest)
            # The title is the link text when the item starts with a link; otherwise the text before a " — note".
            title = lm.group(1).strip() if lm else re.split(r" — ", LINK_RE.sub(r"\1", rest))[0].strip()
            folded = "folded into" in rest.lower()
            path = (found[-1][1] if folded else found[0][1]) if found else None   # folded items point at the covering course
            cur["items"].append((title, m.group(1) == "x", path, folded))
    return cats


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ----------------------------------------------------------------- static SVG

def render(cats):
    size = 1850
    cx = cy = size / 2
    r_cat, r_leaf = 300, 580
    total = sum(len(c["items"]) for c in cats)
    done = sum(ok for c in cats for _, ok, _p, _f in c["items"])
    gap = 0.012  # radians of padding between category sectors
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
             f'font-family="{SANS}" font-size="11">',
             f'<rect width="{size}" height="{size}" fill="{BG}"/>',
             f'<text x="{size - 30}" y="{size - 44}" text-anchor="end" font-family="{DISPLAY}" font-size="22" font-weight="700" fill="{INK}">'
             f'IE Knowledgebase roadmap</text>',
             f'<text x="{size - 30}" y="{size - 22}" text-anchor="end" font-size="13" fill="{MUTED}">'
             f'{done} of {total} courses built</text>']
    edges, nodes, labels = [], [], []
    ang = -math.pi / 2
    for c in cats:
        n = len(c["items"])
        span = 2 * math.pi * n / total
        a_cat = ang + span / 2
        x1, y1 = cx + r_cat * math.cos(a_cat), cy + r_cat * math.sin(a_cat)
        edges.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{LINK}" stroke-width="2"/>')
        inner = span - 2 * gap
        for i, (title, ok, _p, _f) in enumerate(c["items"]):
            a = ang + gap + inner * (i + 0.5) / n
            x2, y2 = cx + r_leaf * math.cos(a), cy + r_leaf * math.sin(a)
            edges.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                         f'stroke="{DONE if ok else LINK}" stroke-width="{1.6 if ok else 1}"/>')
            fill = DONE if ok else BG
            nodes.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="{6 if ok else 4.5}" fill="{fill}" '
                         f'stroke="{DONE if ok else TODO}" stroke-width="1.5"/>')
            deg = math.degrees(a)
            flip = 90 < (deg % 360) < 270
            tx, ty = cx + (r_leaf + 11) * math.cos(a), cy + (r_leaf + 11) * math.sin(a)
            rot = deg + 180 if flip else deg
            anchor = "end" if flip else "start"
            labels.append(f'<text transform="translate({tx:.1f},{ty:.1f}) rotate({rot:.1f})" '
                          f'text-anchor="{anchor}" dominant-baseline="middle" '
                          f'fill="{INK if ok else MUTED}" font-weight="{700 if ok else 400}">{esc(title)}</text>')
        k = sum(ok for _, ok, _p, _f in c["items"])
        nodes.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="36" fill="{CAT}"/>')
        words = c["name"].split()
        lines, line = [], ""
        for w in words:
            if len(line) + len(w) > 13 and line:
                lines.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        lines.append(line)
        lines.append(f"{k}/{n}")
        y0 = y1 - (len(lines) - 1) * 5.5
        for j, ln in enumerate(lines):
            w = "700" if j == len(lines) - 1 else "500"
            labels.append(f'<text x="{x1:.1f}" y="{y0 + j * 11:.1f}" text-anchor="middle" '
                          f'dominant-baseline="middle" fill="{BG}" font-size="9.5" font-weight="{w}">{esc(ln)}</text>')
        ang += span
    nodes.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="{HUB}"/>')
    labels.append(f'<text x="{cx}" y="{cy - 6}" text-anchor="middle" fill="{BG}" font-family="{DISPLAY}" font-size="12" font-weight="700">IE</text>')
    labels.append(f'<text x="{cx}" y="{cy + 9}" text-anchor="middle" fill="{BG}" font-size="10">Knowledgebase</text>')
    legend_y = size - 28
    parts.append(f'<circle cx="30" cy="{legend_y}" r="6" fill="{DONE}"/>'
                 f'<text x="42" y="{legend_y + 4}" fill="{INK}">built</text>'
                 f'<circle cx="100" cy="{legend_y}" r="4.5" fill="{BG}" stroke="{TODO}" stroke-width="1.5"/>'
                 f'<text x="112" y="{legend_y + 4}" fill="{INK}">not started</text>')
    return "\n".join(parts + edges + nodes + labels + ["</svg>"])


# ------------------------------------------------------------ interactive map

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def rel(path):
    return str(path).replace("\\", "/")


def category_table(slug):
    """Course README path -> (topic, length, status) from the category README table."""
    out = {}
    p = ROOT / "courses" / slug / "README.md"
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ["):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        m = LINK_RE.match(cells[0])
        if m and len(cells) >= 3:
            out[f"courses/{slug}/{m.group(2)}"] = (cells[1], cells[2], cells[3] if len(cells) > 3 else "")
    return out


def category_description(slug):
    p = ROOT / "courses" / slug / "README.md"
    if not p.exists():
        return ""
    for line in p.read_text(encoding="utf-8").splitlines()[1:]:
        if line.strip() and not line.startswith("#"):
            return line.strip()
    return ""


def module_summary(path, limit=220):
    """Topics line for a module whose syllabus row has none: its learning objectives
    joined with semicolons; else its section headings; else its first paragraph."""
    try:
        lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
    except OSError:
        print(f"warning: module file not found: {path}", file=sys.stderr)
        return "", "", 0
    items, grab, kind = [], False, "objectives"
    for line in lines:
        if re.match(r"^#+\s*(learning\s+)?objectives", line, re.I):
            grab = True
            continue
        if grab and line.startswith("#"):
            break
        if grab:
            m = re.match(r"^\s*(?:\d+[.)]|[-*])\s+(.+)", line)
            if m:
                items.append(m.group(1).strip())
    if not items:
        items = [re.sub(r"^\d+\.\s*", "", h[3:]).strip() for h in lines if h.startswith("## ")]
        kind = "sections"
    if not items:
        kind = "summary"
        for line in lines[1:]:
            s = line.strip()
            if s and not re.match(r"^(#|\||\*\*Time|\*\*Data|!|`|<|-|\*|\d+[.)])", s):
                items = [s]
                break
    def clean(s):
        s = LINK_RE.sub(r"\1", s)
        s = re.sub(r"(\*\*|\*|`)([^*`]+)\1", r"\2", s)
        s = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", s)
        return re.sub(r"[.;:]\s*$", "", s.strip())
    cleaned = [clean(i) for i in items if i]
    out = "; ".join(cleaned)
    if len(out) > limit:
        head = out[:limit]
        cut = head.rsplit(";", 1)[0] if ";" in head else head.rsplit(" ", 1)[0]
        out = cut.rstrip(" ;,") + " …"
    return out, kind, len(cleaned)


def course_info(readme_path):
    """Description, module rows, prerequisite and related course paths from a course README."""
    base = Path(readme_path).parent
    lines = (ROOT / readme_path).read_text(encoding="utf-8").splitlines()
    desc = ""
    for line in lines[1:]:
        s = line.strip()
        if s and not s.startswith(("#", "|", "**", "-", "!", "`")):
            desc = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", re.sub(r"(\*\*|\*)([^*]+)\1", r"\2", LINK_RE.sub(r"\1", s)))
            break
    modules = []
    time_idx = topics_idx = None
    for k, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        is_header = k + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}", lines[k + 1]) is not None
        if is_header and any("](modules/" in c for c in lines[k + 2:k + 4]):
            # header row of the syllabus table (the one whose rows link to modules/): learn which column holds time and which holds topics
            time_idx = topics_idx = None
            for i, c in enumerate(cells):
                if re.search(r"time|duration|length|hours", c, re.I):
                    time_idx = i
                elif re.search(r"body of knowledge|topics?|covers?|contents?|outline", c, re.I):
                    topics_idx = i
            continue
        if is_header or re.match(r"^\|\s*:?-{3,}", line):
            continue
        m = re.search(r"\[((?:[^\[\]]|\[[^\[\]]*\])+)\]\((modules/[^)\s]+)\)", line)
        if not m:
            continue
        note = cells[time_idx] if time_idx is not None and time_idx < len(cells) else ""
        topics = cells[topics_idx] if topics_idx is not None and topics_idx < len(cells) else ""
        if not note and not topics and len(cells) > 1 and "](" not in cells[-1]:
            last = cells[-1]
            if re.search(r"\d\s*(min|h\b|hour|day)", last):
                note = last
            else:
                topics = last
        mpath = rel(base / m.group(2))
        if topics:
            tkind, tcount = "topics", len([x for x in re.split(r"[;,·|]", topics) if x.strip()])
        else:
            topics, tkind, tcount = module_summary(mpath)
        modules.append({"title": m.group(1), "path": mpath, "note": note, "topics": topics, "tkind": tkind, "tcount": tcount})
    prereq, related = [], []
    for line in lines:
        is_prereq_line = bool(re.match(r"^\s*[-*]?\s*\**prerequisites?\b", line, re.I))
        # On a prerequisites line, links after "Helpful" are recommendations, not requirements.
        hard, soft = (re.split(r"helpful|helps?\b", line, maxsplit=1, flags=re.I) + [""])[:2] if is_prereq_line else ("", line)
        if is_prereq_line and re.match(r"^\s*\**prerequisites?:?\**\s*none\b", line, re.I):
            hard, soft = "", line   # "Prerequisites: none. X helps" — every link is a recommendation
        for part, bucket in ((hard, prereq), (soft, related)):
            for _label, href in LINK_RE.findall(part):
                if not href.startswith("../") or not href.endswith("/README.md"):
                    continue
                try:
                    target = rel((ROOT / base / href).resolve().relative_to(ROOT))
                except ValueError:
                    continue   # the link leaves the repository
                if target == rel(Path(readme_path)):
                    continue
                if target not in prereq and target not in related:
                    bucket.append(target)
    return desc, modules, prereq, related


def first_heading(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#\s+(.+)", line)
        if m:
            return LINK_RE.sub(r"\1", m.group(1)).strip()
    return path.stem


SITE_SOURCES = [
    ("IISE course catalog (public course titles and topic outlines)", "Used only as a map of what an industrial-engineering curriculum covers; the categories and topic names in ROADMAP.md follow it. No IISE material is used.", "https://www.iise.org/TrainingCenter/"),
    ("O*NET OnLine, Industrial Engineers 17-2112.00 (U.S. Department of Labor, ETA; CC BY 4.0)", "The occupational standard for the role advisor: rated tasks, knowledge, skills and technology.", "https://www.onetonline.org/link/summary/17-2112.00"),
    ("BLS Occupational Outlook Handbook, Industrial Engineers (U.S. government work)", "Outlook, pay, entry education, employers and demand drivers for the role advisor.", "https://www.bls.gov/ooh/architecture-and-engineering/industrial-engineers.htm"),
    ("Bootstrap Icons (MIT, The Bootstrap Authors)", "Interface and category icons, vendored under tools/icons/.", "https://github.com/twbs/icons"),
    ("D3 7.9.0, marked 12.0.2, DOMPurify 3.1.6, Mermaid 10.9.1, anime.js 4.5.0 (cdnjs)", "Mind map layout, Markdown rendering and sanitising, diagrams in the reader, and motion.", "https://cdnjs.com/"),
    ("Google Fonts: Inter, Space Grotesk, JetBrains Mono", "Typefaces.", "https://fonts.google.com/"),
]


def course_sources(readme_path):
    """Rows of reference/sources.md: [{id, text, used, cited, verified}] or [] when the course has none."""
    p = ROOT / Path(readme_path).parent / "reference" / "sources.md"
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| ID"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[0]:
            continue
        out.append({"id": cells[0], "text": cells[1], "used": cells[2], "cited": cells[3], "verified": cells[4].lower().startswith("y")})
    return out


def course_extras(readme_path):
    """Reference, solutions and template markdown files shipped with a course, for the reader's nav."""
    base = ROOT / Path(readme_path).parent
    out = []
    for pattern in ("reference/*.md", "solutions/README.md", "templates/*.md", "examples/*.md"):
        for f in sorted(base.glob(pattern)):
            out.append({"label": first_heading(f), "path": rel(f.relative_to(base))})
    return out


def build_model(cats):
    nodes = [{"id": "hub", "type": "hub", "label": "IE Knowledgebase"}]
    links = []
    by_path = {}
    pending = []  # (course node id, prereq paths, related paths)
    total_items = sum(len(c["items"]) for c in cats) or 1
    ang = -math.pi / 2
    for c in cats:
        slug = c["slug"] or slugify(c["name"])
        cid = "cat:" + slug
        span = 2 * math.pi * len(c["items"]) / total_items
        nodes.append({"id": cid, "type": "category", "label": c["name"], "a": round(ang + span / 2, 4),
                      "description": category_description(slug), "tag": c.get("tag", ""),
                      "icon": icon(CATEGORY_ICONS.get(slug, "list"), 18),
                      "path": f"courses/{slug}/README.md"})
        links.append({"source": "hub", "target": cid, "type": "tree"})
        table = category_table(slug)
        for i, (title, ok, path, folded) in enumerate(c["items"]):
            a = round(ang + span * (i + 0.5) / len(c["items"]), 4)
            if ok and path and folded:
                nid = "topic:" + slugify(title)
                nodes.append({"id": nid, "type": "topic", "label": title, "parent": cid, "a": a, "covered_path": path})
            elif ok and path:
                nid = "course:" + Path(path).parent.name
                if not (ROOT / path).exists():
                    sys.exit(f"ROADMAP.md links to a missing course README: {path}")
                topic, length, status = table.get(path, ("", "", ""))
                # Status cell: "draft" (AI-written, unreviewed) or "verified (Reviewer, YYYY-MM-DD)" per REVIEW.md
                verified = status.lower().startswith("verified")
                desc, modules, prereq, related = course_info(path)
                nodes.append({"id": nid, "type": "course", "label": title, "parent": cid, "path": path, "a": a,
                              "length": length, "description": desc, "search": topic, "extras": course_extras(path),
                              "verified": verified, "review": status if verified else "",
                              "sources": course_sources(path)})
                by_path[path] = nid
                pending.append((nid, prereq, related))
                for i, m in enumerate(modules):
                    mid = f"{nid}/{i}"
                    nodes.append({"id": mid, "type": "module", "label": m["title"], "parent": nid, "a": a,
                                  "path": m["path"], "note": m["note"], "topics": m["topics"],
                                  "tkind": m["tkind"], "tcount": m["tcount"]})
                    links.append({"source": nid, "target": mid, "type": "tree"})
            else:
                nid = "topic:" + slugify(title)
                nodes.append({"id": nid, "type": "topic", "label": title, "parent": cid, "a": a})
            links.append({"source": cid, "target": nid, "type": "tree"})
        ang += span
    seen = set()
    for nid, prereq, related in pending:
        for tp in prereq:
            src = by_path.get(tp)
            if src and (src, nid) not in seen:
                links.append({"source": src, "target": nid, "type": "prereq"})
                seen.add((src, nid))
    for nid, prereq, related in pending:
        for tp in related:
            other = by_path.get(tp)
            if not other:
                continue
            key = tuple(sorted((other, nid)))
            if key in seen or (other, nid) in seen or (nid, other) in seen:
                continue
            links.append({"source": nid, "target": other, "type": "related"})
            seen.add(key)
    for n in nodes:
        if n.get("covered_path"):
            n["covered"] = by_path.get(n.pop("covered_path"))
    ids = [n["id"] for n in nodes]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        sys.exit(f"duplicate node ids (same course folder name or topic title in two places?): {dupes}")
    total = sum(len(c["items"]) for c in cats)
    built = sum(1 for c in cats for _, ok, _p, f in c["items"] if ok and not f)
    covered = sum(1 for c in cats for _, ok, _p, f in c["items"] if ok and f)
    verified = sum(1 for n in nodes if n["type"] == "course" and n.get("verified"))
    return {"repo": REPO_URL, "total": total, "built": built, "covered": covered, "verified": verified, "nodes": nodes, "links": links, "tracks": read_tracks(nodes)}


def read_tracks(nodes):
    """roles/tracks.md: '## name', a **Goal:** line, an optional **Role:** line, then a numbered list of course folder names."""
    path = ROOT / "roles" / "tracks.md"
    if not path.exists():
        return []
    by_slug = {n["id"].split(":", 1)[1]: n["id"] for n in nodes if n["type"] == "course"}
    tracks = []
    for block in re.split(r"^## ", path.read_text(encoding="utf-8"), flags=re.M)[1:]:
        name, _, body = block.partition("\n")
        goal = re.search(r"^\*\*Goal:\*\*\s*(.+)$", body, re.M)
        role = re.search(r"^\*\*Role:\*\*\s*(.+)$", body, re.M)
        outlook = re.search(r"^\*\*Outlook:\*\*\s*(.+)$", body, re.M)
        source = re.search(r"^\*\*Source:\*\*\s*<?([^\s>]+)>?\s*(?:\((.+)\))?\s*$", body, re.M)
        if source and not re.match(r"https?://", source.group(1)):
            sys.exit(f"roles/tracks.md: track '{name.strip()}' has a Source that is not an http(s) URL: {source.group(1)}")
        slugs = re.findall(r"^\d+\.\s+([a-z0-9-]+)\s*$", body, re.M)
        missing = [s for s in slugs if s not in by_slug]
        if missing:
            sys.exit(f"roles/tracks.md: track '{name.strip()}' names courses that do not exist: {missing}")
        if len(slugs) < 2:
            sys.exit(f"roles/tracks.md: track '{name.strip()}' needs at least two courses")
        tracks.append({"id": "track:" + slugify(name.strip()), "label": name.strip(), "goal": goal.group(1).strip() if goal else "",
                       "role": "" if not role or role.group(1).strip().lower().startswith("none") else role.group(1).strip(),
                       "outlook": outlook.group(1).strip() if outlook else "", "source": source.group(1) if source else "", "sourceLabel": (source.group(2) or "").strip() if source else "",
                       "courses": [by_slug[s] for s in slugs]})
    return tracks


def write(path, text):
    """Write with LF line endings so the output is identical on Windows and Linux."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def fill(template_path, **slots):
    # Icons go into the template before the slots: course data must never be scanned for __ICON__
    # placeholders, or a label containing one would break the JSON it sits in.
    tpl = inject_logo(inject_icons(inject_hubnav(inject_footer(template_path.read_text(encoding="utf-8")))))
    for key, value in slots.items():
        marker = f"__{key}__"
        n = tpl.count(marker)
        assert n >= 1 and (key != "DATA" or n == 1), f"{template_path.name}: {marker} found {n} times"
        tpl = tpl.replace(marker, value)
    return tpl


def canonical(html, path):
    """Add <link rel="canonical"> after the title, so copies of a page (theiehub.pages.dev, /page.html) point to one URL."""
    return html.replace("</title>", f'</title>\n<link rel="canonical" href="{SITE}/{path}">', 1)


# The home page's WebSite structured data: how Google picks the site name it shows in results.
# https://developers.google.com/search/docs/appearance/site-names
SITE_NAME_LD = ('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "WebSite", '
                f'"name": "The IE Hub", "alternateName": ["IE Hub", "theiehub.com"], "url": "{SITE}/"}}</script>\n')


def write_seo(model):
    """public/robots.txt and public/sitemap.xml: every page, every built course and every module. No lastmod, so the
    files only change when pages are added or removed (and the CI check on public/ stays stable)."""
    write(PUBLIC / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = [f"{SITE}/", f"{SITE}/learn", f"{SITE}/roadmap", f"{SITE}/sources", f"{SITE}/privacy", f"{SITE}/terms"]
    for c in (n for n in model["nodes"] if n["type"] == "course"):
        slug, root = c["id"][7:], c["path"].rsplit("/", 1)[0]
        urls.append(f"{SITE}/course?c={slug}")
        urls += [f"{SITE}/course?c={slug}&amp;f={urllib.parse.quote(m['path'][len(root) + 1:], safe='')}"
                 for m in model["nodes"] if m["type"] == "module" and m["parent"] == c["id"]]
    write(PUBLIC / "sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    return len(urls)


def lint_templates():
    """Checkpoint: content inside a page column keeps one width. No rule may narrow the text
    (max-width on a descendant of .doc, .page or main) while tables and figures keep the column,
    because that produces two right edges. Fails the build so it cannot regress unnoticed."""
    checks = [(READER_TEMPLATE, r"\.doc\s+[a-z0-9.,#:\- ]+\{[^}]*max-width:\s*\d+(ch|px|em|rem)"),
              (TEMPLATE, r"\.page\s+[a-z0-9.,#:\- ]+\{[^}]*max-width:\s*\d+(ch|px|em|rem)"),
              # the home template does not prefix selectors with .page, so any text-unit max-width on a rule is a narrowed column
              (TEMPLATE, r"\.[a-z0-9.,#:\- ]+\{[^}]*max-width:\s*\d+(ch|em|rem)"),
              (LEGAL_TEMPLATE, r"main\s+[a-z0-9.,#:\- ]+\{[^}]*max-width:\s*\d+(ch|px|em|rem)")]
    for path, pattern in checks:
        css = path.read_text(encoding="utf-8")
        hit = re.search(pattern, css)
        if hit:
            sys.exit(f"{path.name}: a rule narrows content inside the column: {hit.group(0)[:80]!r}. Keep one width per column (set it on .doc / .page / main only).")


def sources_page(model):
    """Body of public/sources.html: what the site rests on, then every course's sources table."""
    def h(s):
        return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    def md_inline(s):
        s = h(s)
        s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"&lt;(https?://[^&]+)&gt;", r'<a href="\1" rel="noopener">\1</a>', s)
        return s
    courses = [n for n in model["nodes"] if n["type"] == "course"]
    with_src = [c for c in courses if c.get("sources")]
    total = sum(len(c["sources"]) for c in with_src)
    ver = sum(1 for c in with_src for s in c["sources"] if s["verified"])
    parts = ['<div class="eyebrow">cat sources.html</div>', "<h1>Sources</h1>",
             f'<div class="meta">What the site and each course rest on · {len(with_src)} of {len(courses)} courses have a sources table · {ver} of {total} entries verified</div>',
             '<div class="box"><b>How to read this.</b> A source is listed because the course used it; <em>verified</em> means a reviewer has checked the edition and that the course uses it accurately. Until then it is a pointer. Courses without a table yet still carry a further-reading list in their reference folder. Inside a course, modules cite an entry by its ID, for example (montgomery-8e, ch. 6).</div>',
             '<nav class="toc" aria-label="On this page"><a href="#site">The site</a>' + "".join(f'<a href="#{h(c["id"][7:])}">{h(c["label"])}</a>' for c in with_src) + "</nav>",
             '<h2 id="site">The site</h2>', "<table><tr><th>Source</th><th>Used for</th></tr>"]
    for name, used, url in SITE_SOURCES:
        parts.append(f'<tr><td><a href="{url}" rel="noopener">{h(name)}</a></td><td>{h(used)}</td></tr>')
    parts.append("</table>")
    parts.append('<p class="small">O*NET is a trademark of the U.S. Department of Labor, Employment and Training Administration. This site is not affiliated with or endorsed by USDOL/ETA, BLS or IISE.</p>')
    for c in with_src:
        n = len(c["sources"]); k = sum(1 for s in c["sources"] if s["verified"])
        parts.append(f'<h2 id="{h(c["id"][7:])}">{h(c["label"])}</h2>')
        parts.append(f'<div class="meta">{k} of {n} verified · <a href="course.html?c={h(c["id"][7:])}&amp;f=reference%2Fsources.md">open in the course</a></div>')
        parts.append("<table><tr><th>ID</th><th>Source</th><th>Used for</th><th>Cited in</th><th>Verified</th></tr>")
        for s in c["sources"]:
            parts.append(f'<tr><td><code>{h(s["id"])}</code></td><td>{md_inline(s["text"])}</td><td>{h(s["used"])}</td><td>{h(s["cited"])}</td><td>{"yes" if s["verified"] else "no"}</td></tr>')
        parts.append("</table>")
    return "\n".join(parts)


def fill_counts(text, model):
    """Fill __COURSES__, __MODULES__, __VERIFIED__, __COVERED__, __TOTAL__ and __OPEN__ from the course model."""
    modules = sum(1 for n in model["nodes"] if n["type"] == "module")
    covered = model["built"] + model["covered"]
    for k, v in {"COURSES": model["built"], "MODULES": modules, "VERIFIED": model["verified"], "COVERED": covered,
                 "TOTAL": model["total"], "OPEN": model["total"] - covered}.items():
        text = text.replace(f"__{k}__", str(v))
    return text


def write_html(cats):
    lint_templates()
    model = build_model(cats)
    enc = lambda m: json.dumps(m, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
    write(HTML_OUT, canonical(fill(TEMPLATE, DATA=enc(model)), "learn"))
    # The reader parses this on every page open, so it carries only what the reader reads: courses, modules and categories, no topics or links.
    keep = ("id", "type", "parent", "path", "label", "note", "tcount", "tkind", "extras", "length", "verified", "review")
    slim = {"repo": model["repo"], "nodes": [{k: n[k] for k in keep if k in n} for n in model["nodes"] if n["type"] in ("course", "module", "category")]}
    write(READER_OUT, fill(READER_TEMPLATE, DATA=enc(slim)))
    for key, title in LEGAL_PAGES.items():
        # hand-written bodies may use icons; the sources page is built from course tables, so it is not scanned
        if key == "sources":
            body = sources_page(model)
        else:
            body = (ROOT / "tools" / "legal" / f"{key}.html").read_text(encoding="utf-8")
            if key == "roadmap":
                for k, v in roadmap_parts().items():
                    body = body.replace(f"__{k}__", v)
            body = inject_icons(body)
        body = fill_counts(body, model)
        write(PUBLIC / f"{key}.html", canonical(fill(LEGAL_TEMPLATE, TITLE=f"{title} · The IE Hub", DESC=f"{title} for The IE Hub, free and open industrial engineering courses.",
                                           PATH=f"{key}.html", NAV=hubnav_html("roadmap" if key == "roadmap" else ""), MAIN_ATTR="", HEAD_SCRIPT="", BODY=body), key))
    # The hub home. Old catalog links (/#course:…, /#tab=…, /index.html#…) carry a fragment the server never sees,
    # so a script in the head forwards any fragment that is not one of this page's own anchors to learn.html.
    forward = ("<script>(function () { const h = location.hash.slice(1); "
               "if (h && !['main', 'hero', 'why', 'pillars', 'audiences', 'where'].includes(h)) location.replace('learn.html' + location.hash); })();</script>")
    write(HUB_OUT, canonical(fill(LEGAL_TEMPLATE, TITLE="The IE Hub · industrial engineering, learned and built in the open",
                        DESC="Free, open industrial engineering: original courses with data you can rerun, a learning path, a mind map of the field, and worked projects and insights on the way.",
                        PATH="", NAV=hubnav_html(), MAIN_ATTR=' class="wide"', HEAD_SCRIPT=SITE_NAME_LD + forward, BODY=fill_counts(inject_icons(hub_page(model)), model)), ""))
    return model


if __name__ == "__main__":
    PUBLIC.mkdir(exist_ok=True)
    cats = parse(SRC.read_text(encoding="utf-8"))
    write(OUT, render(cats))
    print(f"wrote {OUT.relative_to(ROOT)}: {sum(len(c['items']) for c in cats)} courses in {len(cats)} categories")
    model = write_html(cats)
    print(f"wrote {READER_OUT.relative_to(ROOT)} and {HUB_OUT.relative_to(ROOT)}")
    print(f"wrote public/robots.txt and public/sitemap.xml: {write_seo(model)} URLs")
    kinds, edges = {}, {}
    for n in model["nodes"]:
        kinds[n["type"]] = kinds.get(n["type"], 0) + 1
    for l in model["links"]:
        edges[l["type"]] = edges.get(l["type"], 0) + 1
    print(f"wrote {HTML_OUT.relative_to(ROOT)}: nodes {kinds}, edges {edges}")
