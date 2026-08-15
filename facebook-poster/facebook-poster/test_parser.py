from crawler import WebsiteCrawler
from company_parser import CompanyParser

crawler = WebsiteCrawler()
pages = crawler.crawl()

parser = CompanyParser()

for url, html in pages.items():

    print("="*80)
    print(url)

    parsed = parser.clean_page(html)

    print(parsed["title"])
    print()

    print(parsed["headings"][:5])