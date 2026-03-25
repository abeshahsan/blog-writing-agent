import os
from pathlib import Path

import dotenv


VALID_ENV_MODES = {"development", "production", "test"}


def bootstrap_env_mode() -> str:
    passed_env_mode = os.environ.get("ENV_MODE")
    env_mode = passed_env_mode or "development"

    # Keep development as the default, but only allow explicit overrides to
    # production or test.
    if passed_env_mode and passed_env_mode not in {"production", "test"}:
        raise ValueError(
            "When ENV_MODE is set explicitly, it must be either 'production' or 'test'"
        )

    if env_mode not in VALID_ENV_MODES:
        raise ValueError(f"Invalid ENV_MODE: {env_mode}")

    os.environ["ENV_MODE"] = env_mode

    project_root = Path(__file__).resolve().parent
    base_env_path = project_root / ".env"
    selected_env_path = project_root / f".env.{env_mode}"

    if base_env_path.exists():
        dotenv.load_dotenv(dotenv_path=base_env_path, override=False)

    if not selected_env_path.exists():
        raise FileNotFoundError(f"Environment file not found: {selected_env_path}")

    dotenv.load_dotenv(dotenv_path=selected_env_path, override=True)

    return env_mode
