#!/usr/bin/env bash
set -euo pipefail

echo "Installing dependencies (including dev extras)..."
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

echo "Running tests..."
pytest -q

echo "Building Docker image..."
IMAGE_NAME="${IMAGE_NAME:-blog-writing-agent:latest}"
docker build -t "$IMAGE_NAME" .

echo "Pipeline completed: $IMAGE_NAME"
