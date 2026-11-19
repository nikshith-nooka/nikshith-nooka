"""Builds the SVG cards used in the profile README.

    python scripts/build.py

Edit the data below (stats, projects, wins, experience) and re-run to update the cards.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
BG, CARD2, LINE = "#0c0c11", "#15151d", "#262632"
FG, SOFT, MUTED = "#f5f5f7", "#c9c9d4", "#8a8a99"
GOLD, ORANGE, VIOLET, CYAN, GREEN, PINK = "#F7B733", "#ff7a45", "#8b7cf6", "#4fd1c5", "#3ddc84", "#f472b6"

BASE_CSS = (
    ".s{font-family:" + SANS + "}.m{font-family:" + MONO + "}"
    ".up{opacity:0;animation:up .9s cubic-bezier(.2,.8,.2,1) forwards}"
    "@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}"
    "@keyframes sp{to{transform:rotate(360deg)}}"
    "@keyframes pl{50%{opacity:.25}}"
    "@keyframes dash{to{stroke-dashoffset:0}}"
    "@media (prefers-reduced-motion: reduce){*{animation:none!important}.up{opacity:1}}"
)
COMMON_DEFS = (
    f'<linearGradient id="gg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{GOLD}"/>'
    f'<stop offset=".55" stop-color="{ORANGE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
    '<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.2" r="1.2" fill="#fff" opacity=".07"/></pattern>'
)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;")


def svg(name, w, h, body, css="", defs="", label=""):
    doc = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">'
        f"<title>{esc(label)}</title><defs>{COMMON_DEFS}{defs}</defs><style>{BASE_CSS}{css}</style>{body}</svg>"
    )
    (OUT / name).write_text(doc, encoding="utf-8")


def card(x, y, w, h, r=24, fill=BG):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{LINE}"/>'


def arrow(x, y, c=FG, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M0 12 L12 0 M3 0 H12 V9"/></g>')


# ───────────────────────────── hero ─────────────────────────────
def hero():
    cx, cy = 930, 228
    css = (
        ".b1{animation:f1 14s ease-in-out infinite alternate}.b2{animation:f2 18s ease-in-out infinite alternate}"
        ".b3{animation:f3 16s ease-in-out infinite alternate}"
        "@keyframes f1{to{transform:translate(140px,70px)}}@keyframes f2{to{transform:translate(-160px,-60px)}}"
        "@keyframes f3{to{transform:translate(80px,-110px)}}"
        f".o1,.o2,.o3{{transform-origin:{cx}px {cy}px}}"
        ".o1{animation:sp 22s linear infinite}.o2{animation:sp 34s linear infinite reverse}.o3{animation:sp 50s linear infinite}"
        ".pl{animation:pl 2s ease-in-out infinite}"
        ".core{animation:core 4s ease-in-out infinite}@keyframes core{50%{r:40px;opacity:.75}}"
    )
    defs = (
        '<clipPath id="c"><rect x="8" y="8" width="1184" height="440" rx="28"/></clipPath>'
        '<filter id="b" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="72"/></filter>'
        '<filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="14"/></filter>'
    )

    def ring(r, cls, dots, dash):
        d = "".join(
            f'<circle cx="{cx + r}" cy="{cy}" r="{s}" fill="{c}" transform="rotate({a} {cx} {cy})"/>' for a, c, s in dots)
        return (f'<g class="{cls}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity=".32" '
                f'stroke-dasharray="{dash}"/>{d}</g>')

    body = (
        card(8, 8, 1184, 440, 28)
        + '<g clip-path="url(#c)">'
        + f'<g filter="url(#b)" opacity=".55"><circle class="b1" cx="760" cy="80" r="170" fill="{VIOLET}"/>'
        + f'<circle class="b2" cx="1120" cy="380" r="190" fill="{ORANGE}"/><circle class="b3" cx="930" cy="300" r="120" fill="{GOLD}"/></g>'
        + '<rect x="8" y="8" width="1184" height="440" fill="url(#dots)"/>'
        + ring(92, "o1", [(0, GOLD, 6), (180, "#fff", 3)], "2 7")
        + ring(140, "o2", [(60, VIOLET, 7), (200, "#fff", 3), (310, CYAN, 4)], "1 9")
        + ring(188, "o3", [(120, ORANGE, 6), (250, "#fff", 3), (20, GOLD, 4)], "3 12")
        + f'<circle cx="{cx}" cy="{cy}" r="44" fill="url(#gg)" filter="url(#glow)" opacity=".8"/>'
        + f'<circle class="core" cx="{cx}" cy="{cy}" r="34" fill="url(#gg)"/>'
        + f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" class="m" font-size="15" font-weight="700" fill="{BG}">AI/ML</text>'
        + "</g>"
        # status pill
        + f'<g class="up"><rect x="56" y="46" width="326" height="34" rx="17" fill="#ffffff" fill-opacity=".06" stroke="#ffffff" stroke-opacity=".14"/>'
        + f'<circle class="pl" cx="76" cy="63" r="5" fill="{GREEN}"/>'
        + f'<text x="92" y="68" class="m" font-size="12.5" letter-spacing="1.4" fill="{SOFT}">OPEN TO INTERNSHIPS · RESEARCH</text></g>'
        # name
        + f'<text x="52" y="236" class="s up" style="animation-delay:.15s" font-size="124" font-weight="800" letter-spacing="-5" fill="{FG}">Nikshith</text>'
        + '<text x="52" y="352" class="s up" style="animation-delay:.3s" font-size="124" font-weight="800" letter-spacing="-5" fill="url(#gg)">Nooka</text>'
        + f'<text x="56" y="412" class="s up" style="animation-delay:.5s" font-size="20" fill="{SOFT}">Building reliable AI for healthcare, public services and cities.</text>'
        + f'<text x="1144" y="412" text-anchor="end" class="m up" style="animation-delay:.6s" font-size="12.5" letter-spacing="1.4" fill="{MUTED}">HYDERABAD · INDIA</text>'
    )
    svg("hero.svg", 1200, 456, body, css, defs, "Nikshith Nooka. Building reliable AI for healthcare, public services and cities. Open to internships and research.")


# ───────────────────────────── stats ─────────────────────────────
def stats():
    tiles = [
        ("HACKATHON WINS", "8", "national + international", GOLD),
        ("CGPA", "9.49", "B.Tech CSE (AI & ML) · 2027", VIOLET),
        ("COMMUNITY", "20K+", "students at The Student Spot", ORANGE),
        ("TAUGHT", "200+", "students in AI & Cloud workshops", CYAN),
    ]
    css = (
        ".bar{transform-box:fill-box;transform-origin:bottom;animation:grow 1.2s cubic-bezier(.2,.8,.2,1) both}"
        "@keyframes grow{from{transform:scaleY(0)}}"
        ".arc{stroke-dasharray:164;stroke-dashoffset:164;animation:arc 1.6s .3s ease-out forwards}@keyframes arc{to{stroke-dashoffset:8}}"
        ".tw{animation:pl 2.4s ease-in-out infinite}"
        ".sl{stroke-dasharray:120;stroke-dashoffset:120;animation:dash 1.8s .3s ease-out forwards}"
    )
    body = ""
    for i, (label, num, sub, c) in enumerate(tiles):
        x = 8 + i * 300
        g = card(x, 8, 284, 180) + f'<rect x="{x}" y="8" width="284" height="180" rx="24" fill="url(#dots)"/>'
        g += f'<text x="{x + 24}" y="44" class="m" font-size="12" letter-spacing="1.6" fill="{MUTED}">{label}</text>'
        g += f'<text x="{x + 22}" y="128" class="s" font-size="76" font-weight="800" letter-spacing="-3" fill="{FG}">{num}</text>'
        g += f'<text x="{x + 24}" y="162" class="s" font-size="13.5" fill="{MUTED}">{esc(sub)}</text>'
        dx, dy = x + 206, 28
        if i == 0:
            for k in range(8):
                hgt = 8 + k * 4.5
                g += (f'<rect class="bar" style="animation-delay:{k * .08:.2f}s" x="{dx + k * 7}" y="{dy + 44 - hgt:.1f}" width="4" height="{hgt:.1f}" rx="2" '
                      f'fill="{c}" opacity="{.35 + k * .09:.2f}"/>')
        elif i == 1:
            g += (f'<circle cx="{dx + 30}" cy="{dy + 22}" r="26" fill="none" stroke="{LINE}" stroke-width="6"/>'
                  f'<circle class="arc" cx="{dx + 30}" cy="{dy + 22}" r="26" fill="none" stroke="{c}" stroke-width="6" stroke-linecap="round" '
                  f'transform="rotate(-90 {dx + 30} {dy + 22})"/>')
        elif i == 2:
            for r in range(4):
                for k in range(6):
                    g += (f'<circle class="tw" style="animation-delay:{(r * 5 + k * 3) % 7 * .3:.1f}s" cx="{dx + 2 + k * 10}" cy="{dy + 4 + r * 11}" r="2.6" fill="{c}"/>')
        else:
            g += (f'<polyline class="sl" points="{dx - 4},{dy + 40} {dx + 8},{dy + 30} {dx + 18},{dy + 34} {dx + 30},{dy + 16} {dx + 42},{dy + 20} {dx + 56},{dy + 2}" '
                  f'fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
                  f'<circle class="tw" cx="{dx + 56}" cy="{dy + 2}" r="4" fill="{c}"/>')
        body += f'<g class="up" style="animation-delay:{i * .12:.2f}s">{g}</g>'
    svg("stats.svg", 1200, 196, body, css, "", "8 hackathon wins. CGPA 9.49. 20K+ student community. 200+ students taught.")


# ───────────────────────────── projects ─────────────────────────────
def m_layers(c):
    names = ["GROUNDING", "SAFETY", "CONSISTENCY", "ATTENDING REVIEW"]
    out = ""
    for i, n in enumerate(names):
        y = 34 + i * 34
        out += (f'<rect x="352" y="{y}" width="208" height="24" rx="7" fill="{CARD2}" stroke="{LINE}"/>'
                f'<rect class="fill f{i}" x="352" y="{y}" width="208" height="24" rx="7" fill="{c}" opacity=".22"/>'
                f'<text x="364" y="{y + 16}" class="m" font-size="10" letter-spacing="1" fill="{SOFT}">{n}</text>'
                f'<path class="ck f{i}" d="M538 {y + 12} l4 4 l8 -8" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
    css = (".fill{transform-box:fill-box;transform-origin:left;animation:sweep 7s ease-in-out infinite}"
           ".ck{animation:ck 7s ease-in-out infinite}"
           "@keyframes sweep{0%,5%{transform:scaleX(0)}22%,88%{transform:scaleX(1)}100%{transform:scaleX(0)}}"
           "@keyframes ck{0%,18%{opacity:0}26%,88%{opacity:1}100%{opacity:0}}"
           + "".join(f".f{i}{{animation-delay:{i * .7:.1f}s}}" for i in range(4)))
    return out, css


def m_rag(c):
    out = ""
    for i, y in enumerate((34, 80, 126)):
        out += (f'<rect x="352" y="{y}" width="32" height="38" rx="5" fill="{CARD2}" stroke="{LINE}"/>'
                f'<path d="M359 {y + 11} h18 M359 {y + 19} h18 M359 {y + 27} h11" stroke="{MUTED}" stroke-width="2" stroke-linecap="round"/>'
                f'<path class="flow" style="animation-delay:{i * .4:.1f}s" d="M388 {y + 19} C 420 {y + 19}, 420 99, 452 99" fill="none" stroke="{c}" stroke-width="1.8"/>')
    out += (f'<circle cx="470" cy="99" r="20" fill="{CARD2}" stroke="{c}" stroke-width="2"/>'
            f'<circle class="tw" cx="470" cy="99" r="7" fill="{c}"/>'
            f'<path class="flow" d="M492 99 H524" fill="none" stroke="{c}" stroke-width="1.8"/>'
            f'<rect x="526" y="82" width="34" height="34" rx="10" fill="{c}" fill-opacity=".16" stroke="{c}"/>'
            f'<path d="M535 99 l6 6 l11 -12" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="470" y="140" text-anchor="middle" class="m" font-size="9.5" letter-spacing="1" fill="{MUTED}">EVIDENCE</text>'
            f'<text x="543" y="140" text-anchor="middle" class="m" font-size="9.5" letter-spacing="1" fill="{MUTED}">ANSWER</text>')
    css = ".flow{stroke-dasharray:5 7;animation:fl 1.2s linear infinite}@keyframes fl{to{stroke-dashoffset:-24}}.tw{animation:pl 2s ease-in-out infinite}"
    return out, css


def m_globe(c):
    cx, cy, r = 458, 98, 66
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" fill-opacity=".06" stroke="{c}" stroke-opacity=".8" stroke-width="1.6"/>'
    for ry in (22, 46):
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}" fill="none" stroke="{c}" stroke-opacity=".28"/>'
    for i, begin in enumerate((0, -2, -4)):
        out += (f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="none" stroke="{c}" stroke-opacity=".45">'
                f'<animate attributeName="rx" values="{r};0;{r}" dur="6s" begin="{begin}s" repeatCount="indefinite"/></ellipse>')
    for (x, y, col, d) in ((430, 78, ORANGE, 0), (486, 112, GOLD, .7), (452, 132, PINK, 1.3)):
        out += (f'<circle cx="{x}" cy="{y}" r="4" fill="{col}"/>'
                f'<circle class="ping" style="animation-delay:{d}s" cx="{x}" cy="{y}" r="4" fill="none" stroke="{col}" stroke-width="1.5"/>')
    css = ".ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}@keyframes ping{to{transform:scale(4);opacity:0}}"
    return out, css


def m_traffic(c):
    hs, vs = (48, 98, 148), (384, 456, 528)
    out = ""
    for y in hs:
        out += f'<path d="M350 {y} H562" stroke="{LINE}" stroke-width="9" stroke-linecap="round"/><path d="M350 {y} H562" stroke="{MUTED}" stroke-opacity=".5" stroke-dasharray="5 9"/>'
    for x in vs:
        out += f'<path d="M{x} 30 V166" stroke="{LINE}" stroke-width="9" stroke-linecap="round"/><path d="M{x} 30 V166" stroke="{MUTED}" stroke-opacity=".5" stroke-dasharray="5 9"/>'
    for y in hs:
        for x in vs:
            out += f'<circle cx="{x}" cy="{y}" r="5.5" fill="{BG}" stroke="{c}" stroke-width="1.6"/>'
    cars = [("M350 48 H562", GREEN, 5, 0), ("M562 98 H350", GOLD, 6.5, -2), ("M350 148 H562", GREEN, 4.2, -1),
            ("M384 30 V166", ORANGE, 5.5, -3), ("M456 166 V30", GREEN, 4.6, -1.5), ("M528 30 V166", GOLD, 6, -4)]
    for p, col, dur, begin in cars:
        out += (f'<circle r="4.2" fill="{col}"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" path="{p}"/></circle>')
    return out, ""


def m_paw(c):
    cx, cy = 458, 104
    out = f'<g fill="{c}" fill-opacity=".14" stroke="{c}" stroke-width="1.8">'
    out += f'<path d="M{cx} {cy - 6} c-22 0 -36 16 -36 30 c0 12 10 18 20 18 c8 0 10 -4 16 -4 s8 4 16 4 c10 0 20 -6 20 -18 c0 -14 -14 -30 -36 -30z"/>'
    for dx, dy, rx, ry, rot in ((-40, -18, 10, 14, -25), (-15, -40, 10, 15, -8), (15, -40, 10, 15, 8), (40, -18, 10, 14, 25)):
        out += f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx + dx} {cy + dy})"/>'
    out += "</g>"
    x0, x1, y0, y1 = 376, 540, 30, 168
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        out += f'<path d="M{x} {y + 16 * sy} V{y} H{x + 16 * sx}" fill="none" stroke="{SOFT}" stroke-width="2" stroke-linecap="round"/>'
    out += f'<rect class="scan" x="{x0 + 6}" y="{y0}" width="{x1 - x0 - 12}" height="2.5" rx="1" fill="{c}"/>'
    css = ".scan{animation:scan 3s ease-in-out infinite alternate}@keyframes scan{to{transform:translateY(136px)}}"
    return out, css


def m_orbit(c):
    cx, cy = 458, 98
    out = f'<circle cx="{cx}" cy="{cy}" r="60" fill="{c}" opacity=".07"/>'
    for i, (r, dash, dur) in enumerate(((44, "2 6", 18), (58, "10 8", 26), (72, "1 7", 40))):
        out += (f'<circle class="rg" style="transform-origin:{cx}px {cy}px;animation-duration:{dur}s{";animation-direction:reverse" if i == 1 else ""}" '
                f'cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-opacity="{.7 - i * .18:.2f}" stroke-dasharray="{dash}"/>')
    out += f'<circle cx="{cx}" cy="{cy}" r="28" fill="url(#pg)"/><path d="M{cx - 24} {cy - 6} q24 12 48 -4" fill="none" stroke="#fff" stroke-opacity=".25"/>'
    out += f'<ellipse cx="{cx}" cy="{cy}" rx="92" ry="30" fill="none" stroke="{SOFT}" stroke-opacity=".25" transform="rotate(-18 {cx} {cy})"/>'
    out += (f'<g transform="rotate(-18 {cx} {cy})"><rect x="-5" y="-5" width="10" height="10" rx="2" fill="{FG}">'
            f'<animateMotion dur="7s" repeatCount="indefinite" path="M{cx - 92} {cy} a92 30 0 1 0 184 0 a92 30 0 1 0 -184 0"/></rect></g>')
    css = ".rg{animation:sp linear infinite}"
    return out, css


PROJECTS = [
    ("govbench", "GovBench-Clinical", "CLINICAL AI · EVALUATION", None,
     ["A benchmark and clinician workbench that measures what each", "safety layer in a multi-agent clinical AI pipeline changes."],
     ["Python", "FastAPI", "React", "183 tests"], VIOLET, m_layers),
    ("govreason", "GovReasonRAG", "RAG · PUBLIC POLICY", None,
     ["Evidence-contracted RAG for Indian welfare schemes, built to", "avoid hallucinated eligibility rules and outdated answers."],
     ["FastAPI", "Next.js", "BM25 + dense", "LoRA"], CYAN, m_rag),
    ("geosick", "GeoSick AI", "ON-DEVICE ML · HEALTH", "WINNER · DARKNETRIX + CODE SURFERS",
     ["Environmental health guidance that runs fully in the", "browser: private, offline-first, no server needed."],
     ["React", "ONNX Runtime Web", "PyTorch", "PWA"], GREEN, m_globe),
    ("marganetra", "MargaNetra", "GRAPH ML · SMART CITIES", None,
     ["A traffic decision-support system that models a city's", "road network with graph neural networks."],
     ["PyTorch GNN", "TypeScript", "React"], GOLD, m_traffic),
    ("petguide", "PetGuide AI", "MULTIMODAL · VET TRIAGE", "WINNER · NAV NIRMAN",
     ["Pet health triage with breed identification, wound", "scanning and tailored nutrition plans."],
     ["Gemini", "React", "TypeScript"], PINK, m_paw),
    ("geotrace", "GeoTrace AI", "3D · ATMOSPHERIC DATA", None,
     ["Planetary atmospheric intelligence: environmental", "telemetry explored on an interactive 3D globe."],
     ["TypeScript", "WebGL", "Vite", "Gemini"], ORANGE, m_orbit),
]


def projects():
    for i, (slug, title, tag, award, desc, chips, c, motif) in enumerate(PROJECTS):
        art, css = motif(c)
        defs = (f'<radialGradient id="halo" cx=".78" cy=".2" r=".75"><stop offset="0" stop-color="{c}" stop-opacity=".2"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
                f'<radialGradient id="pg" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="{GOLD}"/><stop offset="1" stop-color="{c}"/></radialGradient>')
        body = card(8, 8, 584, 300) + '<rect x="8" y="8" width="584" height="300" rx="24" fill="url(#halo)"/>'
        body += f'<text x="32" y="48" class="m" font-size="12" letter-spacing="1.5"><tspan fill="{c}" font-weight="700">{i + 1:02d}</tspan><tspan fill="{MUTED}">  /  {esc(tag)}</tspan></text>'
        if award:
            body += (f'<path d="M38 66 l2.6 5.4 l5.9 .8 l-4.3 4.1 l1 5.9 l-5.2 -2.8 l-5.2 2.8 l1 -5.9 l-4.3 -4.1 l5.9 -.8z" fill="{GOLD}"/>'
                     f'<text x="54" y="79" class="m" font-size="11" letter-spacing="1.2" fill="{GOLD}">{esc(award)}</text>')
        body += art
        body += f'<text x="32" y="210" class="s" font-size="30" font-weight="800" letter-spacing="-.8" fill="{FG}">{esc(title)}</text>'
        for k, line in enumerate(desc):
            body += f'<text x="32" y="{236 + k * 20}" class="s" font-size="14.5" fill="{MUTED}">{esc(line)}</text>'
        x = 32
        for ch in chips:
            w = round(len(ch) * 7 + 20)
            body += (f'<rect x="{x}" y="270" width="{w}" height="22" rx="11" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-opacity=".35"/>'
                     f'<text x="{x + w / 2}" y="285" text-anchor="middle" class="m" font-size="11.5" fill="{SOFT}">{esc(ch)}</text>')
            x += w + 8
        body += f'<circle cx="556" cy="281" r="15" fill="#fff" fill-opacity=".06" stroke="{LINE}"/>' + arrow(550, 275, FG)
        svg(f"p-{slug}.svg", 600, 316, body, css, defs, f"{title}: {' '.join(desc)}")


# ───────────────────────────── wins ─────────────────────────────
WINS = [
    ("Paranox 2.0", "1ST PLACE", "Duality AI", "1"),
    ("HACK-A-THON 1.0", "3RD PLACE", "eHRS", "3"),
    ("Darknetrix", "WINNER", "GeoSick AI", ""),
    ("Code Surfers", "WINNER", "GeoSick AI", ""),
    ("Aignite", "WINNER", "Perf. Predictor", ""),
    ("Promptathon", "WINNER", "Ojas AI", ""),
    ("Build With AI", "WINNER", "VanRaksha", ""),
    ("Nav Nirman", "WINNER", "PetGuide AI", ""),
]


def wins():
    css = (".track{stroke-dasharray:1010;stroke-dashoffset:1010;animation:dash 2.4s .2s ease-out forwards}"
           ".node{opacity:0;animation:up .6s ease-out forwards}")
    body = card(8, 8, 1184, 240) + '<rect x="8" y="8" width="1184" height="240" rx="24" fill="url(#dots)"/>'
    body += f'<text x="56" y="56" class="m" font-size="12" letter-spacing="1.6" fill="{MUTED}">HACKATHON RECORD</text>'
    body += f'<text x="1144" y="56" text-anchor="end" class="m" font-size="12" letter-spacing="1.6" fill="{GOLD}">8 WINS · NATIONAL + INTERNATIONAL</text>'
    body += f'<path d="M96 140 H1104" stroke="{LINE}" stroke-width="2"/><path class="track" d="M96 140 H1104" stroke="url(#gg)" stroke-width="2"/>'
    for i, (name, res, proj, rank) in enumerate(WINS):
        x = 96 + i * 144
        g = f'<text x="{x}" y="104" text-anchor="middle" class="m" font-size="11" letter-spacing="1.4" fill="{GOLD if rank else MUTED}">{res}</text>'
        if rank:
            g += (f'<circle cx="{x}" cy="140" r="19" fill="url(#gg)"/>'
                  f'<text x="{x}" y="147" text-anchor="middle" class="s" font-size="19" font-weight="800" fill="{BG}">{rank}</text>')
        else:
            g += (f'<circle cx="{x}" cy="140" r="13" fill="{BG}" stroke="{GOLD}" stroke-width="2"/>'
                  f'<path d="M{x - 5} 140 l3.6 3.8 l6.6 -7.4" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        g += f'<text x="{x}" y="188" text-anchor="middle" class="s" font-size="14.5" font-weight="700" fill="{FG}">{esc(name)}</text>'
        g += f'<text x="{x}" y="209" text-anchor="middle" class="m" font-size="11" fill="{MUTED}">{esc(proj)}</text>'
        body += f'<g class="node" style="animation-delay:{.3 + i * .22:.2f}s">{g}</g>'
    svg("wins.svg", 1200, 256, body, css, "", "Hackathon record: 8 wins. 1st place at Paranox 2.0, 3rd place at HACK-A-THON 1.0, and wins at Darknetrix, Code Surfers, Aignite, Promptathon, Build With AI and Nav Nirman.")


# ───────────────────────────── stack marquee ─────────────────────────────
ROW1 = ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "LangChain", "Gemini", "Hugging Face", "ONNX Runtime", "Ollama", "OpenCV", "RAG", "Multi-agent systems", "LLM evals"]
ROW2 = ["TypeScript", "React", "Next.js", "Node.js", "FastAPI", "Tailwind CSS", "Three.js", "PostgreSQL", "MongoDB", "Supabase", "Firebase", "Docker", "GCP", "AWS", "Git"]


def stack():
    colors = [GOLD, VIOLET, ORANGE, CYAN, PINK, GREEN]

    def row(items, y, k):
        x, parts = 0, ""
        for rep in range(2):
            for j, t in enumerate(items):
                w = round(len(t) * 8.5 + 44)
                parts += (f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="18" fill="{CARD2}" stroke="{LINE}"/>'
                          f'<circle cx="{x + 18}" cy="{y + 18}" r="4" fill="{colors[(j + k) % 6]}"/>'
                          f'<text x="{x + 30}" y="{y + 23}" class="m" font-size="14" fill="{SOFT}">{esc(t)}</text>')
                x += w + 12
        return parts, x // 2

    r1, t1 = row(ROW1, 28, 0)
    r2, t2 = row(ROW2, 76, 3)
    css = (f".r1{{animation:m1 42s linear infinite}}.r2{{animation:m2 48s linear infinite}}"
           f"@keyframes m1{{to{{transform:translateX(-{t1}px)}}}}@keyframes m2{{from{{transform:translateX(-{t2}px)}}to{{transform:translateX(0)}}}}")
    defs = ('<clipPath id="c"><rect x="8" y="8" width="1184" height="124" rx="24"/></clipPath>'
            f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="fr" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>')
    body = (card(8, 8, 1184, 124) + f'<g clip-path="url(#c)"><g class="r1">{r1}</g><g class="r2">{r2}</g>'
            '<rect x="8" y="8" width="150" height="124" fill="url(#fl)"/><rect x="1042" y="8" width="150" height="124" fill="url(#fr)"/></g>'
            f'<rect x="8" y="8" width="1184" height="124" rx="24" fill="none" stroke="{LINE}"/>')
    svg("stack.svg", 1200, 140, body, css, defs, "Tech stack: " + ", ".join(ROW1 + ROW2))


# ───────────────────────────── experience ─────────────────────────────
EXPERIENCE = [
    ("FEB – MAY 2026", "ML Intern", "XYZON Technologies", "student-performance modelling", False),
    ("JAN 2026 – NOW", "Operations & Community Lead", "The Student Spot", "20K+ student community", True),
    ("AUG 2025 – NOW", "Google Campus Ambassador", "Google", "200+ students taught", True),
    ("SEP – NOV 2025", "Full-Stack Developer Intern", "Swecha · open source", "300+ patient records", False),
    ("AUG – OCT 2025", "AI Developer", "ViswamAI", "RAG over 100 GB of data", False),
    ("AUG – OCT 2025", "AI Developer Intern", "Kartavya Solutions", "5 models unified on GCP", False),
]


def experience():
    n = len(EXPERIENCE)
    h = 84 + n * 54 + 14
    body = card(8, 8, 1184, h)
    body += f'<text x="56" y="56" class="m" font-size="12" letter-spacing="1.6" fill="{MUTED}">EXPERIENCE</text>'
    body += f'<text x="1144" y="56" text-anchor="end" class="m" font-size="12" letter-spacing="1.6" fill="{MUTED}">6 ROLES · 2025 – 2026</text>'
    for i, (period, role, org, note, now) in enumerate(EXPERIENCE):
        y = 84 + i * 54
        g = f'<path d="M56 {y} H1144" stroke="{LINE}"/>'
        if now:
            g += f'<circle class="now" cx="40" cy="{y + 30}" r="4" fill="{GREEN}"/>'
        g += f'<text x="56" y="{y + 34}" class="m" font-size="12.5" letter-spacing="1" fill="{GREEN if now else MUTED}">{period}</text>'
        g += f'<text x="250" y="{y + 35}" class="s" font-size="18" font-weight="700" fill="{FG}">{esc(role)}</text>'
        g += f'<text x="560" y="{y + 35}" class="s" font-size="16" fill="{SOFT}">{esc(org)}</text>'
        g += f'<text x="1144" y="{y + 34}" text-anchor="end" class="m" font-size="12.5" fill="{GOLD}">{esc(note)}</text>'
        body += f'<g class="up" style="animation-delay:{i * .1:.1f}s">{g}</g>'
    svg("experience.svg", 1200, h + 16, body, ".now{animation:pl 2s ease-in-out infinite}", "",
        "Experience: " + "; ".join(f"{r} at {o} ({p})" for p, r, o, _, _ in EXPERIENCE))


# ───────────────────────────── contact buttons ─────────────────────────────
def contact():
    for slug, label, value, c in (("portfolio", "PORTFOLIO", "nikshithnooka.page", GOLD),
                                  ("linkedin", "LINKEDIN", "in/nikshith-nooka", VIOLET),
                                  ("email", "EMAIL", "nikshithnooka@gmail.com", ORANGE)):
        defs = f'<radialGradient id="h" cx="1" cy="0" r="1"><stop offset="0" stop-color="{c}" stop-opacity=".28"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>'
        body = (card(8, 8, 384, 88, 22) + '<rect x="8" y="8" width="384" height="88" rx="22" fill="url(#h)"/>'
                + f'<text x="34" y="44" class="m" font-size="11" letter-spacing="1.6" fill="{c}">{label}</text>'
                + f'<text x="34" y="72" class="s" font-size="18" font-weight="700" fill="{FG}">{esc(value)}</text>'
                + f'<circle cx="352" cy="52" r="17" fill="{c}"/>' + arrow(346, 46, BG))
        svg(f"c-{slug}.svg", 400, 104, body, "", defs, f"{label.title()}: {value}")


if __name__ == "__main__":
    hero(); stats(); projects(); wins(); stack(); experience(); contact()
    print("built", len(list(OUT.glob("*.svg"))), "cards in", OUT)
