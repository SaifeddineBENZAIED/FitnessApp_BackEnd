# Fitness Web App - Backend (Django)

This repository contains the **backend part** of the **Fitness Web App**, built using **Django**. The backend provides **RESTful APIs** for the frontend (built with Angular) to fetch personalized exercise and meal recommendations. It integrates **Machine Learning algorithms** to generate recommendations and is containerized using **Docker** for seamless deployment.

---

## 🚀 Features

- **RESTful APIs**: Provides endpoints for the frontend to fetch exercise and meal recommendations.
- **Machine Learning Integration**: Uses ML algorithms to generate personalized recommendations.
- **Database Integration**: Stores user data and recommendations in a database (e.g., PostgreSQL).
- **DevOps Integration**: Containerized using **Docker** and integrated into a **CI/CD pipeline** with **Jenkins**.
- **Full-Stack Deployment**: Connects with the frontend and other services using **Docker-compose** for a fully containerized app.

---

## 🛠️ Technologies Used

- **Backend Framework**: Django
- **Database**: PostgreSQL
- **API Development**: Django REST Framework (DRF)
- **Machine Learning**: Python (Scikit-learn, TensorFlow, etc.)
- **DevOps Tools**:
  - Docker
  - Docker-compose
  - Jenkins (CI/CD)
  - Kubernetes (Deployment)

---

## 📂 Repository Structure

fitness-web-app-backend/

├── fitness_app/ # Django app for fitness recommendations

│ ├── models.py # Database models

│ ├── views.py # API views

│ ├── serializers.py # Serializers for API responses

│ └── urls.py # API endpoints

├── manage.py # Django management script

├── requirements.txt # Python dependencies

├── Dockerfile # Dockerfile for containerizing the backend

├── docker-compose.yml # Docker-compose configuration for full-stack deployment

├── README.md # Project documentation

└── .gitignore # Git ignore file


---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Docker
- Docker-compose

### Steps to Run the Backend

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SaifeddineBENZAIED/fitness-web-app-backend.git
   cd fitness-web-app-backend

Install Dependencies:

```bash
pip install -r requirements.txt
```

Run Migrations:

```bash
python manage.py migrate
```

Run the Backend Locally:

```bash
python manage.py runserver
```

The backend will be available at http://localhost:8000.

Run with Docker:

Build the Docker image:

```bash
docker build -t fitness-backend .
```

Run the container:

```bash
docker run -p 8000:8000 fitness-backend
```

Run Full-Stack with Docker-compose:

Ensure the frontend and other services are configured in docker-compose.yml.

Start all services:

```bash
docker-compose up
```

🔍 Backend Features

RESTful APIs

- Recommendation Endpoints: APIs to fetch exercise and meal recommendations.

- User Management: APIs for user registration, login, and profile management.

- Database Integration: Stores user preferences, recommendations, and other data.

Machine Learning Integration

- Personalized Recommendations: Uses ML algorithms to generate recommendations based on user data.

- Model Training: Includes scripts for training and updating ML models.

DevOps Integration

- Docker: The backend is containerized for easy deployment and scalability.

- Docker-compose: Connects the backend with the frontend and other services for a full-stack app.

- CI/CD Pipeline: Jenkins automates the build, test, and deployment process.

📫 Contact
For questions or feedback, feel free to reach out:

Email: saif2001benz2036@gmail.com
