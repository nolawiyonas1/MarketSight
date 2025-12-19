# 📈 MarketSight

MarketSight handles AI training workloads using an asynchronous queue-worker architecture. It decouples the API from the training process, ensuring the application remains responsive even during heavy computation.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-red?style=for-the-badge&logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud_Infrastructure-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Message_Queue-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

---

## 🏗️ System Architecture

The system is containerized with **Docker** and orchestrated by **Kubernetes**. It consists of five key components:

1.  **Ingestion API (FastAPI):** Handles CSV file uploads and validation. It acts as the producer, pushing training jobs to the queue.
2.  **Message Broker (Redis):** An in-memory data store that buffers jobs between the API and the workers.
3.  **ML Worker (Python/PyTorch):** A background process that consumes jobs. It performs:
    *   **Preprocessing:** Data normalization using **Pandas** and **Scikit-Learn**.
    *   **Training:** Linear Regression model training using **PyTorch**.
    *   **Storage:** Uploading model artifacts (`.pth`) to **AWS S3**.
4.  **Database (PostgreSQL):** Stores job metadata, training status, and metrics.
5.  **Dashboard (Next.js):** A React-based UI that polls the API for status updates and visualizes results.

---

## ☁️ Infrastructure

*   **AWS EC2 & S3:** Hosting for the application logic and object storage for model files.
*   **Kubernetes:** Manages deployment, scaling, and self-healing of containers.
*   **GitHub Actions:** Automated CI/CD pipeline for testing and deployment.
*   **Docker:** Provides consistent runtime environments across development and production.

---

## 🧠 Machine Learning

The model predicts closing stock prices based on four input features: *Open, High, Low, and Volume*.

*   **Algorithm:** Linear Regression (`torch.nn.Linear`).
*   **Optimization:** Stochastic Gradient Descent (SGD).
*   **Loss Function:** Mean Squared Error (MSE).
*   **Preprocessing:** Min-Max Scaling [0, 1].

---

## 🚀 Project Goal

This project demonstrates a production-grade **MLOps** pipeline. It bridges the gap between training a model in a notebook and deploying a scalable, automated system that can serve users reliably.
