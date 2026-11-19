"""
🧠 Train Nikshith — a community-trained "model" that lives in a GitHub profile README.

Visitors open an issue titled `train|<action>`; the `train.yml` workflow runs this
script, which advances the training run, redraws the loss curve SVG and rewrites
the block between <!-- TRAIN:START --> and <!-- TRAIN:END --> in README.md.

Pure standard library. Inputs come from environment variables (never interpolated
into shell), so issue titles can't inject anything.

Usage:
    python scripts/train.py            # apply one action from env (ACTION_TITLE, TRAINER, ISSUE_NUMBER)
    python scripts/train.py --render   # just re-render README + SVG from the current state
"""
from __future__ import annotations

import json
import math
import os
import random
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "state.json"
README = ROOT / "README.md"
LOSS_SVG = ROOT / "assets" / "loss.svg"
MESSAGE = ROOT / ".train_message.md"  # comment body posted back on the issue (not committed)

REPO = os.environ.get("GITHUB_REPOSITORY", "nikshith-nooka/nikshith-nooka")
START_LOSS = 2.5
CONVERGED = 0.05
HISTORY_CAP = 80

ACTIONS = {
    "step":    ("🧠", "Train one epoch",       "Safe SGD step. Slow and steady."),
    "lr":      ("⚡", "Crank the learning rate", "Big gains… or the run explodes."),
    "dropout": ("🎲", "Add dropout",            "Regularize. Shields the next risky step."),
    "data":    ("📚", "Feed more data",          "Bigger drop, but only once per trainer per run."),
}


# ───────────────────────────── state ─────────────────────────────
def fresh_state() -> dict:
    return {
        "run": 1,
        "epoch": 0,
        "loss": START_LOSS,
        "best_loss": START_LOSS,
        "history": [START_LOSS],
        "shield": False,
        "data_fed_by": [],
        "total_epochs": 0,
        "explosions": 0,
        "converged_runs": [],
        "leaderboard": {},
        "recent": [],
    }


def load() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return fresh_state()


def save(s: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def accuracy(loss: float) -> float:
    return round(100 * math.exp(-loss), 1)


# ───────────────────────────── game ─────────────────────────────
def apply_action(s: dict, action: str, user: str, seed: int) -> str:
    rng = random.Random(seed)
    before = s["loss"]
    note = ""

    if action == "step":
        s["loss"] *= rng.uniform(0.90, 0.96)
        note = "Clean gradient step. The loss goes down quietly."
    elif action == "lr":
        if rng.random() < 0.68:
            s["loss"] *= rng.uniform(0.70, 0.82)
            note = "⚡ Learning rate cranked: **huge** improvement!"
        elif s["shield"]:
            s["shield"] = False
            s["loss"] *= 0.97
            note = "⚡ The run tried to diverge… but 🎲 dropout absorbed the blow. Shield consumed."
        else:
            s["loss"] = min(START_LOSS * 1.2, s["loss"] * rng.uniform(1.25, 1.6))
            s["explosions"] += 1
            note = "💥 **Gradient explosion!** The loss spiked. Somebody add dropout…"
    elif action == "dropout":
        s["loss"] *= rng.uniform(0.95, 0.98)
        s["shield"] = True
        note = "🎲 Dropout added. The next risky learning-rate jump is protected."
    elif action == "data":
        if user in s["data_fed_by"]:
            s["loss"] *= rng.uniform(0.97, 0.99)
            note = "📚 You already fed data this run, so the model is overfitting to you. Tiny gain."
        else:
            s["data_fed_by"].append(user)
            s["loss"] *= rng.uniform(0.80, 0.88)
            note = "📚 Fresh data! Generalization improved a lot."

    s["loss"] = round(max(s["loss"], 0.01), 4)
    s["epoch"] += 1
    s["total_epochs"] += 1
    s["best_loss"] = min(s["best_loss"], s["loss"])
    s["history"].append(s["loss"])
    s["history"] = s["history"][-HISTORY_CAP:]

    s["leaderboard"][user] = s["leaderboard"].get(user, 0) + 1
    s["recent"].insert(0, {
        "user": user,
        "action": action,
        "epoch": s["epoch"],
        "run": s["run"],
        "delta": round(s["loss"] - before, 4),
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    })
    s["recent"] = s["recent"][:6]

    msg = [
        f"### {ACTIONS[action][0]} Epoch {s['epoch']} of run #{s['run']} complete!",
        "",
        note,
        "",
        f"| | before | after |",
        f"|---|---|---|",
        f"| loss | `{before:.4f}` | `{s['loss']:.4f}` |",
        f"| accuracy | `{accuracy(before)}%` | `{accuracy(s['loss'])}%` |",
        "",
    ]

    if s["loss"] <= CONVERGED:
        s["converged_runs"].append({
            "run": s["run"], "epochs": s["epoch"], "finisher": user,
            "at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        })
        msg.append(f"🎉🎉 **@{user} pushed run #{s['run']} to convergence in {s['epoch']} epochs!** "
                   f"You're immortalized in the Hall of Convergence. A new run starts now.")
        s["run"] += 1
        s["epoch"] = 0
        s["loss"] = START_LOSS
        s["best_loss"] = START_LOSS
        s["history"] = [START_LOSS]
        s["shield"] = False
        s["data_fed_by"] = []

    msg.append("")
    msg.append(f"Thanks for training me, @{user}! You've contributed **{s['leaderboard'][user]}** epoch(s). "
               f"[See the live run →](https://github.com/{REPO.split('/')[0]})")
    return "\n".join(msg)


# ─────────────────────────── loss.svg ───────────────────────────
def render_svg(s: dict) -> None:
    W, H = 1000, 260
    L, R, T, B = 64, 24, 52, 40
    hist = s["history"]
    ymax = START_LOSS * 1.25
    n = max(len(hist) - 1, 1)

    def pt(i, v):
        x = L + (W - L - R) * (i / n)
        y = T + (H - T - B) * (1 - min(v, ymax) / ymax)
        return x, y

    pts = [pt(i, v) for i, v in enumerate(hist)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{L},{H-B} " + line + f" {pts[-1][0]:.1f},{H-B}"
    lx, ly = pts[-1]

    grid = []
    for k in range(5):
        v = ymax * k / 4
        _, y = pt(0, v)
        grid.append(f'<line x1="{L}" x2="{W-R}" y1="{y:.1f}" y2="{y:.1f}" stroke="#211f3f"/>'
                    f'<text x="{L-10}" y="{y+4:.1f}" text-anchor="end" class="ax">{v:.1f}</text>')
    _, ty = pt(0, CONVERGED)
    target = (f'<line x1="{L}" x2="{W-R}" y1="{ty:.1f}" y2="{ty:.1f}" stroke="#3ddc84" stroke-dasharray="4 6" opacity=".7"/>'
              f'<text x="{W-R}" y="{ty-6:.1f}" text-anchor="end" class="ax" fill="#3ddc84">convergence · {CONVERGED}</text>')

    shield = ' · 🛡 dropout armed' if s["shield"] else ''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Live training loss for run {s['run']}: {s['loss']:.4f}">
<title>Live training loss — run #{s['run']}</title>
<defs>
  <linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7B733" stop-opacity=".35"/><stop offset="1" stop-color="#F7B733" stop-opacity="0"/></linearGradient>
  <linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#8e7cf0"/><stop offset="1" stop-color="#F7B733"/></linearGradient>
</defs>
<style>
  .ax{{font:12px ui-monospace,Menlo,Consolas,monospace;fill:#6b6890}}
  .h{{font:600 15px ui-monospace,Menlo,Consolas,monospace;fill:#e8e6ff}}
  .ln{{stroke-dasharray:3000;stroke-dashoffset:3000;animation:draw 2.5s ease-out forwards}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
  .dot{{animation:pulse 1.6s ease-in-out infinite}}
  @keyframes pulse{{50%{{r:9;opacity:.35}}}}
  @media (prefers-reduced-motion: reduce){{.ln{{animation:none;stroke-dashoffset:0}}.dot{{animation:none}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="#0b0a1a"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#2a2750"/>
<text x="{L}" y="32" class="h">live training loss · run #{s['run']} · epoch {s['epoch']}</text>
<text x="{W-R}" y="32" class="ax" text-anchor="end">loss {s['loss']:.4f} · acc {accuracy(s['loss'])}%{shield}</text>
{"".join(grid)}
{target}
<polygon points="{area}" fill="url(#a)"/>
<polyline points="{line}" fill="none" stroke="url(#l)" stroke-width="2.5" stroke-linejoin="round" class="ln"/>
<circle cx="{lx:.1f}" cy="{ly:.1f}" r="5" fill="#F7B733" class="dot"/>
<text x="{L}" y="{H-14}" class="ax">epoch 0</text>
<text x="{W-R}" y="{H-14}" class="ax" text-anchor="end">now →</text>
</svg>'''
    LOSS_SVG.parent.mkdir(parents=True, exist_ok=True)
    LOSS_SVG.write_text(svg, encoding="utf-8")


# ─────────────────────────── README block ───────────────────────────
def issue_link(action: str) -> str:
    emoji, label, _ = ACTIONS[action]
    body = (f"Just hit **Submit new issue** — a GitHub Action will run your move "
            f"and reply in a few seconds. No need to write anything 🙌")
    from urllib.parse import quote
    return (f"https://github.com/{REPO}/issues/new?title={quote('train|' + action)}"
            f"&body={quote(body)}")


def bar(pct: float, width: int = 24) -> str:
    filled = round(width * pct / 100)
    return "█" * filled + "░" * (width - filled)


def render_block(s: dict) -> str:
    acc = accuracy(s["loss"])
    progress = max(0.0, min(100.0, 100 * (1 - (s["loss"] - CONVERGED) / (START_LOSS - CONVERGED))))
    from urllib.parse import quote

    def badge(e: str, label: str) -> str:
        text = f"{e} {label}".replace("-", "--").replace("_", "__")
        return f"https://img.shields.io/badge/{quote(text)}-302b63?style=for-the-badge"

    buttons = "\n".join(
        f'<a href="{issue_link(a)}"><img src="{badge(e, label)}" alt="{e} {label}"/></a>'
        for a, (e, label, _) in ACTIONS.items()
    )
    rules = "\n".join(f"| {e} **{label}** | {desc} |" for e, label, desc in ACTIONS.values())

    recent = "\n".join(
        f"| run {r['run']} · epoch {r['epoch']} | {ACTIONS[r['action']][0]} {ACTIONS[r['action']][1]} | "
        f"[@{r['user']}](https://github.com/{r['user']}) | `{'+' if r['delta'] > 0 else ''}{r['delta']:.4f}` |"
        for r in s["recent"]
    ) or "| — | *nobody yet. Be the first to train me!* | — | — |"

    top = sorted(s["leaderboard"].items(), key=lambda kv: (-kv[1], kv[0]))[:5]
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    board = "\n".join(
        f"| {medals[i]} | [@{u}](https://github.com/{u}) | {c} |" for i, (u, c) in enumerate(top)
    ) or "| 🥇 | *your name here* | 0 |"

    hall = ", ".join(
        f"run #{c['run']} by [@{c['finisher']}](https://github.com/{c['finisher']}) ({c['epochs']} epochs)"
        for c in s["converged_runs"][-5:]
    ) or "*No run has converged yet. Will you be the one?*"

    return f"""<!-- TRAIN:START -->
<div align="center">

<img src="assets/loss.svg" width="100%" alt="live training loss"/>

**Run #{s['run']}** · epoch **{s['epoch']}** · loss **`{s['loss']:.4f}`** · accuracy **`{acc}%`**{' · 🛡 dropout armed' if s['shield'] else ''}

`{bar(progress)}` {progress:.0f}% to convergence

{buttons}

<sub>Click a button → hit <b>Submit new issue</b> → a GitHub Action trains me and updates this README in about 30 s.<br/>
Total epochs trained by the community: <b>{s['total_epochs']}</b> · gradient explosions: <b>{s['explosions']}</b> 💥</sub>

</div>

<details>
<summary><b>📜 Rules · recent epochs · leaderboard</b></summary>
<br/>

| Move | Effect |
|---|---|
{rules}

Push the loss below **{CONVERGED}** to converge the run and enter the **Hall of Convergence** 🏛️

**🕒 Recent epochs**

| When | Move | Trainer | Δ loss |
|---|---|---|---|
{recent}

**🏅 Top trainers**

| | Trainer | Epochs |
|---|---|---|
{board}

**🏛️ Hall of Convergence:** {hall}

</details>
<!-- TRAIN:END -->"""


def write_readme(s: dict) -> None:
    text = README.read_text(encoding="utf-8")
    new, count = re.subn(r"<!-- TRAIN:START -->.*?<!-- TRAIN:END -->", lambda _: render_block(s), text, flags=re.S)
    if count != 1:
        sys.exit("README is missing exactly one TRAIN:START/TRAIN:END block")
    README.write_text(new, encoding="utf-8")


# ───────────────────────────── main ─────────────────────────────
def main() -> None:
    s = load()
    if "--render" not in sys.argv:
        title = os.environ.get("ACTION_TITLE", "").strip().lower()
        user = re.sub(r"[^A-Za-z0-9-]", "", os.environ.get("TRAINER", ""))[:39] or "anonymous"
        seed = int(os.environ.get("ISSUE_NUMBER", "0") or 0)
        action = title.split("|", 1)[1].strip() if "|" in title else ""
        if action not in ACTIONS:
            MESSAGE.write_text(
                "🤔 I don't know that move. Use one of the buttons on the profile: "
                + ", ".join(f"`train|{a}`" for a in ACTIONS), encoding="utf-8")
            return
        MESSAGE.write_text(apply_action(s, action, user, seed), encoding="utf-8")
        save(s)
    render_svg(s)
    write_readme(s)


if __name__ == "__main__":
    main()
