import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from pathlib import Path

DEBUG_PATH = Path('output/vinted_debug.html')
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept-Language':'it-IT,it;q=0.9,en;q=0.8'}


def _abs(href):
    if not href:
        return ''
    return href if href.startswith('http') else 'https://www.vinted.it' + href


def search_vinted(query, limit=10):
    url = f'https://www.vinted.it/catalog?search_text={quote_plus(query)}'
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    html = r.text
    DEBUG_PATH.write_text(html, encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    items, seen = [], set()
    for a in soup.select('a[href*="/items/"]'):
        href = _abs(a.get('href'))
        if not href or href in seen:
            continue
        text = a.get_text(' ', strip=True)
        if not text or 'verifica dell'articolo' in text.lower():
            continue
        seen.add(href)
        img = a.find('img')
        image = ''
        if img:
            image = img.get('src') or img.get('data-src') or ''
        price = '—'
        for token in text.split():
            if token.startswith('€'):
                price = token
                break
        items.append({'platform':'Vinted','title':text[:140],'price':price,'meta':'','url':href,'image':image})
        if len(items) >= limit:
            break
    return items
