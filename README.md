# Book Scraper (Python)

Collects title, price, star rating, stock status and link for every book on
[books.toscrape.com](https://books.toscrape.com) (a public practice site built for scraping)
and saves a clean CSV that opens correctly in Excel (UTF-8 with BOM).

Sample result: `books.csv` (1,000 books, 50 pages).

## Run
```bash
pip install -r requirements.txt
python scraper.py                  # all 50 pages
python scraper.py --pages 3 --out sample.csv
```

## Notes
- `requests` + `BeautifulSoup`, follows the "next" button until the last page
- 0.5 s pause between requests (polite scraping), timeout and error handling
- Easy to adapt to another website: change the selectors in `parse_page`

Built by Belal Hani.
