# python-playground

My Git repository for tinkering with Python – from simple scripts to fun mini-projects.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Medium Blog Scraper](#medium-blog-scraper-extract-titles-links-and-publishing-dates)
  * [Valid Medium Blog URL and content](#valid-medium-blog-url-and-content)
  * [Invalid Medium Blog URL](#invalid-medium-blog-url)
  * [Invalid URL](#invalid-url)
* [Read YAML config file](#read-yaml-config-file)
* [Fetch GitHub Repository Stats](#fetch-github-repository-stats)
* [License](#license)

## Prerequisites

This project's dependencies are managed by Poetry. See the `pyproject.toml` file for a complete list.

* **Poetry:** 1.8.2 or later. See installation instructions at https://python-poetry.org/docs/#installation
* **Python:** 3.12 or later.

## Medium Blog Scraper: Extract Titles, Links, and Publishing Dates

A Python script for scraping and compiling a list of article metadata from any Medium blog. By utilizing Selenium and BeautifulSoup to navigate and parse articles through infinite scroll pages, we extract titles, links, and publication dates and store this information in comma-separated text files (e.g., `blog_articles_rschu.me.csv`).

Running the script `poetry run medium_blog` will prompt for any Medium blog URL, including the discontinued custom Medium Blog domains.

### Valid Medium Blog URL and content

```bash
# poetry run medium_blog
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
# poetry run medium_blog
Enter the Medium Blog URL (e.g., https://rschu.me): https://google.com
Processing Blog articles from: https://google.com
'https://google.com' does not seem to be a Medium blog.
```

### Invalid URL

```bash
# poetry run medium_blog
Enter the Medium Blog URL (e.g., https://rschu.me): https://rschume
The given URL 'https://rschume' appears to be invalid.
```

## Read YAML config file

This utils helper is designed to read and validate YAML files.
It utilizes the Pydantic library to enforce type checking and validation for the [config.yaml](python_playground/assets/config.yaml) file.

```bash
# poetry run read_yaml_config
Config:  {
  "app": {
    "name": "MyPythonApp",
    "version": "1.0.0",
    "description": "A versatile Python application for various utilities.",
    "mode": "development"
  },
  "server": {
    "host": "127.0.0.1",
    "port": 8080,
    "enable_ssl": false,
    "ssl_certificate": "/path/to/ssl/certificate.pem"
  },
  "database": {
    "type": "sqlite",
    "sqlite": {
      "path": "/path/to/database.db"
    },
    "mysql": {
      "host": "localhost",
      "port": 3306,
      "username": "user",
      "password": "password",
      "database_name": "mydb"
    },
    "postgresql": {
      "host": "localhost",
      "port": 5432,
      "username": "user",
      "password": "password",
      "database_name": "mydb"
    }
  },
  "logging": {
    "level": "DEBUG",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": "logs/app.log",
    "rotate_logs": true,
    "max_log_size": "10MB",
    "backup_count": 5
  },
  "features": {
    "enable_feature_x": true,
    "enable_feature_y": false,
    "experimental_features": [
      "alpha_feature",
      "beta_feature"
    ]
  },
  "external_services": {
    "service_x": {
      "api_key": "3DEHJQQSTVWXXZcdeipqsv",
      "username": null,
      "password": null,
      "base_url": "https://api.service_x.com",
      "timeout_seconds": 30
    },
    "service_y": {
      "api_key": "3DEHJQQSTVWXXZcdeipqsv",
      "username": "user",
      "password": "pass",
      "base_url": "https://api.service_y.com",
      "timeout_seconds": 10
    }
  },
  "environments": {
    "development": {
      "debug_mode": true,
      "external_services": {
        "service_x": {
          "api_key": "devkey",
          "username": null,
          "password": null,
          "base_url": null,
          "timeout_seconds": 10
        }
      }
    },
    "production": {
      "debug_mode": false,
      "external_services": {
        "service_x": {
          "api_key": "prodkey",
          "username": null,
          "password": null,
          "base_url": null,
          "timeout_seconds": 10
        }
      }
    }
  },
  "custom": {
    "parameter1": "value1",
    "list_of_values": [
      "list_item_1",
      "list_item_2"
    ],
    "nested_config": {
      "sub_config1": "sub_value1",
      "sub_config2": "123"
    }
  }
}
```

## Fetch GitHub Repository Stats
The script requires a GitHub username, repository name, and API token,
all of which can be provided via script arguments or prompts.

> If arguments are missing, the script will prompt for them.

| Argument               |                                                                                                   |
|:-----------------------|:--------------------------------------------------------------------------------------------------|
| `-u` or `--username`   | GitHub username                                                                                   |
| `-r` or `--repository` | GitHub repository name                                                                            |
| `-t` or `--token`      | GitHub API token                                                                                  |
| `-m` or `--metrics`    | Comma-separated list of metrics data to process (e.g., rate_limit, user_info, traffic_views, etc. |

```bash
# With prompts.
poetry run github_stats

# Without prompts.
poetry run github_stats --repo <github_repository> --token <github_api_token> --metrics "user_info"

# Only the token and metrics will be prompted.
poetry run github_stats --repo <github_repository>
```

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
