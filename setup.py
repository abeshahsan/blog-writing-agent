from setuptools import setup, find_packages

setup(
    name="blog-writing-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "langchain-openrouter",
        "langchain-community",
        "python-dotenv",
        "fastapi",
        "uvicorn",
        "from_root",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "jupyter",
            "ipykernel",
        ]
    },
    description="A blog writing agent using LangChain and OpenAI",
    author="Abesh Ahsan",
)
