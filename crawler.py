# crawler.py
import requests
from bs4 import BeautifulSoup

def extract_text(url):
    """
    Extracts main textual content from a webpage.
    Removes scripts, styles, headers, footers, navs, and asides.
    Returns text and page title.
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return "", None

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove irrelevant sections
        for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
            tag.decompose()

        # Page title
        title = soup.title.string.strip() if soup.title else "Untitled Page"

        # Attempt to find main article
        article = soup.find("article") \
               or soup.find("div", class_="text") \
               or soup.find("div", class_="entry-content")

        if article is None:
            return "", title

        text = article.get_text(separator=" ")
        text = " ".join(text.split())

        return text, title

    except Exception:
        return "", None
