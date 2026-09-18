#!/usr/bin/env python3
"""Builds the static site for oona.schweikhardt.de from the extracted Cargo content.
Input:  content/pages.json, content/layout.json, content/mediainfo.json
Output: site/ (html) — media/ and fonts/ are prepared separately and committed."""
import json, re, os, html, shutil
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = os.path.join(ROOT, 'content')
OUT = os.path.join(ROOT, 'site')
pages = json.load(open(f'{C}/pages.json'))
layout = json.load(open(f'{C}/layout.json'))
minfo = json.load(open(f'{C}/mediainfo.json'))

PREFIX = '/oona'  # Pfad unter schweikhardt.de
BASE_URL = 'https://schweikhardt.de' + PREFIX
EMAIL = 'oona.schweikhardt@gmail.com'
SLUG = {  # cargo purl -> (path, title)
    'home': ('', 'Oona Schweikhardt – Junior Art Direktorin, Berlin'),
    'archive': ('projekte', 'Projekte'),
    'info': ('info', 'Info'),
    'page-1': ('genzine', 'GenZine – Editorial Design & Brand'),
    'page-7': ('glow-berlin', 'glow Berlin Arbeiten'),
    'page-2': ('humana', 'Humana – Rebranding Projekt'),
    'page-3': ('lookify', 'Lookify – App & Brand Design'),
    'page-4': ('shelterbox', 'ShelterBox – Redesign Projekt'),
    'page-6': ('freie-arbeiten', 'Freie Arbeiten'),
    'page-5': ('pergamon', 'Pergamon Museum – Poster Design'),
}
DESC = {
    'home': 'Portfolio von Oona Schweikhardt – Junior Art Direktorin aus Berlin. Print, Editorial, Brand Design, Illustration.',
    'archive': 'Projekte von Oona Schweikhardt: Editorial Design, Brand, Print, App Design, freie Arbeiten.',
    'info': 'Oona Schweikhardt – Junior Art Direktorin, Berlin. Grafikdesign mit Schwerpunkt Brand Design.',
}
BACKDROP = {'home': 'home', 'info': 'info'}


def url(purl):
    p = SLUG[purl][0]
    return f'{PREFIX}/' if not p else f'{PREFIX}/{p}/'


def prefix_paths(doc):
    doc = re.sub(r'(=")/(?!/|oona/)', r'\1' + PREFIX + '/', doc)
    doc = re.sub(r', /(media|assets|fonts)/', r', ' + PREFIX + r'/\1/', doc)
    return doc


def rem(v, default='2rem'):
    if v is None or v == '':
        return default
    parts = []
    for x in v.split():
        parts.append(x if re.search(r'[a-z%]', x) else f'{x}rem')
    return ' '.join(parts)


def pct(v):
    if not v:
        return None
    v = v.strip().rstrip('%')
    try:
        return float(v)
    except ValueError:
        return None


def img_tag(h, alt, sizes, eager=False, style=''):
    m = minfo[h]
    if m['type'] == 'video':
        return None
    ws = m['widths']
    src = f'/media/{h}-{ws[min(1, len(ws)-1)]}.webp'
    srcset = ', '.join(f'/media/{h}-{w}.webp {w}w' for w in ws)
    st = f' style="{html.escape(style)}"' if style else ''
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    return (f'<img src="{src}" srcset="{srcset}" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" '
            f'alt="{html.escape(alt)}" loading="{load}" decoding="async"{st}>')


def video_tag(h, autoplay, style=''):
    m = minfo[h]
    st = f' style="{html.escape(style)}"' if style else ''
    attrs = 'autoplay muted loop playsinline' if autoplay else 'controls muted loop playsinline preload="metadata"'
    return (f'<video {attrs} poster="/media/{h}-poster.jpg" width="{m["w"]}" height="{m["h"]}"{st}>'
            f'<source src="/media/{h}.mp4" type="video/mp4"></video>')


class Ctx:
    def __init__(self, purl):
        self.purl = purl
        self.title = SLUG[purl][1].split(' – ')[0]
        self.n = 0
        self.gal_i = 0
        self.solo_i = 0
        self.first = True
        self.d = layout.get('d:' + purl, {'gals': [], 'solo': []})
        self.m = layout.get('m:' + purl, {'gals': [], 'solo': []})

    def alt(self):
        self.n += 1
        return f'{self.title} – Bild {self.n}'


def media_el(mi, ctx, sizes, extra_cls='', pos_style=''):
    h = mi['hash']
    m = minfo[h]
    mstyle = mi.get('media-style', '') or ''
    if m['type'] == 'video':
        inner = video_tag(h, mi.get('autoplay') == 'true', mstyle)
        zoom = False
    else:
        eager = ctx.first
        ctx.first = False
        inner = img_tag(h, ctx.alt(), sizes, eager, mstyle)
        zoom = 'zoomable' in (mi.get('class') or []) and mi.get('disable-zoom') != 'true'
    cap = mi.find('figcaption')
    cap_html = f'<figcaption class="caption">{render_children(cap, ctx)}</figcaption>' if cap else ''
    cls = 'mi ' + extra_cls + (' zoom' if zoom else '')
    data = f' data-full="/media/{h}-{m["widths"][-1]}.webp"' if zoom else ''
    href = mi.get('href')
    if href:
        link = url(href) if href in SLUG else href
        body = f'<a href="{link}">{inner}{cap_html}</a>'
    else:
        body = inner + cap_html
    st = f' style="{pos_style}"' if pos_style else ''
    return f'<figure class="{cls.strip()}"{data}{st}>{body}</figure>'


def gallery_abs(g, ctx, kind):
    gi = ctx.gal_i
    ctx.gal_i += 1
    D = ctx.d['gals'][gi]
    M = ctx.m['gals'][gi] if gi < len(ctx.m['gals']) else D
    assert D['tag'] == g.name, (ctx.purl, D['tag'], g.name)
    items = g.find_all('media-item', recursive=False)
    out = []
    for i, mi in enumerate(items):
        a, b = D['items'][i], M['items'][i]
        pos = ('--x:{:.3f}%;--y:{:.3f}%;--w:{:.3f}%;--h:{:.3f}%;'
               '--mx:{:.3f}%;--my:{:.3f}%;--mw:{:.3f}%;--mh:{:.3f}%').format(
            a['x'], a['y'] / D['hRatio'] * 100, a['w'], a['h'] / D['hRatio'] * 100,
            b['x'], b['y'] / M['hRatio'] * 100, b['w'], b['h'] / M['hRatio'] * 100)
        sizes = f'(max-width:700px) {max(20, round(b["w"]))}vw, {max(10, round(a["w"] * 0.95))}vw'
        out.append(media_el(mi, ctx, sizes, 'gi', pos))
    style = f'--ar:{100 / D["hRatio"]:.5f};--mar:{100 / M["hRatio"]:.5f}'
    return f'<div class="gal gal-abs {kind}" style="{style}">{"".join(out)}</div>'


def gallery_slideshow(g, ctx):
    gi = ctx.gal_i
    ctx.gal_i += 1
    D = ctx.d['gals'][gi]
    M = ctx.m['gals'][gi]
    delay = float(g.get('autoplay-delay', '3')) * 1000
    items = g.find_all('media-item', recursive=False)
    out = [media_el(mi, ctx, '(max-width:700px) 100vw, 60vw', 'slide' + (' on' if i == 0 else ''))
           for i, mi in enumerate(items)]
    style = f'--ar:{100 / D["hRatio"]:.5f};--mar:{100 / M["hRatio"]:.5f}'
    return f'<div class="gal slideshow" data-delay="{int(delay)}" style="{style}">{"".join(out)}</div>'


def gallery_grid(g, ctx):
    ctx.gal_i += 1
    cols = int(g.get('columns', '3'))
    gut = rem(g.get('gutter'), '1rem').split()
    mg = rem(g.get('mobile-gutter'), ' '.join(gut)).split()
    cg, rg = gut[0], gut[-1]
    mcg, mrg = mg[0], mg[-1]
    out = []
    for mi in g.find_all('media-item', recursive=False):
        span = mi.get('grid-span')
        sizes = f'{round(95 / cols)}vw'
        el = media_el(mi, ctx, sizes)
        if span and span != '1':
            el = el.replace('<figure ', f'<figure data-span="{span}" style="grid-column:span {span}" ', 1)
        out.append(el)
    style = f'--cols:{cols};--cg:{cg};--rg:{rg};--mcg:{mcg};--mrg:{mrg}'
    return f'<div class="gal grid" style="{style}">{"".join(out)}</div>'


def column_set(cs, ctx):
    units = cs.find_all('column-unit', recursive=False)
    n = len(units)
    gut = rem(cs.get('gutter'), '2rem')
    mgut = rem(cs.get('mobile-gutter'), gut)
    stack = cs.get('mobile-stack', 'true') != 'false'
    hide_empty = cs.get('mobile-hide-empty', 'true') != 'false'
    out = []
    for u in units:
        span = int(u.get('span') or round(12 / n))
        inner = render_children(u, ctx)
        empty = not re.sub(r'<br>|\s', '', inner)
        cls = 'cu' + (' empty' if empty and hide_empty else '')
        out.append(f'<div class="{cls}" style="--span:{span}">{inner}</div>')
    cls = 'cs' + (' stack' if stack else '')
    return f'<div class="{cls}" style="--gut:{gut};--mgut:{mgut}">{"".join(out)}</div>'


def solo_media(mi, ctx):
    si = ctx.solo_i
    ctx.solo_i += 1
    D = ctx.d['solo'][si] if si < len(ctx.d['solo']) else None
    sc = pct(mi.get('scale'))
    width = f'{sc:g}%' if sc else '100%'
    vw = round(D['w'] / 1440 * 100) if D else 90
    return media_el(mi, ctx, f'(max-width:700px) 100vw, {max(15, vw)}vw', 'solo', f'width:{width}')


def render_children(node, ctx):
    return ''.join(render(c, ctx) for c in node.children)


def render(node, ctx):
    if isinstance(node, NavigableString):
        if type(node).__name__ in ('Comment',):
            return ''
        return html.escape(str(node), quote=False)
    if not isinstance(node, Tag):
        return ''
    n = node.name
    if n == 'media-item':
        return solo_media(node, ctx)
    if n in ('gallery-justify', 'gallery-columnized', 'gallery-freeform'):
        return gallery_abs(node, ctx, n.split('-')[1])
    if n == 'gallery-slideshow':
        return gallery_slideshow(node, ctx)
    if n == 'gallery-grid':
        return gallery_grid(node, ctx)
    if n == 'column-set':
        return column_set(node, ctx)
    if n == 'figcaption':
        return ''
    if n == 'br':
        return '<br>'
    if n == 'a':
        href = node.get('href', '')
        if href in SLUG:
            href = url(href)
        elif 'webmail.strato.de' in href or href.startswith('mailto:'):
            href = f'mailto:{EMAIL}'
        attrs = f' href="{html.escape(href)}"'
        if node.get('class'):
            attrs += f' class="{" ".join(node["class"])}"'
        if node.get('style'):
            attrs += f' style="{html.escape(node["style"])}"'
        return f'<a{attrs}>{render_children(node, ctx)}</a>'
    if n in ('span', 'div', 'b', 'i', 'em', 'strong', 'u', 's', 'sup', 'sub', 'p', 'h1', 'h2', 'ul', 'ol', 'li'):
        attrs = ''
        if node.get('class'):
            attrs += f' class="{" ".join(node["class"])}"'
        if node.get('style'):
            attrs += f' style="{html.escape(node["style"])}"'
        return f'<{n}{attrs}>{render_children(node, ctx)}</{n}>'
    return render_children(node, ctx)


def page_css(p):
    css = p.get('local_css') or ''
    pid = p['id']
    out = []
    for block in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        sel, body = block[0].strip(), block[1].strip()
        if not body or '.mobile' in sel:
            continue
        sel = sel.replace(f'[id="{pid}"].page', 'main.page').replace(f'[id="{pid}"] ', 'main.page ')
        body = body.replace('var(--viewport-height)', '100svh')
        out.append(f'{sel}{{{body}}}')
    return '\n'.join(out)


def fix_content(purl, c):
    if purl == 'info':
        c = c.replace('</div>K\n', '</div>\n')  # stray character in the Cargo source
        c = c.replace(f'KONTAKT<br />\n{EMAIL}', f'KONTAKT<br />\n<a href="mailto:{EMAIL}">{EMAIL}</a>')
    return c


NAV = [('Oona Schweikhardt', 'home', '1 / span 3', 'left'), ('Projekte', 'archive', '5 / span 2', 'left'),
       (EMAIL, None, '7 / span 5', 'center'), ('Info', 'info', '12 / span 1', 'right')]


def nav_html(active):
    out = []
    for label, target, span, align in NAV:
        if target:
            cls = 'go-back' + (' active' if target == active and target != 'home' else '')
            href = url(target)
        else:
            cls, href = 'go-back mail', f'mailto:{EMAIL}'
        out.append(f'<div class="nav-u nav-{align}" style="grid-column:{span}"><a class="{cls}" href="{href}">{html.escape(label)}</a></div>')
    return f'<header class="nav">{"".join(out)}</header>'


def og_image(purl, ctx_first_hash):
    return f'{BASE_URL}/media/{ctx_first_hash}-{[w for w in minfo[ctx_first_hash]["widths"] if w <= 1280][-1]}.webp' if ctx_first_hash else ''


def build_page(purl):
    p = pages[purl]
    ctx = Ctx(purl)
    soup = BeautifulSoup(fix_content(purl, p['content']), 'html.parser')
    body = render_children(soup, ctx)
    path, title = SLUG[purl]
    full_title = title if purl == 'home' else f'{title} – Oona Schweikhardt'
    hashes = re.findall(r'hash="([A-Z0-9]+)"', p['content'])
    first_img = next((h for h in hashes if minfo[h]['type'] == 'image'), None)
    desc = DESC.get(purl) or re.sub(r'\s+', ' ', BeautifulSoup(p['content'], 'html.parser').get_text(' ')).strip()
    desc = re.sub(r'^zurück\s*', '', desc)[:155]
    bd = BACKDROP.get(purl)
    bd_html = f'<div class="backdrop bd-{bd}" aria-hidden="true"></div>' if bd else ''
    canonical = f'https://schweikhardt.de{url(purl)}'
    og = og_image(purl, first_img)
    doc = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
{f'<meta property="og:image" content="{og}">' if og else ''}
<link rel="icon" href="/favicon.ico">
<link rel="preload" href="/fonts/archivo-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/site.css">
<style>{page_css(p)}</style>
</head>
<body class="p-{path or 'home'}">
{nav_html(purl)}
{bd_html}
<main class="page">
<div class="page-layout"><div class="page-content"><div class="bodycopy">{body}</div></div></div>
</main>
<footer class="legal"><a href="https://schweikhardt.de/impressum.html">Impressum</a> · <a href="https://schweikhardt.de/datenschutz.html">Datenschutz</a></footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(prefix_paths(doc))
    return canonical


def main():
    urls = [build_page(k) for k in SLUG]
    nf = open(f'{OUT}/projekte/index.html').read()
    nf = re.sub(r'<main class="page">.*?</main>', f'<main class="page" style="min-height:100svh;justify-content:center;background:#cddde8"><div class="bodycopy" style="text-align:center;padding:6rem 2rem"><span class="text-2">Seite nicht gefunden</span><br><a class="go-back" href="{PREFIX}/projekte/" style="color:#18ff00">zu den Projekten</a></div></main>', nf, flags=re.S)
    nf = re.sub(r'<title>.*?</title>', '<title>Seite nicht gefunden – Oona Schweikhardt</title><meta name="robots" content="noindex">', nf)
    nf = nf.replace('<style>', '<style>/*404*/', 1)
    open(f'{OUT}/404.html', 'w').write(nf)
    sm = ''.join(f'<url><loc>{u}</loc></url>' for u in urls)
    open(f'{OUT}/sitemap.xml', 'w').write(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    print('built', len(urls), 'pages')


if __name__ == '__main__':
    main()
