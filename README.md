﻿# 📌 URL Shortener

A **scalable** and **efficient** URL shortening service built with **Django**, **PostgreSQL**, and **Redis**. This project provides a RESTful API for shortening URLs and managing shortened links with an optional frontend interface.

---

## 🚀 Features

✅ **Create Short URLs** – Convert long URLs into short, user-friendly links.  
✅ **Redirect to Original URL** – Quickly navigate to the original long URL using the short link.  
✅ **Expiration Handling** – URLs can have expiration times for automatic deletion.  
✅ **Rate Limiting** – Prevent abuse by limiting API requests per user.  
✅ **Caching for Performance** – Uses **Redis** to cache redirects and reduce database load.  
✅ **Dockerized Deployment** – Run the entire application using **Docker & Docker Compose**.  

---

## 🛠️ Installation & Setup

### 🖥️ Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started) & Docker Compose
- Python 3.11+

---

### 🐳 Running with Docker (Recommended)

To start the project using **Docker**, simply run:

```sh
docker-compose up --build
```

This will:

- Start the **Django API** (`backend`)
- Start the **HTML/JS/CSS Frontend** (`frontend`)
- Start the **PostgreSQL Database**
- Start the **Redis Cache**
- Start the **Celery Worker** for async tasks

Once running, the services will be available at:

- **Backend API:** [`http://127.0.0.1:8000/api/`](http://127.0.0.1:8000/api/)
- **Frontend App:** [`http://127.0.0.1:8001/`](http://127.0.0.1:8001/)

To stop all containers:

```sh
docker-compose down -v
```

---

## 🔗 API Endpoints

### 🔹 **Shorten a URL**
**`POST /api/shorten/`**  
_Request Body:_
```json
{
  "long_url": "https://example.com"
}
```
_Response:_
```json
{
  "short_url": "http://short-url.xyz/abc123",
  "expires_at": "2025-03-09 18:45:07"
}
```

### 🔹 **Retrieve Original URL**
**`GET /api/retrieve/?short_url=abc123`**  
_Response:_
```json
{
  "long_url": "https://example.com"
}
```

### 🔹 **Analytics**
**`GET /api/stats/?short_url=abc123`**  
_Response:_
```json
{
  "original_url": "https://example.com",
  "visit_count": 42
}
```

---


## 💡 Contributing

We welcome contributions! Feel free to:

- Report issues via [GitHub Issues](https://github.com/dd288/url-shortening/issues)
- Fork the repo and submit pull requests

---
