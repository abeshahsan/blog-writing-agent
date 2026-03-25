FROM python:3.12-slim

WORKDIR /app

COPY setup.py ./
COPY blog_writing_agent ./blog_writing_agent
COPY app.py bootstrap.py ./
COPY frontend ./frontend
COPY .env.production ./.env.production

RUN pip install --no-cache-dir --upgrade pip \
	&& pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]