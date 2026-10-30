"""Gera assets/banner.svg, o banner animado do README.

O nome é o mesmo mosaico de quadradinhos do site (m4ichel.github.io):
a grade abaixo veio da fonte Unbounded amostrada a cada 7px, igual ao
hero.js faz. O SVG não pode carregar fontes nem scripts no GitHub, então
tudo aqui é forma pronta + animação em CSS.

Uso: python assets/banner.py
"""
import math
import pathlib
import random

W, H, STEP = 1200, 440, 7
PAL = ['#ff3fd8', '#ff7ad9', '#b04bff', '#6f8bff', '#ffffff', '#ffd166', '#ff6a3d']

# "LUCAS MICHEL" / "PEREIRA" em Unbounded 900 (y: colunas a cada 7px, 1 = pixel aceso)
GRID = """
98:000000000000000001110000000111100001111000001111100000000111110000000011111000000001111110000011111101111000000111100000011100000111101111111111001111
105:000000000000000001110000000111100001111000111111111000000111111000001111111110000001111110000011111101111000011111111000011100000111101111111111001111
112:000000000000000001110000000111100001111001111111111100001111111000011111111111000001111111000111111101111000111111111100011100000111101111111111001111
119:000000000000000001110000000111100001111011111101111100001111111100011110001111000001111111000111111101111001111100111110011100000111101111000000001111
126:000000000000000001110000000111100001111011110000011110011110111100011111110000000001111111000111111101111001111000011110011111111111100111000000001111
133:000000000000000001110000000111100001111011110000000000011110011100011111111111000001111111101111111101111001110000000000011111111111100111111111001111
140:000000000000000001110000000111100001111011110000000000011111111110001111111111000001111011101110111101111001110000000000011111111111100111111111001111
147:000000000000000001110000000011110001111011110000011110111111111110000000001111000001111011111110111101111001111000011110011100000111100111000000001111
154:000000000000000001111111111011111111110001111111111100111111111111011110001111000001111011111100111101111001111111111110011100000111101111111111101111111111
161:000000000000000001111111111011111111110001111111111101111111111111011111111111000001111001111100111101111000111111111100011100000111101111111111101111111111
168:000000000000000001111111111001111111100000111111110001111000000111101111111110000001111001111100111101111000011111111000011100000111101111111111101111111111
175:000000000000000000000000000000001100000000000111000000000000000000000001110000000000000000000000000000000000000011
203:00000000000000000000000000000000000000000000000111111100000111111111100111111100000111111111100111101111111100000000011111
210:00000000000000000000000000000000000000000000000111111111100111111111100111111111100111111111100111101111111111000000111111
217:00000000000000000000000000000000000000000000000111111111100111111111100111111111100111111111100111101111111111100000111111
224:000000000000000000000000000000000000000000000001111000111101111000000001110000111101111000000001111011110001111000011111111
231:000000000000000000000000000000000000000000000001111000111101111000000001110000111101111000000001111011110000111000011110111
238:0000000000000000000000000000000000000000000000011111111111011111111110011111111110001111111110011110111111111110001111001111
245:0000000000000000000000000000000000000000000000011111111110011111111110011111111110001111111110011110111111111100001111111111
252:00000000000000000000000000000000000000000000000111111111000111100000000111111110000111100000000111101111111110000111111111111
259:00000000000000000000000000000000000000000000000111100000000111111111100111001111000111111111100111101111001111000111111111111
266:000000000000000000000000000000000000000000000001111000000001111111111001110001111001111111111001111011110011111001111111111111
273:000000000000000000000000000000000000000000000001111000000001111111111001110001111101111111111001111011110001111011110000001111
"""


def color_index(x, y, rnd):
    # mesma faixa de cores do hero.js, com 14% de quadradinhos sorteados
    if rnd.random() < 0.14:
        return rnd.randrange(len(PAL))
    n = (math.sin(x * 0.011 + y * 0.006) + math.sin(x * 0.004 - y * 0.015 + 1.3) + 2) / 4
    for i, lim in enumerate((0.36, 0.5, 0.6, 0.7, 0.78, 0.9)):
        if n < lim:
            return i
    return 6


def name_paths():
    rnd = random.Random(7)
    paths = [[] for _ in PAL]
    s = STEP - 2
    for line in GRID.split():
        y, bits = line.split(':')
        y = int(y)
        for i, b in enumerate(bits):
            if b == '1':
                x = i * STEP
                paths[color_index(x, y, rnd)].append(f'M{x} {y}h{s}v{s}h-{s}z')
    return '\n'.join(
        f'    <path stroke="{PAL[i]}" fill="{PAL[i]}" d="{"".join(p)}"/>' for i, p in enumerate(paths) if p
    )


MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "'Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"

SVG = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
  <title id="t">LUCAS MICHEL PEREIRA — Estudante de Ciência da Computação no Inteli</title>
  <style>
    .mono {{ font-family: {MONO}; }}
    .sans {{ font-family: {SANS}; }}
    .blink {{ animation: blink 1.2s steps(1) infinite; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .b1 {{ animation: d1 16s ease-in-out infinite alternate; }}
    .b2 {{ animation: d2 19s ease-in-out infinite alternate; }}
    .b3 {{ animation: d3 13s ease-in-out infinite alternate; }}
    @keyframes d1 {{ to {{ transform: translate(150px, 40px); }} }}
    @keyframes d2 {{ to {{ transform: translate(-170px, -30px); }} }}
    @keyframes d3 {{ to {{ transform: translate(-60px, 60px); }} }}
    .roll {{ animation: roll 7s linear infinite; }}
    @keyframes roll {{ from {{ transform: translateY(-90px); }} to {{ transform: translateY({H + 10}px); }} }}
    /* separação RGB: parada quase sempre, com picos nos momentos de glitch */
    .rc {{ transform: translate(-2px, 0); animation: rc 5s steps(1) infinite; }}
    .rp {{ transform: translate(2px, 0); animation: rp 5s steps(1) infinite; }}
    @keyframes rc {{ 0% {{ transform: translate(-2px, 0); }} 62% {{ transform: translate(-10px, 1px); }} 64% {{ transform: translate(5px, 0); }} 66% {{ transform: translate(-2px, 0); }} 88% {{ transform: translate(-13px, 0); }} 90.5% {{ transform: translate(-2px, 0); }} }}
    @keyframes rp {{ 0% {{ transform: translate(2px, 0); }} 62% {{ transform: translate(10px, -1px); }} 64% {{ transform: translate(-5px, 0); }} 66% {{ transform: translate(2px, 0); }} 88% {{ transform: translate(13px, 0); }} 90.5% {{ transform: translate(2px, 0); }} }}
    /* fatias do nome que escorregam de lado por um instante */
    .sl {{ opacity: 0; }}
    .s1 {{ animation: s1 5s steps(1) infinite; }}
    .s2 {{ animation: s2 5s steps(1) infinite; }}
    .s3 {{ animation: s3 5s steps(1) infinite; }}
    @keyframes s1 {{ 0% {{ opacity: 0; transform: none; }} 62% {{ opacity: 1; transform: translateX(-28px); }} 64% {{ transform: translateX(16px); }} 66% {{ opacity: 0; transform: none; }} }}
    @keyframes s2 {{ 0% {{ opacity: 0; transform: none; }} 63% {{ opacity: 1; transform: translateX(34px); }} 65.5% {{ opacity: 0; transform: none; }} }}
    @keyframes s3 {{ 0% {{ opacity: 0; transform: none; }} 88% {{ opacity: 1; transform: translateX(-44px); }} 90.5% {{ opacity: 0; transform: none; }} }}
    /* medidor de entropia do HUD */
    .m {{ animation: m 2.5s steps(1) infinite; }}
    @keyframes m {{ 0%, 100% {{ opacity: .18; }} 40% {{ opacity: 1; }} 70% {{ opacity: .18; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <defs>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>
    <pattern id="dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="1" fill="#fff" fill-opacity=".07"/></pattern>
    <pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" fill-opacity=".28"/></pattern>
    <radialGradient id="gp"><stop offset="0" stop-color="#ff2bd6" stop-opacity=".5"/><stop offset="1" stop-color="#ff2bd6" stop-opacity="0"/></radialGradient>
    <radialGradient id="gb"><stop offset="0" stop-color="#3d6bff" stop-opacity=".55"/><stop offset="1" stop-color="#3d6bff" stop-opacity="0"/></radialGradient>
    <radialGradient id="gc"><stop offset="0" stop-color="#4fd8ff" stop-opacity=".3"/><stop offset="1" stop-color="#4fd8ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="iri" x1="0" x2="1"><stop offset="0" stop-color="#ff2bd6"/><stop offset=".5" stop-color="#7a5cff"/><stop offset="1" stop-color="#4fd8ff"/></linearGradient>
    <radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#06050b" stop-opacity="0"/><stop offset="1" stop-color="#06050b" stop-opacity=".9"/></radialGradient>
    <linearGradient id="rollg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <filter id="tc" x="-2%" y="-10%" width="104%" height="120%"><feFlood flood-color="#4fd8ff"/><feComposite in2="SourceAlpha" operator="in"/></filter>
    <filter id="tp" x="-2%" y="-10%" width="104%" height="120%"><feFlood flood-color="#ff2bd6"/><feComposite in2="SourceAlpha" operator="in"/></filter>
    <filter id="glow" x="-5%" y="-20%" width="110%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
    <clipPath id="c1"><rect y="116" width="{W}" height="16"/></clipPath>
    <clipPath id="c2"><rect y="150" width="{W}" height="9"/></clipPath>
    <clipPath id="c3"><rect y="226" width="{W}" height="22"/></clipPath>
    <g id="name" stroke-width="1.2" fill-opacity=".28">
{name_paths()}
    </g>
  </defs>

  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="#06050b"/>
    <!-- fundo holográfico -->
    <ellipse class="b1" cx="300" cy="130" rx="420" ry="230" fill="url(#gp)"/>
    <ellipse class="b2" cx="900" cy="320" rx="460" ry="250" fill="url(#gb)"/>
    <ellipse class="b3" cx="780" cy="80" rx="280" ry="170" fill="url(#gc)"/>
    <g class="b2" fill="none" stroke="url(#iri)">
      <path d="M-120 420 C 260 230, 640 470, 1320 150" stroke-width="110" stroke-opacity=".05"/>
      <path d="M-120 420 C 260 230, 640 470, 1320 150" stroke-width="54" stroke-opacity=".07"/>
      <path d="M-120 420 C 260 230, 640 470, 1320 150" stroke-width="16" stroke-opacity=".12"/>
    </g>
    <g class="b1" fill="none" stroke="url(#iri)">
      <path d="M-100 40 C 320 210, 760 -40, 1300 110" stroke-width="80" stroke-opacity=".04"/>
      <path d="M-100 40 C 320 210, 760 -40, 1300 110" stroke-width="26" stroke-opacity=".08"/>
    </g>
    <rect width="{W}" height="{H}" fill="url(#vig)"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>

    <!-- nome: brilho, separação RGB, mosaico e fatias de glitch -->
    <use href="#name" filter="url(#glow)" opacity=".55"/>
    <g class="rc" opacity=".55"><use href="#name" filter="url(#tc)"/></g>
    <g class="rp" opacity=".55"><use href="#name" filter="url(#tp)"/></g>
    <use href="#name"/>
    <g clip-path="url(#c1)"><g class="sl s1"><rect x="100" y="116" width="{W - 200}" height="16" fill="#06050b" fill-opacity=".85"/><use href="#name"/></g></g>
    <g clip-path="url(#c2)"><g class="sl s2"><rect x="100" y="150" width="{W - 200}" height="9" fill="#06050b" fill-opacity=".85"/><use href="#name" filter="url(#tc)"/></g></g>
    <g clip-path="url(#c3)"><g class="sl s3"><rect x="100" y="226" width="{W - 200}" height="22" fill="#06050b" fill-opacity=".85"/><use href="#name"/></g></g>

    <!-- HUD -->
    <text class="mono" x="48" y="54" font-size="13" letter-spacing="2.6" fill="#8a85a8"><tspan class="blink" fill="#ff1f4b">●</tspan> PORTFOLIO.EXE — V2026.10 — SÃO PAULO, SP</text>
    <text class="mono" x="{W - 48}" y="54" font-size="13" letter-spacing="2" fill="#8a85a8" text-anchor="end">CH.01 // SINAL</text>
    <text class="sans" x="48" y="356" font-size="26" font-weight="800" fill="#ece8ff">Estudante de Ciência da Computação no Inteli</text>
    <text class="mono" x="48" y="390" font-size="13" letter-spacing="1.8" fill="#ff86e0">DATA SCIENCE · ENGENHARIA DE SOFTWARE · OTIMIZAÇÃO</text>
    <text class="mono" x="{W - 48}" y="356" font-size="11" letter-spacing="1.6" fill="#8a85a8" text-anchor="end">ENTROPIA</text>
    <g fill="#ff2bd6">
      <rect x="{W - 48 - 8 * 11}" y="364" width="7" height="10"/>
      <rect x="{W - 48 - 7 * 11}" y="364" width="7" height="10"/>
      <rect x="{W - 48 - 6 * 11}" y="364" width="7" height="10"/>
      <rect class="m" x="{W - 48 - 5 * 11}" y="364" width="7" height="10"/>
      <rect class="m" x="{W - 48 - 4 * 11}" y="364" width="7" height="10" style="animation-delay:.3s"/>
      <rect class="m" x="{W - 48 - 3 * 11}" y="364" width="7" height="10" style="animation-delay:.6s"/>
      <rect class="m" x="{W - 48 - 2 * 11}" y="364" width="7" height="10" style="animation-delay:.9s"/>
      <rect class="m" x="{W - 48 - 1 * 11}" y="364" width="7" height="10" style="animation-delay:1.2s"/>
    </g>
    <text class="mono" x="{W - 48}" y="390" font-size="14" letter-spacing="1" fill="#4fd8ff" text-anchor="end">▸ m4ichel.github.io</text>
    <g fill="none" stroke="#4fd8ff" stroke-opacity=".55" stroke-width="1.5">
      <path d="M20 40V20H40M{W - 40} 20H{W - 20}V40M{W - 20} {H - 40}V{H - 20}H{W - 40}M40 {H - 20}H20V{H - 40}"/>
    </g>

    <rect class="roll" width="{W}" height="90" fill="url(#rollg)"/>
    <rect width="{W}" height="{H}" fill="url(#scan)"/>
  </g>
</svg>
"""

out = pathlib.Path(__file__).with_name('banner.svg')
out.write_text(SVG, encoding='utf-8')
print(f'{out} · {len(SVG) // 1024} KB')
