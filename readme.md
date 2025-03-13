# DataTraining Dashboard

A Django application that processes Zoom meeting data, matching registration and participant files to track attendance and participation. The dashboard uses AI models via OpenAI to process and format data, which is stored in a PostgreSQL database and presented through a user-friendly interface.

## Features

- User authentication system
- Upload and process Zoom registration and participant files
- Automated matching of registration and participant data
- AI-powered data processing via OpenAI API
- Asynchronous processing with Celery and Redis
- Visualization dashboard
- Ability to exclude specific individuals from analysis

## Technology Stack

- **Backend**: Python/Django
- **Frontend**: JavaScript, Bootstrap 5
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Message Broker**: Redis
- **AI Integration**: OpenAI API
- **Deployment**: Railway

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/shaisabm/Data-Training.git
   cd DataTraining
    ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with required variables:
   ```
   SECRET_KEY=your_django_secret_key
   POSTGRES_NAME=your_db_name
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   REDIS_URL=redis://localhost:6379
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

8. In a separate terminal, start Celery worker:
   ```bash
   celery -A DataTraining worker --loglevel=info
   ```

## Usage

1. Access the application at `http://localhost:8000`
2. Log in with your credentials
3. Upload Zoom registration and participant files
   - Files should contain an 11-digit meeting ID for automatic matching
4. The system will:
   - Match registration and participant data
   - Process data using AI models
   - Display processed information in the dashboard

### File Format Requirements

The application expects Zoom CSV files with:
- Registration data containing attendee information
- Participant data with meeting attendance details
- Filenames must contain an 11-digit meeting ID (e.g., `registration_93654500555.csv`)

## Project Structure

- `dashboard/`: Main application with views, models, and templates
- `dashboard/data_processing/`: AI processing and data formatting
- `dashboard/spreadsheet_processing/`: File handling and celery tasks
- `DataTraining/`: Project settings and configuration

## Deployment

The application is configured for Railway deployment.

### Railway Configuration

The `railway.json` file specifies:
- Nixpacks as the builder
- Start command to activate virtual environment, collect static files, run migrations, and start Gunicorn
- Automatic restart on failure

## Environment Variables

For production deployment, set:
- `IN_PRODUCTION=True`
- `SECRET_KEY`
- Database credentials (`POSTGRES_NAME`, `POSTGRES_USER`, etc.)
- `REDIS_URL` for Celery

## License

Copyright © 2024 New York Institute of Technology (NYIT). All rights reserved.

This software is the property of New York Institute of Technology. Unauthorized copying, 
modification, distribution, or use of this software, via any medium, is strictly prohibited 
without the express written permission of New York Institute of Technology.

For permission requests, please contact New York Institute of Technology.
