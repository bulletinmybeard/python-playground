from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ExperimentalFeature(str, Enum):
    ALPHA_FEATURE = "alpha_feature"
    BETA_FEATURE = "beta_feature"


class AppConfig(BaseModel):
    name: str = Field(
        description="Application name",
    )
    version: str = Field(
        description="Application version",
    )
    description: Optional[str] = Field(
        description="Application description",
    )
    mode: Optional[str] = Field(
        description="Application mode",
    )


class ServerConfig(BaseModel):
    host: str = Field(description="Server host address")
    port: int = Field(description="Server port")
    enable_ssl: Optional[bool] = Field(default=False, description="Flag to enable SSL")
    ssl_certificate: Optional[str] = Field(description="Path to the SSL certificate")


class SQLiteConfig(BaseModel):
    path: Optional[str] = Field(description="Path to SQLite database file")


class MySQLConfig(BaseModel):
    host: str = Field(description="MySQL server host")
    port: int = Field(description="MySQL server port")
    username: str = Field(description="MySQL username")
    password: str = Field(description="MySQL password")
    database_name: str = Field(description="MySQL database name")


class PostgreSQLConfig(BaseModel):
    host: str = Field(description="PostgreSQL server host")
    port: int = Field(description="PostgreSQL server port")
    username: str = Field(description="PostgreSQL username")
    password: str = Field(description="PostgreSQL password")
    database_name: str = Field(description="PostgreSQL database name")


class DatabaseConfig(BaseModel):
    type: str = Field(description="Database type")
    sqlite: Optional[SQLiteConfig] = Field(description="SQLite configuration")
    mysql: Optional[MySQLConfig] = Field(description="MySQL configuration")
    postgresql: Optional[PostgreSQLConfig] = Field(description="PostgreSQL configuration")


class LoggingConfig(BaseModel):
    level: str = Field(description="Logging level")
    format: str = Field(description="Logging format")
    log_file: str = Field(description="Path to log file")
    rotate_logs: Optional[bool] = Field(default=False, description="Flag to enable log rotation")
    max_log_size: Optional[str] = Field(
        default=1000, description="Maximum log file size before rotation"
    )
    backup_count: Optional[int] = Field(default=10, description="Number of backup logs to keep")


class FeaturesConfig(BaseModel):
    enable_feature_x: Optional[bool] = Field(default=False, description="Flag to enable feature X")
    enable_feature_y: Optional[bool] = Field(default=False, description="Flag to disable feature Y")
    experimental_features: List[ExperimentalFeature] = Field(
        description="List of experimental features"
    )


class ServiceConfig(BaseModel):
    api_key: Optional[str] = Field(default=None, description="API key for the service")
    username: Optional[str] = Field(default=None, description="Username for the service")
    password: Optional[str] = Field(default=None, description="Password for the service")
    base_url: Optional[str] = Field(default=None, description="Base URL for the service")
    timeout_seconds: Optional[int] = Field(
        default=10, description="Timeout in seconds for the service"
    )


class ExternalServicesConfig(BaseModel):
    service_x: Optional[ServiceConfig] = Field(description="Configuration for service X")
    service_y: Optional[ServiceConfig] = Field(description="Configuration for service Y")


class EnvironmentConfig(BaseModel):
    debug_mode: Optional[bool] = Field(default=False, description="Flag to enable debug mode")
    external_services: Optional[Dict[str, ServiceConfig]] = Field(
        default={}, description="External services configuration per environment"
    )


class EnvironmentsConfig(BaseModel):
    development: EnvironmentConfig = Field(
        default=EnvironmentConfig(
            debug_mode=True,
        ),
        description="Development environment configuration",
    )
    production: Optional[EnvironmentConfig] = Field(
        default=None, description="Production environment configuration"
    )


class CustomConfig(BaseModel):
    parameter1: Optional[str] = Field(default=None, description="A custom parameter for testing")
    list_of_values: Optional[List[str]] = Field(
        default=[], description="A list of values for testing"
    )
    nested_config: Optional[Dict[str, str]] = Field(
        default={}, description="A nested configuration for testing"
    )


class ProjectConfig(BaseModel):
    app: Optional[AppConfig] = Field(default=None, description="Application configuration")
    server: Optional[ServerConfig] = Field(default=None, description="Server configuration")
    database: Optional[DatabaseConfig] = Field(default=None, description="Database configuration")
    logging: Optional[LoggingConfig] = Field(default=None, description="Logging configuration")
    features: Optional[FeaturesConfig] = Field(default=None, description="Feature toggles")
    external_services: Optional[ExternalServicesConfig] = Field(
        default=None, description="External services configuration"
    )
    environments: Optional[EnvironmentsConfig] = Field(description="Environment specific settings")
    custom: Optional[CustomConfig] = Field(
        default=None, description="Custom configurations for testing"
    )

    # Forbid extra fields and raise an exception if any are found.
    class Config:
        extra = "forbid"
