from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class WeekDay(BaseModel):
    timestamp: str
    count: int
    uniques: int


class TrafficData(BaseModel):
    count: int
    uniques: int


class TrafficViewsData(TrafficData):
    views: List[WeekDay]


class TrafficClonesData(TrafficData):
    clones: List[WeekDay]


class TrafficPopularPathsData(BaseModel):
    path: str = Field(
        description="The URL path of the popular content on the repository's site.",
    )
    title: str = Field(
        description="The title of the page or content at the given path.",
    )
    count: int = Field(
        description="The total number of views for this path.",
    )
    uniques: int = Field(
        description="The number of unique visitors that have viewed this path.",
    )


class TrafficPopularReferrersData(BaseModel):
    referrer: str = Field(
        description="The domain name of the referring site or the "
        "source through which users reach the repository.",
    )
    count: int = Field(
        description="The total number of visits to the repository from this referrer.",
    )
    uniques: int = Field(
        description="The number of unique visitors coming to the repository from this referrer.",
    )


class RateLimitItem(BaseModel):
    limit: int = Field(
        description="The maximum number of requests "
        "that the consumer is permitted to make per hour.",
    )
    used: int = Field(
        description="The number of requests that have already been made "
        "by the consumer in the current rate limit window.",
    )
    remaining: int = Field(
        description="The number of requests that the consumer "
        "is allowed to make before the rate limit is reached.",
    )
    reset: int = Field(
        description="The time at which the current rate limit window resets in UTC epoch seconds.",
    )


class RateLimitResourceData(BaseModel):
    core: RateLimitItem = Field(
        description="Limits for most GitHub API requests.",
    )
    search: RateLimitItem = Field(
        description="Limits for search API requests, including user, repository, and code search.",
    )
    graphql: RateLimitItem = Field(
        description="Limits for GraphQL API requests.",
    )
    integration_manifest: RateLimitItem = Field(
        description="Limits for integration manifest API requests, used by GitHub Apps.",
    )
    source_import: RateLimitItem = Field(
        description="Limits for source import requests, such as "
        "importing repositories from other platforms.",
    )
    code_scanning_upload: RateLimitItem = Field(
        description="Limits for code scanning results upload requests.",
    )
    actions_runner_registration: RateLimitItem = Field(
        description="Limits for registering self-hosted runners for GitHub Actions.",
    )
    scim: RateLimitItem = Field(
        description="Limits for System for Cross-domain Identity Management "
        "(SCIM) API requests, used for automating user provisioning.",
    )
    dependency_snapshots: RateLimitItem = Field(
        description="Limits for requests related to capturing "
        "dependency snapshots for a repository.",
    )
    audit_log: RateLimitItem = Field(
        description="Limits for accessing the audit log API, which provides a record "
        "of actions taken by users in an organization.",
    )
    code_search: RateLimitItem = Field(
        description="Limits for requests to the code search API, specifically "
        "for searching within a repository's codebase.",
    )


class RateLimitData(BaseModel):
    resources: RateLimitResourceData = Field(
        description="All rate limited resources.",
    )
    rate: RateLimitItem = Field(
        description="Global rate limit stats.",
    )


class GitHubUserData(BaseModel):
    login: str = Field(description="The user's GitHub login name.")
    id: int = Field(description="The user's unique GitHub ID.")
    node_id: str = Field(description="The node ID of the user.")
    avatar_url: HttpUrl = Field(description="The URL of the user's avatar image.")
    gravatar_id: str = Field(description="The user's Gravatar ID.")
    url: HttpUrl = Field(description="The API URL of the user's profile.")
    html_url: HttpUrl = Field(description="The HTML URL of the user's GitHub profile.")
    followers_url: HttpUrl = Field(description="The API URL of the user's followers.")
    following_url: str = Field(
        description="The API URL template of the users followed by the user."
    )
    gists_url: str = Field(description="The API URL template of the user's gists.")
    starred_url: str = Field(description="The API URL template of the repos starred by the user.")
    subscriptions_url: HttpUrl = Field(description="The API URL of the user's subscriptions.")
    organizations_url: HttpUrl = Field(
        description="The API URL of the user's GitHub organizations."
    )
    repos_url: HttpUrl = Field(description="The API URL of the user's repositories.")
    events_url: str = Field(description="The API URL template of the user's events.")
    received_events_url: HttpUrl = Field(
        description="The API URL of the events received by the user."
    )
    type: str = Field(description="The type of the user account.")
    site_admin: bool = Field(description="Whether the user is a GitHub site administrator.")
    name: Optional[str] = Field(description="The name of the user.")
    company: Optional[str] = Field(description="The company the user works for.")
    blog: Optional[HttpUrl] = Field(description="The URL of the user's blog.")
    location: Optional[str] = Field(description="The user's location.")
    email: Optional[str] = Field(description="The user's email address.")
    hireable: Optional[bool] = Field(description="Whether the user is available for hire.")
    bio: Optional[str] = Field(description="The user's biography.")
    twitter_username: Optional[str] = Field(description="The user's Twitter username.")
    public_repos: int = Field(description="The number of public repositories owned by the user.")
    public_gists: int = Field(description="The number of public gists owned by the user.")
    followers: int = Field(description="The number of users following this user.")
    following: int = Field(description="The number of users this user is following.")
    created_at: str = Field(
        description="The ISO8601 timestamp of when the user account was created."
    )
    updated_at: str = Field(
        description="The ISO8601 timestamp of the last update to the user's profile."
    )
