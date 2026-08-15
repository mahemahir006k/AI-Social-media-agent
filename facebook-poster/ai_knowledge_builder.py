from crawler import WebsiteCrawler
from company_parser import CompanyParser


def get_company_text():

    crawler = WebsiteCrawler()
    parser = CompanyParser()

    pages = crawler.crawl()

    company_text = ""

    for url, html in pages.items():

        page = parser.clean_page(html)

        company_text += f"\n\n===== PAGE =====\n"
        company_text += f"URL: {url}\n\n"

        company_text += f"TITLE:\n{page['title']}\n\n"

        company_text += "HEADINGS:\n"

        for heading in page["headings"]:
            company_text += f"- {heading}\n"

        company_text += "\nPARAGRAPHS:\n"

        for paragraph in page["paragraphs"]:
            company_text += paragraph + "\n\n"

    return company_text


if __name__ == "__main__":

    text = get_company_text()

    print(text)

    with open("company_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("\n✅ company_text.txt created successfully.")