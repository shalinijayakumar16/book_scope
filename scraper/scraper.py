import requests
from bs4 import BeautifulSoup
import json
import time
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
BOOK_BASE_URL = "http://books.toscrape.com/catalogue/"

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def get_category(book_url):
    full_url = BOOK_BASE_URL + book_url

    try:
        response = requests.get(full_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        breadcrumb = soup.find("ul", class_="breadcrumb").find_all("li")

        if len(breadcrumb) > 2:
            return breadcrumb[2].text.strip()

    except:
        return "Unknown"

    return "Unknown"


def scrape_page(url):
    response =requests.get(url, headers=HEADERS, timeout=10)
    # stop if page doesn't exist
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    time.sleep(0.5)   # small delay per book
    if not books:
        return None

    page_data = []

    for book in books:
        title = book.h3.a["title"]

        price_text = book.find("p", class_="price_color").text
        price = float(price_text.replace("£", "").replace("Â", ""))

        rating_text = book.find("p")["class"][1]
        rating = rating_map.get(rating_text, 0)

        link = book.h3.a["href"]
        category = get_category(link)  # 🔥 nested scraping

        page_data.append({
            "title": title,
            "price": price,
            "rating": rating,
            "category": category
        })

    return page_data


def scrape_all():
    all_data = []
    page = 1

    while True:
        print(f"📄 Scraping page {page}...")

        url = BASE_URL.format(page)
        page_data = scrape_page(url)

        if page_data is None:
            print("🚫 No more pages found. Stopping...")
            break

        all_data.extend(page_data)

        page += 1
        time.sleep(1)  # polite delay

    return all_data


if __name__ == "__main__":
    data = scrape_all()

    with open("books.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Done! Total books scraped: {len(data)}")