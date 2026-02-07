FROM python:3.13-slim

WORKDIR /app

# Copy pyproject.toml first to cache dependencies (if we were using requirements, but here we install .)
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir .

COPY . .

# Expose port
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
