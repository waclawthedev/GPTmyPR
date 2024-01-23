import json
import sys
from enum import Enum, auto
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt


class Config:
    class ConfigFields(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name

        github_token = auto()
        reaction_to_mark_comment_as_read = auto()
        openai_apikey = auto()
        openai_model = auto()

    def __init__(self, path: str):
        self._config_data = {}
        self._path = Path(path)
        self._load_or_create()

    def __getattr__(self, item):
        if item in self._config_data:
            return self._config_data[item]
        raise AttributeError(f"{item} not found in configuration.")

    def _load_or_create(self):
        if self._path.is_file():
            self._load_config()
        else:
            self._create_config()
            self._save_config()

    def _save_config(self):
        with self._path.open("w") as f:
            json.dump(self._config_data, f, indent=4)

    def _load_config(self):
        try:
            with self._path.open("r") as f:
                self._config_data = json.load(f)
                self._validate_config()
        except Exception as e:
            Console(stderr=True, style="bold red").print(
                f"Failed to load configuration from {self._path}. Error: {e}. Please ensure the file is valid or remove it to proceed."
            )
            sys.exit(1)

    def _create_config(self):
        Console(style="bold green").print(
            f"Configuration file will be created at: {self._path}"
        )
        for field in Config.ConfigFields:
            if field is Config.ConfigFields.openai_model:
                default = "gpt-4-1106-preview"
            elif field is Config.ConfigFields.reaction_to_mark_comment_as_read:
                default = "eyes"
                choices = [
                    "+1",
                    "-1",
                    "laugh",
                    "confused",
                    "heart",
                    "hooray",
                    "rocket",
                    "eyes",
                ]
                self._config_data[field.value] = Prompt.ask(
                    f"{field.value}", choices=choices, default=default
                )
                continue
            else:
                default = None

            self._config_data[field.value] = Prompt.ask(
                f"{field.value}", default=default
            )

    def _validate_config(self):
        for field in Config.ConfigFields:
            if not self._config_data.get(field.value):
                Console(stderr=True, style="bold red").print(
                    f"Missing configuration: '{field.value}' must be set in the config file '{self._path}'."
                )
                sys.exit(1)
