"""Builds the SVG tiles used in the profile README (design v2).

    python scripts/build.py

Edit the data below (stats, projects, wins, experience) and re-run to update the tiles.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
INK, PAPER, EDGE = "#0b0b0c", "#f3efe4", "#2c2c31"
LIME, BLUE, ORANGE, LILAC = "#c9ff3a", "#3d5afe", "#ff5a2c", "#cdbdff"
# palette used inside the light project cards
BG, CARD2, LINE, FG, SOFT, MUTED = PAPER, "#e4dfd0", "#bdb7a6", INK, INK, "#5d5a52"
GREEN, GOLD, PINK = "#0e9f5a", "#e09600", "#e0368c"

BASE_CSS = (
    ".s{font-family:" + SANS + "}.m{font-family:" + MONO + "}"
    "@keyframes sp{to{transform:rotate(360deg)}}@keyframes pl{50%{opacity:.25}}"
    "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def svg(name, w, h, body, css="", defs="", label=""):
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
        f"<title>{esc(label)}</title><defs>{defs}</defs><style>{BASE_CSS}{css}</style>{body}</svg>"
    )
    (OUT / name).write_text(doc, encoding="utf-8")


def tile(x, y, w, h, fill, shadow, r=28):
    stroke = EDGE if fill == INK else INK
    return (f'<rect x="{x + 6}" y="{y + 6}" width="{w}" height="{h}" rx="{r}" fill="{shadow}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')


def arrow(x, y, c, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M0 12 L12 0 M3 0 H12 V9"/></g>')


def star(cx, cy, r, fill, points=8, inner=.55):
    import math
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * inner
        a = math.pi * i / points
        pts.append(f"{cx + rr * math.sin(a):.1f},{cy - rr * math.cos(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'


# ───────────────────────────── hero ─────────────────────────────
def hero():
    css = (
        ".spin{transform-origin:660px 326px;animation:sp 14s linear infinite}"
        ".st{transform-origin:716px 76px;animation:sp 9s linear infinite reverse}"
        ".bn{animation:bn 1.4s cubic-bezier(.5,0,.5,1) infinite alternate}@keyframes bn{to{transform:translateY(-34px)}}"
        ".bk{animation:bk 1.1s steps(1) infinite}@keyframes bk{50%{opacity:0}}"
    )
    defs = '<path id="circ" d="M660 326 m-45 0 a45 45 0 1 1 90 0 a45 45 0 1 1 -90 0"/>'
    left = (
        tile(8, 8, 776, 418, LIME, BLUE, 36)
        + f'<text x="46" y="66" class="m" font-size="13" font-weight="700" letter-spacing="2.2" fill="{INK}">AI/ML ENGINEER · HYDERABAD, IN</text>'
        + f'<text x="40" y="232" class="s" font-size="150" font-weight="900" textLength="690" lengthAdjust="spacingAndGlyphs" fill="{INK}">NIKSHITH</text>'
        + f'<text x="40" y="372" class="s" font-size="150" font-weight="900" textLength="470" lengthAdjust="spacingAndGlyphs" fill="{INK}">NOOKA</text>'
        + f'<g class="st">{star(716, 76, 30, BLUE)}</g>'
        + f'<circle cx="660" cy="326" r="64" fill="{INK}"/>'
        + f'<g class="spin"><text class="m" font-size="12.5" font-weight="700" letter-spacing="2.1" fill="{LIME}"><textPath href="#circ" textLength="276">OPEN TO INTERNSHIPS · RESEARCH ·</textPath></text></g>'
        + arrow(650, 316, LIME, 1.7)
    )
    lines = ["Building", "reliable AI for", "healthcare,", "public services", "& cities."]
    right = tile(806, 8, 380, 418, INK, ORANGE, 36)
    for i, t in enumerate(lines):
        right += f'<text x="838" y="{84 + i * 42}" class="s" font-size="33" font-weight="800" letter-spacing="-.8" fill="{PAPER if i != 1 else LIME}">{esc(t)}</text>'
    right += f'<rect class="bk" x="978" y="226" width="16" height="30" fill="{ORANGE}"/>'
    right += (f'<circle class="bn" cx="866" cy="346" r="24" fill="{LIME}"/>'
              f'<rect class="bn" style="animation-delay:.25s" x="916" y="322" width="48" height="48" rx="8" fill="{BLUE}"/>'
              f'<polygon class="bn" style="animation-delay:.5s" points="1020,320 1048,370 992,370" fill="{ORANGE}"/>'
              f'<circle class="bn" style="animation-delay:.75s" cx="1100" cy="346" r="24" fill="none" stroke="{LILAC}" stroke-width="8"/>')
    right += f'<path d="M838 378 H1154" stroke="{EDGE}" stroke-width="2"/>'
    right += f'<text x="838" y="402" class="m" font-size="11.5" letter-spacing="1.6" fill="#9a978e">B.TECH CSE (AI &amp; ML) · CLASS OF 2027</text>'
    svg("hero.svg", 1200, 440, left + right, css, defs,
        "Nikshith Nooka, AI/ML engineer in Hyderabad. Building reliable AI for healthcare, public services and cities. Open to internships and research.")


# ───────────────────────────── marquee band ─────────────────────────────
def band():
    phrase = "8× HACKATHON WINNER  ★  GOOGLE CAMPUS AMBASSADOR  ★  CGPA 9.46  ★  20K+ STUDENT COMMUNITY  ★  AI DEVELOPER INTERN @ MONDEETECH  ★"
    L = 2050
    css = f".mq{{animation:mq 30s linear infinite}}@keyframes mq{{to{{transform:translateX(-{L + 40}px)}}}}"
    defs = '<clipPath id="c"><rect x="8" y="8" width="1178" height="64" rx="32"/></clipPath>'
    t = "".join(
        f'<text x="{k * (L + 40) + 30}" y="52" class="s" font-size="30" font-weight="900" textLength="{L}" lengthAdjust="spacing" fill="#fff" xml:space="preserve">{esc(phrase)}</text>'
        for k in range(2))
    body = (tile(8, 8, 1178, 64, BLUE, LIME, 32) + f'<g clip-path="url(#c)"><g class="mq">{t}</g></g>'
            + f'<rect x="8" y="8" width="1178" height="64" rx="32" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    svg("band.svg", 1200, 86, body, css, defs, "8x hackathon winner. Google Campus Ambassador. CGPA 9.46. 20K+ student community. AI Developer Intern at MondeeTech.")


# ───────────────────────────── stats ─────────────────────────────
def stats():
    tiles = [
        ("HACKATHON WINS", "8×", "national + international", PAPER, BLUE, INK, INK),
        ("CGPA", "9.46", "B.Tech CSE (AI & ML)", INK, LIME, LIME, PAPER),
        ("COMMUNITY", "20K+", "students at The Student Spot", ORANGE, PAPER, INK, INK),
        ("TAUGHT", "200+", "students in AI & Cloud workshops", LILAC, ORANGE, INK, INK),
    ]
    css = ".w{transform-box:fill-box;transform-origin:center;animation:w 3s ease-in-out infinite}@keyframes w{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}"
    body = ""
    for i, (label, num, sub, fill, shadow, numc, textc) in enumerate(tiles):
        x = 8 + i * 300
        body += tile(x, 8, 278, 190, fill, shadow)
        body += f'<text x="{x + 26}" y="46" class="m" font-size="12" font-weight="700" letter-spacing="1.8" fill="{textc}">{label}</text>'
        body += f'<text x="{x + 22}" y="134" class="s" font-size="88" font-weight="900" letter-spacing="-4" fill="{numc}">{num}</text>'
        body += f'<text x="{x + 26}" y="168" class="s" font-size="13.5" font-weight="600" fill="{textc}" opacity=".75">{esc(sub)}</text>'
        sx, sy = x + 236, 42
        if i == 0:
            body += f'<g class="w">{star(sx, sy, 20, ORANGE, 5, .45)}</g>'
        elif i == 1:
            body += f'<g class="w"><circle cx="{sx}" cy="{sy}" r="17" fill="none" stroke="{LIME}" stroke-width="6" stroke-dasharray="96 12" transform="rotate(-90 {sx} {sy})"/></g>'
        elif i == 2:
            body += f'<g class="w"><circle cx="{sx - 10}" cy="{sy}" r="12" fill="{INK}"/><circle cx="{sx + 8}" cy="{sy}" r="12" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/></g>'
        else:
            body += f'<g class="w"><rect x="{sx - 17}" y="{sy - 17}" width="34" height="34" rx="6" fill="{BLUE}" stroke="{INK}" stroke-width="2.5"/></g>'
    svg("stats.svg", 1200, 212, body, css, "", "8 hackathon wins. CGPA 9.46. 20K+ student community. 200+ students taught.")


# ───────────────────────────── project art ─────────────────────────────
def m_layers(c):
    names = ["GROUNDING", "SAFETY", "CONSISTENCY", "ATTENDING REVIEW"]
    out = ""
    for i, n in enumerate(names):
        y = 34 + i * 34
        out += (f'<rect x="352" y="{y}" width="208" height="24" rx="7" fill="{CARD2}" stroke="{INK}" stroke-width="1.5"/>'
                f'<rect class="fill f{i}" x="352" y="{y}" width="208" height="24" rx="7" fill="{c}" opacity=".3"/>'
                f'<text x="364" y="{y + 16}" class="m" font-size="10" font-weight="700" letter-spacing="1" fill="{INK}">{n}</text>'
                f'<path class="ck f{i}" d="M538 {y + 12} l4 4 l8 -8" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    css = (".fill{transform-box:fill-box;transform-origin:left;animation:sweep 7s ease-in-out infinite}"
           ".ck{animation:ck 7s ease-in-out infinite}"
           "@keyframes sweep{0%,5%{transform:scaleX(0)}22%,88%{transform:scaleX(1)}100%{transform:scaleX(0)}}"
           "@keyframes ck{0%,18%{opacity:0}26%,88%{opacity:1}100%{opacity:0}}"
           + "".join(f".f{i}{{animation-delay:{i * .7:.1f}s}}" for i in range(4)))
    return out, css


def m_rag(c):
    out = ""
    for i, y in enumerate((34, 80, 126)):
        out += (f'<rect x="352" y="{y}" width="32" height="38" rx="5" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
                f'<path d="M359 {y + 11} h18 M359 {y + 19} h18 M359 {y + 27} h11" stroke="{MUTED}" stroke-width="2" stroke-linecap="round"/>'
                f'<path class="flow" style="animation-delay:{i * .4:.1f}s" d="M388 {y + 19} C 420 {y + 19}, 420 99, 452 99" fill="none" stroke="{c}" stroke-width="2.2"/>')
    out += (f'<circle cx="470" cy="99" r="20" fill="#fff" stroke="{INK}" stroke-width="2"/>'
            f'<circle class="tw" cx="470" cy="99" r="8" fill="{c}"/>'
            f'<path class="flow" d="M492 99 H524" fill="none" stroke="{c}" stroke-width="2.2"/>'
            f'<rect x="526" y="82" width="34" height="34" rx="10" fill="{c}" stroke="{INK}" stroke-width="2"/>'
            f'<path d="M535 99 l6 6 l11 -12" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="470" y="140" text-anchor="middle" class="m" font-size="9.5" font-weight="700" letter-spacing="1" fill="{MUTED}">EVIDENCE</text>'
            f'<text x="543" y="140" text-anchor="middle" class="m" font-size="9.5" font-weight="700" letter-spacing="1" fill="{MUTED}">ANSWER</text>')
    css = ".flow{stroke-dasharray:5 7;animation:fl 1.2s linear infinite}@keyframes fl{to{stroke-dashoffset:-24}}.tw{animation:pl 2s ease-in-out infinite}"
    return out, css


def m_globe(c):
    cx, cy, r = 458, 98, 66
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" fill-opacity=".16" stroke="{INK}" stroke-width="2"/>'
    for ry in (22, 46):
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}" fill="none" stroke="{c}" stroke-opacity=".6"/>'
    for begin in (0, -2, -4):
        out += (f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="none" stroke="{c}" stroke-opacity=".8">'
                f'<animate attributeName="rx" values="{r};0;{r}" dur="6s" begin="{begin}s" repeatCount="indefinite"/></ellipse>')
    for (x, y, col, d) in ((430, 78, ORANGE, 0), (486, 112, BLUE, .7), (452, 132, PINK, 1.3)):
        out += (f'<circle cx="{x}" cy="{y}" r="5" fill="{col}" stroke="{INK}" stroke-width="1.5"/>'
                f'<circle class="ping" style="animation-delay:{d}s" cx="{x}" cy="{y}" r="5" fill="none" stroke="{col}" stroke-width="2"/>')
    css = ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}@keyframes ping{to{transform:scale(4);opacity:0}}"
    return out, css


def m_traffic(c):
    hs, vs = (48, 98, 148), (384, 456, 528)
    out = ""
    for y in hs:
        out += f'<path d="M350 {y} H562" stroke="{INK}" stroke-width="11" stroke-linecap="round"/><path d="M350 {y} H562" stroke="{PAPER}" stroke-dasharray="5 9"/>'
    for x in vs:
        out += f'<path d="M{x} 30 V166" stroke="{INK}" stroke-width="11" stroke-linecap="round"/><path d="M{x} 30 V166" stroke="{PAPER}" stroke-dasharray="5 9"/>'
    cars = [("M350 48 H562", LIME, 5, 0), ("M562 98 H350", ORANGE, 6.5, -2), ("M350 148 H562", LIME, 4.2, -1),
            ("M384 30 V166", "#fff", 5.5, -3), ("M456 166 V30", LIME, 4.6, -1.5), ("M528 30 V166", ORANGE, 6, -4)]
    for p, col, dur, begin in cars:
        out += f'<circle r="4.6" fill="{col}"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{p}"/></circle>'
    return out, ""


def m_paw(c):
    cx, cy = 458, 104
    out = f'<g fill="{c}" stroke="{INK}" stroke-width="2">'
    out += f'<path d="M{cx} {cy - 6} c-22 0 -36 16 -36 30 c0 12 10 18 20 18 c8 0 10 -4 16 -4 s8 4 16 4 c10 0 20 -6 20 -18 c0 -14 -14 -30 -36 -30z"/>'
    for dx, dy, rx, ry, rot in ((-40, -18, 10, 14, -25), (-15, -40, 10, 15, -8), (15, -40, 10, 15, 8), (40, -18, 10, 14, 25)):
        out += f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx + dx} {cy + dy})"/>'
    out += "</g>"
    x0, x1, y0, y1 = 376, 540, 30, 168
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        out += f'<path d="M{x} {y + 16 * sy} V{y} H{x + 16 * sx}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
    out += f'<rect class="scan" x="{x0 + 6}" y="{y0}" width="{x1 - x0 - 12}" height="3" rx="1" fill="{INK}"/>'
    css = ".scan{animation:scan 3s ease-in-out infinite alternate}@keyframes scan{to{transform:translateY(136px)}}"
    return out, css


def m_orbit(c):
    cx, cy = 458, 98
    out = ""
    for i, (r, dash, dur) in enumerate(((44, "2 6", 18), (58, "10 8", 26), (72, "1 7", 40))):
        out += (f'<circle class="rg" style="transform-origin:{cx}px {cy}px;animation-duration:{dur}s{";animation-direction:reverse" if i == 1 else ""}" '
                f'cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-opacity="{.8 - i * .2:.2f}" stroke-width="1.5" stroke-dasharray="{dash}"/>')
    out += f'<circle cx="{cx}" cy="{cy}" r="28" fill="{c}" stroke="{INK}" stroke-width="2"/><path d="M{cx - 24} {cy - 6} q24 12 48 -4" fill="none" stroke="{INK}" stroke-opacity=".35" stroke-width="1.5"/>'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="92" ry="30" fill="none" stroke="{INK}" stroke-opacity=".4" transform="rotate(-18 {cx} {cy})"/>'
    out += (f'<g transform="rotate(-18 {cx} {cy})"><rect x="-6" y="-6" width="12" height="12" rx="2" fill="{BLUE}" stroke="{INK}" stroke-width="1.5">'
            f'<animateMotion dur="7s" repeatCount="indefinite" path="M{cx - 92} {cy} a92 30 0 1 0 184 0 a92 30 0 1 0 -184 0"/></rect></g>')
    return out, ".rg{animation:sp linear infinite}"


PROJECTS = [
    ("govbench", "GovBench-Clinical", "CLINICAL AI · EVALUATION", None,
     ["A benchmark and clinician workbench that measures what each", "safety layer in a multi-agent clinical AI pipeline changes."],
     ["Python", "FastAPI", "React", "183 tests"], "#6a3dff", m_layers),
    ("govreason", "GovReasonRAG", "RAG · PUBLIC POLICY", None,
     ["Evidence-contracted RAG for Indian welfare schemes, built to", "avoid hallucinated eligibility rules and outdated answers."],
     ["FastAPI", "Next.js", "BM25 + dense", "LoRA"], "#00897b", m_rag),
    ("geosick", "GeoSick AI", "ON-DEVICE ML · HEALTH", "WINNER · DARKNETRIX + CODE SURFERS",
     ["Environmental health guidance that runs fully in the", "browser: private, offline-first, no server needed."],
     ["React", "ONNX Runtime Web", "PyTorch", "PWA"], "#0e9f5a", m_globe),
    ("marganetra", "MargaNetra", "GRAPH ML · SMART CITIES", None,
     ["A traffic decision-support system that models a city's", "road network with graph neural networks."],
     ["PyTorch GNN", "TypeScript", "React"], BLUE, m_traffic),
    ("petguide", "PetGuide AI", "MULTIMODAL · VET TRIAGE", "WINNER · NAV NIRMAN",
     ["Pet health triage with breed identification, wound", "scanning and tailored nutrition plans."],
     ["Gemini", "React", "TypeScript"], "#ff8fc7", m_paw),
    ("geotrace", "GeoTrace AI", "3D · ATMOSPHERIC DATA", None,
     ["Planetary atmospheric intelligence: environmental", "telemetry explored on an interactive 3D globe."],
     ["TypeScript", "WebGL", "Vite", "Gemini"], ORANGE, m_orbit),
]


def projects():
    for i, (slug, title, tag, award, desc, chips, c, motif) in enumerate(PROJECTS):
        art, css = motif(c)
        body = tile(8, 8, 578, 306, PAPER, c)
        body += (f'<rect x="30" y="30" width="38" height="26" rx="13" fill="{INK}"/>'
                 f'<text x="49" y="48" text-anchor="middle" class="m" font-size="12" font-weight="700" fill="{PAPER}">{i + 1:02d}</text>'
                 f'<text x="78" y="48" class="m" font-size="11.5" font-weight="700" letter-spacing="1.4" fill="{MUTED}">{esc(tag)}</text>')
        if award:
            w = round(len(award) * 7 + 40)
            body += (f'<rect x="30" y="68" width="{w}" height="24" rx="12" fill="{LIME}" stroke="{INK}" stroke-width="1.5"/>'
                     f'<text x="42" y="84" class="m" font-size="10.5" font-weight="700" letter-spacing="1" fill="{INK}">★ {esc(award)}</text>')
        body += art
        body += f'<text x="30" y="214" class="s" font-size="32" font-weight="900" letter-spacing="-1" fill="{INK}">{esc(title)}</text>'
        for k, line in enumerate(desc):
            body += f'<text x="30" y="{240 + k * 20}" class="s" font-size="14.5" font-weight="500" fill="{MUTED}">{esc(line)}</text>'
        x = 30
        for ch in chips:
            w = round(len(ch) * 7 + 20)
            body += (f'<rect x="{x}" y="274" width="{w}" height="22" rx="11" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
                     f'<text x="{x + w / 2}" y="289" text-anchor="middle" class="m" font-size="11.5" font-weight="600" fill="{INK}">{esc(ch)}</text>')
            x += w + 8
        body += f'<circle cx="552" cy="282" r="17" fill="{INK}"/>' + arrow(546, 276, PAPER)
        svg(f"p-{slug}.svg", 600, 328, body, css, "", f"{title}: {' '.join(desc)}")


# ───────────────────────────── wins ─────────────────────────────
WINS = [
    ("Paranox 2.0", "1ST PLACE", "Duality AI · New Delhi", "1"),
    ("HACK-A-THON 1.0", "3RD PLACE", "eHRS · international", "3"),
    ("Darknetrix", "WINNER", "GeoSick AI", ""),
    ("Code Surfers", "WINNER", "GeoSick AI", ""),
    ("Aignite", "WINNER", "Performance Predictor", ""),
    ("Promptathon", "WINNER", "Ojas AI", ""),
    ("Build With AI", "WINNER", "VanRaksha", ""),
    ("Nav Nirman", "WINNER", "PetGuide AI", ""),
]


def wins():
    css = ".tr{transform-origin:190px 150px;animation:w 4s ease-in-out infinite}@keyframes w{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg)}}"
    body = tile(8, 8, 1178, 300, INK, LIME, 36)
    body += f'<text x="50" y="62" class="m" font-size="12" font-weight="700" letter-spacing="1.8" fill="#9a978e">HACKATHON RECORD</text>'
    body += f'<g class="tr"><text x="42" y="232" class="s" font-size="190" font-weight="900" letter-spacing="-8" fill="{LIME}">8×</text></g>'
    body += f'<text x="50" y="276" class="s" font-size="15" font-weight="600" fill="{PAPER}">wins, national + international</text>'
    for i, (name, res, proj, rank) in enumerate(WINS):
        col, row = divmod(i, 4)
        x, y = 372 + col * 408, 36 + row * 62
        if row:
            body += f'<path d="M{x} {y} H{x + 376}" stroke="{EDGE}" stroke-width="2"/>'
        cy = y + 31
        if rank:
            body += (f'<circle cx="{x + 20}" cy="{cy}" r="18" fill="{LIME}"/>'
                     f'<text x="{x + 20}" y="{cy + 7}" text-anchor="middle" class="s" font-size="19" font-weight="900" fill="{INK}">{rank}</text>')
        else:
            body += (f'<circle cx="{x + 20}" cy="{cy}" r="17" fill="none" stroke="{LIME}" stroke-width="2"/>'
                     f'<path d="M{x + 14} {cy} l4.2 4.4 l8 -9" fill="none" stroke="{LIME}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        body += f'<text x="{x + 52}" y="{cy - 1}" class="s" font-size="18.5" font-weight="800" fill="{PAPER}">{esc(name)}</text>'
        body += f'<text x="{x + 52}" y="{cy + 17}" class="m" font-size="11" fill="#9a978e">{esc(proj)}</text>'
        if rank:
            body += (f'<rect x="{x + 284}" y="{cy - 12}" width="92" height="24" rx="12" fill="{ORANGE}"/>'
                     f'<text x="{x + 330}" y="{cy + 4}" text-anchor="middle" class="m" font-size="10.5" font-weight="700" letter-spacing="1" fill="{INK}">{res}</text>')
        else:
            body += f'<text x="{x + 376}" y="{cy + 4}" text-anchor="end" class="m" font-size="10.5" font-weight="700" letter-spacing="1.2" fill="{LIME}">{res}</text>'
    svg("wins.svg", 1200, 322, body, css, "", "Hackathon record: 8 wins. 1st place at Paranox 2.0, 3rd place at HACK-A-THON 1.0, and wins at Darknetrix, Code Surfers, Aignite, Promptathon, Build With AI and Nav Nirman.")


# ───────────────────────────── stack marquee ─────────────────────────────
ROW1 = ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "LangChain", "Gemini", "Hugging Face", "ONNX Runtime", "Ollama", "OpenCV", "RAG", "Multi-agent systems", "LLM evals"]
ROW2 = ["TypeScript", "React", "Next.js", "Node.js", "FastAPI", "Tailwind CSS", "Three.js", "PostgreSQL", "MongoDB", "Supabase", "Firebase", "Docker", "GCP", "AWS", "Git"]


def stack():
    fills = ["#fff", LIME, "#fff", ORANGE, "#fff", PAPER]

    def row(items, y, k):
        x, parts = 0, ""
        for rep in range(2):
            for j, t in enumerate(items):
                w = round(len(t) * 8.6 + 36)
                parts += (f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="18" fill="{fills[(j + k) % 6]}" stroke="{INK}" stroke-width="2"/>'
                          f'<text x="{x + w / 2}" y="{y + 23}" text-anchor="middle" class="m" font-size="14" font-weight="700" fill="{INK}">{esc(t)}</text>')
                x += w + 10
        return parts, x // 2

    r1, t1 = row(ROW1, 26, 0)
    r2, t2 = row(ROW2, 74, 2)
    css = (f".r1{{animation:m1 42s linear infinite}}.r2{{animation:m2 48s linear infinite}}"
           f"@keyframes m1{{to{{transform:translateX(-{t1}px)}}}}@keyframes m2{{from{{transform:translateX(-{t2}px)}}to{{transform:translateX(0)}}}}")
    defs = '<clipPath id="c"><rect x="8" y="8" width="1178" height="120" rx="28"/></clipPath>'
    body = (tile(8, 8, 1178, 120, LILAC, BLUE) + f'<g clip-path="url(#c)"><g class="r1">{r1}</g><g class="r2">{r2}</g></g>'
            + f'<rect x="8" y="8" width="1178" height="120" rx="28" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    svg("stack.svg", 1200, 142, body, css, defs, "Tech stack: " + ", ".join(ROW1 + ROW2))


# ───────────────────────────── experience ─────────────────────────────
EXPERIENCE = [
    ("JUL 2026 – NOW", "AI Developer Intern", "MondeeTech Pvt. Ltd.", "VOICE AGENTS · FARE ANALYSIS", True),
    ("AUG – SEP 2026", "Full Stack Developer", "Studlyf", "FULL-STACK WEB APPS", False),
    ("FEB – MAY 2026", "ML Intern", "XYZON Technologies", "STUDENT-PERFORMANCE MODELS", False),
    ("JAN 2026 – NOW", "Operations & Community Lead", "The Student Spot", "20K+ COMMUNITY", True),
    ("SEP – NOV 2025", "Full Stack Developer Intern", "Swecha · open source", "300+ PATIENT RECORDS", False),
    ("COMPLETED", "Google Campus Ambassador", "Google", "200+ STUDENTS MENTORED", False),
]


def experience():
    n = len(EXPERIENCE)
    h = 112 + n * 56 + 16
    body = tile(8, 8, 1178, h, PAPER, ORANGE, 36)
    body += f'<text x="46" y="82" class="s" font-size="46" font-weight="900" letter-spacing="-2" fill="{INK}">Experience</text>'
    body += f'<text x="1150" y="78" text-anchor="end" class="m" font-size="12" font-weight="700" letter-spacing="1.8" fill="{MUTED}">{n} ROLES · 2025 – NOW</text>'
    for i, (period, role, org, note, now) in enumerate(EXPERIENCE):
        y = 112 + i * 56
        body += f'<path d="M46 {y} H1150" stroke="{INK}" stroke-width="2"/>'
        if now:
            body += f'<circle class="now" cx="56" cy="{y + 29}" r="6" fill="{GREEN}" stroke="{INK}" stroke-width="1.5"/>'
        body += f'<text x="{72 if now else 48}" y="{y + 34}" class="m" font-size="12.5" font-weight="700" letter-spacing="1" fill="{INK if now else MUTED}">{period}</text>'
        body += f'<text x="262" y="{y + 36}" class="s" font-size="21" font-weight="800" letter-spacing="-.4" fill="{INK}">{esc(role)}</text>'
        body += f'<text x="600" y="{y + 35}" class="s" font-size="16.5" font-weight="500" fill="{INK}">{esc(org)}</text>'
        w = round(len(note) * 7.3 + 26)
        body += (f'<rect x="{1150 - w}" y="{y + 16}" width="{w}" height="26" rx="13" fill="{INK if now else "#fff"}" stroke="{INK}" stroke-width="1.5"/>'
                 f'<text x="{1150 - w / 2}" y="{y + 33}" text-anchor="middle" class="m" font-size="11" font-weight="700" letter-spacing=".6" fill="{LIME if now else INK}">{esc(note)}</text>')
    svg("experience.svg", 1200, h + 22, body, ".now{animation:pl 1.8s ease-in-out infinite}", "",
        "Experience: " + "; ".join(f"{r} at {o} ({p})" for p, r, o, _, _ in EXPERIENCE))


# ───────────────────────────── contact buttons ─────────────────────────────
def contact():
    for slug, label, value, fill, shadow, textc in (("portfolio", "PORTFOLIO", "nnooka.netlify.app", LIME, BLUE, INK),
                                                    ("linkedin", "LINKEDIN", "in/nikshith-nooka", BLUE, LIME, "#fff"),
                                                    ("email", "EMAIL", "nikshithnooka@gmail.com", ORANGE, PAPER, INK)):
        body = (tile(8, 8, 378, 82, fill, shadow, 41)
                + f'<text x="40" y="42" class="m" font-size="11" font-weight="700" letter-spacing="1.8" fill="{textc}" opacity=".8">{label}</text>'
                + f'<text x="40" y="68" class="s" font-size="18.5" font-weight="800" fill="{textc}">{esc(value)}</text>'
                + f'<circle cx="344" cy="49" r="22" fill="{INK}"/>' + arrow(336, 41, "#fff", 1.3))
        svg(f"c-{slug}.svg", 400, 104, body, "", "", f"{label.title()}: {value}")


if __name__ == "__main__":
    hero(); band(); stats(); projects(); wins(); stack(); experience(); contact()
    print("built", len(list(OUT.glob("*.svg"))), "tiles in", OUT)
