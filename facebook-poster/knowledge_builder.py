import json
import re

from crawler import WebsiteCrawler
from company_parser import CompanyParser


class KnowledgeBuilder:

    def __init__(self):
        self.crawler = WebsiteCrawler()
        self.parser = CompanyParser()

    def extract_services(self, page):

        services = []

        headings = page["headings"]
        paragraphs = page["paragraphs"]

        for i, heading in enumerate(headings):

            if len(heading) < 80:

                description = ""

                if i < len(paragraphs):
                    description = paragraphs[i]

                services.append({
                    "name": heading,
                    "description": description
                })

        return services

    def build(self):

        pages = self.crawler.crawl()

        company = {
            "company": {},
            "services": [],
            "pages": []
        }

        parser = CompanyParser()

        for url, html in pages.items():

            page = parser.clean_page(html)

            company["pages"].append(page)

            if url == "https://xenhra.in":

                company["company"] = {
                    "name": page["title"],
                    "about": page["paragraphs"][0] if page["paragraphs"] else "",
                    "website": url
                }

            company["services"].extend(
                self.extract_services(page)
            )

        # Remove duplicate services
        unique = {}

        for service in company["services"]:

            unique[service["name"]] = service

        company["services"] = list(unique.values())

        with open(
            "company_data.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                company,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("Knowledge Base Updated")


if __name__ == "__main__":

    KnowledgeBuilder().build()