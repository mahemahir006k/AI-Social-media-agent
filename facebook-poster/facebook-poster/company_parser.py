from bs4 import BeautifulSoup


class CompanyParser:

    def clean_page(self, html):

        soup = BeautifulSoup(html, "lxml")

        # Remove unwanted tags
        for tag in soup([
            "script",
            "style",
            "header",
            "footer",
            "nav",
            "svg",
            "noscript",
            "form",
            "img"
        ]):
            tag.decompose()

        data = {
            "title": "",
            "headings": [],
            "paragraphs": [],
            "lists": []
        }

        # Page title
        if soup.title:
            data["title"] = soup.title.get_text(strip=True)

        # Headings
        for tag in soup.find_all(["h1", "h2", "h3"]):
            text = tag.get_text(" ", strip=True)
            if text:
                data["headings"].append(text)

        # Paragraphs
        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)

            if len(text) > 30:
                data["paragraphs"].append(text)

        # Lists
        for ul in soup.find_all(["ul", "ol"]):

            items = []

            for li in ul.find_all("li"):

                text = li.get_text(" ", strip=True)

                if text:
                    items.append(text)

            if items:
                data["lists"].append(items)

        return data