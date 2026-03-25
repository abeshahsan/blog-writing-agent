import os
from pathlib import Path

import dotenv


VALID_ENV_MODES = {"development", "production", "test"}


def bootstrap_env_mode() -> str:
    env_mode = os.environ.get("ENV_MODE")

    if not env_mode:
        raise RuntimeError("ENV_MODE is not set")

    if env_mode not in VALID_ENV_MODES:
        raise ValueError(f"Invalid ENV_MODE: {env_mode}")

    project_root = Path(__file__).resolve().parent
    base_env_path = project_root / ".env"
    selected_env_path = project_root / f".env.{env_mode}"

    if base_env_path.exists():
        dotenv.load_dotenv(dotenv_path=base_env_path, override=False)

    if not selected_env_path.exists():
        raise FileNotFoundError(f"Environment file not found: {selected_env_path}")

    dotenv.load_dotenv(dotenv_path=selected_env_path, override=True)
    os.environ["ENV_MODE"] = env_mode
    return env_mode
