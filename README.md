# Fitness Class Booking System

A Django-based fitness class booking system with Docker containerization, CI/CD pipeline, and automated deployment.

## Features

- User authentication (registration/login)
- Database persistence with PostgreSQL
- Email notifications for bookings and reminders
- Docker containerization
- CI/CD pipeline with GitHub Actions
- Automated deployment with Ansible

## Project Structure

```
fitness_booking/
├── docker/
│   ├── django/
│   │   └── Dockerfile
│   ├── nginx/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── postgres/
│       └── Dockerfile
├── ansible/
│   ├── deploy.yml
│   ├── env.j2
│   └── docker-compose.yml.j2
├── .github/
│   └── workflows/
│       └── main.yml
├── fitness_booking/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── docker-compose.yml
└── .env
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- PostgreSQL 13+
- Nginx
- Ansible (for deployment)
- Docker Hub account (for CI/CD)

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/GanzAfrica/fitness_booking.git
   cd fitness_booking
   ```

2. Create and configure `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose build
   docker-compose up
   ```

4. Access the application:
   - Main application: http://localhost:80
   - Django admin: http://localhost:80/admin
   - API endpoints: http://localhost:80/api/

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

1. Code Quality Check:
   - Flake8 for linting
   - Black for code formatting
   - isort for import sorting

2. Testing:
   - Django test suite
   - Integration tests

3. Docker Build and Push:
   - Build Docker images
   - Push to Docker Hub

### GitHub Actions Setup

1. Add Docker Hub credentials to GitHub Secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

2. The workflow will automatically:
   - Run code quality checks
   - Run tests
   - Build and push Docker images to Docker Hub
   - Trigger deployment (on main branch)

## Deployment

The application can be deployed using Ansible:

1. Configure your inventory file:
   ```bash
   cp ansible/inventory.ini.example ansible/inventory.ini
   # Edit inventory.ini with your server details
   ```

2. Set up environment variables:
   ```bash
   export DB_PASSWORD=your_database_password
   export DJANGO_SECRET_KEY=your_secret_key
   ```

3. Run the deployment:
   ```bash
   ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
   ```

### Server Configuration

The application is configured to run on:
- Server IP: 64.23.210.235
- Nginx Port: 8080 (assigned port)
- Django Port: 8000 (internal)
- PostgreSQL Port: 5432 (internal)

Access the deployed application at:
- Main application: http://64.23.210.235:8080
- Django admin: http://64.23.210.235:8080/admin
- API endpoints: http://64.23.210.235:8080/api/

## Environment Variables

Required environment variables:
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DATABASE_URL`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`
- `DB_PASSWORD` (for Ansible deployment)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

