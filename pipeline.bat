@echo off
setlocal enabledelayedexpansion

echo Installing dependencies (including dev extras)...
python -m pip install --upgrade pip || goto :error
python -m pip install -e .[dev] || goto :error

echo Running tests...
pytest -q || goto :error

echo Building Docker image...
if "%IMAGE_NAME%"=="" set IMAGE_NAME=blog-writing-agent:latest
docker build -t %IMAGE_NAME% . || goto :error

echo Pipeline completed: %IMAGE_NAME%

echo To run the Docker container:
echo docker run -d --name blog-writing-agent -p 8000:8000 %IMAGE_NAME%
goto :eof

:error
echo Pipeline failed with error code %errorlevel%.
exit /b %errorlevel%
