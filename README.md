# 🧠 AI Cache Saver

> **Return Semantically similar Images based on Vector Embeddings.**

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

---

## 📖 About The Project

**AI Cache Saver** is a full-stack application designed to optimize AI-generated content storage and retrieval. It uses vector embeddings to understand the *meaning* of an image prompt, allowing users to find semantically similar images instantly without regenerating them.

### ✨ Key Features
* **Semantic Search:** Find images based on meaning, not just keywords.
* **Vector Embeddings:** Powered by PostgreSQL (pgvector).
* **Secure Auth:** JWT-based authentication (Sign up/Login).
* **Media Storage:** Integration with Cloudinary for image/video assets.
* **Containerized:** Fully Dockerized for easy deployment.

---

## 🛠️ Tech Stack

### **Backend**
* **Framework:** FastAPI (Python 3.11)
* **Database:** PostgreSQL 15 (with Alembic migrations)
* **Package Manager:** UV (Ultra-fast python package installer)
* **ORM:** SQLAlchemy

### **Frontend**
* **Framework:** React (Vite)
* **Language:** TypeScript
* **Styling:** SCSS / Ant Design
* **Server:** Nginx

---

## 🚀 Getting Started

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
Make sure you have the following installed:
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Running)
* Git

### 2. Clone the Repository
```bash
git clone https://github.com/Jack-Yong-Teoh/ai-cache-saver.git
cd ai-cache-saver
```

### 3. Request the `.env` File
This project requires a `.env` file that contains sensitive configuration such as API keys. Please request the `.env` file directly from the author. Once obtained, place the `.env` file in the root directory of the project.

### 4. Run the Docker Command in the root directory
```bash
docker-compose up --build
```
### Extra:
Remove the container using this command:
```bash
docker-compose down -v
```