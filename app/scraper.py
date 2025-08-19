"""
Simple scraper: fetch the URL and extract main visible text.
This is intentionally simple; for complex career pages you may want to
add site-specific parsers or use Playwright to render JS.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ColdEmailGen/1.0)"}

def fetch_page(url, timeout=15):
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def extract_text(html, max_chars=None):
    soup = BeautifulSoup(html, "html.parser")
    # remove scripts/styles
    for s in soup(["script", "style", "noscript", "meta", "iframe"]):
        s.decompose()
    # Prefer article/main tags if present
    main = soup.find(["article", "main"])
    if main:
        text = main.get_text(separator="\n")
    else:
        # fallback: take largest text block
        texts = [tag.get_text(separator="\n") for tag in soup.find_all(["section","div","p"])]
        # choose the longest combined content
        text = "\n\n".join(texts)
    if max_chars:
        return text[:max_chars]
    return text

def scrape_text_from_url(url, max_chars=20000):
    html = fetch_page(url)
    txt = extract_text(html, max_chars=max_chars)
    # minimal cleanup
    txt = "\n".join([line.strip() for line in txt.splitlines() if line.strip()])
    return txt
