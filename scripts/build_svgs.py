#!/usr/bin/env python3
"""Builds the animated SVGs used by the profile README.

GitHub runs no JavaScript in a README, but it does play SVG (SMIL + CSS)
animations, so all the motion on the profile lives in these files.

Edit the CONTENT section, then run:   python scripts/build_svgs.py
"""
from __future__ import annotations

import html
import math
import textwrap
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

# ─────────────────────────────── CONTENT ────────────────────────────────
PROMPT = "lord343@rbu:~$ "
TERMINAL = [
    ("whoami", [("Ameya Ingole", "white"), ("  ·  aka ", "dim"), ("Lord343", "acc")]),
    ("cat education.txt", [("B.Tech CSE · 3rd year @ Ramdeobaba University (RBU), Nagpur", "txt")]),
    ("cat focus.txt", [("red + blue team fundamentals · web (OWASP Top 10) · networking · linux", "txt")]),
    ("cat toolbox.txt", [("nmap · metasploit · elastic siem · kql · sysmon · powershell · bash · python", "txt")]),
    ("ls ~/arsenal", [("Port-Scanner/  ", "cyan"), ("Locksmith/  ", "cyan"), ("Anti-REA/  ", "cyan"), ("homograph-guard/", "cyan")]),
    ("./progress --live", None),  # special: animated progress line
    ("cat seeking.txt", [("open to: ", "dim"), ("cybersecurity internships · entry-level roles", "acc")]),
]
PROGRESS = ("HTB CJCA path ", " 100%", "  ·  20+ HTB labs  ·  kBxAc CTF 2026 #65")

PROJECTS = [
    dict(id="port-scanner", name="Port-Scanner", kind="network recon", release=None, art="radar",
         desc="Multi-threaded TCP/UDP port scanner in pure-stdlib Python: -sV probes for 14 services, banner grabbing, TTL OS fingerprinting, CSV/JSON export.",
         stack="Python · socket · threading · 0 deps"),
    dict(id="locksmith", name="Locksmith", kind="applied crypto", release=None, art="lock",
         desc="CLI password toolkit: entropy-based strength checks, a CSPRNG generator and AES-256-GCM encryption keyed with PBKDF2 (260k iterations).",
         stack="Python · cryptography · AES-GCM"),
    dict(id="anti-rea", name="Anti-REA", kind="anti reverse-eng", release="v0.1.0", art="shield",
         desc="Hardens apps against AI-assisted reverse engineering. Before/after test: a real RE tool recovered 0 IPC channels or endpoints from the hardened build.",
         stack="Python · Rust core · CLI · AI-agent skill"),
    dict(id="homograph-guard", name="homograph-guard", kind="anti-phishing", release="v1.3.0", art="homograph",
         desc="Catches IDN homograph and phishing links on-device: CLI, desktop app, Windows installer and a browser extension for Chrome, Edge, Brave and Firefox.",
         stack="Python · JavaScript · WebExtension · NSIS"),
]

NAV = ["PLAYER CARD", "ARSENAL", "LOADOUT", "QUEST LOG", "MINI-GAMES", "CONTACT"]
# ────────────────────────────────────────────────────────────────────────

C = dict(bg="#05080a", panel="#0b1016", panel2="#101820", border="#1d2a22", acc="#9fef00", cyan="#2ee6ff",
         amb="#ffb000", red="#ff3b5c", txt="#d6e2d0", dim="#6b7d8f", white="#f2f7f0")
FONT = "'JetBrains Mono','Fira Code','SFMono-Regular','Cascadia Mono',Consolas,'Liberation Mono',Menlo,monospace"
CW = 0.6  # monospace advance width / font-size


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def svg(w: int, h: int, body: str, title: str, extra_css: str = "") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t" xml:space="preserve">
<title id="t">{esc(title)}</title>
<style>
  text {{ font-family: {FONT}; white-space: pre; }}
  .b {{ font-weight: 700; }}
  .glow {{ filter: drop-shadow(0 0 4px {C['acc']}88); }}
  @keyframes pulse {{ 0%,100% {{ opacity: .35 }} 50% {{ opacity: 1 }} }}
  @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
  .pulse {{ animation: pulse 3s ease-in-out infinite; }}
  .blink {{ animation: blink 1.1s steps(1) infinite; }}
  {extra_css}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
{body}
</svg>
"""


def scanlines(w: int, h: int, rx: int = 10) -> str:
    return f"""<defs>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#ffffff" opacity=".035"/></pattern>
  <linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['acc']}" stop-opacity="0"/><stop offset=".5" stop-color="{C['acc']}" stop-opacity=".07"/><stop offset="1" stop-color="{C['acc']}" stop-opacity="0"/></linearGradient>
  <clipPath id="frame"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}"/></clipPath>
</defs>
<g clip-path="url(#frame)" pointer-events="none">
  <rect width="{w}" height="{h}" fill="url(#scan)"/>
  <rect x="0" y="-80" width="{w}" height="80" fill="url(#band)"><animate attributeName="y" values="-80;{h}" dur="7s" repeatCount="indefinite"/></rect>
</g>"""


def window(w: int, h: int, title: str, rx: int = 10) -> str:
    return f"""<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="{C['bg']}" stroke="{C['border']}"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{rx}" fill="none" stroke="{C['acc']}" class="pulse" stroke-opacity=".55"/>
<path d="M1 {rx + 1} a{rx} {rx} 0 0 1 {rx} -{rx} h{w - 2 - 2 * rx} a{rx} {rx} 0 0 1 {rx} {rx} v{24 - rx} h-{w - 2} z" fill="{C['panel']}"/>
<circle cx="20" cy="17" r="5.5" fill="{C['red']}"/><circle cx="38" cy="17" r="5.5" fill="{C['amb']}"/><circle cx="56" cy="17" r="5.5" fill="{C['acc']}"/>
<text x="{w / 2}" y="21.5" fill="{C['dim']}" font-size="12" text-anchor="middle">{esc(title)}</text>
<line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C['border']}"/>"""


def tspans(segs) -> str:
    return "".join(f'<tspan fill="{C[c]}">{esc(t)}</tspan>' for t, c in segs)


def shown_at(t: float, inner: str) -> str:
    return f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>{inner}</g>'


# ─────────────────────────────── header ─────────────────────────────────
def build_header() -> str:
    W, FS, LH = 860, 15, 24
    H = 172 + 2 * len(TERMINAL) * LH + 20
    cw = FS * CW
    px = 28
    pw = len(PROMPT) * cw
    out = [window(W, H, "lord343@rbu: ~ — zsh")]
    # glitch title
    out.append(f"""<g transform="translate(28 94)">
  <text class="b gl-a" font-size="48" letter-spacing="5" fill="{C['cyan']}" opacity=".0">AMEYA INGOLE</text>
  <text class="b gl-b" font-size="48" letter-spacing="5" fill="{C['red']}" opacity=".0">AMEYA INGOLE</text>
  <text class="b glow" font-size="48" letter-spacing="5" fill="{C['acc']}">AMEYA INGOLE</text>
</g>
<text x="30" y="122" font-size="13.5" fill="{C['dim']}">// aka <tspan fill="{C['acc']}">Lord343</tspan> · cybersecurity student · B.Tech CSE @ RBU Nagpur</text>
<g transform="translate({W - 30} 88)">
  <circle cx="{-21 * 12.5 * CW - 10:.1f}" cy="-4.5" r="5" fill="{C['acc']}" class="pulse"/>
  <text x="0" y="0" font-size="12.5" text-anchor="end" textLength="{21 * 12.5 * CW:.1f}" lengthAdjust="spacing"><tspan fill="{C['acc']}" class="b">ONLINE</tspan><tspan fill="{C['dim']}"> · open to work</tspan></text>
</g>
<line x1="28" y1="142" x2="{W - 28}" y2="142" stroke="{C['border']}" stroke-dasharray="3 5"/>""")
    t, y, n = 0.7, 172, 0
    for cmd, result in TERMINAL:
        n += 1
        dur = len(cmd) * 0.045
        cid = f"ty{n}"
        steps = ";".join(f"{i * cw:.1f}" for i in range(len(cmd) + 1))
        keys = ";".join(f"{i / len(cmd):.4f}" for i in range(len(cmd) + 1))
        out.append(shown_at(t, f"""<text x="{px}" y="{y}" font-size="{FS}" fill="{C['acc']}" class="b">{esc(PROMPT)}</text>
<clipPath id="{cid}"><rect x="{px + pw}" y="{y - FS}" width="0" height="{FS * 1.5}"><animate attributeName="width" values="{steps}" keyTimes="{keys}" calcMode="discrete" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>
<text x="{px + pw}" y="{y}" font-size="{FS}" fill="{C['white']}" clip-path="url(#{cid})" textLength="{len(cmd) * cw:.1f}" lengthAdjust="spacing">{esc(cmd)}</text>
<rect x="{px + pw}" y="{y - FS + 2}" width="{cw:.1f}" height="{FS + 2}" fill="{C['acc']}" opacity=".85">
  <animate attributeName="x" values="{';'.join(f'{px + pw + i * cw:.1f}' for i in range(len(cmd) + 1))}" keyTimes="{keys}" calcMode="discrete" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/>
  <set attributeName="opacity" to="0" begin="{t + dur + 0.25:.2f}s" fill="freeze"/>
</rect>"""))
        t += dur + 0.25
        y += LH
        if result is None:  # progress line
            a, pct, rest = PROGRESS
            bx = px + len(a) * cw
            cells = "".join(
                f'<rect x="{bx + 2 + i * 11:.1f}" y="{y - 12}" width="9" height="12" fill="{C["acc"]}" opacity="0"><set attributeName="opacity" to="1" begin="{t + 0.1 + i * 0.09:.2f}s" fill="freeze"/></rect>'
                for i in range(10))
            out.append(shown_at(t, f"""<text x="{px}" y="{y}" font-size="{FS}" fill="{C['txt']}">{esc(a)}</text>
<rect x="{bx}" y="{y - 14}" width="114" height="16" fill="none" stroke="{C['dim']}"/>{cells}
<g opacity="0"><set attributeName="opacity" to="1" begin="{t + 1.05:.2f}s" fill="freeze"/>
<text x="{bx + 118}" y="{y}" font-size="{FS}">{tspans([(pct, 'acc'), (rest, 'txt')])}</text></g>"""))
            t += 1.4
        else:
            out.append(shown_at(t, f'<text x="{px}" y="{y}" font-size="{FS}">{tspans(result)}</text>'))
            t += 0.35
        y += LH
    out.append(shown_at(t, f"""<text x="{px}" y="{y}" font-size="{FS}" fill="{C['acc']}" class="b">{esc(PROMPT)}</text>
<rect x="{px + pw}" y="{y - FS + 2}" width="{cw:.1f}" height="{FS + 2}" fill="{C['acc']}" class="blink"/>"""))
    css = """
  @keyframes ga { 0%,88%,100% { opacity: 0; transform: translate(0,0) } 89% { opacity: .9; transform: translate(-4px,1px) } 91% { opacity: .9; transform: translate(3px,-2px) } 93% { opacity: 0 } }
  @keyframes gb { 0%,88%,100% { opacity: 0; transform: translate(0,0) } 89% { opacity: .9; transform: translate(4px,-1px) } 91% { opacity: .9; transform: translate(-3px,2px) } 93% { opacity: 0 } }
  .gl-a { animation: ga 4s steps(1) infinite; } .gl-b { animation: gb 4s steps(1) infinite; }"""
    return svg(W, H, "\n".join(out) + scanlines(W, H), "Terminal: Ameya Ingole (Lord343), B.Tech CSE 3rd year at Ramdeobaba University. Red and blue team fundamentals. Toolbox: Nmap, Metasploit, Elastic SIEM, KQL, Sysmon, PowerShell, Bash, Python. Projects: Port-Scanner, Locksmith, Anti-REA, homograph-guard. Open to cybersecurity internships and entry-level roles.", css)


# ───────────────────────────── player card ──────────────────────────────
def tile(x: int, y: int, w: int, h: int, label: str, inner: str) -> str:
    return f"""<g transform="translate({x} {y})">
  <rect width="{w}" height="{h}" rx="8" fill="{C['panel']}" stroke="{C['border']}"/>
  <path d="M0 18 V8 a8 8 0 0 1 8 -8 H18" fill="none" stroke="{C['acc']}" stroke-width="2"/>
  <path d="M{w - 18} {h} H{w - 8} a8 8 0 0 0 8 -8 V{h - 18}" fill="none" stroke="{C['acc']}" stroke-width="2"/>
  <text x="16" y="26" font-size="11" fill="{C['dim']}" letter-spacing="2">{esc(label)}</text>
  {inner}
</g>"""


def build_stats() -> str:
    W, H = 860, 236
    tw, th, gap, y0 = 193, 164, 16, 52
    xs = [20 + i * (tw + gap) for i in range(4)]
    out = [f"""<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="{C['bg']}" stroke="{C['border']}"/>
<text x="22" y="34" font-size="15" fill="{C['acc']}" class="b glow">PLAYER CARD</text>
<text x="146" y="34" font-size="13" fill="{C['dim']}">// Lord343 · Ameya Ingole</text>
<text x="{W - 22}" y="34" font-size="12" fill="{C['dim']}" text-anchor="end">class: <tspan fill="{C['txt']}">red + blue team</tspan>  ·  lvl: <tspan fill="{C['txt']}">B.Tech yr 3</tspan></text>"""]
    # 1 — CTF
    out.append(tile(xs[0], y0, tw, th, "CTF", f"""
  <text x="16" y="50" font-size="13" fill="{C['txt']}">kBxAc CTF 2026</text>
  <g opacity="0"><set attributeName="opacity" to="1" begin="0.4s" fill="freeze"/>
    <text x="16" y="104" font-size="46" fill="{C['acc']}" class="b glow">#65</text></g>
  <text x="16" y="128" font-size="11" fill="{C['dim']}">rank · first CTF</text>
  <text x="16" y="146" font-size="11" fill="{C['dim']}">10 Oct 2026</text>
  <g transform="translate(150 86)" class="pulse">
    <path d="M-14 -22 h28 v10 a14 14 0 0 1 -28 0 z" fill="none" stroke="{C['amb']}" stroke-width="2"/>
    <path d="M-14 -18 h-6 a6 6 0 0 0 6 8 M14 -18 h6 a6 6 0 0 1 -6 8" fill="none" stroke="{C['amb']}" stroke-width="2"/>
    <path d="M0 2 v8 M-9 14 h18" stroke="{C['amb']}" stroke-width="2"/>
  </g>"""))
    # 2 — HTB Academy
    out.append(tile(xs[1], y0, tw, th, "HTB ACADEMY", f"""
  <text x="16" y="50" font-size="13" fill="{C['txt']}">CJCA job-role path</text>
  <rect x="16" y="66" width="160" height="12" rx="2" fill="{C['panel2']}" stroke="{C['border']}"/>
  <rect x="16" y="66" width="0" height="12" rx="2" fill="{C['acc']}"><animate attributeName="width" values="0;160" begin="0.3s" dur="1.6s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1"/></rect>
  <g opacity="0"><set attributeName="opacity" to="1" begin="1.9s" fill="freeze"/>
    <text x="16" y="118" font-size="34" fill="{C['acc']}" class="b glow">100%</text></g>
  <text x="16" y="146" font-size="11" fill="{C['dim']}">20/20 modules · red+blue</text>"""))
    # 3 — HTB labs
    squares = "".join(
        f'<rect x="{16 + (i % 10) * 16}" y="{108 + (i // 10) * 16}" width="12" height="12" rx="2" fill="{C["acc"]}" opacity=".12"><set attributeName="opacity" to="1" begin="{0.5 + i * 0.09:.2f}s" fill="freeze"/></rect>'
        for i in range(20))
    out.append(tile(xs[2], y0, tw, th, "HACK THE BOX", f"""
  <text x="16" y="50" font-size="13" fill="{C['txt']}">labs solved</text>
  <text x="16" y="94" font-size="40" fill="{C['acc']}" class="b glow">20<tspan class="pulse">+</tspan></text>
  {squares}"""))
    # 4 — arsenal
    icons = [
        f'<circle r="11" fill="none" stroke="{C["cyan"]}" stroke-width="1.6"/><circle r="5" fill="none" stroke="{C["cyan"]}" stroke-width="1.2"/><line x1="0" y1="0" x2="9" y2="-7" stroke="{C["cyan"]}" stroke-width="1.6"/>',
        f'<rect x="-9" y="-3" width="18" height="14" rx="2" fill="none" stroke="{C["cyan"]}" stroke-width="1.6"/><path d="M-5 -3 v-5 a5 5 0 0 1 10 0 v5" fill="none" stroke="{C["cyan"]}" stroke-width="1.6"/>',
        f'<path d="M0 -12 L10 -8 V0 C10 7 5 11 0 13 C-5 11 -10 7 -10 0 V-8 Z" fill="none" stroke="{C["cyan"]}" stroke-width="1.6"/>',
        f'<path d="M0 -11 L11 9 H-11 Z" fill="none" stroke="{C["cyan"]}" stroke-width="1.6"/><line x1="0" y1="-3" x2="0" y2="3" stroke="{C["cyan"]}" stroke-width="1.6"/><circle cy="6" r="1" fill="{C["cyan"]}"/>',
    ]
    lit = "".join(
        f'<g transform="translate({30 + i * 40} 124)" opacity=".15"><set attributeName="opacity" to="1" begin="{0.6 + i * 0.35:.2f}s" fill="freeze"/>{ic}</g>'
        for i, ic in enumerate(icons))
    out.append(tile(xs[3], y0, tw, th, "ARSENAL", f"""
  <text x="16" y="50" font-size="13" fill="{C['txt']}">tools shipped</text>
  <text x="16" y="94" font-size="40" fill="{C['acc']}" class="b glow">4</text>
  <text x="48" y="94" font-size="11" fill="{C['dim']}">python · rust · js</text>
  {lit}"""))
    return svg(W, H, "\n".join(out) + scanlines(W, H), "Player card: kBxAc CTF 2026 rank 65; HTB Academy Junior Cybersecurity Analyst (CJCA) path 100 percent, 20 of 20 modules; 20+ Hack The Box labs; 4 security tools shipped")


# ───────────────────────────── project cards ────────────────────────────
def art(kind: str, cx: int, cy: int) -> str:
    a, cy_ = C["acc"], cy
    if kind == "radar":
        blips = ""
        for ang, port, r in [(40, "22", 30), (150, "80", 20), (255, "443", 34)]:
            bx, by = cx + r * math.cos(math.radians(ang - 90)), cy + r * math.sin(math.radians(ang - 90))
            beg = ang / 360 * 3
            blips += (f'<g opacity="0"><animate attributeName="opacity" values="1;.15;0" keyTimes="0;.6;1" dur="3s" begin="{beg:.2f}s" repeatCount="indefinite"/>'
                      f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="3.2" fill="{a}"/><text x="{bx + 6:.1f}" y="{by - 4:.1f}" font-size="9" fill="{a}">{port}</text></g>')
        return f"""<defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset="1" stop-color="{a}" stop-opacity=".55"/></linearGradient></defs>
<circle cx="{cx}" cy="{cy}" r="44" fill="{C['panel']}" stroke="{a}" stroke-opacity=".5"/>
<circle cx="{cx}" cy="{cy}" r="29" fill="none" stroke="{a}" stroke-opacity=".25"/>
<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="{a}" stroke-opacity=".25"/>
<path d="M{cx - 44} {cy} H{cx + 44} M{cx} {cy - 44} V{cy + 44}" stroke="{a}" stroke-opacity=".18"/>
<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="3s" repeatCount="indefinite"/>
  <path d="M{cx} {cy} L{cx} {cy - 44} A44 44 0 0 1 {cx + 31.1:.1f} {cy - 31.1:.1f} Z" fill="url(#sw)" transform="rotate(-45 {cx} {cy})"/>
  <line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - 44}" stroke="{a}" stroke-width="1.6"/></g>
{blips}"""
    if kind == "lock":
        frames = ["aes:hSSHLcl2…", "aes:sj2OR3by…", "aes:69BKSO8Z…"]
        cyc = "".join(
            f'<text x="{cx}" y="{cy + 58}" font-size="10" fill="{C["cyan"]}" text-anchor="middle" opacity="0"><animate attributeName="opacity" values="1;0;0" keyTimes="0;.333;1" calcMode="discrete" dur="3s" begin="{i}s" repeatCount="indefinite"/>{esc(f)}</text>'
            for i, f in enumerate(frames))
        return f"""<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -7;0 -7;0 0" keyTimes="0;.45;.55;.9;1" dur="4s" repeatCount="indefinite"/>
  <path d="M{cx - 15} {cy_ - 6} V{cy_ - 20} a15 15 0 0 1 30 0 V{cy_ - 6}" fill="none" stroke="{a}" stroke-width="5" stroke-linecap="round"/></g>
<rect x="{cx - 26}" y="{cy_ - 8}" width="52" height="42" rx="7" fill="{C['panel']}" stroke="{a}" stroke-width="2"/>
<circle cx="{cx}" cy="{cy_ + 8}" r="5" fill="{a}" class="pulse"/><rect x="{cx - 2}" y="{cy_ + 10}" width="4" height="12" rx="1" fill="{a}" class="pulse"/>
{cyc}"""
    if kind == "shield":
        sh = f"M{cx} {cy - 44} L{cx + 36} {cy - 31} V{cy - 3} C{cx + 36} {cy + 22} {cx + 17} {cy + 37} {cx} {cy + 45} C{cx - 17} {cy + 37} {cx - 36} {cy + 22} {cx - 36} {cy - 3} V{cy - 31} Z"
        bars = "".join(f'<rect x="{cx - 22}" y="{cy - 26 + i * 9}" width="{w}" height="4" rx="2" fill="{C["dim"]}" opacity=".55"/>' for i, w in enumerate([30, 40, 22, 36, 28, 18]))
        return f"""<clipPath id="shc"><path d="{sh}"/></clipPath>
<path d="{sh}" fill="{C['panel']}" stroke="{a}" stroke-width="2"/>
<g clip-path="url(#shc)">{bars}<rect x="{cx - 40}" y="{cy - 46}" width="80" height="3" fill="{a}" opacity=".9"><animate attributeName="y" values="{cy - 46};{cy + 46}" dur="2.4s" repeatCount="indefinite"/></rect></g>
<text x="{cx}" y="{cy + 62}" font-size="10" fill="{C['dim']}" text-anchor="middle">unknown nodes</text>
<text x="{cx}" y="{cy + 76}" font-size="11" text-anchor="middle"><tspan fill="{C['txt']}">86</tspan><tspan fill="{C['dim']}"> → </tspan><tspan fill="{a}" class="b">700</tspan></text>"""
    if kind == "homograph":
        fs = 16
        w = 10 * fs * CW
        x0 = cx - w / 2
        return f"""<text x="{cx}" y="{cy - 14}" font-size="{fs}" text-anchor="middle" textLength="{w:.1f}" lengthAdjust="spacing"><tspan fill="{C['txt']}">p</tspan><tspan fill="{C['red']}" class="b">а</tspan><tspan fill="{C['txt']}">ypal.com</tspan></text>
<rect x="{x0 + fs * CW:.1f}" y="{cy - 9}" width="{fs * CW:.1f}" height="2.5" fill="{C['red']}" class="blink"/>
<text x="{x0 + fs * CW * 1.5:.1f}" y="{cy + 6}" font-size="9" fill="{C['red']}" text-anchor="middle">U+0430</text>
<text x="{cx}" y="{cy + 26}" font-size="10.5" fill="{C['cyan']}" text-anchor="middle">xn--pypal-4ve.com</text>
<g class="pulse"><rect x="{cx - 38}" y="{cy + 38}" width="76" height="18" rx="9" fill="none" stroke="{C['red']}"/>
<text x="{cx}" y="{cy + 51}" font-size="10" fill="{C['red']}" text-anchor="middle" class="b">HIGH RISK</text></g>"""
    return ""


def pill(x: float, y: float, text: str, color: str) -> tuple[str, float]:
    w = len(text) * 10.5 * CW + 14
    return (f'<rect x="{x:.1f}" y="{y - 12}" width="{w:.1f}" height="17" rx="8.5" fill="none" stroke="{color}" stroke-opacity=".8"/>'
            f'<text x="{x + 7:.1f}" y="{y}" font-size="10.5" fill="{color}">{esc(text)}</text>'), w


def build_card(p: dict) -> str:
    W, H = 420, 244
    out = [window(W, H, f"~/arsenal/{p['id']}")]
    out.append(f'<text x="20" y="68" font-size="21" fill="{C["acc"]}" class="b glow">{esc(p["name"])}</text>')
    x = 20
    for text, col in [(p["kind"], C["cyan"]), (p["release"], C["amb"])]:
        if text:
            s, w = pill(x, 92, text, col)
            out.append(s)
            x += w + 8
    for i, line in enumerate(textwrap.wrap(p["desc"], 33)[:6]):
        out.append(f'<text x="20" y="{120 + i * 17}" font-size="12" fill="{C["txt"]}">{esc(line)}</text>')
    out.append(art(p["art"], 340, 128))
    out.append(f'<line x1="20" y1="216" x2="{W - 20}" y2="216" stroke="{C["border"]}" stroke-dasharray="3 5"/>')
    out.append(f'<text x="20" y="233" font-size="10.5" fill="{C["dim"]}">{esc(p["stack"])}</text>')
    out.append(f'<text x="{W - 20}" y="233" font-size="10.5" fill="{C["acc"]}" text-anchor="end" class="b">open repo <tspan class="blink">▸</tspan></text>')
    return svg(W, H, "\n".join(out) + scanlines(W, H), f"{p['name']}: {p['desc']}")


# ──────────────────────────── nav + divider ─────────────────────────────
def build_nav(i: int, label: str) -> str:
    W, H = 210, 44
    delay = i * 0.5
    css = f".nv {{ animation: pulse 3s ease-in-out {delay:.1f}s infinite; }}"
    body = f"""<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="8" fill="{C['bg']}" stroke="{C['border']}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="8" fill="none" stroke="{C['acc']}" class="nv"/>
<text x="16" y="27" font-size="12" fill="{C['dim']}">{i + 1:02d}</text>
<text x="42" y="27.5" font-size="13.5" fill="{C['acc']}" class="b">{esc(label)}</text>
<text x="{W - 16}" y="27.5" font-size="13" fill="{C['acc']}" text-anchor="end" class="blink">▸</text>"""
    return svg(W, H, body, f"Jump to {label.lower()}", css)


def build_button(kind: str) -> str:
    """Contact / status buttons (drawn here so the README doesn't depend on a badge service)."""
    if kind == "status":
        W, H = 470, 44
        body = f"""<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="{C['bg']}" stroke="{C['acc']}" stroke-opacity=".7"/>
<circle cx="24" cy="22" r="6" fill="{C['acc']}" class="pulse"/><circle cx="24" cy="22" r="10" fill="none" stroke="{C['acc']}" class="pulse" stroke-opacity=".5"/>
<text x="42" y="27" font-size="13" class="b" fill="{C['acc']}">OPEN TO WORK</text>
<text x="150" y="27" font-size="12.5" fill="{C['txt']}">cybersecurity internships · entry-level</text>"""
        return svg(W, H, body, "Open to work: cybersecurity internships and entry-level roles")
    W, H = 250, 44
    if kind == "linkedin":
        color, label, value = C["cyan"], "LinkedIn", "Ameya Ingole"
        icon = f'<rect x="12" y="10" width="24" height="24" rx="5" fill="{color}"/><text x="24" y="27.5" font-size="14" class="b" fill="{C["bg"]}" text-anchor="middle">in</text>'
    else:
        color, label, value = C["acc"], "GitHub", "Ameya343"
        icon = f'<rect x="12" y="10" width="24" height="24" rx="5" fill="none" stroke="{color}" stroke-width="1.6"/><text x="24" y="26.5" font-size="11" class="b" fill="{color}" text-anchor="middle">&lt;/&gt;</text>'
    body = f"""<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="8" fill="{C['bg']}" stroke="{C['border']}"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="8" fill="none" stroke="{color}" class="pulse"/>
{icon}
<text x="48" y="27.5" font-size="13.5" class="b" fill="{color}">{esc(label)}</text>
<text x="{48 + len(label) * 13.5 * CW + 10:.1f}" y="27.5" font-size="12.5" fill="{C['txt']}">{esc(value)}</text>
<text x="{W - 16}" y="27.5" font-size="13" fill="{color}" text-anchor="end" class="blink">▸</text>"""
    return svg(W, H, body, f"{label}: {value}")


def build_divider() -> str:
    W, H = 860, 14
    body = f"""<defs><linearGradient id="dg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['acc']}" stop-opacity="0"/><stop offset=".5" stop-color="{C['acc']}"/><stop offset="1" stop-color="{C['acc']}" stop-opacity="0"/></linearGradient></defs>
<line x1="0" y1="7" x2="{W}" y2="7" stroke="{C['border']}" stroke-width="1"/>
<rect x="-200" y="6" width="200" height="2" fill="url(#dg)"><animate attributeName="x" values="-200;{W}" dur="4s" repeatCount="indefinite"/></rect>
<rect x="{W / 2 - 4}" y="3" width="8" height="8" fill="{C['bg']}" stroke="{C['acc']}" transform="rotate(45 {W / 2} 7)"/>"""
    return svg(W, H, body, "divider")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    files = {"header.svg": build_header(), "stats.svg": build_stats(), "divider.svg": build_divider()}
    for p in PROJECTS:
        files[f"card-{p['id']}.svg"] = build_card(p)
    for i, label in enumerate(NAV):
        files[f"nav-{i + 1}.svg"] = build_nav(i, label)
    for kind in ("linkedin", "github", "status"):
        files[f"btn-{kind}.svg"] = build_button(kind)
    for name, content in files.items():
        (ASSETS / name).write_text(content, encoding="utf-8")
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
