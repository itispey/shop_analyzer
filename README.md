# Simple Shop Analyzer

A Django-based REST API for analyzing shop data with support for products, customers, and orders.

## Prerequisites

- Python 3.11+ (for local setup)
- Docker and Docker Compose (for containerized setup)

## Installation

### Option 1: Local Python Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/itispey/shop_analyzer.git
   cd shop_analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=shop_analyzer_db
   DB_USER=shop_analyzer_user
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```

5. **Set up the database**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load fake data (optional)**
   ```bash
   python manage.py populate_fake_data
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000`

### Option 2: Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/itispey/shop_analyzer.git
   cd shop_analyzer
   ```

2. **Create a `.env` file** in the project root with your configuration:
   ```
   DEBUG=False
   DB_NAME=shop_analyzer_db
   DB_USER=shop_analyzer_user
   DB_PASSWORD=your-secure-password
   DB_HOST=db
   DB_PORT=5432
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```

3. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```

   The API will be available at `http://localhost:8000`

4. **Create a superuser** (optional)
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Load fake data** (optional)
   ```bash
   docker-compose exec web python manage.py populate_fake_data
   ```

## API Endpoints

- Admin panel: `http://localhost:8000/admin/`
- API: `http://localhost:8000/api/shop/top-sellers`

## Project Structure

- `shop/` - Main Django app with models and API views
- `shop/models/` - Database models for products, customers, and orders
- `shop/management/commands/` - Custom Django management commands
- `shop_analyzer/` - Django project configuration
- `scripts/` - Startup and utility scripts
- `staticfiles/` - Static files for admin and REST Framework
