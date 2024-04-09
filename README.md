# python-playground

My Git repository for tinkering with Python – from simple scripts to fun mini-projects.

## Table of Contents
* [Prerequisites](#prerequisites)
* [Medium Blog Scraper](#medium-blog-scraper-extract-titles-links-and-publishing-dates)
  * [Valid Medium Blog URL and content](#valid-medium-blog-url-and-content)
  * [Invalid Medium Blog URL](#invalid-medium-blog-url)
  * [Invalid URL](#invalid-url)
* [License](#license)


## Prerequisites
This project's dependencies are managed by Poetry. See the `pyproject.toml` file for a complete list.

* **Poetry:** 1.8.2 or later. See installation instructions at https://python-poetry.org/docs/#installation
* **Python:** 3.12 or later.


## Medium Blog Scraper: Extract Titles, Links, and Publishing Dates
A simple Python script for scraping and compiling a list of article metadata from any Medium blog. By utilizing Selenium and BeautifulSoup to navigate and parse articles through infinite scroll pages, we extract titles, links, and publication dates and store this information in comma-separated text files (e.g., `blog_articles_rschu.me.csv`).

Running the script `poetry run medium_blog` will prompt for any Medium blog URL, including the discontinued custom Medium Blog domains. 

### Valid Medium Blog URL and content
```bash
Enter the Medium Blog URL (e.g., https://rschu.me): https://rschu.me
Processing Blog articles from: https://rschu.me
Found 113 articles so far                [/]

------------------
113 Articles found
------------------

Example:
Title:  Unlock the ability to place bets using Twitch Channel Points for chat predictions.
Link:  https://rschu.me/unlock-placing-bets-with-twitch-channel-points-for-chat-predictions-783c2eadeab8
Published at:  Dec 28, 2021

CSV file created: .../blog_articles_rschu.me.csv
```

### Invalid Medium Blog URL
```bash
Enter the Medium Blog URL (e.g., https://rschu.me): https://google.com
Processing Blog articles from: https://google.com
'https://google.com' does not seem to be a Medium blog.
```

### Invalid URL
```bash
Enter the Medium Blog URL (e.g., https://rschu.me): https://rschume
The given URL 'https://rschume' appears to be invalid.
```

## License
This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
