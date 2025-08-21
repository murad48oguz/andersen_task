
## ✨ Features

- **🔐 JWT Authentication** - Secure token-based user authentication
- **✅ Full CRUD Operations** - Create, read, update, and delete tasks effortlessly
- **📊 Task Status Management** - Track tasks through New, In Progress, and Completed states
- **🔍 Advanced Filtering** - Filter tasks by status and other criteria
- **📄 Pagination** - Efficient handling of large task lists
- **👤 User Permissions** - Users can only access their own tasks
- **🧪 Comprehensive Testing** - Complete test coverage for reliability
- **🐳 Docker Support** - Easy containerized deployment
- **🐘 PostgreSQL Database** - Production-ready data storage

## 🛠 Tech Stack

| Component               | Technology |
|-------------------------|------------|
| **Backend Framework**   | Django 4.2 + Django REST Framework |
| **Database**            | PostgreSQL (production), SQLite (testing) |
| **Authentication**      | JWT with Simple JWT |
| **Containerization**    | Docker + Docker Compose |
| **Testing**             | pytest + Django test framework |

## 📋 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/users/register/` | User registration |
| `POST` | `/api/token/` | Obtain JWT tokens |
| `POST` | `/api/token/refresh/` | Refresh access token |

### Task Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tasks/` | List user tasks (paginated) |
| `POST` | `/api/tasks/` | Create new task |
| `GET` | `/api/tasks/{id}/` | Get specific task |
| `PATCH` | `/api/tasks/{id}/` | Update task |
| `DELETE` | `/api/tasks/{id}/` | Delete task |
| `PATCH` | `/api/tasks/{id}/mark-completed/` | Mark task as completed |

### Query Parameters
- `?status={status}` - Filter by task status (`new`, `in_progress`, `completed`)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Docker (optional)

### Local Development

1. **Clone and setup environment**
```bash
git clone <https://github.com/murad48oguz/andersen_task/>
cd taskflow-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt



Configure environment variables

bash
cp .env.example .env
# Edit .env with your database credentials
Setup database and run server

bash
python manage.py migrate
python manage.py runserver
Docker Deployment
Start services in background

bash
docker-compose up -d
Run database migrations

bash
docker-compose exec web python manage.py migrate
The API will be available at http://localhost:8000

🔐 Authentication
Register a New User
bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password",
    "first_name": "Your",
    "last_name": "Name"
  }'
Obtain Access Token
bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
📝 Usage Examples
Create a New Task
bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "in_progress"
  }'
Filter Tasks by Status
bash
curl -X GET "http://localhost:8000/api/tasks/?status=completed" \
  -H "Authorization: Bearer <your_token>"
Mark Task as Completed
bash
curl -X PATCH http://localhost:8000/api/tasks/1/mark-completed/ \
  -H "Authorization: Bearer <your_token>"
🧪 Testing
Run the complete test suite:

bash
python manage.py test
Run tests for specific apps:

bash
python manage.py test users
python manage.py test tasks
🔧 Configuration
Create or update your .env file:

env
# Django Settings
SECRET_KEY=your-secure-secret-key-here
DEBUG=True

# Database Settings
DB_NAME=taskflow
DB_USER=your_username
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
