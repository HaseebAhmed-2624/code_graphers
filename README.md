# Code Graphers

A Django-based web application with modern features and robust architecture.

## Features

- Django REST Framework for API development
- Celery for asynchronous task processing
- Redis for caching and message brokering
- PostgreSQL database
- Docker containerization
- JWT authentication
- Swagger/OpenAPI documentation
- Email integration
- Payment processing with Stripe

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- PostgreSQL
- Redis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HaseebAhmed-2624/code_graphers.git 
cd code_graphers
```

2. Copy .env.docker file to .env

3. Activate virtual environment and install dependencies

4. Start the application using Docker:

```bash
./start.sh
```

This will:

- Build and start all necessary containers
- Run database migrations
- Collect static files

## Development Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

## Docker Compose Setup

1. copy .env.docker to .env

2. Start docker compose containers:

```bash
bash start.sh
```


## Project Structure

```
code_graphers/
├── apps/              # Django applications
├── config/            # Configuration files
├── devops/            # Docker and deployment configurations
├── envs/              # Environment-specific settings
├── .venv/             # Virtual environment
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
└── start.sh           # Startup script
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- Postman: `https://documenter.getpostman.com/view/24419455/2sB2iwEEPR`
## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Support

For support, please [add your contact information or support channels here]

## Note

1. Pushed the .env file to github for ease in testing
2. Didn't write unit tests due to short time


