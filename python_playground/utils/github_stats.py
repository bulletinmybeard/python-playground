import argparse
import json
from typing import Any, Dict, List, Tuple, Union

from pydantic import parse_obj_as
from requests import HTTPError, Response, Session

from python_playground.models.github_stats import (
    GitHubUserData,
    RateLimitData,
    TrafficClonesData,
    TrafficPopularPathsData,
    TrafficPopularReferrersData,
    TrafficViewsData,
)

valid_data_items = [
    "rate_limit",
    "user_info",
    "traffic_views",
    "traffic_clones",
    "traffic_popular_referrers",
    "traffic_popular_paths",
]

parser = argparse.ArgumentParser(description="GitHub Statistics Collector")
parser.add_argument("-u", "--username", required=True, help="GitHub username", type=str)
parser.add_argument("-r", "--repo", required=True, help="GitHub repository name", type=str)
parser.add_argument("-t", "--token", required=True, help="GitHub API token", type=str)
parser.add_argument(
    "-d",
    "--data",
    required=False,
    help="Comma separated list of data to process: rate_limit, user_info, traffic_views, etc.",
    type=str,
)

args = parser.parse_args()


class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Pydantic models."""

    def default(self, obj: Any) -> Any:
        if hasattr(obj, "scheme"):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


class GitHubApiClient:

    process_data_items: List[str] = []

    """GitHub REST API client."""

    def __init__(self, username: str, repo: str, token: Union[str, None] = None):
        self.username = username
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.session = Session()
        self.session.headers.update({"Authorization": f"token {token}"} if token else {})
        self.process_arg_data()

    def request(self, path: str, requires_repo: bool = True) -> Union[Any, Response]:
        """Handle REST API requests."""
        if requires_repo and self.username and self.repo:
            url = f"{self.base_url}/repos/{self.username}/{self.repo}/{path}"
        else:
            url = f"{self.base_url}/{path}"

        response = self.session.get(url)
        try:
            response.raise_for_status()
        except HTTPError as e:
            raise Exception(
                f"API request failed with status {response.status_code}: {response.text}. Error: {str(e)}"  # noqa: E501
            )
        return response.json()

    def get_user_info(self) -> GitHubUserData:
        """Get the GitHub user information."""
        return parse_obj_as(GitHubUserData, self.request("user", False))

    def get_rate_limit(self) -> RateLimitData:
        """Get the GitHub users rate limit for all resources."""
        return parse_obj_as(RateLimitData, self.request("rate_limit", False))

    def get_traffic_clones(self) -> TrafficClonesData:
        """Get the GitHub branch traffic information: (Unique) Clones."""
        return parse_obj_as(TrafficClonesData, self.request("traffic/clones"))

    def get_traffic_views(self) -> TrafficViewsData:
        """Get the GitHub branch traffic information: (Unique) Views."""
        return parse_obj_as(TrafficViewsData, self.request("traffic/views"))

    def get_traffic_popular_paths(self) -> List[TrafficPopularPathsData]:
        """Get the GitHub branch traffic information: (Unique) Popular paths."""
        return parse_obj_as(List[TrafficPopularPathsData], self.request("traffic/popular/paths"))

    def get_traffic_popular_referrers(self) -> List[TrafficPopularReferrersData]:
        """Get the GitHub branch traffic information: Popular referrers."""
        return parse_obj_as(
            List[TrafficPopularReferrersData], self.request("traffic/popular/referrers")
        )

    def process_arg_data(self) -> None:
        """Process each item in the comma separated list."""
        # data_items = self.process_data_items
        if args.data:
            data_items = []
            options = args.data.split(",")
            for option in options:
                item = option.strip().lower()
                if item not in valid_data_items or item in data_items:
                    print(f"Invalid data item: {item} (skip)")
                else:
                    data_items.append(item)
            self.process_data_items = data_items
        else:
            self.process_data_items = valid_data_items

    @staticmethod
    def transform_response(data: Any) -> Union[Any, Tuple[Dict[Any, Any], ...]]:
        if isinstance(data, List):
            return [item.dict() for item in data]
        else:
            return data.dict()

    @staticmethod
    def json_stdout(stdout: Any) -> Any:
        if "views" in stdout["traffic"]:
            stdout["traffic"]["views"]["data"] = stdout["traffic"]["views"].pop("views")
        if "clones" in stdout["traffic"]:
            stdout["traffic"]["clones"]["data"] = stdout["traffic"]["clones"].pop("clones")
        return json.dumps(stdout, indent=2, cls=CustomJSONEncoder)


def main() -> None:
    client = GitHubApiClient(args.username, args.repo, args.token)

    data_methods = {
        "traffic_clones": client.get_traffic_clones,
        "traffic_views": client.get_traffic_views,
        "rate_limit": client.get_rate_limit,
        "user_info": client.get_user_info,
        "traffic_popular_paths": client.get_traffic_popular_paths,
        "traffic_popular_referrers": client.get_traffic_popular_referrers,
    }

    stdout: Dict[str, Any] = {"traffic": {}}

    for data_item in client.process_data_items:
        if data_item in data_methods:
            response = data_methods[data_item]()
            if "traffic" in data_item:
                key = data_item.replace("traffic_", "")
                stdout["traffic"][key] = client.transform_response(response)
            else:
                stdout[data_item] = client.transform_response(response)

    print(client.json_stdout(stdout))


if __name__ == "__main__":
    main()
