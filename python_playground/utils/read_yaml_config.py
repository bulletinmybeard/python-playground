import json
import os
from typing import Any, Optional

import yaml
from pydantic import ValidationError

from python_playground.models.project_config import ProjectConfig


class ConfigManager:
    _config: Optional[ProjectConfig] = None

    @classmethod
    def load_config(cls, config_file_path: str) -> Optional[ProjectConfig]:
        """
        Load and validate configuration from a YAML file.
        """
        if not os.path.exists(config_file_path):
            raise FileNotFoundError("Config file not found: %s", config_file_path)

        with open(config_file_path, "r") as f:
            raw_config = yaml.safe_load(f)

        try:
            cls._config = ProjectConfig(**raw_config)
            return cls._config
        except ValidationError as e:
            errors = e.errors()
            simplified_errors = [
                {
                    "msg": error["msg"],
                    "type": error["type"],
                    "field": error["loc"][1] if len(error["loc"]) > 1 else None,
                }
                for error in errors
            ]
            print(simplified_errors)
            return None

    @classmethod
    def get_config(cls) -> ProjectConfig:
        """
        Access the loaded configuration. Ensures configuration is loaded.
        """
        if cls._config is None:
            raise ValueError("Configuration has not been loaded.")
        return cls._config


def main() -> None:
    config = ConfigManager.load_config("python_playground/assets/config.yaml")
    if config:
        config_json: Any = json.dumps(config.dict(), indent=2)
        print("Config: ", config_json)


if __name__ == "__main__":
    main()
