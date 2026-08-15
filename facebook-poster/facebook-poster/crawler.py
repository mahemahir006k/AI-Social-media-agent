import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "https://xenhra.in"

MAX_PAGES = 50


class WebsiteCrawler:

    def __init__(self):
        self.visited = set()
        self.pages = {}

    def normalize_url(self, url):
        parsed = urlparse(url)

        return (
            parsed.scheme +
            "://" +
            parsed.netloc +
            parsed.path.rstrip("/")
        )

    def is_internal(self, url):
        return urlparse(url).netloc == urlparse(BASE_URL).netloc

    def crawl(self):

        queue = [BASE_URL]

        while queue and len(self.visited) < MAX_PAGES:

            url = self.normalize_url(queue.pop(0))

            if url in self.visited:
                continue

            print(f"Crawling: {url}")

            self.visited.add(url)

            try:

                response = requests.get(
                    url,
                    timeout=15,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                if response.status_code != 200:
                    print(f"Skipped ({response.status_code})")
                    continue

                html = response.text

                self.pages[url] = html

                soup = BeautifulSoup(html, "lxml")

                for link in soup.find_all("a", href=True):

                    href = urljoin(BASE_URL, link["href"])

                    href = self.normalize_url(href)

                    if self.is_internal(href):

                        if href not in self.visited:
                            queue.append(href)

            except Exception as e:

                print(f"Error: {e}")

        return self.pages


if __name__ == "__main__":

    crawler = WebsiteCrawler()

    pages = crawler.crawl()

    print("\n======================")

    print(f"Pages Found: {len(pages)}")

    print("======================\n")

    for page in pages:
        print(page)