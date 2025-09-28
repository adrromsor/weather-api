# Weather API 🌦️

A lightweight FastAPI application that acts as a wrapper around third-party weather providers.
The API exposes a unified and typed interface so clients don’t need to deal with different provider formats.

## 📦 Installation

Clone the repo:

<code>git clone https://github.com/adrromsor/weather-api.git</code><br>

Install dependencies using uv:

<code>uv sync</code>

## ▶️ Running the app

Run with Uvicorn:

<code>uv run uvicorn src.weather.api.main:app --reload</code>

The API will be available at:

http://127.0.0.1:8000


## 📜 Interactive docs:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc