import argparse
import os
from pathlib import Path
from typing import Sequence

import dotenv
from from_root import from_root


def env_setup(argv: Sequence[str] | None = None) -> str:
    parser = argparse.ArgumentParser(
        description="Run the blog writing agent with optional environment mode"
    )
    parser.add_argument(
        "--env",
        choices=["development", "production", "test"],
        default=os.getenv("ENV_MODE", "development"),
        help="Environment mode to load",
    )

    args = parser.parse_args(argv)
    env_mode = args.env
    project_root = from_root()

    base_env_path = project_root / ".env"
    selected_env_path = project_root / f".env.{env_mode}"

    if base_env_path.exists():
        dotenv.load_dotenv(dotenv_path=base_env_path, override=False)

    if not selected_env_path.exists():
        raise FileNotFoundError(f"Environment file not found: {selected_env_path}")

    dotenv.load_dotenv(dotenv_path=selected_env_path, override=True)
    os.environ["ENV_MODE"] = env_mode
    return env_mode


def main() -> None:
    env_mode = env_setup()
    print(f"Using env: {env_mode}")

    from blog_writing_agent import BlogService

    service = BlogService()
    result = service.generate_blog("Write a blog on Self Attention")
    print(result["final"])


if __name__ == "__main__":
    main()
