"""Books scraper: collects title, price, rating, availability and link
from books.toscrape.com (a public site built for scraping practice)
and saves everything to a clean CSV file.

Usage:
    python scraper.py                 # all pages
    python scraper.py --pages 3       # first 3 pages only
    python scraper.py --out books.csv
"""
import argparse
import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/catalogue/"
START = "https://books.toscrape.com/catalogue/page-1.html"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_page(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select("article.product_pod"):
        link = card.h3.a
        rating_word = card.select_one("p.star-rating")["class"][1]
        price = card.select_one("p.price_color").text.strip()
        rows.append({
            "title": link["title"],
            "price_gbp": float(price.replace("£", "").replace("Â", "")),
            "rating": RATINGS.get(rating_word, 0),
            "in_stock": "In stock" in card.select_one("p.availability").text,
            "url": urljoin(page_url, link["href"]),
        })
    nxt = soup.select_one("li.next a")
    return rows, (urljoin(page_url, nxt["href"]) if nxt else None)


def scrape(max_pages=None, delay=0.5):
    session = requests.Session()
    session.headers["User-Agent"] = "portfolio-demo-scraper/1.0"
    url, books, n = START, [], 0
    while url and (max_pages is None or n < max_pages):
        resp = session.get(url, timeout=20)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        rows, url = parse_page(resp.text, resp.url)
        books.extend(rows)
        n += 1
        print(f"page {n}: {len(rows)} books (total {len(books)})")
        time.sleep(delay)  # be polite to the server
    return books


def save_csv(books, path):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["title", "price_gbp", "rating", "in_stock", "url"])
        w.writeheader()
        w.writerows(books)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=None)
    ap.add_argument("--out", default="books.csv")
    a = ap.parse_args()
    data = scrape(a.pages)
    save_csv(data, a.out)
    print(f"saved {len(data)} books to {a.out}")
