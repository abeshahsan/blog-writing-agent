FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY setup.py ./
COPY blog_writing_agent ./blog_writing_agent

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

COPY . .


EXPOSE 8000

ENV ENV_MODE=production
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]