# Fitness Class Booking System

A Django application for booking fitness classes, deployed using DevOps practices including Docker containerization, CI/CD with GitHub Actions, and automated deployment with Ansible.

## Features

- User authentication (registration/login)
- Fitness class browsing and booking
- User profiles
- Email notifications for bookings and cancellations
- Admin interface for managing classes and bookings

## Tech Stack

- Django with PostgreSQL database
- Docker and Docker Compose for containerization
- Nginx as a reverse proxy
- MailHog for email testing
- GitHub Actions for CI/CD
- Ansible for deployment automation

## Local Development

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- pip

### Setup

1. Clone the repository: git clone https://github.com/your-username/fitness-booking-devops.git
cd fitness-booking-devops
2. Create .env file from the example:
3. Build and run the Docker containers:
4. Access the application at http://localhost:8080

### Running Tests
## Deployment

### Prerequisites

- Ansible 2.9+
- Docker Hub account

### Steps

1. Set your Docker Hub username as an environment variable:
export DOCKER_HUB_USERNAME=your-dockerhub-username
2. Update the inventory file with your server details:vim ansible/inventory.ini
3. Run the Ansible playbook:
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml
4. Access the deployed application at http://server-ip:port

## CI/CD Pipeline

The project uses GitHub Actions for CI/CD:

1. Code linting with flake8
2. Running tests against PostgreSQL
3. Building and pushing Docker images to Docker Hub
4. Automated deployment using Ansible (manual trigger)

## Project Structure

- `booking/` - Django app for fitness class bookings
- `fitness_booking/` - Django project settings
- `docker/` - Dockerfiles for each service
- `.github/workflows/` - GitHub Actions workflows
- `ansible/` - Ansible playbooks and templates for deployment

## License

Step 7: Deploy with Ansible
Once you've pushed your code to GitHub and your GitHub Actions workflow has pushed images to Docker Hub, deploy using Ansible:

# Set your Docker Hub username
export DOCKER_HUB_USERNAME=your-dockerhub-username

# Run the Ansible playbook
ansible-playbook -i ansible/inventory.ini ansible/deploy.yml

# Check if the application is running on your server:
http://64.23.210.235:8080
- (Replace 8080 with your assigned port)

