import csv
import os
import re
import time
from typing import Any, Generator
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver

ua: Any = UserAgent()


def is_valid_url(url: str) -> bool:
    # Check for a valid scheme and netloc.
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return False

    # Regular expression for validating a URL.
    regex = re.compile(
        r"^(?:http|ftp)s?://"
        r"(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)"  # noga
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, url) is not None


def spinner() -> Generator[str, None, None]:
    while True:
        for character in "|/-\\":
            yield character


def status_loader_text(articles_found: int, spinner_char: str) -> str:
    """Prints a message with a right-aligned spinner."""
    base_text = "Found {} articles so far"
    filler_spaces = max(0, 40 - len(base_text.format(articles_found)))
    return f"\r{base_text.format(articles_found)}{filler_spaces*' '} [{spinner_char}]"


def main() -> None:
    # ----- Site configuration -----
    scroll_pause_time = 2
    scrolls_before_check = 2
    default_blog_url = "https://rschu.me"
    blog_url = (
        input(f"Enter the Medium Blog URL (e.g., {default_blog_url}): ").strip("/")
        or default_blog_url
    )

    if not is_valid_url(blog_url):
        print(f"The given URL '{blog_url}' appears to be invalid.", end="", flush=True)
        exit(0)

    spin = spinner()

    print(f"Processing Blog articles from: {blog_url}")

    # ----- Webdriver setup -----
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={ua.random}")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.get(blog_url)

    # ----- Scrolling and data extraction -----
    last_height = driver.execute_script("return document.body.scrollHeight")  # type: ignore
    articles_data = []

    while True:
        # Scroll to the bottom of the page.
        for _ in range(scrolls_before_check):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # type: ignore
            time.sleep(scroll_pause_time)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")

        is_medium_url = bool(soup.find("meta", {"content": "com.medium.reader"}))
        if not is_medium_url:
            print(
                f"\r'{blog_url}' does not appear to be a Medium blog.",
                end="",
                flush=True,
            )
            exit(0)

        # Check if we've reached the end of the page.
        new_height = driver.execute_script("return document.body.scrollHeight")  # type: ignore
        if new_height == last_height:
            break
        last_height = new_height

        # Extract articles from the page.
        articles = soup.find_all("article")
        for article in articles:
            link_url = ""
            publishing_date = "not-found"
            links = article.find_all("a")

            # Find the primary article link within the 'article' block.
            for link in links:
                href = link.get("href")
                if href and href.startswith("/"):
                    parsed_url = urlparse(href)
                    full_url = urljoin(blog_url, parsed_url.path)
                    link_url = full_url
                    break

            date_pattern = re.compile(
                r"\bJan|Feb|Mar|Apr|May|Jun|Jul|" r"Aug|Sep|Oct|Nov|Dec\b \d{1,2}, \d{4}"
            )
            date_tag = article.find(string=date_pattern)
            if date_tag:
                publishing_date = date_tag

            title = article.find("h2")
            if title:
                articles_data.append(
                    {
                        "title": title.text,
                        "link": link_url,
                        "published": publishing_date,
                    }
                )

        print(
            f"\r{status_loader_text(len(articles_data), next(spin))}",
            end="",
            flush=True,
        )

    # ----- Results -----
    result_text = f"{len(articles_data)} Articles found"
    separator_line = "-" * len(result_text)

    print(f"\n\n{separator_line}")
    print(result_text)
    print(f"{separator_line}")

    if len(articles_data) > 0:
        print("\nExample:")
        print("Title: ", articles_data[0]["title"])
        print("Link: ", articles_data[0]["link"])
        print("Published at: ", articles_data[0]["published"])

        try:
            # Save the result to a CSV file.
            domain_name = urlparse(blog_url).netloc
            csv_filename = f"blog_articles_{domain_name}.csv"

            with open(csv_filename, "w", newline="") as csvfile:
                fieldnames = ["title", "link", "published"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(articles_data)

                print(f"\nCSV file created: {os.path.abspath(csv_filename)}")
        except Exception as e:
            print(f"Error: {str(e)}")

    # Close the browser.
    driver.quit()


if __name__ == "__main__":
    main()
