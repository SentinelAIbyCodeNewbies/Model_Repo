# n8n Workflow Setup Guide

This repository contains an **n8n workflow JSON** that helps analyze links and videos by routing requests through webhook endpoints, downloading Instagram media when needed, and forwarding data to your local backend API.

---

## 📦 Prerequisites

Before running this workflow locally, make sure you have:

* **Docker Desktop** installed
* **Git** installed
* Your **backend API running on port `8080`**
* The exported workflow JSON file present in this repo

---

## 🐳 Install & Run n8n Locally with Docker

The easiest way for teammates to run n8n is through Docker.

### 1) Create a `docker-compose.yml`

Create this file in the root of the project:

```yaml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

### 2) Start n8n

Run:

```bash
docker compose up -d
```

### 3) Open n8n

Visit:

```text
http://localhost:5678
```

Create your local owner account on first launch.

---

## 📥 Import the Workflow JSON

After n8n is running:

1. Open **n8n dashboard**
2. Click **“Import from File”**
3. Select the workflow JSON from this repository
4. Save the workflow
5. Make sure the workflow is **Active**

---

## ⚙️ Important Backend Requirement

This workflow sends requests to a local backend running on:

```text
http://host.docker.internal:8080
```

Your teammates must make sure the backend service is running locally before testing the workflow.

Required endpoints:

* `POST /analyze_video`
* `POST /analyze_url`

### If using Mac / Windows

`host.docker.internal` works directly.

### If using Linux

Replace `host.docker.internal` with your machine IP or use:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

inside the n8n Docker service.

---

## 🔐 RapidAPI Key Setup (Important)

The current workflow includes a **hardcoded RapidAPI key** for Instagram reels download.

For security, teammates should **replace it with their own key**.

### Recommended way

In n8n:

1. Open the **HTTP Request** node for Instagram download
2. Replace the header:

```json
"x-rapidapi-key": "YOUR_RAPIDAPI_KEY"
```

3. Use your own RapidAPI subscription key

> ⚠️ Never commit real API keys to GitHub.

---

## 🧠 How This Workflow Works

### Flow Logic

1. A **Webhook** receives a POST request with a URL
2. **Switch node checks** if the URL contains `instagram.com`
3. If **Instagram URL**:

   * Download reel metadata from RapidAPI
   * Download actual media file
   * Send video file to `/analyze_video`
4. If **normal URL**:

   * Send URL directly to `/analyze_url`
5. Return response back through webhook

---

## 🧪 Test the Workflow

Use Postman / frontend / curl:

```bash
curl -X POST http://localhost:5678/webhook/YOUR_WEBHOOK_ID \
-H "Content-Type: application/json" \
-d '{"url":"https://example.com/video.mp4"}'
```

For Instagram:

```bash
curl -X POST http://localhost:5678/webhook/YOUR_WEBHOOK_ID \
-H "Content-Type: application/json" \
-d '{"url":"https://www.instagram.com/reel/XYZ/"}'
```

---

## 🚀 Team Collaboration Workflow

Recommended workflow for teammates:

```bash
git clone <repo-url>
cd <repo-name>
docker compose up -d
```

Then:

* Start backend locally
* Import workflow JSON
* Add their own API keys
* Test webhook endpoint

---

## 🛠 Troubleshooting

### n8n cannot reach backend

* Ensure backend is running on port `8080`
* Verify `host.docker.internal` works
* Linux users may need `host-gateway`

### Instagram download fails

* Check RapidAPI key validity
* Verify API subscription is active

### Webhook not responding

* Make sure workflow is **Active**
* Use correct webhook URL from n8n

---

## ✅ Recommended Repo Structure

```text
.
├── docker-compose.yml
├── README.md
├── workflow.json
└── backend/
```

---

## 💡 Best Practice Suggestion

For better collaboration, store:

* workflow JSON exports
* backend `.env.example`
* sample request payloads
* Postman collection

This makes hackathon onboarding much faster for your teammates.
